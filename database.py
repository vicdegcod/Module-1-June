import sqlite3
import streamlit as st


# ==========================================
# DATABASE CONNECTION
# ==========================================

@st.cache_resource
def get_connection():
    conn = sqlite3.connect(
        "rehabilitation.db",
        check_same_thread=False
    )
    return conn

conn = get_connection()
cursor = conn.cursor()

# ==========================================
# CREATE TABLES
# ==========================================

def create_tables():

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        user_id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        role TEXT NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS clients(
        client_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER NOT NULL,
        gender TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        condition TEXT NOT NULL,
        completed_sessions INTEGER DEFAULT 0,
        total_sessions INTEGER DEFAULT 0
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS therapists(
        therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        specialization TEXT NOT NULL,
        phone TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS appointments(
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        therapist_id INTEGER NOT NULL,
        appointment_date TEXT NOT NULL,
        status TEXT DEFAULT 'Booked',

        FOREIGN KEY(client_id)
        REFERENCES clients(client_id),

        FOREIGN KEY(therapist_id)
        REFERENCES therapists(therapist_id)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS therapy_notes(
        note_id INTEGER PRIMARY KEY AUTOINCREMENT,
        client_id INTEGER NOT NULL,
        therapist_id INTEGER NOT NULL,
        session_date TEXT NOT NULL,
        notes TEXT NOT NULL,

        FOREIGN KEY(client_id)
        REFERENCES clients(client_id),

        FOREIGN KEY(therapist_id)
        REFERENCES therapists(therapist_id)
    )
    """)

    conn.commit()


# ==========================================
# CREATE DEFAULT USERS
# ==========================================

def create_default_users():

    users = [

        ("admin", "admin123", "Admin"),

        ("therapist", "therapy123", "Therapist")

    ]

    for user in users:

        cursor.execute("""

        SELECT *

        FROM users

        WHERE username=?

        """,

        (user[0],))

        if cursor.fetchone() is None:

            cursor.execute("""

            INSERT INTO users
            (
                username,
                password,
                role
            )

            VALUES(?,?,?)

            """,

            user)

    conn.commit()


# ==========================================
# INITIALIZE DATABASE
# ==========================================

create_tables()

create_default_users()


# ==========================================
# CLOSE DATABASE
# ==========================================

def close_database():
    conn.commit()