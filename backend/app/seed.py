from datetime import datetime
from uuid import uuid4

from .db import InMemoryPatient, InMemoryUser, patients, users


async def seed_sample_data() -> None:
	if users.get_by_email("anesth@example.com") is None:
		user = InMemoryUser(
			id=str(uuid4()),
			email="anesth@example.com",
			full_name="Dr. Ana Esth",
			role="anesthetist",
			password_hash=users.hash_password("changeme"),
		)
		users.upsert(user)

	# Seed a sample patient
	if not patients.list():
		p = InMemoryPatient(
			id=str(uuid4()),
			first_name="Jean",
			last_name="Dupont",
			dob="1980-05-15",
			height_cm=175.0,
			weight_kg=82.0,
			allergies=["penicillin"],
			medications=["aspirin"],
			comorbidities=["HTA"],
			last_lab_results={"creatinine": 1.1},
			consent=True,
			gdpr_consent_at=datetime.utcnow().isoformat(),
		)
		patients.upsert(p)