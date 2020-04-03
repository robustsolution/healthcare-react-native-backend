import os
from google.cloud import storage
from config import LOCAL_PHOTO_STORAGE_DIR, PHOTOS_STORAGE_BUCKET

storage_client = storage.Client()


def store_photo(file_storage):
    base_name = file_storage.filename
    local_filename = os.path.join(LOCAL_PHOTO_STORAGE_DIR, base_name)
    with open(local_filename, 'wb') as handle:
        file_storage.save(handle)

    bucket = storage_client.bucket(PHOTOS_STORAGE_BUCKET)
    blob = bucket.blob(base_name)
    print(f'Uploading {base_name} to GCS bucket {PHOTOS_STORAGE_BUCKET}...')
    blob.upload_from_filename(local_filename)
    return local_filename


def retrieve_photo(base_filename):
    local_filename = os.path.join(LOCAL_PHOTO_STORAGE_DIR, base_filename)
    if os.path.exists(local_filename):
        return local_filename
    else:
        return _retrieve_photo_from_gcs(base_filename)


def _retrieve_photo_from_gcs(base_filename):
    bucket = storage_client.bucket(PHOTOS_STORAGE_BUCKET)
    blob = bucket.blob(base_filename)
    local_filename = os.path.join(LOCAL_PHOTO_STORAGE_DIR, base_filename)
    blob.download_to_filename(local_filename)
    return local_filename
