from datetime import datetime
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .db import audit_logger
from .routers.auth import router as auth_router
from .routers.patients import router as patients_router
from .routers.consultations import router as consultations_router
from .routers.teleconsult import router as teleconsult_router
from .seed import seed_sample_data


settings = get_settings()

app = FastAPI(
	title="Anesth AI",
	description="AI-assisted pre-op and post-op workflow for anesthetists in France",
	version="0.1.0",
)

# CORS for local dev and configurable origins
app.add_middleware(
	CORSMiddleware,
	allow_origins=settings.cors_origins,
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)


@app.middleware("http")
async def audit_middleware(request: Request, call_next):
	start = datetime.utcnow()
	response = await call_next(request)
	try:
		user_id = request.headers.get("x-user-id", "anonymous")
		await audit_logger.log(
			when=start,
			actor=user_id,
			action=f"{request.method} {request.url.path}",
			status_code=response.status_code,
		)
	except Exception:
		# Do not break responses due to logging
		pass
	return response


@app.on_event("startup")
async def on_startup() -> None:
	await seed_sample_data()


@app.get("/health")
async def health() -> dict:
	return {"status": "ok", "time": datetime.utcnow().isoformat()}


# Routers
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(patients_router, prefix="/patients", tags=["patients"])
app.include_router(consultations_router, prefix="/consultations", tags=["consultations"])
app.include_router(teleconsult_router, prefix="/teleconsult", tags=["teleconsult"])