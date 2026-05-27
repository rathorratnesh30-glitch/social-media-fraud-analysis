import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# ==========================================
# DETECTION PAGE
# ==========================================
def detection_page(
    scaler,
    best_model,
    features,
    data_pipeline
):

    st.title("🔍 AI Fraud Detection Engine")

    st.caption(
        "Analyze suspicious social media behavior using AI"
    )

    st.markdown("---")

    # ==========================================
    # DETECTION MODE
    # ==========================================
    mode = st.radio(
        "Detection Mode",
        ["Manual", "Random", "CSV"]
    )

    st.markdown("---")

    # ==========================================
    # MANUAL DETECTION
    # ==========================================
    if mode == "Manual":

        st.subheader("🧾 Manual Account Analysis")

        col1, col2, col3 = st.columns(3)

        with col1:

            followers = st.number_input(
                "Followers",
                0, 100000, 100
            )

            following = st.number_input(
                "Following",
                0, 100000, 150
            )

        with col2:

            posts = st.number_input(
                "Posts",
                0, 10000, 20
            )

            likes = st.number_input(
                "Likes",
                0, 100000, 50
            )

        with col3:

            comments = st.number_input(
                "Comments",
                0, 10000, 10
            )

            age = st.number_input(
                "Account Age",
                1, 5000, 100
            )

        # ==========================================
        # ANALYZE BUTTON
        # ==========================================
        if st.button("🚀 Analyze Account"):

            df_input = pd.DataFrame([{
                'followers': followers,
                'following': following,
                'posts': posts,
                'likes': likes,
                'comments': comments,
                'account_age': age
            }])

            df_input = data_pipeline(df_input)

            Xp = scaler.transform(
                df_input[features]
            )

            prob = best_model.predict_proba(Xp)[0][1]

            st.markdown("---")

            # ==========================================
            # KPI
            # ==========================================
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "🚨 Fraud Probability",
                f"{prob*100:.2f}%"
            )

            col2.metric(
                "⭐ Engagement Rate",
                f"{df_input['engagement_rate'].iloc[0]:.2f}"
            )

            col3.metric(
                "⚡ Activity Score",
                f"{df_input['activity_score'].iloc[0]:.2f}"
            )

            # ==========================================
            # ALERT
            # ==========================================
            if prob > 0.7:

                st.error(
                    "🚨 HIGH RISK ACCOUNT DETECTED"
                )

            elif prob > 0.4:

                st.warning(
                    "⚠️ Suspicious Account"
                )

            else:

                st.success(
                    "✅ Account Appears Safe"
                )

            st.markdown("---")

            # ==========================================
            # FEATURE ANALYSIS
            # ==========================================
            st.subheader("📈 Behavioral Analysis")

            viz_df = pd.DataFrame({
                "Feature": [
                    "Followers",
                    "Following",
                    "Posts",
                    "Likes",
                    "Comments"
                ],
                "Value": [
                    followers,
                    following,
                    posts,
                    likes,
                    comments
                ]
            })

            fig1 = px.bar(
                viz_df,
                x="Feature",
                y="Value",
                color="Feature"
            )

            st.plotly_chart(
                fig1,
                use_container_width=True
            )

            # ==========================================
            # INSIGHTS
            # ==========================================
            st.subheader("🧠 AI Insights")

            st.write(
                f"👥 Followers/Following Ratio: "
                f"{df_input['ff_ratio'].iloc[0]:.2f}"
            )

            st.write(
                f"📉 Posts Per Day: "
                f"{df_input['posts_per_day'].iloc[0]:.2f}"
            )

            st.write(
                f"⭐ Engagement Rate: "
                f"{df_input['engagement_rate'].iloc[0]:.2f}"
            )

    # ==========================================
    # RANDOM DETECTION
    # ==========================================
    elif mode == "Random":

        st.subheader("🎲 Random Fraud Simulation")

        n = st.slider(
            "Generate Random Users",
            5,
            100,
            20
        )

        if st.button("🚀 Generate & Analyze"):

            df_random = pd.DataFrame({

                'followers': np.random.randint(
                    10, 5000, n
                ),

                'following': np.random.randint(
                    50, 5000, n
                ),

                'posts': np.random.randint(
                    1, 500, n
                ),

                'likes': np.random.randint(
                    0, 1000, n
                ),

                'comments': np.random.randint(
                    0, 300, n
                ),

                'account_age': np.random.randint(
                    1, 365, n
                )
            })

            df_random = data_pipeline(df_random)

            Xr = scaler.transform(
                df_random[features]
            )

            df_random['fraud_prob'] = (
                best_model.predict_proba(Xr)[:,1]
            )

            # ==========================================
            # RISK LEVEL
            # ==========================================
            df_random['risk_level'] = (
                df_random['fraud_prob']
                .apply(
                    lambda x:
                    "High Risk"
                    if x > 0.7 else
                    "Medium Risk"
                    if x > 0.4 else
                    "Low Risk"
                )
            )

            st.markdown("---")

            # ==========================================
            # KPI
            # ==========================================
            col1, col2, col3 = st.columns(3)

            col1.metric(
                "👥 Users",
                len(df_random)
            )

            col2.metric(
                "🚨 High Risk",
                len(
                    df_random[
                        df_random['risk_level']
                        == "High Risk"
                    ]
                )
            )

            col3.metric(
                "⚠️ Avg Fraud %",
                f"{df_random['fraud_prob'].mean()*100:.2f}%"
            )

            st.markdown("---")

            # ==========================================
            # CHARTS
            # ==========================================
            col1, col2 = st.columns(2)

            with col1:

                fig1 = px.pie(
                    df_random,
                    names="risk_level",
                    hole=0.4,
                    title="Risk Distribution"
                )

                st.plotly_chart(
                    fig1,
                    use_container_width=True
                )

            with col2:

                fig2 = px.scatter(
                    df_random,
                    x="followers",
                    y="fraud_prob",
                    color="risk_level",
                    size="posts",
                    hover_data=["following"],
                    title="Fraud Risk Analysis"
                )

                st.plotly_chart(
                    fig2,
                    use_container_width=True
                )

            st.markdown("---")

            # ==========================================
            # TOP RISK
            # ==========================================
            st.subheader("🚨 Top Suspicious Accounts")

            risky = df_random.sort_values(
                by="fraud_prob",
                ascending=False
            ).head(10)

            st.dataframe(risky)

    # ==========================================
    # CSV DETECTION
    # ==========================================
    elif mode == "CSV":

        st.subheader("📂 CSV Fraud Analysis")

        file2 = st.file_uploader(
            "Upload Prediction CSV",
            type=["csv"]
        )

        if file2:

            try:

                df_pred = pd.read_csv(file2)

                df_pred.columns = (
                    df_pred.columns.str.lower()
                )

                df_pred['followers'] = df_pred.get(
                    'followers',
                    0
                )

                df_pred['following'] = df_pred.get(
                    'following',
                    0
                )

                df_pred['posts'] = df_pred.get(
                    'posts',
                    0
                )

                df_pred['likes'] = df_pred.get(
                    'likes',
                    0
                )

                df_pred['comments'] = df_pred.get(
                    'comments',
                    0
                )

                df_pred['account_age'] = df_pred.get(
                    'account_age',
                    100
                )

                df_pred = data_pipeline(df_pred)

                Xp = scaler.transform(
                    df_pred[features]
                )

                df_pred['fraud_prob'] = (
                    best_model.predict_proba(Xp)[:,1]
                )

                df_pred['label'] = (
                    df_pred['fraud_prob']
                    .apply(
                        lambda x:
                        "Fraud"
                        if x > 0.7
                        else "Normal"
                    )
                )

                st.markdown("---")

                # ==========================================
                # KPI
                # ==========================================
                col1, col2, col3 = st.columns(3)

                col1.metric(
                    "👥 Total Users",
                    len(df_pred)
                )

                col2.metric(
                    "🚨 Fraud Accounts",
                    len(
                        df_pred[
                            df_pred['label']
                            == "Fraud"
                        ]
                    )
                )

                col3.metric(
                    "⚠️ Avg Fraud %",
                    f"{df_pred['fraud_prob'].mean()*100:.2f}%"
                )

                st.markdown("---")

                # ==========================================
                # CHARTS
                # ==========================================
                col1, col2 = st.columns(2)

                with col1:

                    fig1 = px.pie(
                        df_pred,
                        names="label",
                        hole=0.4,
                        title="Fraud Distribution"
                    )

                    st.plotly_chart(
                        fig1,
                        use_container_width=True
                    )

                with col2:

                    fig2 = px.histogram(
                        df_pred,
                        x="fraud_prob",
                        nbins=20,
                        title="Fraud Probability"
                    )

                    st.plotly_chart(
                        fig2,
                        use_container_width=True
                    )

                st.markdown("---")

                # ==========================================
                # TABLE
                # ==========================================
                st.subheader(
                    "🚨 Suspicious Accounts"
                )

                fraud_df = df_pred[
                    df_pred['label'] == "Fraud"
                ]

                st.dataframe(
                    fraud_df.sort_values(
                        by="fraud_prob",
                        ascending=False
                    )
                )

            except Exception as e:

                st.error(e)