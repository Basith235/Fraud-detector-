import pandas as pd

# --- THE DATASET ---
data = {
    'user_id': ['a1', 'b2', 'c3', 'd4', 'e5', 'f6', 'g7', 'h8'],
    # MESSY DATA: Many countries with only 1 user each
    'country': ['USA', 'IND', 'GER', 'USA', 'IND', 'MEX', 'CAN', 'CHL'], 
    'status': ['active', 'inactive', 'active', 'banned', 'active', 'active', 'inactive', 'banned'],
    'login_count': [5, 0, 12, 100, 2, 8, 1, 9]
}
df = pd.DataFrame(data)

# --- THE "OTHER" STRATEGY (Managing Complexity) ---

# 1. Identify the Top 2 (USA and IND)
top_2 = df['country'].value_counts().nlargest(2).index.tolist()
print(f"Top 2 Markets identified: {top_2}")

# 2. Group the rest into 'OTHER'
# This stops our Dot Product matrix from becoming too wide.
df['country_cleaned'] = df['country'].apply(lambda x: x if x in top_2 else 'OTHER')

# 3. One-Hot Encoding (The Binary Switches)
# We now only get columns for USA and OTHER. (GER/IND are handled by logic/drop_first)
df_final = pd.get_dummies(df, columns=['country_cleaned'], prefix='country', drop_first=True)

# Mapping Status (Day 2 Recap)
status_mapping = {'active': 1, 'inactive': 0, 'banned': 2}
df_final['status_code'] = df['status'].map(status_mapping)

print("\n--- FINAL CLEANED VIEW ---")
# See how MEX, CAN, CHL, and GER all effectively became 'OTHER'
cols_to_show = ['user_id', 'country', 'country_OTHER', 'country_USA', 'status_code']
print(df_final[cols_to_show])

print("\n✅ RESULT: 8 countries reduced to 2 binary columns. Performance optimized!")