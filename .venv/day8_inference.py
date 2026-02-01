import joblib

# 1. SETUP
# In a real startup, this script runs on a server that has never seen the training data.
model_filename = "startup_model.pkl"

print(f"--- 🚀 DAY 8: SIMULATING PRODUCTION SERVER ---")
print(f"Loading brain from: {model_filename}...")

# 2. LOAD THE BRAIN
try:
    # This reads the binary weights from the hard drive
    loaded_model = joblib.load(model_filename)
    print("✅ Model loaded successfully!")
except FileNotFoundError:
    print("❌ ERROR: You need to run day7_save_model.py first to create the file!")
    exit()

# 3. NEW USER ARRIVES
# Let's say a user logs in with 95 logins.
# The model expects a 2D list: [[login_count]]
new_user_data = [[95]] 

# 4. PREDICT
# We use [0] to open the box, as we learned!
prediction_code = loaded_model.predict(new_user_data)[0]

# 5. TRANSLATE
status_map = {0: 'Inactive', 1: 'Active', 2: 'Banned'}
final_status = status_map[prediction_code]

print(f"\nUser Login Count: {new_user_data[0][0]}")
print(f"AI Prediction: {final_status}")

if final_status == 'Banned':
    print("🚨 ACTION: BLOCK THIS USER IMMEDIATELY!")
else:
    print("✅ ACTION: Let them in.")