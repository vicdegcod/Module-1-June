import streamlit as st
import pandas as pd

from database import conn, cursor
from validation import (
    validate_name,
    validate_age,
    validate_gender,
    validate_email,
    validate_sessions
)


# ==========================================
# CALCULATE PROGRESS
# ==========================================

def calculate_progress(completed, total):

    if total == 0:
        return 0

    return (completed / total) * 100


# ==========================================
# ADD CLIENT
# ==========================================

def add_client():

    st.header("➕ Add Client")

    with st.form("add_client"):

        name = st.text_input("Name")

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=120
        )

        gender = st.selectbox(
            "Gender",
            ["Male", "Female", "Other"]
        )

        email = st.text_input("Email")

        condition = st.text_input(
            "Rehabilitation Condition"
        )

        total = st.number_input(
            "Total Therapy Sessions",
            min_value=1
        )

        completed = st.number_input(
            "Completed Sessions",
            min_value=0
        )

        submit = st.form_submit_button(
            "Add Client"
        )

    if submit:

        valid, msg = validate_name(name)
        if not valid:
            st.error(msg)
            return

        valid, msg = validate_age(str(age))
        if not valid:
            st.error(msg)
            return

        valid, msg = validate_gender(gender)
        if not valid:
            st.error(msg)
            return

        valid, msg = validate_email(email)
        if not valid:
            st.error(msg)
            return

        valid, msg = validate_sessions(str(total))
        if not valid:
            st.error(msg)
            return

        if completed > total:
            st.error(
                "Completed sessions cannot exceed total sessions."
            )
            return

        cursor.execute("""
        INSERT INTO clients
        (
        name,
        age,
        gender,
        email,
        condition,
        completed_sessions,
        total_sessions
        )
        VALUES(?,?,?,?,?,?,?)
        """,

        (
            name,
            age,
            gender,
            email,
            condition,
            completed,
            total
        ))

        conn.commit()

        st.success("Client added successfully.")


# ==========================================
# VIEW CLIENTS
# ==========================================

def view_clients():

    st.header("👥 Clients")

    cursor.execute("SELECT * FROM clients")

    rows = cursor.fetchall()

    if not rows:

        st.info("No clients found.")

        return

    df = pd.DataFrame(

        rows,

        columns=[
            "ID",
            "Name",
            "Age",
            "Gender",
            "Email",
            "Condition",
            "Completed",
            "Total"
        ]

    )

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================
# UPDATE CLIENT
# ==========================================

def update_client():

    st.header("✏ Update Client")

    client_id = st.number_input(
        "Client ID",
        min_value=1,
        step=1
    )

    if st.button("Load Client"):

        cursor.execute(
            "SELECT * FROM clients WHERE client_id=?",
            (client_id,)
        )

        client = cursor.fetchone()

        if client is None:

            st.error("Client not found.")

            return

        st.session_state.client = client

    if "client" in st.session_state:

        client = st.session_state.client

        with st.form("update_client"):

            name = st.text_input(
                "Name",
                value=client[1]
            )

            age = st.number_input(
                "Age",
                value=client[2]
            )

            gender = st.selectbox(
                "Gender",
                ["Male", "Female", "Other"],
                index=["Male","Female","Other"].index(client[3])
            )

            email = st.text_input(
                "Email",
                value=client[4]
            )

            condition = st.text_input(
                "Condition",
                value=client[5]
            )

            completed = st.number_input(
                "Completed Sessions",
                value=client[6]
            )

            total = st.number_input(
                "Total Sessions",
                value=client[7]
            )

            update = st.form_submit_button(
                "Update Client"
            )

        if update:

            cursor.execute("""

            UPDATE clients

            SET

            name=?,
            age=?,
            gender=?,
            email=?,
            condition=?,
            completed_sessions=?,
            total_sessions=?

            WHERE client_id=?

            """,

            (
                name,
                age,
                gender,
                email,
                condition,
                completed,
                total,
                client_id
            ))

            conn.commit()

            del st.session_state.client

            st.success("Client updated successfully.")


# ==========================================
# DELETE CLIENT
# ==========================================

def delete_client():

    st.header("🗑 Delete Client")

    client_id = st.number_input(
        "Client ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Client"):

        cursor.execute(
            "SELECT * FROM clients WHERE client_id=?",
            (client_id,)
        )

        if cursor.fetchone() is None:

            st.error("Client not found.")

            return

        cursor.execute(
            "DELETE FROM clients WHERE client_id=?",
            (client_id,)
        )

        conn.commit()

        st.success("Client deleted successfully.")


# ==========================================
# VIEW CLIENT PROGRESS
# ==========================================

def view_progress():

    st.header("📈 Client Progress")

    cursor.execute("""
    SELECT
    client_id,
    name,
    completed_sessions,
    total_sessions
    FROM clients
    """)

    rows = cursor.fetchall()

    if not rows:

        st.info("No clients available.")

        return

    for row in rows:

        progress = calculate_progress(
            row[2],
            row[3]
        )

        st.subheader(
            f"{row[1]} (ID {row[0]})"
        )

        st.write(
            f"{row[2]} / {row[3]} Sessions"
        )

        st.progress(progress / 100)

        st.write(
            f"{progress:.1f}% Complete"
        )

        st.divider()