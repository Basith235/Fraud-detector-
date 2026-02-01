import pandas as pd
import numpy as np
import joblib
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

# CONFIGURATION (Global Variables)
MODEL_FILE = "startup_model.pkl"

# --- TOOL 1: THE TRAINER ---
def train_brain():
    """
    Simulates loading data, training the model, and saving it to disk.
    Returns: The accuracy score.
    """
    print("⚙️  TRAINING: Starting process...")
    
    # 1. GENERATE DATA (Same as Day 6/7)
    np.random.seed(42)
    n_users = 1000
    logins = np.random.randint(0, 100, size=n_users)
    status_list = [2 if l > 85 else 0 if l < 10 else 1 for l in logins]
    
    df = pd.DataFrame({'login_count': logins, 'status_code': status_list})
    
    # 2. TRAIN
    X = df[['login_count']]
    y = df['status_code']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LogisticRegression()
    model.fit(X_train, y_train)
    
    # 3. SAVE
    joblib.dump(model, MODEL_FILE)
    accuracy = model.score(X_test, y_test)
    
    print(f"✅ TRAINING: Model saved to '{MODEL_FILE}' with {accuracy*100:.1f}% accuracy.")
    return accuracy

# --- TOOL 2: THE PREDICTOR ---
def ask_brain(login_count):
    """
    Loads the saved model and predicts the status for a SINGLE user.
    Args:
        login_count (int): The number of times the user logged in.
    Returns:
        str: 'Active', 'Inactive', or 'Banned'
    """
    # 1. LOAD
    try:
        model = joblib.load(MODEL_FILE)
    except FileNotFoundError:
        return "ERROR: Model not found. Run train_brain() first."

    # 2. PREDICT
    # FIX: We create a DataFrame with the same column name used in training ('login_count')
    # This prevents the "X does not have valid feature names" warning.
    user_df = pd.DataFrame([[login_count]], columns=['login_count'])
    prediction_code = model.predict(user_df)[0]
    
    # 3. TRANSLATE
    labels = {0: 'Inactive', 1: 'Active', 2: 'Banned'}
    return labels[prediction_code]

# --- MAIN EXECUTION BLOCK ---
# This ensures the code runs only when we tell it to.
if __name__ == "__main__":
    
    # Step 1: Train the brain once
    train_brain()
    
    # Step 2: Test the brain multiple times
    print("\n--- 🧪 TESTING THE FUNCTIONS ---")
    
    user1 = 95
    print(f"User with {user1} logins is: {ask_brain(user1)}")
    
    user2 = 5
    print(f"User with {user2} logins is: {ask_brain(user2)}")
    
    user3 = 50
    print(f"User with {user3} logins is: {ask_brain(user3)}")