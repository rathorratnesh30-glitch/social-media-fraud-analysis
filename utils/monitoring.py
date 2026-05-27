# ==========================================
# DATA QUALITY
# ==========================================
def data_quality_score(df):

    return round(
        (1 - df.isnull().mean().mean()) * 100,
        2
    )

# ==========================================
# DRIFT DETECTION
# ==========================================
def detect_drift(train_df, new_df):

    drift = abs(
        train_df['followers'].mean() -
        new_df['followers'].mean()
    )

    return (
        "⚠️ Drift"
        if drift > 10000
        else "✅ Stable"
    )