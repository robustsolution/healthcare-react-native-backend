from admin_api.patient_data_export import PatientDataExporter
from config import EXPORTS_STORAGE_BUCKET
from google.cloud import storage
from datetime import datetime

storage_client = storage.Client()


exporter = PatientDataExporter()
local_filename = exporter.run()

bucket = storage_client.bucket(EXPORTS_STORAGE_BUCKET)
base_name = datetime.utcnow().isoformat() + '.xlsx'
blob = bucket.blob(base_name)
print(f'Uploading {base_name} to GCS bucket {EXPORTS_STORAGE_BUCKET}...')
blob.upload_from_filename(local_filename)