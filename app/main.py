from datetime import datetime, timezone
from fastapi import FastAPI, HTTPException


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


@app.get("/calculate/sum")
def calculate_sum(a: int, b: int):
    """Sum calculation endpoint.

    'a' ve 'b' adında iki zorunlu integer query parametresi alır ve
    bu değerlerin toplamını, kendileriyle birlikte döner.

    'a' veya 'b' eksik ya da geçersiz bir tip ile gönderilirse, FastAPI'nin
    yerleşik doğrulaması otomatik olarak 422 Unprocessable Entity yanıtı
    döner; bu yüzden burada ekstra bir doğrulama koduna gerek yoktur.
    """
    # Yeni özellik için eklenen toplama işlemi
    result = a + b
    return {
        "a": a,
        "b": b,
        "result": result,
    }


@app.get("/calculate/multiply")
def calculate_multiply(a: int, b: int):
    """Multiply calculation endpoint.

    'a' ve 'b' adında iki zorunlu integer query parametresi alır ve
    bu değerlerin çarpımını, kendileriyle birlikte döner.

    'a' veya 'b' eksik ya da geçersiz bir tip ile gönderilirse, FastAPI'nin
    yerleşik doğrulaması otomatik olarak 422 Unprocessable Entity yanıtı
    döner; bu yüzden burada ekstra bir doğrulama koduna gerek yoktur.
    """
    # Yeni özellik için eklenen çarpma işlemi
    result = a * b
    return {
        "a": a,
        "b": b,
        "result": result,
    }


@app.get("/calculate/divide")
def calculate_divide(a: float, b: float):
    """Divide calculation endpoint.

    'a' ve 'b' adında iki zorunlu number query parametresi alır ve
    'a' değerinin 'b' değerine bölümünü, kendileriyle birlikte döner.

    'b' değeri 0 olduğunda HTTP 400 Bad Request yanıtı döner.

    'a' veya 'b' eksik ya da geçersiz bir tip ile gönderilirse, FastAPI'nin
    yerleşik doğrulaması otomatik olarak 422 Unprocessable Entity yanıtı
    döner; bu yüzden burada ekstra bir doğrulama koduna gerek yoktur.
    """
    # Yeni özellik için eklenen bölme işlemi
    if b == 0:
        raise HTTPException(
            status_code=400, detail="Division by zero is not allowed"
        )

    result = a / b

    # Sonuçları tam sayı olarak temsil edebiliyorsak int'e çeviriyoruz,
    # böylece örnekte olduğu gibi "5" döner, "5.0" değil.
    def _normalize(value: float):
        return int(value) if value.is_integer() else value

    return {
        "a": _normalize(a),
        "b": _normalize(b),
        "result": _normalize(result),
        "operation": "divide",
    }


@app.get("/calculate/subtract")
def calculate_subtract(a: int, b: int):
    """Subtract calculation endpoint.

    'a' ve 'b' adında iki zorunlu integer query parametresi alır ve
    'a' değerinden 'b' değerinin çıkarılması sonucunu, kendileriyle
    birlikte döner.

    'a' veya 'b' eksik ya da geçersiz bir tip ile gönderilirse, FastAPI'nin
    yerleşik doğrulaması otomatik olarak 422 Unprocessable Entity yanıtı
    döner; bu yüzden burada ekstra bir doğrulama koduna gerek yoktur.
    """
    # Yeni özellik için eklenen çıkarma işlemi
    result = a - b
    return {
        "a": a,
        "b": b,
        "result": result,
        "operation": "subtract",
    }
