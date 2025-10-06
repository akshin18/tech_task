from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from app.crud.base import CRUDBase
from app.models.note import PatientNote
from app.schemas.note import PatientNoteCreate, PatientNoteUpdate


class CRUDNote(CRUDBase[PatientNote, PatientNoteCreate, PatientNoteUpdate]):
    async def get_multi_by_patient(
        self,
        db: AsyncSession,
        *,
        patient_id: int,
        skip: int = 0,
        limit: int = 100,
        sort_clause=None,
    ) -> tuple[list[PatientNote], int]:
        query = select(PatientNote).where(PatientNote.patient_id == patient_id)

        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply sorting if provided
        if sort_clause is not None:
            query = query.order_by(sort_clause)

        # Apply pagination
        query = query.offset(skip).limit(limit)
        notes_result = await db.execute(query)
        notes = notes_result.scalars().all()

        return notes, total


note = CRUDNote(PatientNote)
