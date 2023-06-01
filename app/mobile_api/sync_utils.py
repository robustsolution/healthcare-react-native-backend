from flask import jsonify
import time
from datetime import timezone, datetime

from db_util import get_connection


def getNthTimeSyncData(timestamp):
    # print("timestamp: ", timestamp)
    # query for all events that have been updated since the last sync
    events_new = []
    events_updated = []
    events_deleted = []

    patients_new = []
    patients_updated = []
    patients_deleted = []

    clinics_new = []
    clinics_updated = []
    clinics_deleted = []

    visits_new = []
    visits_updated = []
    visits_deleted = []

    string_ids_new = []
    string_ids_updated = []
    string_ids_deleted = []

    string_content_new = []
    string_content_updated = []
    string_content_deleted = []

    event_forms_new = []
    event_forms_updated = []
    event_forms_deleted = []

    is_not_deleted_str = " AND is_deleted = false"
    is_deleted_str = " AND is_deleted = true"

    with get_connection() as conn:
        # updated events
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM events WHERE last_modified > %s AND server_created_at < %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            events_updated = cur.fetchall()

            events_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in events_updated
            ]

        # new events
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM events WHERE server_created_at > %s AND last_modified > %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            events_new = cur.fetchall()
            events_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in events_new
            ]

        # deleted events
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM events WHERE deleted_at > %s" + is_deleted_str,
                (timestamp,),
            )
            events_deleted = cur.fetchall()
            events_deleted = [
                dict(zip([column[0] for column in cur.description], row))
                for row in events_deleted
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM patients WHERE last_modified > %s AND server_created_at < %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            patients_updated = cur.fetchall()
            patients_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in patients_updated
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM patients WHERE server_created_at > %s"
                + is_not_deleted_str,
                (timestamp,),
            )
            patients_new = cur.fetchall()
            patients_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in patients_new
            ]

        # deleted patients
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM patients WHERE deleted_at > %s" + is_deleted_str,
                (timestamp,),
            )
            patients_deleted = cur.fetchall()
            patients_deleted = [
                dict(zip([column[0] for column in cur.description], row))
                for row in patients_deleted
            ]

        # new cursor and select by last modiied and server_created_at, like above for visits, string_ids and string_content
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM clinics WHERE last_modified > %s AND last_modified < %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            clinics_updated = cur.fetchall()
            clinics_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in clinics_updated
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM clinics WHERE server_created_at > %s AND last_modified > %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            clinics_new = cur.fetchall()
            clinics_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in clinics_new
            ]

        ##############
        ### VISITS ###
        ##############
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM visits WHERE last_modified > %s AND last_modified < %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            visits_updated = cur.fetchall()
            visits_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in visits_updated
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM visits WHERE server_created_at > %s AND last_modified > %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            visits_new = cur.fetchall()
            visits_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in visits_new
            ]

        # deleted visits
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM visits WHERE deleted_at > %s" + is_deleted_str,
                (timestamp,),
            )
            visits_deleted = cur.fetchall()
            visits_deleted = [
                dict(zip([column[0] for column in cur.description], row))
                for row in visits_deleted
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM string_ids WHERE last_modified > %s",
                (timestamp,),
            )
            string_ids_updated = cur.fetchall()
            string_ids_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in string_ids_updated
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM string_ids WHERE server_created_at > %s",
                (timestamp,),
            )
            string_ids_new = cur.fetchall()
            string_ids_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in string_ids_new
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM string_content WHERE last_modified > %s",
                (timestamp,),
            )
            string_content_updated = cur.fetchall()
            string_content_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in string_content_updated
            ]

        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM string_content WHERE server_created_at > %s",
                (timestamp,),
            )
            string_content_new = cur.fetchall()
            string_content_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in string_content_new
            ]

        #################################
        ######### EVENT FORMS ###########
        #################################
        # Updated event forms
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM event_forms WHERE last_modified > %s AND last_modified < %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            # cur.execute(
            #     "SELECT * fromOM event_forms WHERE last_modified > %s", (timestamp,),
            # )
            event_forms_updated = cur.fetchall()
            event_forms_updated = [
                dict(zip([column[0] for column in cur.description], row))
                for row in event_forms_updated
            ]

        # New event forms
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM event_forms WHERE server_created_at > %s AND last_modified > %s"
                + is_not_deleted_str,
                (timestamp, timestamp),
            )
            # cur.execute(
            #     "SELECT * FROM event_forms WHERE server_created_at > %s", (timestamp,),
            # )
            event_forms_new = cur.fetchall()
            event_forms_new = [
                dict(zip([column[0] for column in cur.description], row))
                for row in event_forms_new
            ]

        # Deleted event forms
        with conn.cursor() as cur:
            cur.execute(
                "SELECT * FROM event_forms WHERE deleted_at > %s" + is_deleted_str,
                (timestamp,),
            )
            event_forms_deleted = cur.fetchall()
            event_forms_deleted = [
                dict(zip([column[0] for column in cur.description], row))
                for row in event_forms_deleted
            ]

    return (
        (events_new, events_updated, events_deleted),
        (patients_new, patients_updated, patients_deleted),
        (clinics_new, clinics_updated, clinics_deleted),
        (visits_new, visits_updated, visits_deleted),
        (string_ids_new, string_ids_updated, string_ids_deleted),
        (string_content_new, string_content_updated, string_content_deleted),
        (event_forms_new, event_forms_updated, event_forms_deleted),
    )


