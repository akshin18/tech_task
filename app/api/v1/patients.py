from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import asc, desc

from app import crud, models, schemas
from app.db.session import get_db

router = APIRouter()


@router.get("/", response_model=schemas.PaginatedPatients)
async def list_patients(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0, description="Number of records to skip"),
    limit: int = Query(
        50, ge=1, le=100, description="Maximum number of records to return"
    ),
    sort_by: str = Query("id", description="Field to sort by"),
    sort_order: str = Query("asc", description="Sort order: asc or desc"),
    search: str | None = Query(None, description="Search term for patient name"),
):
    """
    Retrieve patients with pagination, sorting, and optional search.
    """
    # Validate sort parameters
    valid_sort_fields = {
        "id",
        "name",
        "date_of_birth",
        "medical_record_number",
        "created_at",
    }
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
    sort_column = getattr(models.Patient, sort_by)
    sort_clause = asc(sort_column) if sort_order == "asc" else desc(sort_column)

    # Build search filter
    search_filter = None
    if search:
        search_filter = models.Patient.name.ilike(f"%{search}%")

    patients, total = await crud.patient.get_multi_with_filter(
        db, skip=skip, limit=limit, sort_clause=sort_clause, search_filter=search_filter
    )

    # Calculate pagination info
    pages = (total + limit - 1) // limit

    return schemas.PaginatedPatients(
        patients=patients,
        total=total,
        page=(skip // limit) + 1,
        size=limit,
        pages=pages,
    )


@router.get("/{id}", response_model=schemas.Patient)
async def get_patient(id: int, db: AsyncSession = Depends(get_db)):
    """
    Get a specific patient by ID.
    """
    patient = await crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


@router.post("/", response_model=schemas.Patient)
async def create_patient(
    patient: schemas.PatientCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new patient.
    """
    # Check if patient with same medical record number already exists
    existing_patient = await crud.patient.get_by_mr_number(
        db, medical_record_number=patient.medical_record_number
    )
    if existing_patient:
        raise HTTPException(
            status_code=400,
            detail="Patient with this medical record number already exists",
        )

    return await crud.patient.create(db, obj_in=patient)


@router.put("/{id}", response_model=schemas.Patient)
async def update_patient(
    id: int, patient_in: schemas.PatientUpdate, db: AsyncSession = Depends(get_db)
):
    """
    Update an existing patient.
    """
    patient = await crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    # Update the patient
    updated_patient = await crud.patient.update(db, db_obj=patient, obj_in=patient_in)
    return updated_patient


@router.delete("/{id}")
async def delete_patient(id: int, db: AsyncSession = Depends(get_db)):
    """
    Delete a patient.
    """
    patient = await crud.patient.get(db, id=id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    await crud.patient.remove(db, id=id)
    return {"message": "Patient deleted successfully"}
