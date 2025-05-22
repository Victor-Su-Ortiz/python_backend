# patient needs to book appointment with doctor
# time involved, location involved
# relationship between appointment and patient and doctor foreign key
# patient will have name, id, phone number, email, age
# doctor will have name, id, phone number
from typing import List
from enum import Enum
from datetime import date, datetime
from pydantic import BaseModel


class Specialty(str, Enum):
    """Doctor specialty"""

    ONCOLOGY = "oncology"
    DERMATOLOGY = "dermatology"
    RADIOLOGY = "radiology"


class Person(BaseModel):
    """base class for a person"""

    id: int
    name: str


class Appointment(BaseModel):
    """Appointmenet"""

    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    end_time: datetime


class Patient(Person):
    """Patient for the appointment"""

    appointments: List[Appointment]


class Doctor(Person):
    """Doctor for the appointment"""

    id: int
    specialty: Specialty
