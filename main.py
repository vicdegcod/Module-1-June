import streamlit as st

from auth import login, logout, change_password

from client import (
    add_client,
    view_clients,
    update_client,
    delete_client,
    view_progress
)

from therapist import (
    add_therapist,
    view_therapists,
    update_therapist,
    delete_therapist
)

from appointment import (
    book_appointment,
    view_appointments,
    cancel_appointment,
    complete_appointment,
    delete_appointment
)

from notes import (
    add_note,
    view_notes,
    search_notes,
    update_note,
    delete_note,
    export_notes_csv,
    count_notes
)

from database import close_database


# ======================================================
# PAGE CONFIGURATION
# ======================================================

st.set_page_config(
    page_title="Rehabilitation Management System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)


# ======================================================
# PROFESSIONAL DARK THEME
# ======================================================

st.markdown("""
<style>

#MainMenu{
visibility:hidden;
}

footer{
visibility:hidden;
}

header{
visibility:hidden;
}

.stApp{
    background:#0f172a;
    color:white;
}

section[data-testid="stSidebar"]{
    background:#111827;
    border-right:2px solid #1e293b;
}

h1,h2,h3,h4{
    color:#38bdf8;
}

p,label{
    color:white;
}

hr{
    border:1px solid #1e293b;
}

/* Buttons */

.stButton>button{

    width:100%;
    background:#2563eb;
    color:white;
    border:none;
    border-radius:10px;
    font-weight:bold;
    padding:12px;
}

.stButton>button:hover{

    background:#1d4ed8;
}

/* Text boxes */

.stTextInput input{

    background:#1e293b;
    color:white;
    border-radius:8px;
}

/* Select Boxes */

.stSelectbox div[data-baseweb="select"]{

    background:#1e293b;
}

/* Radio */

.stRadio label{

    color:white;
}

/* Metrics */

div[data-testid="metric-container"]{

    background:#1e293b;

    border-radius:12px;

    padding:18px;

    border:1px solid #334155;

}

/* Tables */

thead tr th{

    background:#1e293b;

    color:white;

}

tbody{

    color:white;

}

/* Success */

.stSuccess{

    border-radius:10px;

}

/* Info */

.stInfo{

    border-radius:10px;

}

/* Sidebar */

.sidebar-title{

    font-size:26px;

    font-weight:bold;

    color:#38bdf8;

    text-align:center;

    margin-bottom:15px;

}

.profile-card{

    background:#1e293b;

    padding:15px;

    border-radius:12px;

    text-align:center;

    margin-bottom:20px;

    border:1px solid #334155;

}

.dashboard-card{

    background:#1e293b;

    padding:25px;

    border-radius:15px;

    border:1px solid #334155;

}

</style>
""", unsafe_allow_html=True)


# ======================================================
# SESSION STATE
# ======================================================

if "user" not in st.session_state:

    st.session_state.user = None


# ======================================================
# LOGIN PAGE
# ======================================================

if st.session_state.user is None:

    col1, col2, col3 = st.columns([1,2,1])

    with col2:

        st.markdown("<br><br>", unsafe_allow_html=True)

        st.markdown(
            "<h1 style='text-align:center;color:#38bdf8;'>🏥 Rehabilitation Management System</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            "<h4 style='text-align:center;color:white;'>Secure Login</h4>",
            unsafe_allow_html=True
        )

        st.markdown("---")

        username = st.text_input(
            "Username",
            placeholder="Enter username"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        if st.button("🔐 Login"):

            user = login(username, password)

            if user:

                st.session_state.user = user

                st.success("Login Successful")

                st.rerun()

            else:

                st.error("Invalid Username or Password")

    st.stop()


# ======================================================
# LOGGED USER
# ======================================================

user = st.session_state.user


# ======================================================
# SIDEBAR HEADER
# ======================================================

st.sidebar.markdown(
    "<div class='sidebar-title'>🏥 Rehab System</div>",
    unsafe_allow_html=True
)

st.sidebar.markdown(
    f"""
<div class="profile-card">

<h3>👤 {user['username']}</h3>

<b>Role</b><br>

{user['role']}

</div>
""",
    unsafe_allow_html=True
)

st.sidebar.divider()


# ======================================================
# MAIN HEADER
# ======================================================

st.title("🏥 Rehabilitation Management Dashboard")

st.caption("Rehabilitation Centre Management System")

st.markdown("---")

# ======================================================
# ADMIN SIDEBAR MENU
# ======================================================

menu = None
module = None

if user["role"] == "Admin":

    # ---------------------------------------------
    # MAIN MODULES
    # ---------------------------------------------

    module = st.sidebar.selectbox(
        "📂 Select Module",
        (
            "🏠 Dashboard",
            "👥 Clients",
            "🩺 Therapists",
            "📅 Appointments",
            "📝 Therapy Notes",
            "📈 Client Progress",
            "⚙ Account"
        )
    )

    st.sidebar.markdown("---")

    # ======================================================
    # DASHBOARD
    # ======================================================

    if module == "🏠 Dashboard":

        menu = "Dashboard"

    # ======================================================
    # CLIENTS
    # ======================================================

    elif module == "👥 Clients":

        st.sidebar.subheader("👥 Client Management")

        menu = st.sidebar.radio(
            "Clients",
            (
                "Add Client",
                "View Clients",
                "Update Client",
                "Delete Client"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # THERAPISTS
    # ======================================================

    elif module == "🩺 Therapists":

        st.sidebar.subheader("🩺 Therapist Management")

        menu = st.sidebar.radio(
            "Therapists",
            (
                "Add Therapist",
                "View Therapists",
                "Update Therapist",
                "Delete Therapist"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # APPOINTMENTS
    # ======================================================

    elif module == "📅 Appointments":

        st.sidebar.subheader("📅 Appointment Management")

        menu = st.sidebar.radio(
            "Appointments",
            (
                "Book Appointment",
                "View Appointments",
                "Cancel Appointment",
                "Complete Appointment",
                "Delete Appointment"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # THERAPY NOTES
    # ======================================================

    elif module == "📝 Therapy Notes":

        st.sidebar.subheader("📝 Therapy Notes")

        menu = st.sidebar.radio(
            "Therapy Notes",
            (
                "Add Therapy Note",
                "View Therapy Notes",
                "Search Therapy Notes",
                "Update Therapy Note",
                "Delete Therapy Note",
                "Export Therapy Notes",
                "Count Therapy Notes"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # CLIENT PROGRESS
    # ======================================================

    elif module == "📈 Client Progress":

        st.sidebar.subheader("📈 Progress")

        menu = "View Client Progress"

    # ======================================================
    # ACCOUNT
    # ======================================================

    elif module == "⚙ Account":

        st.sidebar.subheader("⚙ Account")

        menu = st.sidebar.radio(
            "Account",
            (
                "Change Password",
                "Logout"
            ),
            label_visibility="collapsed"
        )


        # ======================================================
# THERAPIST SIDEBAR MENU
# ======================================================

else:

    # ---------------------------------------------
    # MAIN MODULES
    # ---------------------------------------------

    module = st.sidebar.selectbox(
        "📂 Select Module",
        (
            "🏠 Dashboard",
            "👥 Clients",
            "🩺 Therapists",
            "📅 Appointments",
            "📝 Therapy Notes",
            "📈 Client Progress",
            "⚙ Account"
        )
    )

    st.sidebar.markdown("---")

    # ======================================================
    # DASHBOARD
    # ======================================================

    if module == "🏠 Dashboard":

        menu = "Dashboard"

    # ======================================================
    # CLIENTS
    # ======================================================

    elif module == "👥 Clients":

        st.sidebar.subheader("👥 Clients")

        menu = st.sidebar.radio(
            "Clients",
            (
                "View Clients",
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # THERAPISTS
    # ======================================================

    elif module == "🩺 Therapists":

        st.sidebar.subheader("🩺 Therapists")

        menu = st.sidebar.radio(
            "Therapists",
            (
                "View Therapists",
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # APPOINTMENTS
    # ======================================================

    elif module == "📅 Appointments":

        st.sidebar.subheader("📅 Appointments")

        menu = st.sidebar.radio(
            "Appointments",
            (
                "Book Appointment",
                "View Appointments",
                "Cancel Appointment",
                "Complete Appointment"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # THERAPY NOTES
    # ======================================================

    elif module == "📝 Therapy Notes":

        st.sidebar.subheader("📝 Therapy Notes")

        menu = st.sidebar.radio(
            "Therapy Notes",
            (
                "Add Therapy Note",
                "View Therapy Notes",
                "Search Therapy Notes",
                "Export Therapy Notes",
                "Count Therapy Notes"
            ),
            label_visibility="collapsed"
        )

    # ======================================================
    # CLIENT PROGRESS
    # ======================================================

    elif module == "📈 Client Progress":

        st.sidebar.subheader("📈 Client Progress")

        menu = "View Client Progress"

    # ======================================================
    # ACCOUNT
    # ======================================================

    elif module == "⚙ Account":

        st.sidebar.subheader("⚙ Account")

        menu = st.sidebar.radio(
            "Account",
            (
                "Change Password",
                "Logout"
            ),
            label_visibility="collapsed"
        )

        # ======================================================
# SHARED DASHBOARD
# ======================================================

if menu == "Dashboard":

    st.subheader("🏥 Dashboard")

    st.write("Welcome to the Rehabilitation Management System.")

    st.markdown("")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            label="👥 Clients",
            value="Manage",
            delta=None
        )

    with col2:
        st.metric(
            label="🩺 Therapists",
            value="Manage",
            delta=None
        )

    with col3:
        st.metric(
            label="📅 Appointments",
            value="Schedule",
            delta=None
        )

    with col4:
        st.metric(
            label="📝 Therapy Notes",
            value="Records",
            delta=None
        )

    st.markdown("---")

    left, right = st.columns([2, 1])

    with left:

        st.info(
            """
### System Overview

Use the navigation menu on the left to manage:

- 👥 Clients
- 🩺 Therapists
- 📅 Therapy Appointments
- 📝 Therapy Notes
- 📈 Client Progress
- ⚙ Account Settings

The available options depend on your user role.
            """
        )

    with right:

        st.success(
            f"""
### Current User

**Username:** {user['username']}

**Role:** {user['role']}
            """
        )


# ======================================================
# ACCOUNT ACTIONS
# ======================================================

elif menu == "Change Password":

    change_password(user)


elif menu == "Logout":

    logout()

    st.session_state.user = None

    st.success("Logged out successfully.")

    st.rerun()


# ======================================================
# PART 3 STARTS BELOW THIS SECTION
# ======================================================
#
# if menu == "Add Client":
#     add_client()
#
# elif menu == "View Clients":
#     view_clients()
#
# ...
#
# (Continue with all menu routing in Part 3.)
#

# ======================================================
# CLIENT MANAGEMENT
# ======================================================

elif menu == "Add Client":

    st.header("👥 Add Client")
    add_client()


elif menu == "View Clients":

    st.header("👥 Client Records")
    view_clients()


elif menu == "Update Client":

    st.header("✏ Update Client")
    update_client()


elif menu == "Delete Client":

    st.header("🗑 Delete Client")
    delete_client()


# ======================================================
# THERAPIST MANAGEMENT
# ======================================================

elif menu == "Add Therapist":

    st.header("🩺 Add Therapist")
    add_therapist()


elif menu == "View Therapists":

    st.header("🩺 Therapist Records")
    view_therapists()


elif menu == "Update Therapist":

    st.header("✏ Update Therapist")
    update_therapist()


elif menu == "Delete Therapist":

    st.header("🗑 Delete Therapist")
    delete_therapist()


# ======================================================
# APPOINTMENT MANAGEMENT
# ======================================================

elif menu == "Book Appointment":

    st.header("📅 Book Appointment")
    book_appointment()


elif menu == "View Appointments":

    st.header("📅 Appointment Records")
    view_appointments()


elif menu == "Cancel Appointment":

    st.header("❌ Cancel Appointment")
    cancel_appointment()


elif menu == "Complete Appointment":

    st.header("✅ Complete Appointment")
    complete_appointment()


elif menu == "Delete Appointment":

    st.header("🗑 Delete Appointment")
    delete_appointment()


# ======================================================
# THERAPY NOTES
# ======================================================

elif menu == "Add Therapy Note":

    st.header("📝 Add Therapy Note")
    add_note()


elif menu == "View Therapy Notes":

    st.header("📝 Therapy Notes")
    view_notes()


elif menu == "Search Therapy Notes":

    st.header("🔍 Search Therapy Notes")
    search_notes()


elif menu == "Update Therapy Note":

    st.header("✏ Update Therapy Note")
    update_note()


elif menu == "Delete Therapy Note":

    st.header("🗑 Delete Therapy Note")
    delete_note()


elif menu == "Export Therapy Notes":

    st.header("📤 Export Therapy Notes")
    export_notes_csv()


elif menu == "Count Therapy Notes":

    st.header("📊 Therapy Notes Statistics")
    count_notes()


# ======================================================
# CLIENT PROGRESS
# ======================================================

elif menu == "View Client Progress":

    st.header("📈 Client Progress")
    view_progress()

    # ==========================================================
# SIDEBAR FOOTER
# ==========================================================

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
<div style="text-align:center">

<h4 style="color:#38bdf8;">
🏥 Rehabilitation Management System
</h4>

<p style="font-size:13px;">
Version 1.0
</p>

</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# LOGOUT BUTTON
# ==========================================================

# Show the logout button only if it wasn't already selected
# from the Account menu.

if menu != "Logout":

    if st.sidebar.button(
        "🚪 Logout",
        use_container_width=True
    ):

        logout()

        st.session_state.user = None

        st.success("Logged out successfully.")

        st.rerun()


# ==========================================================
# PAGE FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
<div style="text-align:center; color:#94a3b8; padding:15px;">

© 2026 SLIP Rehabilitation Management System

</div>
""",
    unsafe_allow_html=True
)


# ==========================================================
# CLOSE DATABASE CONNECTION
# ==========================================================

try:
    close_database()
except Exception:
    # Ignore cleanup errors so they don't interrupt the UI
    pass