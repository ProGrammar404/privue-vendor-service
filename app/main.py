from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.routers import vendor, metric, score, admin
from app.db_migrations import run_migrations


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    try:
        print("🚀 Applying database migrations...")
        await run_migrations()
        print("✅ Migrations complete!")
    except Exception as e:
        print(f"❌ Migration failed: {e}")
    yield
    # Shutdown (optional cleanup here later)
    print("🔻 Application shutting down...")


app = FastAPI(
    title="Vendor Performance Service",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


# API Routers
app.include_router(vendor.router, prefix="/vendors", tags=["Vendors"])
app.include_router(metric.router, prefix="/metrics", tags=["Metrics"])
app.include_router(score.router, prefix="/scores", tags=["Scores"])
app.include_router(admin.router, prefix="/admin", tags=["Admin"])
