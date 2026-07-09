import streamlit as st
from database import cursor, conn
from streamlit_option_menu import option_menu

# ==========================================
# LOGIN
# ==========================================

def login(username, password):

    cursor.execute("""
        SELECT username, password, role
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user is None:
        return None

    # Plain-text password comparison
    # Replace with bcrypt.checkpw() if using hashed passwords
    if password != user[1]:
        return None

    return {
        "username": user[0],
        "role": user[2]
    }
user = st.session_state.get("user")

if user is None:
    st.error("Please login first.")
    st.stop()


# ==========================================
# LOGOUT
# ==========================================

def logout():

    st.session_state.user = None


# ==========================================
# CHANGE PASSWORD
# ==========================================

def change_password(user):

    st.subheader("Change Password")

    with st.form("change_password"):

        old_password = st.text_input(
            "Current Password",
            type="password"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        confirm_password = st.text_input(
            "Confirm Password",
            type="password"
        )

        submit = st.form_submit_button(
            "Update Password"
        )

    if submit:

        cursor.execute("""
            SELECT password
            FROM users
            WHERE username=?
        """, (user["username"],))

        current_password = cursor.fetchone()[0]

        if old_password != current_password:

            st.error("Current password is incorrect.")

            return

        if len(new_password) < 4:

            st.error("Password must be at least 4 characters.")

            return

        if new_password != confirm_password:

            st.error("Passwords do not match.")

            return

        cursor.execute("""
            UPDATE users
            SET password=?
            WHERE username=?
        """, (
            new_password,
            user["username"]
        ))

        conn.commit()

        st.success("Password changed successfully.")

        # ==========================================================
# SIDEBAR
# ==========================================================

with st.sidebar:

    st.markdown(
        """
<div class="sidebar-title">

🏥 Rehabilitation System

</div>
""",
        unsafe_allow_html=True
    )

    ##profile_card(user)

    st.markdown("---")

    # =====================================================
    # MAIN NAVIGATION
    # =====================================================

    if user["role"] == "Admin":

        module = option_menu(

            menu_title="Navigation",

            options=[
                "Dashboard",
                "Clients",
                "Therapists",
                "Appointments",
                "Therapy Notes",
                "Client Progress",
                "Account"
            ],

            icons=[
                "speedometer2",
                "people",
                "person-badge",
                "calendar-event",
                "journal-medical",
                "graph-up-arrow",
                "gear"
            ],

            menu_icon="list",

            default_index=0,

            styles={

                "container":{
                    "padding":"5px",
                    "background-color":"#0f172a"
                },

                "icon":{
                    "color":"#38bdf8",
                    "font-size":"18px"
                },

                "nav-link":{

                    "font-size":"15px",

                    "text-align":"left",

                    "margin":"3px",

                    "--hover-color":"#1e293b"

                },

                "nav-link-selected":{

                    "background-color":"#2563eb"

                }

            }

        )

    else:

        module = option_menu(

            menu_title="Navigation",

            options=[
                "Dashboard",
                "Clients",
                "Therapists",
                "Appointments",
                "Therapy Notes",
                "Client Progress",
                "Account"
            ],

            icons=[
                "speedometer2",
                "people",
                "person-badge",
                "calendar-event",
                "journal-medical",
                "graph-up-arrow",
                "gear"
            ],

            menu_icon="list",

            default_index=0
        )

st.session_state.module = module

# ==========================================================
# SUB MENUS
# ==========================================================

menu = None

# ----------------------------------------------------------
# DASHBOARD
# ----------------------------------------------------------

if module == "Dashboard":

    menu = "Dashboard"

# ----------------------------------------------------------
# CLIENTS
# ----------------------------------------------------------

elif module == "Clients":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Client Management",

            (

                "Add Client",

                "View Clients",

                "Update Client",

                "Delete Client"

            )

        )

    else:

        menu = "View Clients"

# ----------------------------------------------------------
# THERAPISTS
# ----------------------------------------------------------

elif module == "Therapists":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Therapist Management",

            (

                "Add Therapist",

                "View Therapists",

                "Update Therapist",

                "Delete Therapist"

            )

        )

    else:

        menu = "View Therapists"

# ----------------------------------------------------------
# APPOINTMENTS
# ----------------------------------------------------------

elif module == "Appointments":

    if user["role"] == "Admin":

        menu = st.sidebar.radio(

            "Appointments",

            (

                "Book Appointment",

                "View Appointments",

                "Cancel Appointment",

                "Complete Appointment",

                "Delete Appointment"

            )

        )

    else:

        menu = st.sidebar.radio(

            "Appointments",

            (

                "Book Appointment",

                "View Appointments",

                "Cancel Appointment",

                "Complete Appointment"

            )

        )

# ----------------------------------------------------------
# NOTES
# ----------------------------------------------------------

elif module == "Therapy Notes":

    if user["role"] == "Admin":

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

            )

        )

    else:

        menu = st.sidebar.radio(

            "Therapy Notes",

            (

                "Add Therapy Note",

                "View Therapy Notes",

                "Search Therapy Notes",

                "Export Therapy Notes",

                "Count Therapy Notes"

            )

        )

# ----------------------------------------------------------
# CLIENT PROGRESS
# ----------------------------------------------------------

elif module == "Client Progress":

    menu = "View Client Progress"

# ----------------------------------------------------------
# ACCOUNT
# ----------------------------------------------------------

elif module == "Account":

    menu = st.sidebar.radio(

        "Account",

        (

            "Change Password",

            "Logout"

        )

    )

# ==========================================================
# PAGE HEADER
# ==========================================================

page_header(

    "🏥 Rehabilitation Management Dashboard",

    f"Logged in as {user['username']} ({user['role']})"

)

# ==========================================================
# PART 2A
# LIVE DASHBOARD
# ==========================================================

from database import cursor

# ==========================================================
# DASHBOARD STATISTICS
# ==========================================================

def dashboard_statistics():

    stats = {}

    # ----------------------------
    # Clients
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM clients")

        stats["clients"] = cursor.fetchone()[0]

    except:

        stats["clients"] = 0

    # ----------------------------
    # Therapists
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM therapists")

        stats["therapists"] = cursor.fetchone()[0]

    except:

        stats["therapists"] = 0

    # ----------------------------
    # Appointments
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM appointments")

        stats["appointments"] = cursor.fetchone()[0]

    except:

        stats["appointments"] = 0

    # ----------------------------
    # Therapy Notes
    # ----------------------------

    try:

        cursor.execute("SELECT COUNT(*) FROM therapy_notes")

        stats["notes"] = cursor.fetchone()[0]

    except:

        stats["notes"] = 0

    return stats


# ==========================================================
# DASHBOARD
# ==========================================================

if menu == "Dashboard":

    page_header(

        "🏥 Rehabilitation Dashboard",

        "Welcome to the Rehabilitation Management System"

    )

    stats = dashboard_statistics()

    # ======================================================
    # KPI CARDS
    # ======================================================

    c1, c2, c3, c4 = st.columns(4)

    with c1:

        st.metric(

            "👥 Clients",

            stats["clients"]

        )

    with c2:

        st.metric(

            "🩺 Therapists",

            stats["therapists"]

        )

    with c3:

        st.metric(

            "📅 Appointments",

            stats["appointments"]

        )

    with c4:

        st.metric(

            "📝 Therapy Notes",

            stats["notes"]

        )

    st.markdown("---")

    # ======================================================
    # QUICK ACTIONS
    # ======================================================

    st.subheader("⚡ Quick Actions")

    q1, q2, q3, q4 = st.columns(4)

    with q1:

        if st.button(

            "➕ Add Client",

            use_container_width=True

        ):

            st.session_state.menu = "Add Client"

            st.rerun()

    with q2:

        if st.button(

            "📅 Book Appointment",

            use_container_width=True

        ):

            st.session_state.menu = "Book Appointment"

            st.rerun()

    with q3:

        if st.button(

            "📝 Add Therapy Note",

            use_container_width=True

        ):

            st.session_state.menu = "Add Therapy Note"

            st.rerun()

    with q4:

        if st.button(

            "📈 View Progress",

            use_container_width=True

        ):

            st.session_state.menu = "View Client Progress"

            st.rerun()

    st.markdown("---")

    # ======================================================
    # SYSTEM OVERVIEW
    # ======================================================

    left, right = st.columns([2, 1])

    with left:

        st.markdown(
            """
### 🏥 System Overview

The Rehabilitation Management System allows you to:

- 👥 Manage rehabilitation clients
- 🩺 Manage therapists
- 📅 Schedule therapy appointments
- 📝 Record therapy notes
- 📈 Track rehabilitation progress
- 🔒 Secure administrator and therapist access
"""
        )

    with right:

        st.info(

            f"""
### Logged-in User

**Username**

{user['username']}

**Role**

{user['role']}
"""

        )

    st.markdown("---")

    st.success("✅ System is ready.")

    