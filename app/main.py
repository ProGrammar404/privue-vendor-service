from fastapi import FastAPI
from app.routers import vendor
from app.routers import metric
from app.routers import score
from app.routers import admin

app = FastAPI(
    title="Vendor Performance Service",
    version="1.0.0"
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

app.include_router(vendor.router, prefix="/vendors", tags=["Vendors"])
app.include_router(metric.router, prefix="/metrics", tags=["Metrics"])
app.include_router(score.router, prefix="/scores", tags=["Scores"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
