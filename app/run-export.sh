#!/bin/bash

./cloud_sql_proxy -instances=${DB_INSTANCE}=tcp:5432 -credential_file=${GOOGLE_APPLICATION_CREDENTIALS} &
sleep 5
python3.7 scripts/run_patient_data_export.py