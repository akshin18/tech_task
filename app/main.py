from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import patients, notes
from app.core.config import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Healthcare Data Processing API",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/health", status_code=200)
def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok"}


app.include_router(
    patients.router, prefix=f"{settings.API_V1_STR}/patients", tags=["patients"]
)
app.include_router(notes.router, prefix=settings.API_V1_STR, tags=["notes"])
