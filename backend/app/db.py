from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Optional

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


@dataclass
class InMemoryUser:
	id: str
	email: str
	full_name: str
	role: str
	password_hash: str


@dataclass
class InMemoryPatient:
	id: str
	first_name: str
	last_name: str
	dob: str
	height_cm: Optional[float] = None
	weight_kg: Optional[float] = None
	allergies: List[str] = field(default_factory=list)
	medications: List[str] = field(default_factory=list)
	comorbidities: List[str] = field(default_factory=list)
	last_lab_results: Dict[str, float] = field(default_factory=dict)
	consent: bool = False
	gdpr_consent_at: Optional[str] = None
	created_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())


@dataclass
class InMemoryConsultation:
	id: str
	patient_id: str
	type: str
	scheduled_at: Optional[str] = None
	completed_at: Optional[str] = None
	notes: Optional[str] = None
	tasks: List[Dict] = field(default_factory=list)


class UserRepository:
	def __init__(self) -> None:
		self._users: Dict[str, InMemoryUser] = {}
		self._email_index: Dict[str, str] = {}

	def upsert(self, user: InMemoryUser) -> None:
		self._users[user.id] = user
		self._email_index[user.email.lower()] = user.id

	def get_by_email(self, email: str) -> Optional[InMemoryUser]:
		user_id = self._email_index.get(email.lower())
		return self._users.get(user_id) if user_id else None

	def verify_password(self, plain_password: str, password_hash: str) -> bool:
		return pwd_context.verify(plain_password, password_hash)

	def hash_password(self, plain_password: str) -> str:
		return pwd_context.hash(plain_password)


class PatientRepository:
	def __init__(self) -> None:
		self._patients: Dict[str, InMemoryPatient] = {}

	def upsert(self, patient: InMemoryPatient) -> None:
		self._patients[patient.id] = patient

	def list(self) -> List[InMemoryPatient]:
		return list(self._patients.values())

	def get(self, patient_id: str) -> Optional[InMemoryPatient]:
		return self._patients.get(patient_id)


class ConsultationRepository:
	def __init__(self) -> None:
		self._consultations: Dict[str, InMemoryConsultation] = {}

	def upsert(self, consultation: InMemoryConsultation) -> None:
		self._consultations[consultation.id] = consultation

	def list_by_patient(self, patient_id: str) -> List[InMemoryConsultation]:
		return [c for c in self._consultations.values() if c.patient_id == patient_id]


class AuditLogger:
	async def log(self, when: datetime, actor: str, action: str, status_code: int) -> None:
		line = f"{when.isoformat()}\t{actor}\t{action}\t{status_code}\n"
		with open("audit.log", "a", encoding="utf-8") as f:
			f.write(line)


users = UserRepository()
patients = PatientRepository()
consultations = ConsultationRepository()
audit_logger = AuditLogger()