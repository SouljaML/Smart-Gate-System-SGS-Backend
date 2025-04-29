# from fastapi import FastAPI

# from app.db.database import init_db
import os
import uvicorn
from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.routes.gate_routes import router as gate_router  # Ensure this is imported
from app.routes.api_key_route import router as api_router
from app.db.database import init_db  # Ensure this is imported

# from app.routes.websocket_routes import router as websocket_router
# from app.routes.Websocket import websocket_endpoint as socket_conn

app = FastAPI(title="Smart Gate System API", version="1.0.0")

# Include routes
app.include_router(gate_router)
app.include_router(api_router)
# app.include_router(websocket_router)
# app.include_router(gate_router, prefix="/gate", tags=["Gate"])
app.include_router(user_router, prefix="/users", tags=["Users"])


@app.get("/")
def root():
    return {"message": "Welcome to the Smart Gate System API"}


@app.on_event("startup")
def startup_event():
    init_db()


# Ensure FastAPI runs on PORT 8080 when deployed
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))  # Use Cloud Run's PORT env variable
    uvicorn.run(app, host="0.0.0.0", port=port)
