import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

# 1. THE DATASET
data = {
    'country': ['USA', 'IND', 'GER', 'USA', 'IND', 'MEX', 'CAN', 'CHL', 'USA', 'IND', 'GER', 'MEX'], 
    'status': ['active', 'inactive', 'active', 'banned', 'active', 'active', 'inactive', 'banned', 'active', 'active', 'inactive', 'active'],
    'login_count': [45, 2, 12, 100, 5, 8, 1, 9, 55, 11, 3, 7]
}
df = pd.DataFrame(data)

# 2. PREP
df['status_code'] = df['status'].map({'active': 1, 'inactive': 0, 'banned': 2})
top_2 = df['country'].value_counts().nlargest(2).index.tolist()
df['country_clean'] = df['country'].apply(lambda x: x if x in top_2 else 'OTHER')
df_final = pd.get_dummies(df, columns=['country_clean'], drop_first=True)

# 3. SPLIT
X = df_final.drop(columns=['country', 'status', 'status_code'])
y = df_final['status_code']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# 4. TRAIN
model = LogisticRegression()
model.fit(X_train, y_train)

# 5. RESULT
accuracy = model.score(X_test, y_test)
print(f"--- 🧠 DAY 3 COMPLETE ---")
print(f"Model Accuracy Score: {accuracy * 100:.1f}%")