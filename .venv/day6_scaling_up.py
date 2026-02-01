import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report

# 1. DATA SIMULATOR (Generating 1,000 Users)
# We use a "Seed" so everyone gets the same random numbers
np.random.seed(42) 
n_users = 1000

# Generate random logins (0 to 100) and countries
logins = np.random.randint(0, 100, size=n_users)
countries = np.random.choice(['USA', 'IND', 'GER', 'FRA', 'MEX', 'CAN', 'BRA'], size=n_users)

# INJECTING THE HIDDEN PATTERN
# The logic: 
# - If logins > 85: They are a Bot -> 'banned'
# - If logins < 10: They are lazy -> 'inactive'
# - Everyone else -> 'active'
status_list = []
for l in logins:
    if l > 85:
        status_list.append('banned')
    elif l < 10:
        status_list.append('inactive')
    else:
        status_list.append('active')

# Create the DataFrame
data = {'country': countries, 'login_count': logins, 'status': status_list}
df = pd.DataFrame(data)

# Introduce Dirty Data (The Janitor Test)
# Set 50 random logins to NaN (Blank)
df.loc[np.random.choice(df.index, 50), 'login_count'] = np.nan

print(f"--- 📊 DAY 6: GENERATED {len(df)} USERS ---")
print(df['status'].value_counts()) # Show how many of each type we have

# 2. CLEANING (The Janitor)
imputer_num = SimpleImputer(strategy='mean')
df['login_count'] = imputer_num.fit_transform(df[['login_count']])
# (We skip country cleaning since we didn't add blanks there today)

# 3. FEATURE ENGINEERING
df['status_code'] = df['status'].map({'active': 1, 'inactive': 0, 'banned': 2})

# 'Other' Strategy (Top 3 this time)
top_3 = df['country'].value_counts().nlargest(3).index.tolist()
df['country_clean'] = df['country'].apply(lambda x: x if x in top_3 else 'OTHER')
df_final = pd.get_dummies(df, columns=['country_clean'], drop_first=True)

# Scaling
scaler = StandardScaler()
df_final[['login_count']] = scaler.fit_transform(df_final[['login_count']])

# 4. SPLIT & TRAIN
X = df_final.drop(columns=['country', 'status', 'status_code'])
y = df_final['status_code']

# 800 for Training, 200 for Testing
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# 5. EVALUATE
print("\n--- ✅ DAY 6 REPORT ---")
y_pred = model.predict(X_test)

# This time, we should see PLENTY of support for 'Banned' users
print(classification_report(y_test, y_pred, target_names=['Inactive', 'Active', 'Banned'], zero_division=0))