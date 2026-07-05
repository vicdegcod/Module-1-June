import sqlite3

# ==========================================
# DATABASE
# ==========================================

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("sliprehab.db")
        self.cursor = self.conn.cursor()
        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            gender TEXT,
            addiction TEXT,
            admission_date TEXT,
            completed_sessions INTEGER DEFAULT 0,
            total_sessions INTEGER
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS therapists(
            therapist_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            specialization TEXT,
            phone TEXT
        )
        """)

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS appointments(
            appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER,
            therapist_id INTEGER,
            visit_date TEXT,
            visit_time TEXT,
            status TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(client_id),
            FOREIGN KEY(therapist_id) REFERENCES therapists(therapist_id)
        )
        """)

        self.conn.commit()


db = Database()


# ==========================================
# FUNCTIONS
# ==========================================

def add_client():

    print("\nADD CLIENT")

    name = input("Client Name: ")
    age = int(input("Age: "))
    gender = input("Gender (Male/Female/Other): ")
    addiction = input("Addiction Type: ")
    admission = input("Admission Date (YYYY-MM-DD): ")
    sessions = int(input("Total Therapy Sessions: "))

    db.cursor.execute("""
    INSERT INTO clients
    (name,age,gender,addiction,admission_date,total_sessions)
    VALUES(?,?,?,?,?,?)
    """,
    (
        name,
        age,
        gender,
        addiction,
        admission,
        sessions
    ))

    db.conn.commit()

    print("Client Added Successfully")


def delete_client():

    print("\nDELETE CLIENT")

    cid = int(input("Client ID: "))

    db.cursor.execute(
        "DELETE FROM appointments WHERE client_id=?",
        (cid,)
    )

    db.cursor.execute(
        "DELETE FROM clients WHERE client_id=?",
        (cid,)
    )

    db.conn.commit()

    print("Client Deleted Successfully")


def view_clients():

    print("\nCLIENT LIST")

    db.cursor.execute("SELECT * FROM clients")

    rows = db.cursor.fetchall()

    if not rows:
        print("No clients found.")
        return

    print("-" * 90)

    for row in rows:
        print(row)


def add_therapist():

    print("\nADD THERAPIST")

    name = input("Therapist Name: ")
    specialization = input("Specialization: ")
    phone = input("Phone: ")

    db.cursor.execute("""
    INSERT INTO therapists(name,specialization,phone)
    VALUES(?,?,?)
    """,
    (
        name,
        specialization,
        phone
    ))

    db.conn.commit()

    print("Therapist Added Successfully")


def view_therapists():

    print("\nTHERAPISTS")

    db.cursor.execute("SELECT * FROM therapists")

    rows = db.cursor.fetchall()

    if not rows:
        print("No therapists found.")
        return

    print("-" * 70)

    for row in rows:
        print(row)


def book_visit():

    print("\nBOOK THERAPY VISIT")

    client = int(input("Client ID: "))
    therapist = int(input("Therapist ID: "))
    visit_date = input("Visit Date (YYYY-MM-DD): ")
    visit_time = input("Visit Time (HH:MM): ")

    db.cursor.execute("""
    INSERT INTO appointments
    (client_id,therapist_id,visit_date,visit_time,status)
    VALUES(?,?,?,?,?)
    """,
    (
        client,
        therapist,
        visit_date,
        visit_time,
        "Booked"
    ))

    db.conn.commit()

    print("Therapy Visit Booked Successfully")


def cancel_visit():

    print("\nCANCEL THERAPY VISIT")

    appointment = int(input("Appointment ID: "))

    db.cursor.execute("""
    UPDATE appointments
    SET status='Cancelled'
    WHERE appointment_id=?
    """,
    (
        appointment,
    ))

    db.conn.commit()

    print("Appointment Cancelled")


def view_visits():

    print("\nTHERAPY VISITS")

    db.cursor.execute("""
    SELECT
    appointment_id,
    client_id,
    therapist_id,
    visit_date,
    visit_time,
    status
    FROM appointments
    """)

    rows = db.cursor.fetchall()

    if not rows:
        print("No appointments found.")
        return

    print("-" * 90)

    for row in rows:
        print(row)


def update_progress():

    print("\nUPDATE TREATMENT PROGRESS")

    cid = int(input("Client ID: "))
    completed = int(input("Completed Sessions: "))

    db.cursor.execute("""
    UPDATE clients
    SET completed_sessions=?
    WHERE client_id=?
    """,
    (
        completed,
        cid
    ))

    db.conn.commit()

    print("Treatment Progress Updated")


def calculate_progress():

    print("\nCALCULATE TREATMENT PROGRESS")

    cid = int(input("Client ID: "))

    db.cursor.execute("""
    SELECT
    name,
    completed_sessions,
    total_sessions
    FROM clients
    WHERE client_id=?
    """,
    (
        cid,
    ))

    row = db.cursor.fetchone()

    if row:

        name = row[0]
        completed = row[1]
        total = row[2]

        if total == 0:
            progress = 0
        else:
            progress = (completed / total) * 100

        print("\nClient:", name)
        print("Completed Sessions:", completed)
        print("Total Sessions:", total)

        bar = "#" * int(progress / 5)

        print(f"[{bar:<20}] {progress:.2f}%")

    else:
        print("Client Not Found")


# ==========================================
# MAIN MENU
# ==========================================

while True:

    print("\n")
    print("=" * 50)
    print("REHABILITATION MANAGEMENT SYSTEM")
    print("=" * 50)

    print("1. Add Client")
    print("2. Delete Client")
    print("3. View Clients")
    print("4. Add Therapist")
    print("5. View Therapists")
    print("6. Book Therapy Visit")
    print("7. Cancel Therapy Visit")
    print("8. View Therapy Visits")
    print("9. Update Treatment Progress")
    print("10. Calculate Progress")
    print("11. Exit")

    choice = input("\nEnter your choice: ")

    if choice == "1":
        add_client()

    elif choice == "2":
        delete_client()

    elif choice == "3":
        view_clients()

    elif choice == "4":
        add_therapist()

    elif choice == "5":
        view_therapists()

    elif choice == "6":
        book_visit()

    elif choice == "7":
        cancel_visit()

    elif choice == "8":
        view_visits()

    elif choice == "9":
        update_progress()

    elif choice == "10":
        calculate_progress()

    elif choice == "11":
        print("Thank you for using the Rehabilitation Management System.")
        db.conn.close()
        break

    else:
        print("Invalid choice. Please try again.")