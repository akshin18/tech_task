# This file makes app.models a Python package
from .patient import Patient
from .note import PatientNote

__all__ = ["Patient", "PatientNote"]
