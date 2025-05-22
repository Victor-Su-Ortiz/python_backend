from fastapi import APIRouter

from app.schemas import medical

router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("/{patient_id}", response_model=medical.patient)
