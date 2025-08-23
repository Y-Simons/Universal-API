from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from ..ai import score_patient
from ..db import InMemoryPatient, patients
from ..models import Patient, PatientCreate, RiskScore
from ..security import get_current_user


router = APIRouter()


@router.get("/", response_model=List[Patient])
async def list_patients(_: str = Depends(get_current_user)) -> List[Patient]:
	return [Patient(**p.__dict__) for p in patients.list()]


@router.post("/", response_model=Patient)
async def create_patient(payload: PatientCreate, _: str = Depends(get_current_user)) -> Patient:
	patient = InMemoryPatient(
		id=str(uuid4()),
		first_name=payload.first_name,
		last_name=payload.last_name,
		dob=payload.dob,
		height_cm=payload.height_cm,
		weight_kg=payload.weight_kg,
		allergies=payload.allergies,
		medications=payload.medications,
		comorbidities=payload.comorbidities,
		last_lab_results=payload.last_lab_results,
		consent=payload.consent,
	)
	patients.upsert(patient)
	return Patient(**patient.__dict__)


@router.get("/{patient_id}", response_model=Patient)
async def get_patient(patient_id: str, _: str = Depends(get_current_user)) -> Patient:
	p = patients.get(patient_id)
	if p is None:
		raise HTTPException(status_code=404, detail="Patient not found")
	return Patient(**p.__dict__)


@router.get("/{patient_id}/risk", response_model=RiskScore)
async def get_patient_risk(patient_id: str, _: str = Depends(get_current_user)) -> RiskScore:
	p = patients.get(patient_id)
	if p is None:
		raise HTTPException(status_code=404, detail="Patient not found")
	return score_patient(p.__dict__)