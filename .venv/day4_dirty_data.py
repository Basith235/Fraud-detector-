import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

# 1. THE DIRTY DATASET (Simulation of Real World Data)
# Notice 'np.nan'? These are blank/missing values that break models.
data = {
    'country': ['USA', 'IND', 'GER', 'USA', 'IND', 'MEX', 'CAN', np.nan, 'USA', 'IND', 'GER', 'MEX'], 
    'status': ['active', 'inactive', 'active', 'banned', 'active', 'active', 'inactive', 'banned', 'active', 'active', 'inactive', 'active'],
    'login_count': [45, 2, 12, 100, 5, 8, np.nan, 9, 55, 11, 3, 7]
}
df = pd.DataFrame(data)

print("--- 🧹 RAW DIRTY DATA (Count of Missing Values) ---")
print(df.isnull().sum()) # This counts the blanks

# 2. CLEANING PHASE (The Janitor)

# A. Fix Missing Categorical Data (Country)
# Rule: If country is missing, assume it is the "Most Frequent" one (Mode).
imputer_cat = SimpleImputer(strategy='most_frequent')
# We reshape(-1,1) because Imputer expects a 2D array, not a 1D list
df['country'] = imputer_cat.fit_transform(df[['country']]).ravel()

# B. Fix Missing Numerical Data (Login Count)
# Rule: If number is missing, assume it is the "Average" (Mean).
imputer_num = SimpleImputer(strategy='mean')
df['login_count'] = imputer_num.fit_transform(df[['login_count']])

# 3. FEATURE ENGINEERING (Day 1 & 2 Recap)
df['status_code'] = df['status'].map({'active': 1, 'inactive': 0, 'banned': 2})

# "Other" Strategy
top_2 = df['country'].value_counts().nlargest(2).index.tolist()
df['country_clean'] = df['country'].apply(lambda x: x if x in top_2 else 'OTHER')

# One-Hot Encoding
df_final = pd.get_dummies(df, columns=['country_clean'], drop_first=True)

# 4. SCALING (New Concept!)
# We shrink 'login_count' so it doesn't overpower the small 0s and 1s of the country columns.
scaler = StandardScaler()
df_final[['login_count']] = scaler.fit_transform(df_final[['login_count']])

# 5. TRAIN (Same as Day 3)
X = df_final.drop(columns=['country', 'status', 'status_code'])
y = df_final['status_code']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

print("\n--- ✅ DAY 4: CLEANED & TRAINED ---")
print(f"Model Accuracy on Dirty Data: {model.score(X_test, y_test) * 100:.1f}%")