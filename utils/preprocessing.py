import pandas as pd

# ==========================================
# VALIDATION
# ==========================================
def validate_data(df):

    required = ['followers', 'following', 'posts']

    missing = [
        col for col in required
        if col not in df.columns
    ]

    if missing:
        raise ValueError(f"Missing columns: {missing}")

    return df

# ==========================================
# CLEANING
# ==========================================
def clean_data(df):

    df = df.copy()

    df.fillna(0, inplace=True)

    return df[
        (df['followers'] >= 0) &
        (df['following'] >= 0) &
        (df['posts'] >= 0)
    ]

# ==========================================
# OUTLIERS
# ==========================================
def handle_outliers(df):

    for col in ['followers', 'following', 'posts']:

        df[col] = df[col].clip(
            df[col].quantile(0.01),
            df[col].quantile(0.99)
        )

    return df

# ==========================================
# FEATURES
# ==========================================
def create_features(df):

    df['engagement_rate'] = (
        df['likes'] + df['comments']
    ) / (df['followers'] + 1)

    df['ff_ratio'] = (
        df['followers']
    ) / (df['following'] + 1)

    df['posts_per_day'] = (
        df['posts']
    ) / (df['account_age'] + 1)

    df['activity_score'] = (
        df['posts'] +
        df['likes'] +
        df['comments']
    ) / (df['account_age'] + 1)

    return df.fillna(0)

# ==========================================
# MAIN PIPELINE
# ==========================================
def data_pipeline(df):

    df = validate_data(df)
    df = clean_data(df)
    df = handle_outliers(df)
    df = create_features(df)

    return df