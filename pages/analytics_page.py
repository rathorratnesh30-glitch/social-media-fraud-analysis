import streamlit as st
import plotly.express as px
import pandas as pd

# ==========================================
# ANALYTICS PAGE
# ==========================================
def analytics_page(df):

    st.title("📈 Fraud Intelligence Dashboard")

    st.caption(
        "Advanced behavioral analytics for fraud detection"
    )

    st.markdown("---")

    # ==========================================
    # FILTERS
    # ==========================================
    st.sidebar.subheader("🔎 Analytics Filters")

    fraud_filter = st.sidebar.selectbox(
        "Account Type",
        ["All", "Fraud Only", "Genuine Only"]
    )

    min_followers = st.sidebar.slider(
        "Minimum Followers",
        0,
        int(df['followers'].max()),
        0
    )

    # ==========================================
    # FILTER LOGIC
    # ==========================================
    filtered_df = df[
        df['followers'] >= min_followers
    ]

    if fraud_filter == "Fraud Only":

        filtered_df = filtered_df[
            filtered_df['is_fraud'] == 1
        ]

    elif fraud_filter == "Genuine Only":

        filtered_df = filtered_df[
            filtered_df['is_fraud'] == 0
        ]

    st.markdown("---")

    # ==========================================
    # KPI SECTION
    # ==========================================
    total_users = len(filtered_df)

    fraud_users = int(
        filtered_df['is_fraud'].sum()
    )

    fraud_percent = (
        fraud_users / total_users
    ) * 100 if total_users > 0 else 0

    avg_engagement = (
        filtered_df['engagement_rate'].mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Users",
        total_users
    )

    col2.metric(
        "🚨 Fraud Cases",
        fraud_users
    )

    col3.metric(
        "⚠️ Fraud %",
        f"{fraud_percent:.2f}%"
    )

    col4.metric(
        "⭐ Avg Engagement",
        f"{avg_engagement:.2f}"
    )

    st.markdown("---")

    # ==========================================
    # CHARTS
    # ==========================================
    col1, col2 = st.columns(2)

    # ==========================================
    # FOLLOWERS DISTRIBUTION
    # ==========================================
    with col1:

        st.subheader("📊 Followers Distribution")

        fig1 = px.histogram(
            filtered_df,
            x="followers",
            nbins=40
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ==========================================
    # FRAUD DISTRIBUTION
    # ==========================================
    with col2:

        st.subheader("🧩 Fraud Distribution")

        fig2 = px.pie(
            filtered_df,
            names="is_fraud",
            hole=0.4
        )

        st.plotly_chart(
            fig2,
            use_container_width=True
        )

    st.markdown("---")

    # ==========================================
    # ENGAGEMENT ANALYSIS
    # ==========================================
    st.subheader("📡 Engagement Intelligence")

    fig3 = px.scatter(
        filtered_df,
        x="followers",
        y="engagement_rate",
        color="is_fraud",
        size="posts",
        hover_data=["following"],
        title="Engagement vs Followers"
    )

    st.plotly_chart(
        fig3,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # FOLLOWER VS FOLLOWING
    # ==========================================
    st.subheader("📉 Follower vs Following Analysis")

    fig4 = px.scatter(
        filtered_df,
        x="following",
        y="followers",
        color="is_fraud",
        size="activity_score",
        hover_data=["posts"],
        title="Behavior Pattern Analysis"
    )

    st.plotly_chart(
        fig4,
        use_container_width=True
    )

    st.markdown("---")

    # ==========================================
    # TOP RISK ACCOUNTS
    # ==========================================
    st.subheader("🚨 High Risk Accounts")

    risky = filtered_df.sort_values(
        by="engagement_rate",
        ascending=False
    ).head(10)

    st.dataframe(risky)

    st.markdown("---")

    # ==========================================
    # AI INSIGHTS
    # ==========================================
    st.subheader("🧠 AI Insights")

    high_risk = filtered_df[
        filtered_df['engagement_rate'] > 2
    ]

    st.write(
        f"🚨 High engagement suspicious accounts: "
        f"{len(high_risk)}"
    )

    st.write(
        f"📊 Average followers: "
        f"{filtered_df['followers'].mean():.0f}"
    )

    st.write(
        f"⚡ Highest activity score: "
        f"{filtered_df['activity_score'].max():.2f}"
    )

    st.write(
        f"📉 Average fraud ratio: "
        f"{fraud_percent:.2f}%"
    )