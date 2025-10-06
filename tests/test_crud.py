import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.patient import patient
from app.crud.note import note
from app.schemas.patient import PatientCreate
from app.schemas.note import PatientNoteCreate
from datetime import date


@pytest.mark.asyncio
async def test_create_patient_crud(session: AsyncSession):
    patient_data = PatientCreate(
        name="Test Patient",
        date_of_birth=date(1990, 1, 1),
        medical_record_number="MRNTEST001",
    )
    created_patient = await patient.create(session, obj_in=patient_data)

    assert created_patient.name == "Test Patient"
    assert created_patient.medical_record_number == "MRNTEST001"

    # Test get
    retrieved_patient = await patient.get(session, id=created_patient.id)
    assert retrieved_patient is not None
    assert retrieved_patient.name == "Test Patient"


@pytest.mark.asyncio
async def test_update_patient_crud(session: AsyncSession):
    # Create a patient first
    patient_data = PatientCreate(
        name="Original Name",
        date_of_birth=date(1990, 1, 1),
        medical_record_number="MRNTEST002",
    )
    created_patient = await patient.create(session, obj_in=patient_data)

    # Update the patient
    from app.schemas.patient import PatientUpdate

    update_data = PatientUpdate(name="Updated Name")
    updated_patient = await patient.update(
        session, db_obj=created_patient, obj_in=update_data
    )

    assert updated_patient.name == "Updated Name"


@pytest.mark.asyncio
async def test_create_note_crud(session: AsyncSession):
    # Create a patient first
    patient_data = PatientCreate(
        name="Note Test Patient",
        date_of_birth=date(1990, 1, 1),
        medical_record_number="MRNTEST003",
    )
    created_patient = await patient.create(session, obj_in=patient_data)

    # Create a note for the patient
    note_data = PatientNoteCreate(
        patient_id=created_patient.id,
        content="This is a test note",
        note_type="general",
    )
    created_note = await note.create(session, obj_in=note_data)

    assert created_note.content == "This is a test note"
    assert created_note.patient_id == created_patient.id

    # Test get
    retrieved_note = await note.get(session, id=created_note.id)
    assert retrieved_note is not None
    assert retrieved_note.content == "This is a test note"


@pytest.mark.asyncio
async def test_get_multi_notes_crud(session: AsyncSession):
    # Create a patient first
    patient_data = PatientCreate(
        name="Multi Note Test Patient",
        date_of_birth=date(1990, 1, 1),
        medical_record_number="MRNTEST004",
    )
    created_patient = await patient.create(session, obj_in=patient_data)

    # Create multiple notes
    for i in range(3):
        note_data = PatientNoteCreate(
            patient_id=created_patient.id,
            content=f"Test note {i + 1}",
            note_type="general",
        )
        await note.create(session, obj_in=note_data)

    # Get all notes for the patient
    notes, total = await note.get_multi_by_patient(
        session, patient_id=created_patient.id
    )

    assert len(notes) == 3
    assert total == 3
