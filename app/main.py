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


@app.get("/ready")
def ready():
    """Readiness check endpoint.

    Uygulamanın istekleri karşılamaya hazır olduğunu belirtmek için
    servis adı ve versiyon bilgisiyle birlikte "ready" durumunu döner.
    """
    return {
        "status": "ready",
        "service": "issue-to-pr-test-repo",
        "version": app.version,
    }


@app.get("/ping")
def ping():
    """Ping endpoint.

    Servisin ayakta olduğunu belirtmek için "ping" durumunu döner.
    """
    return {
        "status": "ping",
        "service": "issue-to-pr-test-repo",
    }
