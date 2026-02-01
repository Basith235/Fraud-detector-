import pandas as pd
import numpy as np
import joblib  # <--- THE NEW TOOL (For saving)
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# 1. GENERATE DATA (Same as Day 6)
np.random.seed(42)
n_users = 1000
logins = np.random.randint(0, 100, size=n_users)
countries = np.random.choice(['USA', 'IND', 'GER', 'FRA', 'MEX'], size=n_users)

status_list = []
for l in logins:
    if l > 85: status_list.append(2) # Banned
    elif l < 10: status_list.append(0) # Inactive
    else: status_list.append(1) # Active

df = pd.DataFrame({'country': countries, 'login_count': logins, 'status_code': status_list})

# 2. PREPARE & TRAIN
# (We are skipping the cleaning/scaling details just to focus on the SAVING part today)
X = df[['login_count']] # Simple model using just logins
y = df['status_code']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

print(f"--- 🧠 TRAINING COMPLETE ---")
print(f"Model Accuracy in RAM: {model.score(X_test, y_test)*100:.1f}%")

# 3. SAVE THE BRAIN (The "Save Game" Point)
model_filename = "startup_model.pkl"
joblib.dump(model, model_filename)
print(f"\n💾 Model saved to file: '{model_filename}'")

# 4. SIMULATE RESTART
print("Deleting model from RAM...")
del model  # This deletes the variable from memory

# 5. LOAD THE BRAIN (The "Load Game" Point)
# This is what your API will do in Phase 2
loaded_model = joblib.load(model_filename)
print(f"📂 Model loaded back from disk!")

# 6. PROVE IT WORKS
# Make a prediction with the loaded brain
test_user = [[90]] # A user with 90 logins (Should be Banned/2)
prediction = loaded_model.predict(test_user)[0]

labels = {0: 'Inactive', 1: 'Active', 2: 'Banned'}
print(f"\n🔮 Prediction for 90 logins: {labels[prediction]}")