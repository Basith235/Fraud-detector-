import os
from dotenv import load_dotenv

# 1. LOAD SECRETS
# This command looks for the .env file and loads it into memory
load_dotenv()

print("--- 🔐 DAY 21: SECURITY CHECK ---")

# 2. GET THE SECRET
# We use os.getenv() to grab the value.
# If the file is missing, it returns None (safety check).
api_key = os.getenv("STARTUP_API_KEY")
environment = os.getenv("APP_ENV")

# 3. VERIFY
if api_key:
    print(f"✅ SUCCESS: Found API Key!")
    # We only print the first few chars for safety (Never print the whole key in logs!)
    print(f"   Key value: {api_key[:4]}********")
    print(f"   Environment: {environment}")
else:
    print("❌ ERROR: Could not find .env file or STARTUP_API_KEY is missing.")
    print("   Make sure you created a file named '.env' in this folder.")