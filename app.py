import streamlit as st
import pandas as pd
import numpy as np

# ==========================================
# IMPORTS
# ==========================================
from utils.preprocessing import data_pipeline
from models.train_model import train_models

from pages.home import home_page
from pages.overview import overview_page
from pages.analytics_page import analytics_page
from pages.detection import detection_page
from pages.live_monitor import live_monitor_page

# ==========================================
# PAGE CONFIG
# ==========================================
st.set_page_config(
    page_title="Social Media Fraud Detection",
    layout="wide"
)

# ==========================================
# SIDEBAR
# ==========================================
st.sidebar.title("🚀 Fraud Dashboard")

page = st.sidebar.radio(
    "Navigate",
    [
        "🏠 Home",
        "📊 Overview",
        "📈 Analytics",
        "🔍 Detection",
        "🚨 Live Monitor"
    ]
)

st.sidebar.markdown("---")

# ==========================================
# CSV UPLOAD
# ==========================================
file = st.sidebar.file_uploader(
    "📂 Upload CSV Dataset",
    type=["csv"]
)

# ==========================================
# HOME PAGE
# ==========================================
if page == "🏠 Home":

    home_page(file)

# ==========================================
# OTHER PAGES REQUIRE CSV
# ==========================================
else:

    # ==========================================
    # STOP IF NO FILE
    # ==========================================
    if not file:

        st.warning(
            "⚠️ Please upload CSV file from sidebar"
        )

        st.stop()

    # ==========================================
    # READ CSV
    # ==========================================
    try:

        df = pd.read_csv(file)

    except Exception as e:

        st.error(f"CSV Error: {e}")

        st.stop()

    # ==========================================
    # LOWERCASE COLUMNS
    # ==========================================
    df.columns = df.columns.str.lower()

    # ==========================================
    # COLUMN FIXES
    # ==========================================

    # Followers
    if 'followers' in df.columns:

        df['followers'] = df['followers']

    elif 'followers_count' in df.columns:

        df['followers'] = df['followers_count']

    else:

        df['followers'] = 0

    # Following
    if 'following' in df.columns:

        df['following'] = df['following']

    elif 'friends_count' in df.columns:

        df['following'] = df['friends_count']

    else:

        df['following'] = 0

    # Posts
    if 'posts' in df.columns:

        df['posts'] = df['posts']

    elif 'statuses_count' in df.columns:

        df['posts'] = df['statuses_count']

    else:

        df['posts'] = 0

    # Likes
    if 'likes' not in df.columns:

        df['likes'] = 0

    # Comments
    if 'comments' not in df.columns:

        df['comments'] = 0

    # Account Age
    if 'account_age' not in df.columns:

        df['account_age'] = 100

    # ==========================================
    # GENERATE LABELS IF MISSING
    # ==========================================
    if 'is_fraud' not in df.columns:

        df['is_fraud'] = np.random.randint(
            0,
            2,
            len(df)
        )

    # ==========================================
    # DATA PIPELINE
    # ==========================================
    try:

        df = data_pipeline(df)

    except Exception as e:

        st.error(f"Pipeline Error: {e}")

        st.stop()

    # ==========================================
    # FEATURES
    # ==========================================
    features = [
        'followers',
        'following',
        'posts',
        'engagement_rate',
        'ff_ratio',
        'posts_per_day',
        'activity_score'
    ]

    # ==========================================
    # MODEL DATA
    # ==========================================
    X = df[features]

    y = df['is_fraud']

    # ==========================================
    # TRAIN MODEL
    # ==========================================
    try:

        rf_model, xgb_model, scaler, X_test_scaled, y_test = train_models(X, y)

        best_model = xgb_model

    except Exception as e:

        st.error(f"Model Error: {e}")

        st.stop()

    # ==========================================
    # PAGE ROUTING
    # ==========================================
    if page == "📊 Overview":

        overview_page(df)

    elif page == "📈 Analytics":

        analytics_page(df)

    elif page == "🔍 Detection":

        detection_page(
            scaler,
            best_model,
            features,
            data_pipeline
        )

    elif page == "🚨 Live Monitor":

        live_monitor_page(
            scaler,
            best_model,
            features,
            data_pipeline,
            df
        )