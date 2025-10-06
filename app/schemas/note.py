from datetime import datetime
from pydantic import BaseModel


class PatientNoteBase(BaseModel):
    patient_id: int
    content: str
    timestamp: datetime | None = None
    note_type: str | None = "general"


class PatientNoteCreate(PatientNoteBase):
    pass


class PatientNoteUpdate(BaseModel):
    content: str | None = None
    note_type: str | None = None


class PatientNote(PatientNoteBase):
    id: int
    created_at: datetime
    updated_at: datetime | None = None

    class Config:
        from_attributes = True


class PatientSummary(BaseModel):
    patient_info: str
    summary: str


class PaginatedNotes(BaseModel):
    notes: list[PatientNote]
    total: int
    page: int
    size: int
    pages: int
