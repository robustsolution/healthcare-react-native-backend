#!/bin/bash

./run_migrations.sh

export PYTHONUNBUFFERED=TRUE

case ${APP_ENV} in
    prod)
        ./cloud_sql_proxy -instances=${DB_INSTANCE}=tcp:5432 -credential_file=${GOOGLE_APPLICATION_CREDENTIALS} &
        gunicorn --timeout 6000 --access-logfile - --error-logfile - --log-level debug -w 1 -b 0.0.0.0:8080 app:app
        ;;
    dev_docker)
        gunicorn --timeout 6000 --access-logfile - --error-logfile - --log-level debug -w 1 -b 0.0.0.0:8080 app:app
        ;;
    *)
        gunicorn --timeout 6000 --access-logfile - --error-logfile - --log-level debug -w 1 -b 0.0.0.0:8080 app:app
        ;;
esac
