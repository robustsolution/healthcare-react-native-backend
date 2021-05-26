from events.event import Event
from admin_api.patient_data_import import PatientDataRow
import json


def get_field(data, field):
    if data.get(field) is None:
        return None
    return 'Yes' if data.get(field) else 'No'

def get_text_field(data, field, text_field):
    if data.get(field) is None:
        return None
    if data.get(field) is not None and not data.get(text_field):
        return 'Yes' if data.get(field) else 'No'
    return data.get(text_field) if data.get(field) else 'No'

def write_vitals_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.heart_rate = data.get('heartRate')
    if data.get('systolic') and data.get('diastolic'):
        row.blood_pressure = f"{data.get('systolic')}/{data.get('diastolic')}"
    row.sats = data.get('sats')
    row.temp = data.get('temp')
    row.respiratory_rate = data.get('respiratoryRate')
    row.weight = data.get('weight')
    row.blood_glucose = data.get('bloodGlucose')

def write_medical_hx_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.allergies = data.get('allergies')
    row.surgery_hx = data.get('surgeryHx')
    row.chronic_conditions = data.get('chronicConditions')
    row.current_medications = data.get('currentMedications')
    row.vaccinations = data.get('vaccinations')

def write_examination_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.examination = data.get('examination')
    row.general_observations = data.get('generalObservations')
    row.diagnosis = data.get('diagnosis')
    row.treatment = data.get('treatment')
    row.covid_19 = get_field(data, 'covid19')
    row.referral = get_text_field(data, 'referral', 'referralText')

def write_med1_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.medication_1 = data.get('medication')
    row.type_1 = data.get('type')
    row.dosage_1 = data.get('dosage')
    row.days_1 = data.get('days')

def write_med2_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.medication_2 = data.get('medication')
    row.type_2 = data.get('type')
    row.dosage_2 = data.get('dosage')
    row.days_2 = data.get('days')

def write_med3_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.medication_3 = data.get('medication')
    row.type_3 = data.get('type')
    row.dosage_3 = data.get('dosage')
    row.days_3 = data.get('days')
		
def write_med4_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.medication_4 = data.get('medication')
    row.type_4 = data.get('type')
    row.dosage_4 = data.get('dosage')
    row.days_4 = data.get('days')

def write_med5_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.medication_5 = data.get('medication')
    row.type_5 = data.get('type')
    row.dosage_5 = data.get('dosage')
    row.days_5 = data.get('days')

def write_physiotherapy_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    row.previous_treatment = get_text_field(data, 'previousTreatment', 'previousTreatmentText')
    row.complaint_p = data.get('complaint')
    row.findings = data.get('findings')
    row.treatment_plan = data.get('treatmentPlan')
    row.treatment_session = data.get('treatmentSession')
    row.recommendations = data.get('recommendations')
    row.referral = get_text_field(data, 'referral', 'referralText')

def write_covid_19_event(row: PatientDataRow, event):
    data = json.loads(event.event_metadata)
    if data.get('seekCare'):
        row.covid_19_result = 'Seek Emergency Care and Isolate'
    elif data.get('testAndIsolate'):
        row.covid_19_result = 'Test/Isolate Patient'  
    else:
        row.covid_19_result = 'No Action Necessary'    
