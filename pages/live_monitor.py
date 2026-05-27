import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

# ==========================================
# LIVE MONITOR PAGE
# ==========================================
def live_monitor_page(
    scaler,
    best_model,
    features,
    data_pipeline,
    df
):

    st.title("🚨 Real-Time Fraud Monitoring Center")

    st.caption(
        "Live AI monitoring of suspicious social media behavior"
    )

    st.markdown("---")

    # ==========================================
    # AUTO REFRESH
    # ==========================================
    auto_refresh = st.sidebar.checkbox(
        "🔄 Auto Refresh",
        value=False
    )

    refresh_rate = st.sidebar.slider(
        "Refresh Rate (seconds)",
        1,
        10,
        3
    )

    if st.button("⚡ Generate Live Activity"):
        st.rerun()

    # ==========================================
    # GENERATE LIVE DATA
    # ==========================================
    live_df = pd.DataFrame({

        'followers': np.random.randint(
            10, 10000, 100
        ),

        'following': np.random.randint(
            50, 15000, 100
        ),

        'posts': np.random.randint(
            1, 1000, 100
        ),

        'likes': np.random.randint(
            0, 5000, 100
        ),

        'comments': np.random.randint(
            0, 1000, 100
        ),

        'account_age': np.random.randint(
            1, 3650, 100
        )
    })

    # ==========================================
    # PIPELINE
    # ==========================================
    live_df = data_pipeline(live_df)

    # ==========================================
    # MODEL PREDICTION
    # ==========================================
    X_live = scaler.transform(
        live_df[features]
    )

    live_df['fraud_prob'] = (
        best_model.predict_proba(X_live)[:,1]
    )

    # ==========================================
    # RISK CLASSIFICATION
    # ==========================================
    live_df['risk_level'] = (
        live_df['fraud_prob']
        .apply(
            lambda x:
            "High Risk"
            if x > 0.7 else
            "Medium Risk"
            if x > 0.4 else
            "Low Risk"
        )
    )

    # ==========================================
    # ALERTS
    # ==========================================
    fraud_alerts = live_df[
        live_df['risk_level'] == "High Risk"
    ]

    # ==========================================
    # KPI SECTION
    # ==========================================
    st.subheader("📊 Live Monitoring Metrics")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Active Accounts",
        len(live_df)
    )

    col2.metric(
        "🚨 Fraud Alerts",
        len(fraud_alerts)
    )

    col3.metric(
        "⚠️ Avg Risk",
        f"{live_df['fraud_prob'].mean()*100:.2f}%"
    )

    col4.metric(
        "🔥 Highest Risk",
        f"{live_df['fraud_prob'].max()*100:.2f}%"
    )

    st.markdown("---")

    # ==========================================
    # LIVE CHARTS
    # ==========================================
    col1, col2 = st.columns(2)

    # ==========================================
    # LIVE FRAUD ANALYSIS
    # ==========================================
    with col1:

        st.subheader("📡 Fraud Activity Stream")

        fig1 = px.scatter(
            live_df,
            x="followers",
            y="fraud_prob",
            color="risk_level",
            size="posts",
            hover_data=["following"],
            title="Live Fraud Risk Analysis"
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ==========================================
    # RISK DISTRIBUTION
    # ==========================================
    with col2:

        st.subheader("🧩 Risk Distribution")

        fig2 = px.pie(
            live_df,
            names="risk_level",
            hole=0.4
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================================
    # FRAUD PROBABILITY TREND
    # ==========================================
    st.subheader("📈 Fraud Probability Trend")

    trend_df = live_df.sort_values(
        by="fraud_prob",
        ascending=False
    ).head(20)

    fig3 = px.line(
        trend_df,
        y="fraud_prob",
        markers=True,
        title="Highest Fraud Probability Accounts"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TOP FRAUD ACCOUNTS
    # ==========================================
    st.subheader("🚨 High Risk Accounts")

    top_fraud = fraud_alerts.sort_values(
        by="fraud_prob",
        ascending=False
    ).head(15)

    st.dataframe(top_fraud)

    st.markdown("---")

    # ==========================================
    # AI INSIGHTS
    # ==========================================
    st.subheader("🧠 AI Monitoring Insights")

    st.write(
        f"🚨 Suspicious accounts detected: "
        f"{len(fraud_alerts)}"
    )

    st.write(
        f"📊 Average fraud probability: "
        f"{live_df['fraud_prob'].mean():.2f}"
    )

    st.write(
        f"⚡ Highest detected fraud risk: "
        f"{live_df['fraud_prob'].max():.2f}"
    )

    st.write(
        f"📉 Average engagement score: "
        f"{live_df['engagement_rate'].mean():.2f}"
    )

    st.write(
        f"👥 Average followers count: "
        f"{live_df['followers'].mean():.0f}"
    )

    st.markdown("---")

    # ==========================================
    # LIVE ALERT FEED
    # ==========================================
    st.subheader("🚨 Live Fraud Alert Feed")

    for index, row in top_fraud.head(5).iterrows():

        st.error(
            f"⚠️ High Risk Account Detected | "
            f"Followers: {row['followers']} | "
            f"Fraud Probability: "
            f"{row['fraud_prob']:.2f}"
        )

    # ==========================================
    # AUTO REFRESH
    # ==========================================
    if auto_refresh:

        time.sleep(refresh_rate)

        st.rerun()