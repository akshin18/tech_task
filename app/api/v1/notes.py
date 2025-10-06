from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc

from app import crud, models, schemas
from app.db.session import get_db

router = APIRouter()


@router.post("/patients/{patient_id}/notes", response_model=schemas.PatientNote)
async def create_patient_note(
    patient_id: int, note: schemas.PatientNoteCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new note for a patient.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Ensure the patient_id in the path matches the one in the request body
    if note.patient_id != patient_id:
        raise HTTPException(
            status_code=400, detail="Patient ID in path does not match request body"
        )

    return await crud.note.create(db, obj_in=note)


@router.post("/patients/{patient_id}/notes/upload", response_model=schemas.PatientNote)
async def upload_patient_note(
    patient_id: int,
    file: UploadFile = File(...),
    note_type: str = "general",
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a note file for a patient.
    Supports text files, PDFs, and other formats.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Read the file content
    content = await file.read()
    content_str = content.decode("utf-8")

    # Create a note object
    note_data = schemas.PatientNoteCreate(
        patient_id=patient_id, content=content_str, note_type=note_type
    )

    return await crud.note.create(db, obj_in=note_data)


@router.get("/patients/{patient_id}/notes", response_model=schemas.PaginatedNotes)
async def list_patient_notes(
    patient_id: int,
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        50, ge=1, le=100, description="Maximum number of records to return"
    ),
    sort_by: str = Query("timestamp", description="Field to sort by"),
    sort_order: str = Query("desc", description="Sort order: asc or desc"),
):
    """
    List all notes for a specific patient with pagination and sorting.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Validate sort parameters
    valid_sort_fields = {"id", "timestamp", "created_at", "updated_at", "note_type"}
    if sort_by not in valid_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort field. Valid fields: {valid_sort_fields}",
        )

    if sort_order not in {"asc", "desc"}:
        raise HTTPException(
            status_code=400, detail="Invalid sort order. Use 'asc' or 'desc'"
        )

    # Build sort clause
    sort_column = getattr(models.PatientNote, sort_by)
    sort_clause = asc(sort_column) if sort_order == "asc" else desc(sort_column)

    notes, total = await crud.note.get_multi_by_patient(
        db, patient_id=patient_id, skip=skip, limit=limit, sort_clause=sort_clause
    )

    # Calculate pagination info
    pages = (total + limit - 1) // limit

    return schemas.PaginatedNotes(
        notes=notes, total=total, page=(skip // limit) + 1, size=limit, pages=pages
    )


@router.get(
    "/patients/{patient_id}/notes/{note_id}", response_model=schemas.PatientNote
)
async def get_patient_note(
    patient_id: int, note_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Get a specific note for a patient.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get the note and verify it belongs to the specified patient
    note = await crud.note.get(db, id=note_id)
    if not note or note.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Note not found for this patient")

    return note


@router.delete("/patients/{patient_id}/notes/{note_id}")
async def delete_patient_note(
    patient_id: int, note_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Delete a specific note for a patient.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get the note and verify it belongs to the specified patient
    note = await crud.note.get(db, id=note_id)
    if not note or note.patient_id != patient_id:
        raise HTTPException(status_code=404, detail="Note not found for this patient")

    await crud.note.remove(db, id=note_id)
    return {"message": "Note deleted successfully"}


@router.get("/patients/{patient_id}/summary", response_model=schemas.PatientSummary)
async def get_patient_summary(patient_id: int, db: AsyncSession = Depends(get_db)):
    """
    Generate a summary for a patient based on their notes.
    """
    # Verify that the patient exists
    patient = await crud.patient.get(db, id=patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Get all notes for the patient
    notes, _ = await crud.note.get_multi_by_patient(
        db, patient_id=patient_id, limit=None
    )

    # Import the summary generation function
    from app.utils.llm_summary import generate_patient_summary_with_llm

    # Generate summary using the utility function
    summary_result = await generate_patient_summary_with_llm(patient, notes)

    return summary_result
