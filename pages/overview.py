import streamlit as st
import plotly.express as px

from utils.monitoring import data_quality_score

# ==========================================
# OVERVIEW PAGE
# ==========================================
def overview_page(df):

    st.title("📊 Fraud Detection Overview")

    st.caption(
        "Real-time insights into social media fraud behavior"
    )

    st.markdown("---")

    # ==========================================
    # KPI SECTION
    # ==========================================
    total_users = len(df)

    fraud_users = int(df['is_fraud'].sum())

    fraud_percent = (
        fraud_users / total_users
    ) * 100

    avg_engagement = (
        df['engagement_rate'].mean()
    )

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Total Users",
        total_users
    )

    col2.metric(
        "🚨 Fraud Accounts",
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
    # DATA QUALITY
    # ==========================================
    st.subheader("🛡️ System Health")

    quality = data_quality_score(df)

    st.progress(quality / 100)

    st.success(
        f"Dataset Quality Score: {quality}%"
    )

    st.markdown("---")

    # ==========================================
    # VISUAL ANALYTICS
    # ==========================================
    st.subheader("📈 Platform Insights")

    col1, col2 = st.columns(2)

    # ==========================================
    # PIE CHART
    # ==========================================
    with col1:

        fig1 = px.pie(
            df,
            names="is_fraud",
            title="Fraud Distribution",
            hole=0.4
        )

        st.plotly_chart(
            fig1,
            use_container_width=True
        )

    # ==========================================
    # FOLLOWERS DISTRIBUTION
    # ==========================================
    with col2:

        fig2 = px.histogram(
            df,
            x="followers",
            nbins=30,
            title="Followers Distribution"
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
        df,
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
    # HIGH RISK ACCOUNTS
    # ==========================================
    st.subheader("🚨 High Risk Accounts")

    risky = df.sort_values(
        by="engagement_rate",
        ascending=False
    ).head(10)

    st.dataframe(risky)

    st.markdown("---")

    # ==========================================
    # INSIGHTS
    # ==========================================
    st.subheader("🧠 AI Insights")

    st.write(
        f"🚨 Fraud accounts detected: "
        f"{fraud_users}"
    )

    st.write(
        f"📊 Average engagement rate: "
        f"{avg_engagement:.2f}"
    )

    st.write(
        f"⚡ Highest follower count: "
        f"{df['followers'].max()}"
    )

    st.write(
        f"📉 Average fraud ratio: "
        f"{fraud_percent:.2f}%"
    )