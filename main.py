from fastapi import FastAPI

from app.db.database import init_db
from app.routes.gate_routes import router as gate_router
from app.routes.user_routes import router as user_router


app = FastAPI(title="Smart Gate System API", version="1.0.0")

# Include routes
app.include_router(gate_router)
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "Welcome to the Smart Gate System API"}


@app.on_event("startup")
def startup_event():
    init_db()