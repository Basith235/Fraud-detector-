from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import day9_refactoring

# --- PART 1: THE CONTRACT ---
class UserInput(BaseModel):
    login_count: int
    country: str = "USA"

# --- PART 2: THE SERVER SETUP ---
app = FastAPI(title="Startup AI MVP")

# ENABLE CORS (Critical for Professional Setup)
# Since the Website (Port 5500) and API (Port 8000) are separate,
# The browser will block connections unless we explicitly allow them here.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- PART 3: THE LOGIC ---
@app.get("/")
def health_check():
    return {"status": "operational", "model_version": "v1"}

@app.post("/predict_status")
def predict(data: UserInput):
    try:
        prediction = day9_refactoring.ask_brain(data.login_count)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {
        "user_login_count": data.login_count,
        "ai_decision": prediction,
        "action_required": "BLOCK" if prediction == "Banned" else "NONE"
    }

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.environ.get("PORT", 10000))
    # IT MUST SAY 0.0.0.0 HERE 👇
    uvicorn.run(app, host="0.0.0.0", port=port)