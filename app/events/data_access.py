from db_util import get_connection
from events.event import Event


def clear_all_events(visit_id: str):
    assert visit_id is not None
    query = "DELETE FROM events WHERE visit_id = %s"
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [visit_id])


def add_event(event: Event):
    query = """
    INSERT INTO events (id, patient_id, visit_id, event_type, event_timestamp, event_metadata, edited_at)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [event.id, event.patient_id, event.visit_id, event.event_type, event.event_timestamp,
                                event.event_metadata, event.edited_at]
                        )


def events_by_visit(visit_id: str):
    query = """
    SELECT id, patient_id, event_type, event_timestamp, event_metadata, edited_at FROM events
    WHERE visit_id = %s
    ORDER BY event_timestamp
    """
    with get_connection() as conn:
        with conn.cursor() as cur:
            cur.execute(query, [visit_id])
            for row in cur:
                id, patient_id, event_type, event_timestamp, event_metadata, edited_at = row
                yield Event(
                    id=id,
                    patient_id=patient_id,
                    visit_id=visit_id,
                    event_type=event_type,
                    event_timestamp=event_timestamp,
                    event_metadata=event_metadata,
                    edited_at=edited_at
                )