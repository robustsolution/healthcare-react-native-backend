<p align="centr">
<img src="https://images.squarespace-cdn.com/content/5cc0e57236f8e70001651ea6/1599789508819-NGZXYWJDQRCULLU94QEJ/hikma-hb.png?format=300w&content-type=image/png" alt="Hikma Health" />
</p>

# Hikma Health Admin Application
The Hikma Health platform is a mobile electronic health record system designed for organizations working in low-resource settings to collect and access patient health information. The repository contains the backend code that communicates with the Databae and ensures only authenticated users have access. Additional functionality can be added, along with updating the correct migration files.

The platform is designed to be intuitive and allow for efficient patient workflows for patient registration, data entry, and data download. You can see a user demo here: https://drive.google.com/file/d/1ssBdEPShWCu3ZXNCXnoodbwWgqlTncJb/view?usp=drive_link


For more comprehensive documentation visit: https://docs.hikmahealth.org/

*NOTE: This repository contains transition code for users coming from previous versions. If there are functions that you do not need, check twice and feel free to remove the dead code.*

*If you are stuck for more thatn 10 minutes, please file an issue and our team can help you figure it out 🚀. No issue is too small.*


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)

## Get started locally

Clone the project

```bash
  git clone git@github.com:hikmahealth/hikma-health-backend.git
```

Go to the project directory

```bash
  cd hikma-health-backend/app
```

Create a new virtual environment to avoid conflicts and global polution of your system

```bash
  python3 -m venv /path/to/new/virtual/environment
```

Activate your virtual environment

```bash
  source <venv>/bin/activate

  # if windows use the following:
  # <venv>\Scripts\activate.bat
```

Install the requirements from the the `requirements.txt` file

```bash
  pip3 install -r requirements.txt
```

Start the server

```bash
  ./run.sh
```
Your service will start on the port specified or port 8080 by default.

To connect to a database, there are 2 options:

Option 1: Easy & Simple Method

- Spin up a free managed database on a service like render.com
- Download the latest version of PGAdmin, and add your DB credentials to it. This gives you a nice interface to manage your data directly.
- Add your database credentials and connection strings to the `config.py` folder. Use the development block for testing data and the production block for production access.

Option 2: Interesting (and possibly treacherous) Method
- Install PostgreSQL on your local computer
- Set up users with appropriate permissions
- Add your database credentials and connection strings to the `config.py` folder. Use the development block for testing data and the production block for production access.

This option is better if you wish to do most of your deployment offline, or are running earlier version of this project. For everyone else, Option 1 is highly recommended.

*Option 2 is interesting and potentially challenging because a few things can go wrong during the installation of PostgreSQL due to your local computer set up, and connecting from a physical device to your server can have its own additional steps.*

*For anyone in a hurry to get things to work so that they can focus on customizations needed for the deployment, use Option 1. As a bonus, it gets you more comfortable with the service that will host your main deployments*

🔥 DO NOT USE THE PRODUCTION DATABASE FOR TESTING (UNLESS YOU ARE VERY CAREFUL AND AWARE OF THE POTENTIAL CONSEQUENCES)🔥

## Environment Variables

To run this project, you will need to add the following environment variable to your .env file

`NEXT_PUBLIC_HIKMA_API`

This variable holds a link to the backend (server) which connects to the database.This file is by default already ignored in the `.gitignore` file, make sure it remains there.

🔥 DO NOT COMMIT THIS INFORMATION TO YOUR VERSION CONTROL (GITHUB) OR SHARE IT WITH UNAUTHORIZED PERSONEL 🔥
## Technology Stack

- **Python (v3.10):** https://www.python.org/downloads/release/python-3100/
- **Flask (v2.2.2):** https://flask.palletsprojects.com/en/2.2.x/
- **SQLAlchemy (v1.3.11):** https://www.sqlalchemy.org/
- **Bcrypt (v3.1.7):** https://pypi.org/project/bcrypt/
- **Gunicorn (v20.1.0):** https://gunicorn.org/
- **PyScopePG2 (v2.9.5):** https://pypi.org/project/psycopg2/

## Roadmap
Features on the roadmap represent the vision for the admin portal over the coming versions, but none are guaranteed. If there is a feature you would love to see supported, open a feature-request / issue with more details and we can prioritize features with the most requests.

- [ ]  Improve backup functionality for self-hosted options (not recommended - use a managed database service)
- [ ]  Remove all transition code from previous deployment (next version)
- [ ]  Add documentation for fully hosted solutions like supabase
- [ ]  Improve test coverage

## License

[MIT](https://choosealicense.com/licenses/mit/)


