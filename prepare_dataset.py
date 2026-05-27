import pandas as pd

# Load your original dataset
df = pd.read_csv("dataset.csv")

# Convert column names to lowercase
df.columns = df.columns.str.lower()

# Rename columns (based on common Twitter datasets)
df.rename(columns={
    "followers_count": "followers",
    "friends_count": "following",
    "statuses_count": "posts"
}, inplace=True)

# Create missing columns (if not present)
df['likes'] = df.get('likes', 0)
df['comments'] = df.get('comments', 0)

# Create account_age (if not present)
if "created_at" in df.columns:
    df['created_at'] = pd.to_datetime(df['created_at'], errors='coerce')
    df['account_age'] = (pd.Timestamp.now() - df['created_at']).dt.days
else:
    df['account_age'] = 100  # default

# Create fraud label (simple logic)
df['is_fraud'] = (
    (df['followers'] < 50) &
    (df['following'] > 500)
).astype(int)

# Select required columns
final_df = df[[
    'followers',
    'following',
    'posts',
    'likes',
    'comments',
    'account_age',
    'is_fraud'
]]

# Save clean dataset
final_df.to_csv("clean_social_media_data.csv", index=False)

print("✅ Clean dataset created!") 