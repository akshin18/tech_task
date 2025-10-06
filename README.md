# Healthcare Data Processing API

A FastAPI-based backend application for processing healthcare data with modern API development practices.

## Features

- RESTful JSON API for managing patient records
- Patient note management with file upload support
- AI-powered patient summary generation
- Containerized deployment with Docker
- Comprehensive error handling and input validation
- Asynchronous database operations with SQLAlchemy and asyncpg
- Full CRUD operations for patients and their notes
- Built with Python 3.13 and FastAPI for high performance

## Prerequisites

- Docker and Docker Compose
- Python 3.13+ (for local development)

## Quick Start with Docker

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd healthcare-data-processing-api
   ```

2. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

3. Update the `.env` file with your configuration (optional for basic usage)

4. Start the services:
   ```bash
   docker-compose up --build
   ```

5. The API will be available at `http://localhost:8000`
6. API documentation will be available at `http://localhost:8000/docs`

## Local Development

1. Install uv (recommended package manager):
   ```bash
   pip install uv
   # Or install with homebrew: brew install uv
   ```

2. Install dependencies:
   ```bash
   uv sync --dev
   # This creates a virtual environment and installs all dependencies
   ```

3. Set up environment variables:
   ```bash
   cp .env.example .env
   # Update .env with your configuration
   ```

4. Initialize the database:
   ```bash
   python -c "import asyncio; from app.db.init_db import init_db; asyncio.run(init_db())"
   ```

5. Start the application:
   ```bash
   uv run uvicorn app.main:app --reload
   ```

## API Endpoints

### Health Check
- `GET /health` - Health check endpoint

### Patients
- `GET /api/v1/patients` - List all patients with pagination and search
- `GET /api/v1/patients/{id}` - Get a specific patient
- `POST /api/v1/patients` - Create a new patient
- `PUT /api/v1/patients/{id}` - Update a patient
- `DELETE /api/v1/patients/{id}` - Delete a patient

### Patient Notes
- `POST /api/v1/patients/{patient_id}/notes` - Create a new note for a specific patient
- `POST /api/v1/patients/{patient_id}/notes/upload` - Upload a note file for a patient
- `GET /api/v1/patients/{patient_id}/notes` - List all notes for a specific patient
- `GET /api/v1/patients/{patient_id}/notes/{note_id}` - Get a specific note
- `DELETE /api/v1/patients/{patient_id}/notes/{note_id}` - Delete a specific note

### Patient Summary
- `GET /api/v1/patients/{id}/summary` - Generate a summary for a patient based on their notes

## Configuration

The application can be configured using environment variables:

- `POSTGRES_SERVER`: PostgreSQL server address (default: localhost)
- `POSTGRES_USER`: PostgreSQL username (default: postgres)
- `POSTGRES_PASSWORD`: PostgreSQL password (default: postgres)
- `POSTGRES_DB`: PostgreSQL database name (default: healthcare_db)
- `OPENAI_API_KEY`: OpenAI API key for summary generation (optional)
- `LLM_MODEL`: LLM model to use for summaries (default: gpt-3.5-turbo)
- `SECRET_KEY`: Secret key for JWT tokens (auto-generated if not provided)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiration time in minutes (default: 30)
- `BACKEND_CORS_ORIGINS`: List of allowed origins for CORS (optional)

## Database Schema

The application uses PostgreSQL with the following main tables:

- `patients`: Stores patient information (id, name, date_of_birth, medical_record_number)
- `patient_notes`: Stores patient notes (id, patient_id, timestamp, content, note_type)

## API Documentation

Interactive API documentation is available at `/docs` when the application is running.
The documentation follows OpenAPI specification and includes examples and validation rules.

## Security

- Input validation using Pydantic models
- SQL injection prevention through SQLAlchemy ORM
- Proper error handling without exposing internal details
- JWT-based authentication (when implemented)
- CORS middleware for cross-origin requests

## Testing

To run tests:
```bash
# Install test dependencies (if not already installed)
uv sync --dev

# Run tests
uv run pytest
```

Or with docker:
```bash
docker-compose exec api pytest
```

## LLM Integration

The patient summary endpoint uses LLM integration for generating comprehensive summaries.
To enable this feature, set the `OPENAI_API_KEY` in your environment variables.
The application uses the `gpt-3.5-turbo` model by default, but this can be changed with the `LLM_MODEL` variable.

## File Upload

The application supports file uploads for patient notes. Files are processed and stored as note content in the database.

## Development

This project follows FastAPI best practices with:
- Dependency injection
- Pydantic models for validation
- SQLAlchemy ORM for database operations
- CRUD operations in separate layer
- Proper separation of concerns
- Async support where appropriate
- Modern Python packaging with uv and pyproject.toml

### Project Structure
```
app/
├── main.py                 # FastAPI application entry point
├── api/                    # API routes
│   └── v1/                 # API version 1
│       ├── patients.py     # Patient-related endpoints
│       └── notes.py        # Note-related endpoints
├── core/                   # Core application logic
│   ├── config.py           # Configuration settings
│   └── exceptions.py       # Custom exceptions
├── crud/                   # CRUD operations
│   ├── base.py             # Base CRUD operations
│   ├── patient.py          # Patient CRUD
│   └── note.py             # Note CRUD
├── db/                     # Database-related code
│   ├── base.py             # Base database models
│   ├── init_db.py          # Database initialization
│   └── session.py          # Database session management
├── models/                 # SQLAlchemy models
│   ├── patient.py          # Patient model (table: patients)
│   └── note.py             # PatientNote model (table: patient_notes)
├── schemas/                # Pydantic schemas
│   ├── patient.py          # Patient schemas
│   └── note.py             # Note schemas
└── utils/                  # Utility functions
    └── llm_summary.py      # LLM summary generation
```

## Dependencies

This project uses modern Python tooling:
- FastAPI: Web framework
- uvicorn: ASGI server
- SQLAlchemy: ORM with async support
- asyncpg: Asynchronous PostgreSQL driver
- Pydantic: Data validation
- OpenAI: LLM integration
- uv: Package installer and resolver (alternative to pip)

## License

MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.