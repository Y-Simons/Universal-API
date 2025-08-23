from __future__ import annotations

from typing import Dict, List, Tuple

from .models import RiskLevel, RiskScore, Task


ASA_MAPPING = {
	0: (RiskLevel.low, 0.1),
	1: (RiskLevel.low, 0.2),
	2: (RiskLevel.moderate, 0.4),
	3: (RiskLevel.high, 0.7),
	4: (RiskLevel.very_high, 0.9),
	5: (RiskLevel.very_high, 0.98),
}


def score_patient(features: Dict) -> RiskScore:
	# Very naive placeholder: weight comorbidities, abnormal labs, BMI, age
	comorbidity_weight = min(len(features.get("comorbidities", [])) * 0.1, 0.5)
	abnormal_labs = 0.0
	for name, value in features.get("last_lab_results", {}).items():
		if name.lower() in {"creatinine", "troponin", "ntprobnp"} and value > 1.2:
			abnormal_labs += 0.2
	bmi = None
	h = features.get("height_cm")
	w = features.get("weight_kg")
	if h and w and h > 0:
		bmi = w / ((h / 100) ** 2)
	bmi_penalty = 0.15 if bmi and (bmi < 18.5 or bmi >= 35) else 0.0
	base = min(1.0, comorbidity_weight + abnormal_labs + bmi_penalty)
	asa_class = 1 if base < 0.25 else 2 if base < 0.5 else 3 if base < 0.75 else 4
	risk_level, mapped = ASA_MAPPING.get(asa_class, (RiskLevel.moderate, 0.5))
	score = max(mapped, base)
	rationale = (
		f"Comorbidities={len(features.get('comorbidities', []))}, "
		f"AbnormalLabs={abnormal_labs:.2f}, BMIpenalty={bmi_penalty:.2f}"
	)
	return RiskScore(asa_class=asa_class, risk_level=risk_level, score=round(score, 2), rationale=rationale)


def generate_preop_tasks(features: Dict, risk: RiskScore) -> List[Task]:
	base_tasks: List[Task] = []
	from uuid import uuid4

	base_tasks.append(Task(id=str(uuid4()), title="Consentement RGPD", description="Signer le consentement de traitement des données."))
	base_tasks.append(Task(id=str(uuid4()), title="Jeûne préopératoire", description="Arrêt d'alimentation 6h avant, liquides clairs jusqu'à 2h."))
	if any(m.lower().startswith("aspirin") or m.lower().startswith("clopidogrel") for m in features.get("medications", [])):
		base_tasks.append(Task(id=str(uuid4()), title="Arrêt des anti-plaquettaires", description="Suivre la conduite selon le chirurgien et l'anesthésiste."))
	if risk.risk_level in {RiskLevel.high, RiskLevel.very_high}:
		base_tasks.append(Task(id=str(uuid4()), title="Bilan préop complémentaire", description="ECG, bilan biologique, avis cardiologique si nécessaire."))
	return base_tasks


def generate_postop_tasks(features: Dict, risk: RiskScore) -> List[Task]:
	from uuid import uuid4
	return [
		Task(id=str(uuid4()), title="Contrôle douleur", description="Échelle EVA toutes les 4 heures"),
		Task(id=str(uuid4()), title="Prévention NVPO", description="Antiemétiques si nausées/vomissements"),
		Task(id=str(uuid4()), title="Mobilisation précoce", description="Selon protocole"),
	]