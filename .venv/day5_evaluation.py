import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix, classification_report

# 1. SETUP DIRTY DATA (Same as Day 4)
data = {
    'country': ['USA', 'IND', 'GER', 'USA', 'IND', 'MEX', 'CAN', np.nan, 'USA', 'IND', 'GER', 'MEX'], 
    'status': ['active', 'inactive', 'active', 'banned', 'active', 'active', 'inactive', 'banned', 'active', 'active', 'inactive', 'active'],
    'login_count': [45, 2, 12, 100, 5, 8, np.nan, 9, 55, 11, 3, 7]
}
df = pd.DataFrame(data)

# 2. CLEANING & ENGINEERING
# Impute
imputer_cat = SimpleImputer(strategy='most_frequent')
df['country'] = imputer_cat.fit_transform(df[['country']]).ravel()
imputer_num = SimpleImputer(strategy='mean')
df['login_count'] = imputer_num.fit_transform(df[['login_count']])

# Encode
# 0=Inactive, 1=Active, 2=Banned (Sorted Order: 0, 1, 2)
df['status_code'] = df['status'].map({'active': 1, 'inactive': 0, 'banned': 2})
top_2 = df['country'].value_counts().nlargest(2).index.tolist()
df['country_clean'] = df['country'].apply(lambda x: x if x in top_2 else 'OTHER')
df_final = pd.get_dummies(df, columns=['country_clean'], drop_first=True)

# Scale
scaler = StandardScaler()
df_final[['login_count']] = scaler.fit_transform(df_final[['login_count']])

# 3. SPLIT & TRAIN
X = df_final.drop(columns=['country', 'status', 'status_code'])
y = df_final['status_code']

# We force a specific split so we get a mix of classes for the demo
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.4, random_state=42)

model = LogisticRegression()
model.fit(X_train, y_train)

# 4. THE LIE DETECTOR (Day 5 New Stuff!)
y_pred = model.predict(X_test)

# Confusion Matrix: The Truth Table
# Scikit-learn sorts labels: 0 (Inactive), 1 (Active), 2 (Banned)
cm = confusion_matrix(y_test, y_pred)

print("--- 🕵️‍♀️ DAY 5: THE LIE DETECTOR ---")
print(f"Overall Accuracy: {model.score(X_test, y_test)*100:.1f}%\n")

print("--- CONFUSION MATRIX (Rows=Real, Cols=Pred) ---")
# We manually print this to make it readable in the terminal
try:
    print(f"               Pred Inactive | Pred Active | Pred Banned")
    print(f"Real Inactive:       {cm[0][0]}             {cm[0][1]}           {cm[0][2]}")
    print(f"Real Active:         {cm[1][0]}             {cm[1][1]}           {cm[1][2]}")
    print(f"Real Banned:         {cm[2][0]}             {cm[2][1]}           {cm[2][2]}")
except IndexError:
    print("Not enough data in test set to show full matrix!")
    print(cm)

print("\n--- CLASSIFICATION REPORT ---")
# Precision = When it guesses 'Banned', is it right?
# Recall = Did it find ALL the 'Banned' users?
print(classification_report(y_test, y_pred, target_names=['Inactive', 'Active', 'Banned'], zero_division=0))