# data = { "patients": { "created": [], "updated": [], "deleted": [] }, "events": {}, "visits": {}, "users": {}, "clinics": "" }
def apply_edge_changes(data, lastPulledAt):
    # patients
    patients = data["patients"]
    events = data["events"]
    visits = data["visits"]

    with get_connection() as conn:
        with conn.cursor() as cur:
            try:
                apply_edge_patient_changes(patients, cur, lastPulledAt)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("Error while executing SQL commands: ", e)
                raise e

            try:
                apply_edge_visits_changes(visits, cur, lastPulledAt)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("Error while executing SQL commands: ", e)
                raise e

            try:
                apply_edge_event_changes(events, cur, lastPulledAt)
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("Error while executing SQL commands: ", e)
                raise e


# Function that takes the results of getNthTimeSyncData and formats them into a JSON object to be returned to the client
def formatGETSyncResponse(syncData):
    (
        events,
        patients,
        clinics,
        visits,
        string_ids,
        string_content,
        event_forms,
    ) = syncData
    return jsonify(
        {
            "changes": {
                "events": {
                    "created": events[0],
                    "updated": events[1],
                    "deleted": events[2],
                },
                "patients": {
                    "created": patients[0],
                    "updated": patients[1],
                    "deleted": patients[2],
                },
                "clinics": {
                    "created": clinics[0],
                    "updated": clinics[1],
                    "deleted": clinics[2],
                },
                "visits": {
                    "created": visits[0],
                    "updated": visits[1],
                    "deleted": visits[2],
                },
                "string_ids": {
                    "created": string_ids[0],
                    "updated": string_ids[1],
                    "deleted": string_ids[2],
                },
                "string_content": {
                    "created": string_content[0],
                    "updated": string_content[1],
                    "deleted": string_content[2],
                },
                "event_forms": {
                    "created": event_forms[0],
                    "updated": event_forms[1],
                    "deleted": event_forms[2],
                },
            },
            "timestamp": get_timestamp_now(),
        }
    )


def apply_edge_patient_changes(patients, cur, lastPulledAt):
    # CREATED PATIENTS
    if len(patients["created"]) > 0:
        patient_insert = """INSERT INTO patients (id, given_name, surname, date_of_birth, country, hometown, sex, phone, camp, created_at, updated_at, server_created_at, last_modified)"""
        patients_sql = [
            (
                patient["id"],
                patient["given_name"],
                patient["surname"],
                patient["date_of_birth"],
                patient["country"],
                patient["hometown"],
                patient["sex"],
                patient["phone"],
                patient["camp"],
                date_from_timestamp(patient["created_at"]),
                date_from_timestamp(patient["updated_at"]),
                # server timestamps set to be those of the client during creation
                date_from_timestamp(patient["created_at"]),
                date_from_timestamp(patient["updated_at"]),
            )
            for patient in patients["created"]
        ]

        args = ",".join(
            cur.mogrify(
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i
            ).decode("utf-8")
            for i in patients_sql
        )
        cur.execute(patient_insert + " VALUES " + (args))

    # UPDATED PATIENTS
    # UPDATE patients SET name = 'new name' WHERE id = 'id'
    for patient in patients["updated"]:
        cur.execute(
            f"""UPDATE patients SET given_name='{patient["given_name"]}', surname='{patient["surname"]}', date_of_birth='{patient["date_of_birth"]}', country='{patient["country"]}', hometown='{patient["hometown"]}', sex='{patient["sex"]}', phone='{patient["phone"]}', camp='{patient["camp"]}', created_at='{date_from_timestamp(patient["created_at"])}', updated_at='{date_from_timestamp(patient["updated_at"])}', last_modified='{date_from_timestamp(patient["updated_at"])}' WHERE id='{patient["id"]}';"""
        )

    # DELETED PATIENTS
    for patient in patients["deleted"]:
        # if len(patients["deleted"]) > 0:
        # convert array of strings to tuple of strings
        # deleted_ids = tuple(patients["deleted"])
        # cur.execute(f"""DELETE FROM patients WHERE id IN ({deleted_ids});""")
        cur.execute(
            f"""UPDATE patients SET is_deleted=true, deleted_at='{date_from_timestamp(lastPulledAt)}' WHERE id = '{patient}';"""
        )


