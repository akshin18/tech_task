"""
Script to initialize the database with sample data for testing.
"""

from datetime import date, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.db.base import Base
from app.models.patient import Patient
from app.models.note import PatientNote


def init_db_with_samples():
    # Create sync database engine and session
    # Replace asyncpg with psycopg2 for sync operations
    sync_db_uri = str(settings.SQLALCHEMY_DATABASE_URI).replace(
        "postgresql+asyncpg://", "postgresql://"
    )
    engine = create_engine(sync_db_uri)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Create tables
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        # Check if patients already exist
        if db.query(Patient).count() > 0:
            print("Database already has sample data. Skipping initialization.")
            return

        # Create sample patients
        patient1 = Patient(
            name="John Doe",
            date_of_birth=date(1985, 6, 15),
            medical_record_number="MRN001",
        )

        patient2 = Patient(
            name="Jane Smith",
            date_of_birth=date(1990, 11, 3),
            medical_record_number="MRN002",
        )

        patient3 = Patient(
            name="Robert Johnson",
            date_of_birth=date(1978, 3, 22),
            medical_record_number="MRN003",
        )

        db.add(patient1)
        db.add(patient2)
        db.add(patient3)
        db.commit()

        # Refresh to get IDs
        db.refresh(patient1)
        db.refresh(patient2)
        db.refresh(patient3)

        # Create sample notes for patient 1
        note1 = PatientNote(
            patient_id=patient1.id,
            timestamp=datetime(2024, 1, 15, 10, 30),
            content="Patient presented with chief complaint of persistent cough and mild fever for 3 days. No shortness of breath reported. Vital signs stable.",
            note_type="admission",
        )

        note2 = PatientNote(
            patient_id=patient1.id,
            timestamp=datetime(2024, 1, 16, 14, 20),
            content="Patient's condition improved. Cough reduced significantly. Temperature returned to normal. Discharge planned for tomorrow.",
            note_type="progress",
        )

        note3 = PatientNote(
            patient_id=patient1.id,
            timestamp=datetime(2024, 1, 17, 9, 15),
            content="Patient discharged with instructions to continue medication for 5 more days. Follow-up appointment scheduled in 2 weeks.",
            note_type="discharge",
        )

        # Create sample notes for patient 2
        note4 = PatientNote(
            patient_id=patient2.id,
            timestamp=datetime(2024, 2, 10, 11, 45),
            content="Routine checkup. Patient reports occasional headaches and fatigue. Blood pressure slightly elevated at 142/90.",
            note_type="checkup",
        )

        note5 = PatientNote(
            patient_id=patient2.id,
            timestamp=datetime(2024, 2, 20, 16, 30),
            content="Follow-up on blood pressure medication. Patient reports improvement in symptoms. Blood pressure now 130/85.",
            note_type="follow-up",
        )

        # Create sample notes for patient 3
        note6 = PatientNote(
            patient_id=patient3.id,
            timestamp=datetime(2024, 3, 5, 13, 10),
            content="Patient admitted for observation after minor car accident. Conscious and alert. No visible injuries except minor bruising on left arm.",
            note_type="admission",
        )

        note7 = PatientNote(
            patient_id=patient3.id,
            timestamp=datetime(2024, 3, 6, 10, 0),
            content="Patient doing well. No complications observed. Discharged with recommendation for follow-up in 1 week to ensure no delayed symptoms.",
            note_type="discharge",
        )

        db.add(note1)
        db.add(note2)
        db.add(note3)
        db.add(note4)
        db.add(note5)
        db.add(note6)
        db.add(note7)
        db.commit()

        print("Database initialized with sample patients and notes successfully!")

    except Exception as e:
        print(f"Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    init_db_with_samples()
