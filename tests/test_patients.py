

def test_create_patient(client):
    response = client.post(
        "/api/v1/patients/",
        json={
            "name": "John Doe",
            "date_of_birth": "1990-01-01",
            "medical_record_number": "MRN123456",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["medical_record_number"] == "MRN123456"


def test_get_patient(client):
    # First create a patient
    create_response = client.post(
        "/api/v1/patients/",
        json={
            "name": "Jane Smith",
            "date_of_birth": "1985-05-15",
            "medical_record_number": "MRN789012",
        },
    )
    patient_id = create_response.json()["id"]

    # Then get the patient
    response = client.get(f"/api/v1/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Jane Smith"


def test_list_patients(client):
    response = client.get("/api/v1/patients/")
    assert response.status_code == 200
    data = response.json()
    assert "patients" in data
    assert "total" in data
