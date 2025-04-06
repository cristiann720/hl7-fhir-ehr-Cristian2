from connection import connect_to_mongodb
from bson import ObjectId
from fhir.resources.patient import Patient
from pydantic import BaseModel
from datetime import datetime
import json
collection = connect_to_mongodb("SamplePatientService", "patients")
def GetPatientById(patient_id: str):
    try:
        patient = collection.find_one({"_id": ObjectId(patient_id)})
        if patient:
            patient["_id"] = str(patient["_id"])
            return "success", patient
        return "notFound", None
    except Exception as e:
        return f"notFound", None
def WritePatient(patient_dict: dict):
    try:
        pat = Patient.model_validate(patient_dict)
    except Exception as e:
        return f"errorValidating: {str(e)}",None
    validated_patient_json = pat.model_dump()
    result = collection.insert_one(patient_dict)
    if result:
        inserted_id = str(result.inserted_id)
        return "success",inserted_id
    else:
        return "errorInserting", None
def GetPatientByIdentifier(patientSystem, patientValue):
    try:
        patient = collection.find_one({"identifier.system": patientSystem, "identifier.value": patientValue})
        if patient:
            patient["_id"] = str (patient["_id"])
            return "success", patient
        return "notfound", None
    except Exception as e:
        return f"notfound", None
class ServiceRequest(BaseModel):
    patientIdentifierTyped: str
    patientId: str
    patientName: str
    requesterId: str
    requesterName: str
    specimenType: str
    collectionDate: str
    collectionTime: str
    priority: str
    reason: str
    status: str = "pending"
    created_at: datetime = datetime.utcnow()
# Conectarse a la colección service_requests
service_collection = connect_to_mongodb("SamplePatientService", "service_requests")
def WriteServiceRequest(request_dict: dict):
    try:
        service = ServiceRequest(**request_dict)
        result = service_collection.insert_one(service.model_dump())
        if result.inserted_id:
            return "success", str(result.inserted_id)
        else:
            return "errorInserting", None
    except Exception as e:
        print(":x: Error en WriteServiceRequest:", str(e))
        return f"errorValidating: {str(e)}", None