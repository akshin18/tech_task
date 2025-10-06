from datetime import date
from pydantic import BaseModel

from .note import PatientNote


class PatientBase(BaseModel):
    name: str
    date_of_birth: date
    medical_record_number: str


class PatientCreate(PatientBase):
    pass


class PatientUpdate(BaseModel):
    name: str | None = None
    date_of_birth: date | None = None


class Patient(PatientBase):
    id: int

    class Config:
        from_attributes = True


class PatientWithNotes(Patient):
    notes: list["PatientNote"] = []


# For pagination
class PaginatedPatients(BaseModel):
    patients: list[Patient]
    total: int
    page: int
    size: int
    pages: int
