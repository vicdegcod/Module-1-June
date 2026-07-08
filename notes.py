import streamlit as st
import pandas as pd
import io

from database import conn, cursor
from validation import validate_date


# ==========================================
# HELPER FUNCTION
# ==========================================

def get_note_details():

    cursor.execute("""

    SELECT

    therapy_notes.note_id,

    clients.name,

    therapists.name,

    therapy_notes.session_date,

    therapy_notes.notes

    FROM therapy_notes

    JOIN clients

    ON therapy_notes.client_id=clients.client_id

    JOIN therapists

    ON therapy_notes.therapist_id=therapists.therapist_id

    ORDER BY therapy_notes.session_date DESC

    """)

    rows = cursor.fetchall()

    return pd.DataFrame(

        rows,

        columns=[
            "Note ID",
            "Client",
            "Therapist",
            "Session Date",
            "Notes"
        ]

    )


# ==========================================
# ADD NOTE
# ==========================================

def add_note():

    st.header("📝 Add Therapy Note")

    with st.form("add_note"):

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

        session_date = st.date_input(
            "Session Date"
        )

        notes = st.text_area(
            "Therapy Notes"
        )

        submit = st.form_submit_button(
            "Save Note"
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
            str(session_date)
        )

        if not valid:

            st.error(message)

            return

        if notes.strip() == "":

            st.error("Therapy notes cannot be empty.")

            return

        cursor.execute("""

        INSERT INTO therapy_notes
        (
            client_id,
            therapist_id,
            session_date,
            notes
        )

        VALUES(?,?,?,?)

        """,

        (
            client_id,
            therapist_id,
            str(session_date),
            notes
        ))

        conn.commit()

        st.success("Therapy note saved successfully.")


# ==========================================
# VIEW NOTES
# ==========================================

def view_notes():

    st.header("📋 Therapy Notes")

    df = get_note_details()

    if df.empty:

        st.info("No therapy notes found.")

        return

    st.dataframe(
        df,
        use_container_width=True
    )


# ==========================================
# SEARCH NOTES
# ==========================================

def search_notes():

    st.header("🔍 Search Therapy Notes")

    client_id = st.number_input(
        "Client ID",
        min_value=1,
        step=1
    )

    if st.button("Search"):

        cursor.execute("""

        SELECT

        therapy_notes.note_id,

        clients.name,

        therapists.name,

        therapy_notes.session_date,

        therapy_notes.notes

        FROM therapy_notes

        JOIN clients

        ON therapy_notes.client_id=clients.client_id

        JOIN therapists

        ON therapy_notes.therapist_id=therapists.therapist_id

        WHERE therapy_notes.client_id=?

        ORDER BY therapy_notes.session_date DESC

        """,

        (client_id,))

        rows = cursor.fetchall()

        if not rows:

            st.info("No notes found.")

            return

        df = pd.DataFrame(

            rows,

            columns=[
                "Note ID",
                "Client",
                "Therapist",
                "Session Date",
                "Notes"
            ]

        )

        st.dataframe(
            df,
            use_container_width=True
        )


# ==========================================
# UPDATE NOTE
# ==========================================

def update_note():

    st.header("✏️ Update Therapy Note")

    note_id = st.number_input(
        "Note ID",
        min_value=1,
        step=1
    )

    if st.button("Load Note"):

        cursor.execute(
            "SELECT * FROM therapy_notes WHERE note_id=?",
            (note_id,)
        )

        note = cursor.fetchone()

        if note is None:

            st.error("Note not found.")

            return

        st.session_state.note = note

    if "note" in st.session_state:

        note = st.session_state.note

        with st.form("update_note"):

            session_date = st.date_input(
                "Session Date"
            )

            notes = st.text_area(
                "Therapy Notes",
                value=note[4]
            )

            update = st.form_submit_button(
                "Update Note"
            )

        if update:

            cursor.execute("""

            UPDATE therapy_notes

            SET

            session_date=?,
            notes=?

            WHERE note_id=?

            """,

            (
                str(session_date),
                notes,
                note_id
            ))

            conn.commit()

            del st.session_state.note

            st.success(
                "Therapy note updated successfully."
            )


# ==========================================
# DELETE NOTE
# ==========================================

def delete_note():

    st.header("🗑️ Delete Therapy Note")

    note_id = st.number_input(
        "Note ID",
        min_value=1,
        step=1
    )

    if st.button("Delete Note"):

        cursor.execute(
            "SELECT * FROM therapy_notes WHERE note_id=?",
            (note_id,)
        )

        if cursor.fetchone() is None:

            st.error("Note not found.")

            return

        cursor.execute(
            "DELETE FROM therapy_notes WHERE note_id=?",
            (note_id,)
        )

        conn.commit()

        st.success("Therapy note deleted successfully.")


# ==========================================
# EXPORT CSV
# ==========================================

def export_notes_csv():

    st.header("📥 Export Therapy Notes")

    df = get_note_details()

    if df.empty:

        st.info("No therapy notes available.")

        return

    csv_data = io.StringIO()

    df.to_csv(
        csv_data,
        index=False
    )

    st.download_button(

        label="Download Therapy Notes",

        data=csv_data.getvalue(),

        file_name="therapy_notes.csv",

        mime="text/csv"

    )


# ==========================================
# COUNT NOTES
# ==========================================

def count_notes():

    cursor.execute(
        "SELECT COUNT(*) FROM therapy_notes"
    )

    total = cursor.fetchone()[0]

    st.metric(
        "Total Therapy Notes",
        total
    )