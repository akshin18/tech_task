class PatientNotFoundException(Exception):
    """Exception raised when a patient is not found."""

    def __init__(self, patient_id: int):
        self.patient_id = patient_id
        super().__init__(f"Patient with id {patient_id} not found")


class NoteNotFoundException(Exception):
    """Exception raised when a note is not found."""

    def __init__(self, note_id: int):
        self.note_id = note_id
        super().__init__(f"Note with id {note_id} not found")
