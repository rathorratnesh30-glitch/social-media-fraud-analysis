import streamlit as st

# ==========================================
# HOME PAGE
# ==========================================
def home_page(file):

    # ==========================================
    # TITLE
    # ==========================================
    st.title("🚀 Social Media Fraud Detection")

    st.subheader(
        "AI-powered fraud intelligence platform"
    )

    st.write(
        """
        Analyze suspicious social media behavior
        using machine learning, fraud analytics,
        and real-time monitoring systems.
        """
    )

    st.divider()

    # ==========================================
    # STATUS SECTION
    # ==========================================
    st.subheader("🛡️ System Status")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "🤖 AI Engine",
        "Active"
    )

    col2.metric(
        "📊 Analytics",
        "Ready"
    )

    col3.metric(
        "🚨 Monitoring",
        "Live"
    )

    col4.metric(
        "⚡ Detection",
        "Online"
    )

    st.divider()

    # ==========================================
    # DATASET STATUS
    # ==========================================
    st.subheader("📂 Dataset Connection")

    if file:

        st.success(
            "✅ Dataset connected successfully"
        )

    else:

        st.warning(
            "⚠️ Upload CSV dataset from sidebar"
        )

    st.divider()

    # ==========================================
    # FEATURES
    # ==========================================
    st.subheader("🧠 Platform Features")

    col1, col2 = st.columns(2)

    with col1:

        st.info(
            """
            🔍 Fraud Detection Engine
            
            Analyze suspicious accounts
            using machine learning.
            """
        )

        st.info(
            """
            📈 Analytics Dashboard
            
            Visualize fraud patterns
            and engagement behavior.
            """
        )

    with col2:

        st.info(
            """
            🚨 Live Monitoring
            
            Track suspicious activity
            in real time.
            """
        )

        st.info(
            """
            📂 CSV Prediction
            
            Upload datasets for
            fraud intelligence analysis.
            """
        )

    st.divider()

    # ==========================================
    # PLATFORM STATS
    # ==========================================
    st.subheader("📊 Platform Intelligence")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "📡 Detection Accuracy",
        "94%"
    )

    col2.metric(
        "⚠️ Threat Monitoring",
        "Real-Time"
    )

    col3.metric(
        "👥 Dataset Support",
        "5000+"
    )

    st.divider()

    # ==========================================
    # QUICK START
    # ==========================================
    st.subheader("⚙️ Quick Start")

    st.write("1️⃣ Upload CSV dataset")

    st.write("2️⃣ Open Analytics section")

    st.write("3️⃣ Detect suspicious accounts")

    st.write("4️⃣ Monitor live fraud activity")

    st.divider()

    # ==========================================
    # FOOTER
    # ==========================================
    st.caption(
        "🚀 MCA Final Year Project | "
        "AI Fraud Intelligence Platform"
    )