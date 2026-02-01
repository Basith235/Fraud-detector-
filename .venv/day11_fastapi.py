from fastapi import FastAPI

# 1. INITIALIZE THE APP
# This creates the server instance.
app = FastAPI()

# 2. DEFINE A "ROUTE" (Endpoint)
# When a user visits the root URL ("/"), run this function.
@app.get("/")
def home():
    """
    The 'Hello World' of your API.
    Returns a simple JSON message to prove the server is running.
    """
    return {"message": "System is operational. AI Brain is sleeping."}

# 3. DEFINE A SECOND ROUTE
# When a user visits "/status", run this.
@app.get("/status")
def status_check():
    return {"status": "OK", "version": "1.0.0"} 