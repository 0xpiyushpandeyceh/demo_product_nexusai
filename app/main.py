"""CivicFix Lite API."""
from fastapi import FastAPI

from .routes import analytics, issues

app = FastAPI(title="CivicFix Lite", version="0.1.0")
app.include_router(issues.router)
app.include_router(analytics.router)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
