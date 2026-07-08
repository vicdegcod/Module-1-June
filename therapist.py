import streamlit as st
import pandas as pd

from database import conn, cursor
from validation import (
    validate_name,
    validate_email,
    validate_phone
)


# ==========================================
# ADD THERAPIST
# ==========================================

def add_therapist():

    st.header("👨‍⚕️ Add Therapist")

    with st.form("add_therapist"):

        name = st.text_input("Therapist Name")

        specialization = st.text_input("Specialization")

        phone = st.text_input("Phone Number")

        email = st.text_input("Email")

        submit = st.form_submit_button(
            "Add Therapist"
        )

    if submit:

        valid, message = validate_name(name)
        if not valid:
            st.error(message)
            return

        if specialization.strip() == "":
            st.error("Specialization cannot be empty.")
            return

        valid, message = validate_phone(phone)
        if not valid:
            st.error(message)
            return

        valid, message = validate_email(email)
        if not valid:
            st.error(message)
            return

        cursor.execute("""

        INSERT INTO therapists
        (
            name,
            specialization,
            phone,
            email
        )

        VALUES(?,?,?,?)

        """,

        (
            name,
            specialization,
            phone,
            email
        ))

        conn.commit()

        st.success("Therapist added successfully.")


# ==========================================
# VIEW THERAPISTS
# ==========================================

def view_therapists():

    st.header("👨‍⚕️ Therapists")

    cursor.execute("""
    SELECT *
    FROM therapists
    """)

    rows = cursor.fetchall()

    if not rows:

        st.info("No therapists found.")

        return

    df = pd.DataFrame(

        rows,

        columns=[
            "ID",
            "Name",
            "Specialization",
            "Phone",
            "Email"
        ]

    )

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================
# UPDATE THERAPIST
# ==========================================

def update_therapist():

    st.header("✏️ Update Therapist")

    therapist_id = st.number_input(
        "Therapist ID",
        min_value=1,
        step=1
    )

    if st.button("Load Therapist"):

        cursor.execute("""

        SELECT *

        FROM therapists

        WHERE therapist_id=?

        """,

        (therapist_id,))

        therapist = cursor.fetchone()

        if therapist is None:

            st.error("Therapist not found.")

            return

        st.session_state.therapist = therapist

    if "therapist" in st.session_state:

        therapist = st.session_state.therapist

        with st.form("update_therapist"):

            name = st.text_input(
                "Name",
                value=therapist[1]
            )

            specialization = st.text_input(
                "Specialization",
                value=therapist[2]
            )

            phone = st.text_input(
                "Phone",
                value=therapist[3]
            )

            email = st.text_input(
                "Email",
                value=therapist[4]
            )

            update = st.form_submit_button(
                "Update Therapist"
            )

        if update:

            valid, message = validate_name(name)
            if not valid:
                st.error(message)
                return

            if specialization.strip() == "":
                st.error("Specialization cannot be empty.")
                return

            valid, message = validate_phone(phone)
            if not valid:
                st.error(message)
                return

            valid, message = validate_email(email)
            if not valid:
                st.error(message)
                return

            cursor.execute("""

            UPDATE therapists

            SET

            name=?,
            specialization=?,
            phone=?,
            email=?

            WHERE therapist_id=?

            """,

            (
                name,
                specialization,
                phone,
                email,
                therapist_id
            ))

            conn.commit()

            del st.session_state.therapist

            st.success(
                "Therapist updated successfully."
            )


# ==========================================
# DELETE THERAPIST
# ==========================================

def delete_therapist():

    st.header("🗑️ Delete Therapist")

    therapist_id = st.number_input(
        "Therapist ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Therapist"):

        cursor.execute("""

        SELECT name

        FROM therapists

        WHERE therapist_id=?

        """,

        (therapist_id,))

        therapist = cursor.fetchone()

        if therapist is None:

            st.error("Therapist not found.")

            return

        cursor.execute("""

        DELETE FROM therapists

        WHERE therapist_id=?

        """,

        (therapist_id,))

        conn.commit()

        st.success(
            f"{therapist[0]} deleted successfully."
        )