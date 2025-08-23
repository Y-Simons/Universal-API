from typing import List
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException

from ..ai import generate_postop_tasks, generate_preop_tasks, score_patient
from ..db import InMemoryConsultation, consultations, patients
from ..models import Consultation, ConsultationType, Patient, RiskScore, Task
from ..security import get_current_user


router = APIRouter()


@router.post("/preop/{patient_id}", response_model=Consultation)
async def create_preop(patient_id: str, _: str = Depends(get_current_user)) -> Consultation:
	p = patients.get(patient_id)
	if p is None:
		raise HTTPException(status_code=404, detail="Patient not found")
	risk: RiskScore = score_patient(p.__dict__)
	tasks: List[Task] = generate_preop_tasks(p.__dict__, risk)
	c = InMemoryConsultation(
		id=str(uuid4()),
		patient_id=patient_id,
		type=ConsultationType.preop.value,
		tasks=[t.model_dump() for t in tasks],
	)
	consultations.upsert(c)
	return Consultation(
		id=c.id,
		patient_id=c.patient_id,
		type=ConsultationType.preop,
		tasks=tasks,
	)


@router.post("/postop/{patient_id}", response_model=Consultation)
async def create_postop(patient_id: str, _: str = Depends(get_current_user)) -> Consultation:
	p = patients.get(patient_id)
	if p is None:
		raise HTTPException(status_code=404, detail="Patient not found")
	risk: RiskScore = score_patient(p.__dict__)
	tasks: List[Task] = generate_postop_tasks(p.__dict__, risk)
	c = InMemoryConsultation(
		id=str(uuid4()),
		patient_id=patient_id,
		type=ConsultationType.postop.value,
		tasks=[t.model_dump() for t in tasks],
	)
	consultations.upsert(c)
	return Consultation(
		id=c.id,
		patient_id=c.patient_id,
		type=ConsultationType.postop,
		tasks=tasks,
	)


@router.get("/{patient_id}", response_model=List[Consultation])
async def list_consultations(patient_id: str, _: str = Depends(get_current_user)) -> List[Consultation]:
	if patients.get(patient_id) is None:
		raise HTTPException(status_code=404, detail="Patient not found")
	items = consultations.list_by_patient(patient_id)
	result: List[Consultation] = []
	for item in items:
		result.append(
			Consultation(
				id=item.id,
				patient_id=item.patient_id,
				type=ConsultationType(item.type),
				scheduled_at=item.scheduled_at,
				completed_at=item.completed_at,
				notes=item.notes,
				tasks=[Task(**t) for t in item.tasks],
			)
		)
	return result