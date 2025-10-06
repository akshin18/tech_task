from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from app.crud.base import CRUDBase
from app.models.patient import Patient
from app.schemas.patient import PatientCreate, PatientUpdate


class CRUDPatient(CRUDBase[Patient, PatientCreate, PatientUpdate]):
    async def get_by_mr_number(
        self, db: AsyncSession, *, medical_record_number: str
    ) -> Patient | None:
        result = await db.execute(
            select(Patient).filter(
                Patient.medical_record_number == medical_record_number
            )
        )
        return result.scalar_one_or_none()

    async def get_multi_with_filter(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
        sort_clause=None,
        search_filter=None,
    ) -> tuple[list[Patient], int]:
        query = select(Patient)

        # Apply search filter if provided
        if search_filter is not None:
            query = query.where(search_filter)

        # Get total count before pagination
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Apply sorting and pagination
        if sort_clause is not None:
            query = query.order_by(sort_clause)

        query = query.offset(skip).limit(limit)
        patients_result = await db.execute(query)
        patients = patients_result.scalars().all()

        return patients, total


patient = CRUDPatient(Patient)