def apply_edge_event_changes(events, cur, lastPulledAt):
    # CREATED EVENTS
    if len(events["created"]) > 0:
        event_insert = "INSERT INTO events (id, patient_id, visit_id, event_type, event_metadata, is_deleted, created_at, updated_at, server_created_at, last_modified) VALUES "
        events_sql = [
            (
                event["id"],
                event["patient_id"],
                event["visit_id"],
                event["event_type"],
                event["event_metadata"],
                event["is_deleted"],
                date_from_timestamp(event["created_at"]),
                date_from_timestamp(event["updated_at"]),
                # server timestamps set to be those of the client during creation
                date_from_timestamp(event["created_at"]),
                date_from_timestamp(event["updated_at"]),
            )
            for event in events["created"]
        ]

        # print("EVENTS SQL: ", events_sql)

        args = ",".join(
            cur.mogrify("(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)", i).decode("utf-8")
            for i in events_sql
        )
        cur.execute(event_insert + (args))

    # UPDATED EVENTS
    # UPDATE events SET name = 'new name' WHERE id = 'id'
    for event in events["updated"]:
        cur.execute(
            f"""UPDATE events SET patient_id='{event["patient_id"]}', visit_id='{event["visit_id"]}', event_type='{event["event_type"]}', event_metadata='{event["event_metadata"]}', is_deleted='{event["is_deleted"]}', created_at='{date_from_timestamp(event["created_at"])}', updated_at='{date_from_timestamp(event["updated_at"])}' WHERE id='{event["id"]}';"""
        )

    # DELETED EVENTS
    # if len(events["deleted"]) > 0:
    for event in events["deleted"]:
        # deleted_ids = tuple(events["deleted"])
        # cur.execute(f"""DELETE FROM events WHERE id IN ({deleted_ids});""")
        cur.execute(
            f"""UPDATE events SET is_deleted=true, deleted_at='{date_from_timestamp(lastPulledAt)}' WHERE id = '{event}';"""
        )


def apply_edge_visits_changes(visits, cur, lastPulledAt):
    # CREATED VISITS
    if len(visits["created"]) > 0:
        visit_insert = "INSERT INTO visits (id, patient_id, clinic_id, provider_id, provider_name, check_in_timestamp, is_deleted, metadata, created_at, updated_at, server_created_at, last_modified) VALUES "
        visits_sql = [
            (
                visit["id"],
                visit["patient_id"],
                visit["clinic_id"],
                visit["provider_id"],
                visit["provider_name"],
                date_from_timestamp(visit["check_in_timestamp"]),
                visit["is_deleted"],
                visit["metadata"],
                date_from_timestamp(visit["created_at"]),
                date_from_timestamp(visit["updated_at"]),
                # server timestamps set to be those of the client during creation
                date_from_timestamp(visit["created_at"]),
                date_from_timestamp(visit["updated_at"]),
            )
            for visit in visits["created"]
        ]

        args = ",".join(
            cur.mogrify("(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", i).decode("utf-8")
            for i in visits_sql
        )
        cur.execute(visit_insert + (args))

    # UPDATED VISITS
    # UPDATE visits SET name = 'new name' WHERE id = 'id'
    for visit in visits["updated"]:
        cur.execute(
            f"""UPDATE visits SET patient_id='{visit["patient_id"]}', clinic_id='{visit["clinic_id"]}', provider_id='{visit["provider_id"]}', provider_name='{visit["provider_name"]}', check_in_timestamp='{visit["check_in_timestamp"]}', is_deleted='{visit["is_deleted"]}', metadata='{visit["metadata"]}', created_at='{date_from_timestamp(visit["created_at"])}', updated_at='{date_from_timestamp(visit["updated_at"])}' WHERE id='{visit["id"]}';"""
        )

    # DELETED VISITS
    for visit in visits["deleted"]:
        # deleted_ids = tuple(visits["deleted"])
        # cur.execute(f"""DELETE FROM visits WHERE id IN {deleted_ids};""")
        cur.execute(
            f"""UPDATE visits SET is_deleted=true, deleted_at='{date_from_timestamp(lastPulledAt)}' WHERE id = '{visit}';"""
        )


# TODO: Move to utils
def date_from_timestamp(timestamp):
    date = datetime.utcfromtimestamp(timestamp / 1000).strftime("%Y-%m-%d %H:%M:%S")
    return date


def get_timestamp_now():
    return time.mktime(datetime.now().timetuple()) * 1000


# function to convert a javascript timestamp into a datetime object at gmt time
def convert_timestamp_to_gmt(timestamp):
    # convert the lastPuledAt milliseconds string into a date object of gmt time
    return datetime.fromtimestamp(int(timestamp) / 1000, tz=timezone.utc)
