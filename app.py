# app.py
import streamlit as st
from src.predict import predict_alert
import pandas as pd
import matplotlib.pyplot as plt
import os

# ---------------- UI ENHANCEMENT STYLES ----------------
st.markdown("""
<style>

/* Card container */
.ui-card {
    background: rgba(255,255,255,0.9);
    padding: 16px;
    border-radius: 14px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    margin-bottom: 14px;
}

/* Card titles */
.ui-card h4 {
    font-size: 17px;   /* ⬆ increased */
    font-weight: 600;
    margin-bottom: 8px;
}

/* Card paragraph text */
.ui-card p,
.ui-card li {
    font-size: 15px;   /* ⬆ increased */
    line-height: 1.6;
}

/* Section titles */
.section-title {
    font-size: 22px;   /* ⬆ increased */
    font-weight: 600;
    margin-bottom: 10px;
}

/* Badge text */
.badge {
    font-size: 13px;   /* ⬆ increased */
    padding: 5px 12px;
    border-radius: 14px;
    font-weight: 600;
    color: white;
}

.green { background: #4caf50; }
.yellow { background: #fbc02d; color: black; }
.orange { background: #fb8c00; }
.red { background: #e53935; }

/* Dialog / popup text (IMPORTANT) */
div[role="dialog"] p,
div[role="dialog"] span,
div[role="dialog"] li {
    font-size: 15px;   /* ⬆ popup text */
}

div[role="dialog"] h1,
div[role="dialog"] h2,
div[role="dialog"] h3 {
    font-size: 20px;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

/* Prediction result card */
.result-card {
    background: rgba(255,255,255,0.92);
    padding: 18px;
    border-radius: 16px;
    box-shadow: 0 8px 20px rgba(0,0,0,0.18);
    margin-top: 15px;
}

/* Alert badge large */
.alert-badge {
    display: inline-block;
    padding: 8px 18px;
    border-radius: 20px;
    font-size: 16px;
    font-weight: 700;
    color: white;
    margin-bottom: 10px;
}

.alert-green { background: #4caf50; }
.alert-yellow { background: #fbc02d; color: black; }
.alert-orange { background: #fb8c00; }
.alert-red { background: #e53935; }

/* Risk text */
.result-text {
    font-size: 15px;
    margin-bottom: 6px;
}

/* Progress bar spacing */
.stProgress {
    margin-top: 10px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- BACKGROUND ----------------
def set_light_earth_background():
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(
                120deg,
                #f0f4ff,
                #f7fbff,
                #eef7f3
            );
            background-size: 400% 400%;
            animation: gradientBG 12s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .block-container {
            background-color: transparent;
        }

        h1, h2, h3 {
            color: #1f2937;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Earthquake Risk Assessment System",
    layout="wide"
)

# ✅ Call AFTER definition
set_light_earth_background()

# ---------------- SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

if "page" not in st.session_state:
    st.session_state.page = "Login"

# ---------------- USER CSV HANDLING ----------------
def load_users():
    if not os.path.exists("users.csv"):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv("users.csv", index=False)
    return pd.read_csv("users.csv")

def save_user(username, password):
    df = load_users()
    if username in df["username"].values:
        return False
    df.loc[len(df)] = [username, password]
    df.to_csv("users.csv", index=False)
    return True

# ---------------- AUTH PAGES ----------------
def signup_page():
    st.title("📝 Sign Up")

    new_username = st.text_input("Create Username")
    new_password = st.text_input("Create Password", type="password")

    if st.button("Sign Up"):
        if new_username and new_password:
            if save_user(new_username, new_password):
                st.success("✅ Account created! Please login.")
                st.session_state.page = "Login"
            else:
                st.error("❌ Username already exists")
        else:
            st.warning("⚠️ Fill all fields")

    if st.button("Already have an account? Login"):
        st.session_state.page = "Login"

def login_page():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        match = users[
            (users["username"] == username) &
            (users["password"] == password)
        ]
        if not match.empty:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.page = "Home"
        else:
            st.error("❌ Invalid credentials")

    if st.button("New user? Sign up"):
        st.session_state.page = "Signup"

def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.session_state.page = "Login"

def set_light_earth_background():
    st.markdown(
        """
        <style>
        /* Main app background */
        .stApp {
            background: linear-gradient(
                120deg,
                #f0f4ff,
                #f7fbff,
                #eef7f3
            );
            background-size: 400% 400%;
            animation: gradientBG 12s ease infinite;
        }

        @keyframes gradientBG {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        /* Make containers transparent */
        .block-container {
            background-color: transparent;
        }

        /* Improve text readability */
        h1, h2, h3 {
            color: #1f2937;
        }
        </style>
        """,
        unsafe_allow_html=True
    )


# ---------------- AUTH FLOW ----------------
if not st.session_state.logged_in:
    if st.session_state.page == "Login":
        login_page()
    elif st.session_state.page == "Signup":
        signup_page()

else:
    # ---------------- TOP NAV BAR ----------------
    st.markdown(
        f"""
        <div style="
            display:flex;
            justify-content:space-between;
            align-items:center;
            padding:12px 20px;
        ">
            <h2>🌍 Earthquake Risk Assessment System</h2>
            <p>Welcome <b>{st.session_state.username}</b> 👋</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    #st.markdown("###")

    tab1, tab2, tab3, tab4, tab5 = st.tabs(
    ["🏠 Home", "ℹ️ About", "🔮 Predict", "🛡️ Precautions", "🚪 Logout"]
)


    st.divider()

    # ---------------- WIDTH CONTROL CONTAINER ----------------
    st.markdown(
        """
        <style>
        .main-container {
            max-width: 200px;
            margin: auto;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="main-container">', unsafe_allow_html=True)

    page = st.session_state.page

    # ---------------- HOME PAGE ----------------
    with tab1:
        st.title("🌍 Earthquake Risk Awareness Dashboard")
        st.caption("Understand historical earthquake patterns and risk distribution")

        st.markdown("---")

        # ---------------- HISTORICAL ALERT DISTRIBUTION (LEFT-ALIGNED SMALL CARD) ----------------
        st.subheader("📊 Alert Distribution")

        # Load dataset
        data = pd.read_csv("usgs_earthquake_realistic_1000.csv")
        alert_counts = data["alert"].value_counts()

        # Use columns to left-align the card
        left_col, spacer = st.columns([1, 3])  # left column small, spacer takes rest

        with left_col:
            fig, ax = plt.subplots(figsize=(2.5, 1.8))  # very small, card-size
            colors = {
                "green": "#4caf50",
                "yellow": "#ffeb3b",
                "orange": "#ff9800",
                "red": "#f44336"
            }
            bar_colors = [colors.get(alert.lower(), "#607d8b") for alert in alert_counts.index]
            ax.bar(alert_counts.index, alert_counts.values, color=bar_colors)
            ax.set_title("Alert Levels", fontsize=9)
            ax.set_ylabel("Count", fontsize=7)
            ax.set_xlabel("", fontsize=7)
            ax.tick_params(axis='x', labelsize=7)
            ax.tick_params(axis='y', labelsize=7)
            ax.grid(False)  # remove grid for clean card look
            st.pyplot(fig, use_container_width=False)  # keep small width

        st.markdown("---")

        # ---------------- QUICK STATISTICS ----------------
        st.subheader("📈 Quick Earthquake Stats")
        total_quakes = len(data)
        high_risk_quakes = len(data[data["alert"].isin(["orange", "red"])])
        most_common_alert = alert_counts.idxmax()

        c1, c2, c3 = st.columns(3)

        with c1:
            st.markdown(f"""
            <div class="ui-card">
                <h4>🌍 Total Earthquakes</h4>
                <p><b>{total_quakes}</b> recorded events</p>
            </div>
            """, unsafe_allow_html=True)

        with c2:
            st.markdown(f"""
            <div class="ui-card">
                <h4>⚠️ High Risk Events</h4>
                <p><b>{high_risk_quakes}</b> orange / red alerts</p>
            </div>
            """, unsafe_allow_html=True)

        with c3:
            st.markdown(f"""
            <div class="ui-card">
                <h4>🏆 Frequent Alert Level</h4>
                <span class="badge {most_common_alert.lower()}">
                    {most_common_alert.upper()}
                </span>
            </div>
            """, unsafe_allow_html=True)


        # ---------------- SAFETY TIPS ----------------
        with st.expander("🛡️ Quick Safety Tips"):
            st.markdown("""
            - Secure heavy furniture at home  
            - Prepare emergency kits with food, water, and medicines  
            - Drop, Cover, Hold On during shaking  
            - Stay away from glass and windows  
            - Follow official instructions after the earthquake
            """)

        st.caption("⚠️ For educational and awareness purposes only — not an official alert system")



    # ---------------- ABOUT PAGE ----------------

    with tab2:
        st.title("ℹ️ About This App")

        st.markdown('<div class="section-title">🌍 About the System</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="ui-card">
            <p>
            The <b>Earthquake Risk Assessment System</b> helps users understand
            earthquake severity using parameters such as magnitude, depth,
            and seismic intensity indicators.
            </p>
        </div>
        """, unsafe_allow_html=True)


        st.markdown('<div class="section-title">🚦 Alert Levels</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="ui-card">
            <p><span class="badge green">GREEN</span> – Low risk, safe conditions</p><br>
            <p><span class="badge yellow">YELLOW</span> – Moderate risk, stay alert</p><br>
            <p><span class="badge orange">ORANGE</span> – High risk, be prepared</p><br>
            <p><span class="badge red">RED</span> – Severe risk, immediate action</p>
        </div>
        """, unsafe_allow_html=True)


        st.markdown('<div class="section-title">⚠️ Disclaimer</div>', unsafe_allow_html=True)

        st.markdown("""
        <div class="ui-card">
            <p>
            This application is designed for <b>educational and awareness purposes</b>.
            It should not be considered as an official earthquake warning system.
            </p>
        </div>
        """, unsafe_allow_html=True)




    # ---------------- PREDICT PAGE ----------------
    with tab3:
        st.title("🔮 Earthquake Alert Prediction")

        magnitude = st.number_input("Magnitude", 0.0, 10.0, 6.5)
        depth = st.number_input("Depth (km)", 0.0, 700.0, 50.0)
        cdi = st.number_input("CDI", 0.0, 10.0, 5.0)
        mmi = st.number_input("MMI", 0.0, 10.0, 5.0)
        sig = st.number_input("SIG", 0.0, 1000.0, 100.0)

        # ✅ Initialize variables (VERY IMPORTANT)
        alert = None
        risk = None
        confidence = None
        aftershock = None

        if st.button("🚨 Predict Alert"):
            alert, risk, confidence, aftershock = predict_alert(
                magnitude, depth, cdi, mmi, sig
            )

        # ✅ Output section (runs ONLY after prediction)
        if alert is not None:
            st.markdown("### 🔍 Risk Assessment Result")

            col1, col2 = st.columns(2)

            with col1:
                st.metric("🚦 Alert Level", alert)
                st.metric("⚠️ Risk Score", f"{risk}/100")

            with col2:
                st.metric("📊 Confidence", f"{confidence}%")
                st.metric("🌊 Aftershock Risk", f"{aftershock}%")

            st.progress(int(risk))

            if alert.lower() == "green":
                st.success("🟢 GREEN ALERT – Minimal risk")
            elif alert.lower() == "yellow":
                st.warning("🟡 YELLOW ALERT – Stay alert")
            elif alert.lower() == "orange":
                st.warning("🟠 ORANGE ALERT – High risk")
            elif alert.lower() == "red":
                st.error("🔴 RED ALERT – Severe risk")
        else:
            st.info("👆 Enter values and click **Predict Alert** to see the risk assessment.")


    # ---------------- PRECAUTIONS PAGE ----------------
    # ---------------- PRECAUTIONS PAGE ----------------
    with tab4:
        st.title("🛡️ Earthquake Safety Precautions")
        st.markdown('<div class="section-title">🛡️ Earthquake Safety Guidelines</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        # -------- BEFORE --------
        with col1:
            st.markdown("""
            <div class="ui-card">
                <h4>✅ Before</h4>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🔧 Secure heavy furniture"):
                st.write("""
                Anchor cupboards, shelves, and televisions to walls.
                This prevents falling objects that can cause serious injuries during shaking.
                """)

            with st.expander("🎒 Prepare emergency kits"):
                st.write("""
                Keep a kit with water, food, flashlight, batteries, medicines,
                first aid supplies, and important documents.
                """)

            with st.expander("📍 Identify safe spots"):
                st.write("""
                Identify strong areas like under sturdy tables or against interior walls.
                Avoid windows and heavy objects.
                """)

        # -------- DURING --------
        with col2:
            st.markdown("""
            <div class="ui-card">
                <h4>🚨 During</h4>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🛑 Drop, Cover, Hold On"):
                st.write("""
                Drop to the ground, take cover under sturdy furniture,
                and hold on until shaking stops.
                """)

            with st.expander("🪟 Stay away from glass"):
                st.write("""
                Windows, mirrors, and glass doors can shatter and cause severe injuries.
                Move away immediately.
                """)

            with st.expander("🚫 Do not use elevators"):
                st.write("""
                Elevators may stop or malfunction during earthquakes.
                Always use stairs after shaking stops.
                """)

        # -------- AFTER --------
        with col3:
            st.markdown("""
            <div class="ui-card">
                <h4>🏥 After</h4>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("🩹 Check for injuries"):
                st.write("""
                Provide first aid if needed and seek medical help
                for serious injuries immediately.
                """)

            with st.expander("🔥 Turn off gas supply"):
                st.write("""
                If you smell gas or see leaks, turn off the main gas valve
                to prevent fires or explosions.
                """)

            with st.expander("📢 Follow official updates"):
                st.write("""
                Listen to government alerts, radio, or emergency services
                for instructions and aftershock warnings.
                """)


                # ---------------- CLOSE CONTAINER ----------------
                st.markdown('</div>', unsafe_allow_html=True)
    # ---------------- LOGOUT PAGE ----------------
    with tab5:
        st.title("🚪 Logout")

        st.warning("Are you sure you want to logout?")

        if st.button("Yes, Logout"):
            logout()
            st.success("✅ Logged out successfully")
            st.rerun()

