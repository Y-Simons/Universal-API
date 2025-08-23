from __future__ import annotations

from datetime import datetime
from enum import Enum
from typing import Dict, List, Optional

from pydantic import BaseModel, EmailStr, Field


class UserRole(str, Enum):
	anesthetist = "anesthetist"
	nurse = "nurse"
	admin = "admin"


class User(BaseModel):
	id: str
	email: EmailStr
	full_name: str
	role: UserRole


class UserLogin(BaseModel):
	email: EmailStr
	password: str


class Token(BaseModel):
	access_token: str
	token_type: str = "bearer"


class RiskLevel(str, Enum):
	low = "low"
	moderate = "moderate"
	high = "high"
	very_high = "very_high"


class RiskScore(BaseModel):
	asa_class: int = Field(..., ge=1, le=5)
	risk_level: RiskLevel
	score: float = Field(..., ge=0, le=1)
	rationale: str


class Patient(BaseModel):
	id: str
	first_name: str
	last_name: str
	dob: str
	height_cm: Optional[float] = None
	weight_kg: Optional[float] = None
	allergies: List[str] = []
	medications: List[str] = []
	comorbidities: List[str] = []
	last_lab_results: Dict[str, float] = {}
	consent: bool = False
	gdpr_consent_at: Optional[str] = None
	created_at: Optional[str] = None


class PatientCreate(BaseModel):
	first_name: str
	last_name: str
	dob: str
	height_cm: Optional[float] = None
	weight_kg: Optional[float] = None
	allergies: List[str] = []
	medications: List[str] = []
	comorbidities: List[str] = []
	last_lab_results: Dict[str, float] = {}
	consent: bool = False


class TaskStatus(str, Enum):
	pending = "pending"
	in_progress = "in_progress"
	completed = "completed"


class Task(BaseModel):
	id: str
	title: str
	description: Optional[str] = None
	status: TaskStatus = TaskStatus.pending


class ConsultationType(str, Enum):
	preop = "preop"
	postop = "postop"
	tele = "tele"


class Consultation(BaseModel):
	id: str
	patient_id: str
	type: ConsultationType
	scheduled_at: Optional[str] = None
	completed_at: Optional[str] = None
	notes: Optional[str] = None
	tasks: List[Task] = []


class InstructionRequest(BaseModel):
	patient_id: str