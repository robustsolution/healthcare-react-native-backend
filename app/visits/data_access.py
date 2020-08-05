from db_util import get_connection
import datetime
from visits.visit import Visit
from typing import Tuple, Optional


def add_visit(visit: Visit):
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute('INSERT INTO visits (id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at) VALUES (%s, %s, %s, %s, %s, %s)',
                        [visit.id,
                         visit.patient_id,
                         visit.clinic_id,
                         visit.provider_id,
                         visit.check_in_timestamp,
                         visit.edited_at
                         ])


def first_visit_by_patient_and_date(patient_id: str, date: datetime.date) -> Tuple[Optional[str], Optional[str]]:
    query = "SELECT id, check_in_timestamp FROM visits WHERE patient_id = %s AND date(check_in_timestamp) = %s;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id, date])
            row = cur.fetchone()
            if row is None:
                return None, None
            else:
                return row[0], row[1]


def all_visits():
    query = "SELECT id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at FROM visits ORDER BY check_in_timestamp DESC;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [])
            for row in cur:
                yield Visit(
                    id=row[0],
                    patient_id=row[1],
                    clinic_id=row[2],
                    provider_id=row[3],
                    check_in_timestamp=row[4],
                    edited_at=row[5]
                )


def patient_visits(patient_id: str):
    query = "SELECT id, patient_id, clinic_id, provider_id, check_in_timestamp, edited_at FROM visits WHERE patient_id = %s ORDER BY check_in_timestamp DESC;"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [patient_id])
            for row in cur:
                yield Visit(
                    id=row[0],
                    patient_id=row[1],
                    clinic_id=row[2],
                    provider_id=row[3],
                    check_in_timestamp=row[4],
                    edited_at=row[5]
                )