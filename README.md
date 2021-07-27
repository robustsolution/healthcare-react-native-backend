Hikma Mobile Application: Server
===============================

The Hikma Health platform is a mobile electronic health record system designed for organizations working in low-resource settings to collect and access patient health information. The platform is a lightweight android application that supports offline functionality and multiple languages including Arabic, Spanish, and English. The medical workflows are designed to be intuitive and allow for efficient patient registration and data entry in low-resource, dynamic, and mobile settings.

This repository contains the server-side code for Hikma Health's mobile application. The corresponding client-side code is located at https://github.com/hikmahealth/hikma-app. Please feel free to file 
feature requests and bugs at either location.


Local Backend Setup + GCP configuration
---------------------------------------

**Requirements: Cloud SDK command line tools, postgreSQL, python**

**Create Cluster:**
Google Cloud Console > Google Kubernetes Engine - new cluster, choose closest region, zonal location type, static version, 3 nodes > create
**Create DB:**
GCP > SQL > Create Instance “hikma-db”:
create default user (“postgres”), create UUID password and save it somewhere. 
Use the same compute zone as the cluster.

**Create bash alias:**
This activates google account for hikma, also sets local kubernetes to use the hikma cluster
(in your .bash_profile add this line, with your account, project name, compute zone, and cluster name
```
alias activate_hikma='gcloud config set account [GCP account email] && gcloud config set project [GCP_project] && gcloud config set compute/zone [zone] && gcloud container clusters get-credentials [cluster_name]'
```
Close and reopen terminal for that to take effect

Run activate alias script.

**Create local db user and db:**

In terminal,

```
psql
create user hikma_dev login password [password]; //use UUID and record this
\q
Createdb hikma_dev -O hikma_dev
```


In ./app/config.py
Set PG_USER to user you just created
Set PG_DB to db you just created
Set PHOTOS_STORAGE_BUCKET to hikma-api-photos (to be created)
Set EXPORTS_STORAGE_BUCKET to hikma-api-exports (to be created)

**Create Key Ring/ Service Account, and Key:**
GCP left nav> Security > Cryptographic Keys > Create Key Ring and Key
IAM > Service accounts > Create Service Account > “hikma-app-service-account” (or whatever you want to call it) > Create> Give it the Cloud SQL Admin Role > Continue
In Service accounts list, on hikma-app-service-account, click actions, create key (JSON)
Json key will download
Copy key into ./app
Add [key_filename].json to .gitignore
(Go ahead and remove the other [key].json.enc files that we used for our deployments)

Encode the key so you have something to commit and use to build:
```
gcloud kms encrypt --location=global --keyring=[keyring_name] --key=[key_name] --plaintext-file=[key_filename].json --ciphertext-file=[key_filename].json.enc
```


In backend repository /app folder

```
source venv/bin/activate
```

(you may need to initially run `virtualenv -p python3 venv`)
```
pip3 install -r requirements.txt

export GOOGLE_APPLICATION_CREDENTIALS=[key_filename].json
```


At this point, you should be able to `./run.sh` in your venv to run locally

Create PHOTOS_STORAGE_BUCKET as “hikma-api-photos” and EXPORTS_STORAGE_BUCKET as “hikma-api-exports”
Same region as cluster, uniform access, 
Under permissions give the service account you created access to the buckets as a “Storage Object Admin” Role

**Add a demo clinic and initial demo user to your local database**

Refer to `./app/scripts/` for scripts to do this.

Run `add_demo_clinic.py` first, and then run `add_new_user.py` with the three required arguments.
```
cd app/
export PYTHONPATH=.
python scripts/add_demo_clinic.py
python scripts/add_demo_clinic.py
```
(example credentials below)
```
python scripts/add_new_user.py  local_user user@endlessmedicaladvantage.com password123
```

**Setting up deployment**

Create an app user and app db for the hikma db instance hikma-db:
GCP left nav> SQL > Select hikma-db > Add User > Built in authentication >
Create an app user with username hikma_prod and password a randomly generated UUID that you store somewhere safe along with the password for the default user.

Select Databases on the left nav and Create an app Database
Call it hikma_prod as well

You should have this information for the hikma-db instance
```
Default User: postgres
Default DB: postgres
Default User password: [uuid from step 2]
App User: hikma_prod
App DB: hikma_prod
App User password [uuid from this step]
```

Depending on your version of the backend repository, you may have both a cloudbuild.yaml and a cloudbuild-ema.yaml. This is because Hikma Health currently has a demo environment and a prod environment for a given clinic that use different service accounts. You are welcome to persist this architecture to more easily test changes to the app, but might want to only have a prod environment in order to keep hosting costs down and reduce overhead.
Assuming you just have a production environment, you can delete one of the cloudbuild files.

**In cloudbuild.yaml:**
Replace the ciphertextfile with the encoded keyfile ([key_filename].json.enc) you just created.
Replace the plaintext file with [key_filename].json you just created on GCP.
In build args, update image name if you want, and set credential_file_arg=[key_filename].json
Remove the arg for default provider id
Remove the following lines:

```
 name: 'gcr.io/cloud-builders/kubectl'
 env: ['CLOUDSDK_COMPUTE_ZONE=us-east1-c', 'CLOUDSDK_CONTAINER_CLUSTER=ema-cluster']
 args: ['set', 'image', 'deployment/hikma-health-backend-ema',
       'hikma-health-backend=gcr.io/$PROJECT_ID/hikma-health-backend:$COMMIT_SHA']
```

This deployment does not exist yet, and we can’t make deployment until we create the image, so we must add in the automatic deployment step after the initial deployment.

(When you add this step back in, you will need to update CLOUDSDK_COMPUTE_ZONE and CLOUDSDK_CONTAINER_CLUSTER, deployment name and image name)

Set image name to same thing you specify in build args, and set `_DB_NAME` to the name of the production DB (hikma_prod) and set `_DB_INSTANCE`  to the connection string for that DB ([project]:[region]:hikma-db)
You can find this connection string by going to the overview of the SQL instance.

In GCP Cloud Build > Triggers, Create a trigger with the forked backend repo from your github as a source, “Push to a branch” as the repository event, set ^master$ as source branch, set build configuration to Cloud Build configuration file

Add the following variables:
`_DB_PASSWORD`= password for the hikma_prod App User (Not the postgres user)
`_EXPORTS_STORAGE_BUCKET`= exports storage bucket you created earlier
`_PHOTOS_STORAGE_BUCKET`= photos storage bucket you created earlier

Commit all your changes to master, which should cause your build trigger to create an image.

**Create deployment, certificate, service and ingress with Kubernetes**
Templates for the yaml files needed for configuration can be found here: https://github.com/hikmahealth/hikma-health-backend-nv/tree/master/k8s
(You'll need all 6 files prefixed with "nv-")
 
Here is some k8s documentation for how to apply these changes
https://kubernetes.io/docs/tasks/run-application/run-stateless-application-deployment/
Most importantly, you'll use:
```
  kubectl apply -f ./path_to/filename.yaml
```

If they are not already there, copy these 6 files into the k8s directory of your repository and update the filenames. 
Using backend-config.yaml, create the BackendConfig.
In certificate.yaml, specify your hostname and domain, and create the ManagedCertificate.
 
In deployment.yaml, Make sure to point to the image that was created from the build trigger. Name this deployment something like `hikma-health-backend` with an app label so that you can reference it from the service. Also provide a container name, which can be the same. Create the Deployment. 
 
In nodeport-service.yaml, Make sure to point to the backend config and the app name from the deployment. Create the Service.
 
In service-ingress.yaml, Make sure to point to the managed certificate, the name of the service you just created, and create a unique IP name. Create the Ingress.
 
Go to https://domains.google.com and add a new DNS Resource Record. Use the same host name as the domain that you specified in the certificate.yaml. Add the IP address of the Ingress for the record
 
In export-cronjob.yaml, specify what schedule you want to use for the patient visit data export (`"0 * * * *"` is every hour). Point to the image to use. You may want to make this dynamic so that you don’t have to update the CronJob after the deployment runs. Create the CronJob.
 
Lastly, using the correct compute zone, cluster name, deployment name, container name, and image, add the following lines back into the cloudbuild file:
``` 
 name: 'gcr.io/cloud-builders/kubectl'
 env: ['CLOUDSDK_COMPUTE_ZONE=us-east1-c', 'CLOUDSDK_CONTAINER_CLUSTER=ema-cluster']
 args: ['set', 'image', 'deployment/hikma-health-backend-ema',
       'hikma-health-backend=gcr.io/$PROJECT_ID/hikma-health-backend:$COMMIT_SHA']
```

This will set the image to be deployed. You could do this for the CronJob image as well.
 
Once everything is created, make sure that it is working by navigating to the resource record. You should see:
`
{"message":"Welcome to the Hikma Health backend.","status":"OK"}
`


