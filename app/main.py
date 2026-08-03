from datetime import datetime, timezone
from fastapi import FastAPI


app = FastAPI(
    title="Issue to PR Test API",
    version="1.0.0",
)


@app.get("/")
def root():
    return {
        "message": "Test API is running.",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "version": app.version,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/info")
def info():
    return {
        "service_name": "issue-to-pr-test-repo",
        "application_version": app.version,
        "environment": "development",
    }
