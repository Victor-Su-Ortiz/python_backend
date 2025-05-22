from typing import Dict, List
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException

from app.schemas import medical

appointments: Dict[int, medical.Appointment] = {
    1: medical.Appointment(
        id=1,
        patient_id=1,
        doctor_id=2,
        start_time=datetime.now(),
        end_time=datetime.now()
    )
}


router = APIRouter(prefix="/patients", tags=["patients"])

@router.get("/{patient_id}", response_model=medical.Patient)
def get_patient(
    patient_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user),
):
    """
    Get a patient by ID
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient
)
