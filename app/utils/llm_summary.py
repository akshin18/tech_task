from app.models.note import PatientNote
from app.models.patient import Patient
from app.schemas.note import PatientSummary
from datetime import date


async def generate_patient_summary(
    patient: Patient, notes: list[PatientNote]
) -> PatientSummary:
    """
    Generate a patient summary using LLM.
    This is a mock implementation that will be replaced with actual LLM integration.
    """
    # Calculate patient age
    today = date.today()
    age = (today - patient.date_of_birth).days // 365

    patient_info = (
        f"Name: {patient.name}, Age: {age}, MRN: {patient.medical_record_number}"
    )

    if not notes:
        summary = "No clinical notes available for this patient."
    else:
        # In a real implementation, this would use an LLM to generate a comprehensive summary
        # For now, we'll create a structured summary from the notes
        summary_parts = [
            f"Patient has {len(notes)} clinical note{'s' if len(notes) != 1 else ''}.",
            "",
            "Clinical Timeline:",
        ]

        # Sort notes by timestamp
        sorted_notes = sorted(notes, key=lambda x: x.timestamp)

        for note in sorted_notes:
            note_date = note.timestamp.strftime("%Y-%m-%d %H:%M")
            summary_parts.append(f"  {note_date}: {note.content}")

        summary = "\n".join(summary_parts)

    return PatientSummary(patient_info=patient_info, summary=summary)


def generate_mock_summary_for_testing(
    patient: Patient, notes: list[PatientNote]
) -> PatientSummary:
    """
    Generate a mock summary for testing purposes without async.
    """
    today = date.today()
    age = (today - patient.date_of_birth).days // 365

    patient_info = (
        f"Name: {patient.name}, Age: {age}, MRN: {patient.medical_record_number}"
    )

    if not notes:
        summary = "No clinical notes available for this patient."
    else:
        summary_parts = [
            f"Patient has {len(notes)} clinical note{'s' if len(notes) != 1 else ''}.",
            "",
            "Clinical Timeline:",
        ]

        sorted_notes = sorted(notes, key=lambda x: x.timestamp)

        for note in sorted_notes:
            note_date = note.timestamp.strftime("%Y-%m-%d %H:%M")
            summary_parts.append(f"  {note_date}: {note.content}")

        summary = "\n".join(summary_parts)

    return PatientSummary(patient_info=patient_info, summary=summary)


async def generate_patient_summary_with_llm(
    patient: Patient, notes: list[PatientNote]
) -> PatientSummary:
    """
    Generate a patient summary using actual LLM integration.
    This function would call an LLM API to create a comprehensive summary.
    """
    # Calculate patient age
    today = date.today()
    age = (today - patient.date_of_birth).days // 365

    patient_info = (
        f"Name: {patient.name}, Age: {age}, MRN: {patient.medical_record_number}"
    )

    if not notes:
        summary = "No clinical notes available for this patient."
    else:
        # Prepare the prompt for the LLM
        notes_text = "\n".join(
            [
                f"- {note.timestamp.strftime('%Y-%m-%d %H:%M')} ({note.note_type}): {note.content}"
                for note in sorted(notes, key=lambda x: x.timestamp)
            ]
        )

        # In a real implementation, we would call an LLM API like OpenAI
        # For now, we'll return a structured summary that mimics what an LLM might produce
        summary = f"""Patient Summary for {patient.name} (Age: {age}, MRN: {patient.medical_record_number})

Chief Complaints:
- Based on clinical notes provided

History of Present Illness:
- Multiple clinical encounters documented

Physical Examination:
- As noted in clinical records

Assessment:
- Based on clinical notes from {len(notes)} encounter{"s" if len(notes) != 1 else ""}

Plan:
- Ongoing monitoring and treatment as per clinical notes

Clinical Timeline:
{notes_text}"""

    return PatientSummary(patient_info=patient_info, summary=summary)
