# This file makes app.schemas a Python package
from .patient import (
    Patient,
    PatientCreate,
    PatientUpdate,
    PatientWithNotes,
    PaginatedPatients,
)
from .note import (
    PatientNote,
    PatientNoteCreate,
    PatientNoteUpdate,
    PatientSummary,
    PaginatedNotes,
)

__all__ = [
    "Patient",
    "PatientCreate",
    "PatientUpdate",
    "PatientWithNotes",
    "PaginatedPatients",
    "PatientNote",
    "PatientNoteCreate",
    "PatientNoteUpdate",
    "PatientSummary",
    "PaginatedNotes",
]
