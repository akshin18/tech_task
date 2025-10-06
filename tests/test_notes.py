

def test_create_note(client):
    # First create a patient
    patient_response = client.post(
        "/api/v1/patients/",
        json={
            "name": "Test Patient",
            "date_of_birth": "1990-01-01",
            "medical_record_number": "MRNTEST001",
        },
    )
    patient_id = patient_response.json()["id"]

    # Then create a note for the patient
    response = client.post(
        f"/api/v1/patients/{patient_id}/notes",
        json={
            "patient_id": patient_id,
            "content": "This is a test note",
            "note_type": "general",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "This is a test note"
    assert data["patient_id"] == patient_id


def test_get_note(client):
    # First create a patient
    patient_response = client.post(
        "/api/v1/patients/",
        json={
            "name": "Test Patient 2",
            "date_of_birth": "1985-05-15",
            "medical_record_number": "MRNTEST002",
        },
    )
    patient_id = patient_response.json()["id"]

    # Create a note
    note_response = client.post(
        f"/api/v1/patients/{patient_id}/notes",
        json={
            "patient_id": patient_id,
            "content": "Another test note",
            "note_type": "follow-up",
        },
    )
    note_id = note_response.json()["id"]

    # Get the note
    response = client.get(f"/api/v1/patients/{patient_id}/notes/{note_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["content"] == "Another test note"


def test_list_patient_notes(client):
    # First create a patient
    patient_response = client.post(
        "/api/v1/patients/",
        json={
            "name": "Test Patient 3",
            "date_of_birth": "1980-10-10",
            "medical_record_number": "MRNTEST003",
        },
    )
    patient_id = patient_response.json()["id"]

    # Create a note
    client.post(
        f"/api/v1/patients/{patient_id}/notes",
        json={
            "patient_id": patient_id,
            "content": "List test note",
            "note_type": "general",
        },
    )

    # List notes
    response = client.get(f"/api/v1/patients/{patient_id}/notes")
    assert response.status_code == 200
    data = response.json()
    assert "notes" in data
    assert "total" in data
