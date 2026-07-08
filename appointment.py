import streamlit as st
import pandas as pd

from database import conn, cursor
from validation import validate_date


# ==========================================
# BOOK APPOINTMENT
# ==========================================

def book_appointment():

    st.header("📅 Book Appointment")

    with st.form("book_appointment"):

        client_id = st.number_input(
            "Client ID",
            min_value=1,
            step=1
        )

        therapist_id = st.number_input(
            "Therapist ID",
            min_value=1,
            step=1
        )

        appointment_date = st.date_input(
            "Appointment Date"
        )

        submit = st.form_submit_button(
            "Book Appointment"
        )

    if submit:

        cursor.execute(
            "SELECT * FROM clients WHERE client_id=?",
            (client_id,)
        )

        if cursor.fetchone() is None:

            st.error("Client not found.")

            return

        cursor.execute(
            "SELECT * FROM therapists WHERE therapist_id=?",
            (therapist_id,)
        )

        if cursor.fetchone() is None:

            st.error("Therapist not found.")

            return

        valid, message = validate_date(
            str(appointment_date)
        )

        if not valid:

            st.error(message)

            return

        cursor.execute("""

        INSERT INTO appointments
        (
            client_id,
            therapist_id,
            appointment_date,
            status
        )

        VALUES(?,?,?,?)

        """,

        (
            client_id,
            therapist_id,
            str(appointment_date),
            "Booked"
        ))

        conn.commit()

        st.success("Appointment booked successfully.")


# ==========================================
# VIEW APPOINTMENTS
# ==========================================

def view_appointments():

    st.header("📋 Appointments")

    cursor.execute("""

    SELECT

    appointments.appointment_id,

    clients.name,

    therapists.name,

    appointments.appointment_date,

    appointments.status

    FROM appointments

    JOIN clients

    ON appointments.client_id=clients.client_id

    JOIN therapists

    ON appointments.therapist_id=therapists.therapist_id

    ORDER BY appointments.appointment_date

    """)

    rows = cursor.fetchall()

    if not rows:

        st.info("No appointments found.")

        return

    df = pd.DataFrame(

        rows,

        columns=[

            "Appointment ID",

            "Client",

            "Therapist",

            "Date",

            "Status"

        ]

    )

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================
# CANCEL APPOINTMENT
# ==========================================

def cancel_appointment():

    st.header("❌ Cancel Appointment")

    appointment_id = st.number_input(
        "Appointment ID",
        min_value=1,
        step=1
    )

    if st.button("Cancel Appointment"):

        cursor.execute(

            "SELECT * FROM appointments WHERE appointment_id=?",

            (appointment_id,)

        )

        if cursor.fetchone() is None:

            st.error("Appointment not found.")

            return

        cursor.execute("""

        UPDATE appointments

        SET status='Cancelled'

        WHERE appointment_id=?

        """,

        (appointment_id,))

        conn.commit()

        st.success("Appointment cancelled successfully.")


# ==========================================
# COMPLETE APPOINTMENT
# ==========================================

def complete_appointment():

    st.header("✅ Complete Appointment")

    appointment_id = st.number_input(

        "Appointment ID",

        min_value=1,

        step=1

    )

    if st.button("Complete Appointment"):

        cursor.execute("""

        SELECT client_id,status

        FROM appointments

        WHERE appointment_id=?

        """,

        (appointment_id,))

        appointment = cursor.fetchone()

        if appointment is None:

            st.error("Appointment not found.")

            return

        if appointment[1] == "Cancelled":

            st.error(
                "Cancelled appointments cannot be completed."
            )

            return

        cursor.execute("""

        UPDATE appointments

        SET status='Completed'

        WHERE appointment_id=?

        """,

        (appointment_id,))

        cursor.execute("""

        UPDATE clients

        SET completed_sessions=
        completed_sessions+1

        WHERE client_id=?

        AND completed_sessions<total_sessions

        """,

        (appointment[0],))

        conn.commit()

        st.success(
            "Appointment completed successfully."
        )


# ==========================================
# DELETE APPOINTMENT
# ==========================================

def delete_appointment():

    st.header("🗑 Delete Appointment")

    appointment_id = st.number_input(

        "Appointment ID",

        min_value=1,

        step=1

    )

    if st.button("Delete Appointment"):

        cursor.execute(

            "SELECT * FROM appointments WHERE appointment_id=?",

            (appointment_id,)

        )

        if cursor.fetchone() is None:

            st.error("Appointment not found.")

            return

        cursor.execute(

            "DELETE FROM appointments WHERE appointment_id=?",

            (appointment_id,)

        )

        conn.commit()

        st.success("Appointment deleted successfully.")