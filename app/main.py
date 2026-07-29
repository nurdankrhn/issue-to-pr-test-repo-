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
    }
