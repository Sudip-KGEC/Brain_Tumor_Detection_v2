from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from routes import router

app = FastAPI(
    title="Brain Tumor Detection API",
    description="Final Year Brain Tumor Detection Project using CNN + ESP32",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # React/Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(router, prefix="/api")

@app.get("/")
def root():
    return {
        "message": "Brain Tumor Detection API Running",
        "status": "success"
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

if __name__ == "__main__":
    # Ensure reload is OFF to prevent multiprocessing port hijacking
    uvicorn.run("app:app", host="0.0.0.0", port=8000)