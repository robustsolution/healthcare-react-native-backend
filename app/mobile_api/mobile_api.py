from flask import Blueprint, request, jsonify
import time
from base64 import b64decode

from datetime import timezone, datetime
from web_util import assert_data_has_keys

from web_errors import WebError
from users.user import User
from sync.db_sychronization import DbSynchronizer
from mobile_api.sync_utils import (
    getNthTimeSyncData,
    formatGETSyncResponse,
    apply_edge_changes,
    convert_timestamp_to_gmt,
)


from db_util import get_connection

mobile_api = Blueprint("mobile_api", __name__, url_prefix="/api")


@mobile_api.route("/instances", methods=["GET"])
def all_instances():
    return jsonify(
        [
            {"name": "Demo Instance", "url": "https://demo-api.hikmahealth.org"},
            {"name": "EMA", "url": "https://ema-api.hikmahealth.org"},
            {"name": "Local (testing)", "url": "http://192.168.86.250:8080"},
        ]
    )


@mobile_api.route("/login", methods=["POST"])
def login():
    params = assert_data_has_keys(request, {"email", "password"})
    user = User.authenticate(params["email"], params["password"])
    return jsonify(user.to_dict())


@mobile_api.route("/sync", methods=["POST"])
def sync():
    params = assert_data_has_keys(request, {"email", "password"}, data_type="form")
    User.authenticate(params["email"], params["password"])
    if "db" not in request.files:
        raise WebError("db must be provided", 400)

    synchronizer = DbSynchronizer(request.files["db"])
    if not synchronizer.prepare_sync():
        raise WebError("Synchronization failed", 500)

    synchronizer.execute_server_side_sql()
    return jsonify({"to_execute": synchronizer.get_client_sql()})


# Send and Ask for changes from server
@mobile_api.route("/v2/sync", methods=["GET", "POST"])
def sync_v2():
    # authorization_header = request.headers['Authorization']
    auth_header = request.headers.get('Authorization')
    encoded_username_password = auth_header.split(' ')[1]

    # Decode the username and password
    decoded_username_password = base64.b64decode(encoded_username_password).decode()

    # Split the decoded string into email and password
    email, password = decoded_username_password.split(':')
    # email, password = b64decode(authorization_header).decode('utf-8').split(':')

    User.authenticate(email, password)

    lastPulledAtReq = request.args.get("last_pulled_at", 0)
    lastPulledAt = (
        int(lastPulledAtReq)
        if type(lastPulledAtReq) == int
        or type(lastPulledAtReq) == float
        or (type(lastPulledAtReq) == str and str(lastPulledAtReq).isnumeric())
        else 0
    )

    ms = datetime.now()
    syncTimestamp = time.mktime(ms.timetuple()) * 1000

    print(
        f"lastPulledAt: {lastPulledAt} ({lastPulledAtReq}) and server says: {syncTimestamp} and a difference of: {int(lastPulledAt or 0) - syncTimestamp}"
    )

    ## GET REQUEST ##
    ## REQUESTING CHANGES FROM THE SERVER THAT CLIENT DOES NOT HAVE
    # Response must look like:
    # Changes = {
    #   [table_name: string]: {
    #     created: RawRecord[],
    #     updated: RawRecord[],
    #     deleted: string[],
    #   }
    # }
    if request.method == "GET":
        schemaVersion = request.args.get("schemaVersion", None)
        migration = request.args.get("migration", None)

        syncData = getNthTimeSyncData(convert_timestamp_to_gmt(lastPulledAt))
        return formatGETSyncResponse(syncData)

    ## POST REQUEST ##
    ## PUSHING CHANGES FROM CLIENT TO SERVER
    if request.method == "POST":
        # 2. If the changes object contains a record that has been modified on the server after lastPulledAt, you MUST abort push and return an error code
        body = request.get_json()

        apply_edge_changes(body, lastPulledAt)
        return jsonify({"message": True})

    return jsonify({"message": "OK"})
