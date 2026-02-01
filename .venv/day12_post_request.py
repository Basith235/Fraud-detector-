from fastapi import FastAPI
from pydantic import BaseModel

# 1. DEFINE THE DATA SHAPE (The Bouncer)
# This Class tells the API: "I only accept data that looks exactly like this."
class UserInput(BaseModel):
    login_count: int
    country: str = "USA" # Default to USA if missing

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Day 12: Ready to accept POST requests."}

# 2. DEFINE THE POST ENDPOINT (The Ears)
# Notice we use @app.post instead of @app.get
@app.post("/predict")
def predict_status(data: UserInput):
    """
    Receives user data, validates it, and prints it to the terminal.
    """
    # FastAPI automatically validates 'data' before this line runs.
    
    print(f"📥 RECEIVED DATA: {data}")
    print(f"   Login Count: {data.login_count}")
    print(f"   Country: {data.country}")
    
    # SIMULATION (We will connect the real brain in Day 13)
    if data.login_count > 85:
        return {"result": "Banned", "confidence": 0.99}
    else:
        return {"result": "Active", "confidence": 0.85}