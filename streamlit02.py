import sqlite3
import pandas as pd


class Database:

    def __init__(self):
        self.conn = sqlite3.connect(
            "sliprehab.db",
            check_same_thread=False
        )

        self.cursor = self.conn.cursor()

        self.create_tables()

    # -------------------------------------------------
    # CREATE TABLES
    # -------------------------------------------------

    def create_tables(self):

        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS clients(
            client_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
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
            name TEXT NOT NULL,
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

    # -------------------------------------------------
    # CLIENT FUNCTIONS
    # -------------------------------------------------

    def add_client(
        self,
        name,
        age,
        gender,
        addiction,
        admission_date,
        total_sessions
    ):

        self.cursor.execute("""
        INSERT INTO clients(
            name,
            age,
            gender,
            addiction,
            admission_date,
            total_sessions
        )
        VALUES(?,?,?,?,?,?)
        """,
        (
            name,
            age,
            gender,
            addiction,
            admission_date,
            total_sessions
        ))

        self.conn.commit()

    def delete_client(self, client_id):

        self.cursor.execute(
            "DELETE FROM appointments WHERE client_id=?",
            (client_id,)
        )

        self.cursor.execute(
            "DELETE FROM clients WHERE client_id=?",
            (client_id,)
        )

        self.conn.commit()

    def get_clients(self):

        query = "SELECT * FROM clients"

        return pd.read_sql(query, self.conn)

    def get_client(self, client_id):

        self.cursor.execute("""
        SELECT *
        FROM clients
        WHERE client_id=?
        """, (client_id,))

        return self.cursor.fetchone()

    # -------------------------------------------------
    # THERAPISTS
    # -------------------------------------------------

    def add_therapist(
        self,
        name,
        specialization,
        phone
    ):

        self.cursor.execute("""
        INSERT INTO therapists(
            name,
            specialization,
            phone
        )
        VALUES(?,?,?)
        """,
        (
            name,
            specialization,
            phone
        ))

        self.conn.commit()

    def get_therapists(self):

        query = "SELECT * FROM therapists"

        return pd.read_sql(query, self.conn)

    # -------------------------------------------------
    # APPOINTMENTS
    # -------------------------------------------------

    def book_visit(
        self,
        client_id,
        therapist_id,
        visit_date,
        visit_time
    ):

        self.cursor.execute("""
        INSERT INTO appointments(
            client_id,
            therapist_id,
            visit_date,
            visit_time,
            status
        )
        VALUES(?,?,?,?,?)
        """,
        (
            client_id,
            therapist_id,
            visit_date,
            visit_time,
            "Booked"
        ))

        self.conn.commit()

    def cancel_visit(self, appointment_id):

        self.cursor.execute("""
        UPDATE appointments
        SET status='Cancelled'
        WHERE appointment_id=?
        """,
        (appointment_id,)
        )

        self.conn.commit()

    def get_appointments(self):

        query = """
        SELECT
            appointment_id,
            client_id,
            therapist_id,
            visit_date,
            visit_time,
            status
        FROM appointments
        """

        return pd.read_sql(query, self.conn)

    # -------------------------------------------------
    # PROGRESS
    # -------------------------------------------------

    def update_progress(
        self,
        client_id,
        completed_sessions
    ):

        self.cursor.execute("""
        UPDATE clients
        SET completed_sessions=?
        WHERE client_id=?
        """,
        (
            completed_sessions,
            client_id
        ))

        self.conn.commit()

    def calculate_progress(self, client_id):

        self.cursor.execute("""
        SELECT
            name,
            completed_sessions,
            total_sessions
        FROM clients
        WHERE client_id=?
        """,
        (client_id,)
        )

        row = self.cursor.fetchone()

        if row is None:
            return None

        name, completed, total = row

        progress = 0

        if total > 0:
            progress = (completed / total) * 100

        return {
            "name": name,
            "completed": completed,
            "total": total,
            "progress": progress
        }

    # -------------------------------------------------
    # DASHBOARD
    # -------------------------------------------------

    def total_clients(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM clients"
        )

        return self.cursor.fetchone()[0]

    def total_therapists(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM therapists"
        )

        return self.cursor.fetchone()[0]

    def total_appointments(self):

        self.cursor.execute(
            "SELECT COUNT(*) FROM appointments"
        )

        return self.cursor.fetchone()[0]
    

    import streamlit as st 
    import streamlit_shadcn_ui as ui
    
    st.set_page_config( page_title="Rehabilitation Management System", page_icon="🏥", layout="wide", initial_sidebar_state="expanded" )
    db = Database() 
    st.markdown(""" <style> .block-container{ padding-top:2rem; padding-bottom:2rem; } .main-title{ text-align:center; font-size:42px; font-weight:bold; color:#2563eb; } .subtitle{ text-align:center; color:gray; margin-bottom:30px; } </style> """, unsafe_allow_html=True) 
    st.markdown("<h1 class='main-title'>🏥 Rehabilitation Management System</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Addiction Recovery & Therapy Management Dashboard</p>", unsafe_allow_html=True)
    st.divider() 
    clients = db.total_clients() 
    therapists = db.total_therapists()
    appointments = db.total_appointments() 
    col1, col2, col3 = st.columns(3) 
    with col1: ui.metric_card( title="Clients", content=str(clients), description="Registered Clients", key="clients_card" ) 
    with col2: ui.metric_card( title="Therapists", content=str(therapists), description="Available Therapists", key="therapists_card" ) with col3: ui.metric_card( title="Appointments", content=str(appointments), description="Scheduled Visits", key="appointments_card" ) 
    st.divider()
    left, right = st.columns([2, 1]) 
    with left: st.subheader("Welcome") 
    st.write(""" The Rehabilitation Management System helps rehabilitation centres manage clients, therapists, therapy appointments and treatment progress from one simple dashboard. """) 
    st.info(""" Use the navigation menu on the left to access: • Dashboard • Clients • Therapists • Appointments • Treatment Progress """) 
    with right: ui.alert_dialog( show=True, title="System Ready", description="Database connected successfully." ) 
    st.divider()
    st.subheader("Quick Overview") 
    overview1, overview2 = st.columns(2) 
    with overview1: st.success(f"👥 Total Clients: {clients}") 
    st.success(f"🩺 Total Therapists: {therapists}") 
    with overview2: st.success(f"📅 Total Appointments: {appointments}") if clients > 0:average = appointments / clients else: average = 0 st.success(f"📈 Average Visits per Client: {average:.2f}") st.divider() 
    st.caption("Rehabilitation Management System | Streamlit + streamlit-shadcn-ui")

    import streamlit as st 
    import streamlit_shadcn_ui as ui 
    db = Database() 
    st.set_page_config( page_title="Clients", page_icon="👥", layout="wide" ) 
    st.title("👥 Client Management") 
    tab = ui.tabs( options=[ "Add Client", "View Clients", "Update Client", "Delete Client" ], default_value="Add Client", key="client_tabs" ) if tab == "Add Client": st.subheader("➕ Register New Client") with st.container(border=True): col1, col2 = st.columns(2) with col1: name = st.text_input("Client Name") age = st.number_input( "Age", min_value=1, max_value=120, value=18 ) gender = st.selectbox( "Gender", [ "Male", "Female", "Other" ] ) with col2: addiction = st.text_input("Addiction Type") admission_date = st.date_input( "Admission Date" ) total_sessions = st.number_input( "Total Therapy Sessions", min_value=1, value=10 ) st.divider() if ui.button( text="Add Client", key="add_client_button" ): if name.strip() == "": st.error("Client name is required.") elif addiction.strip() == "": st.error("Please enter the addiction type.") else: db.add_client( name=name, age=age, gender=gender, addiction=addiction, admission_date=str(admission_date), total_sessions=total_sessions ) st.success("✅ Client registered successfully!") elif tab == "View Clients": st.subheader("📋 Registered Clients") clients = db.get_clients() if clients.empty: st.info("No clients have been registered.") else: col1, col2 = st.columns([3, 1]) with col1: search = st.text_input( "🔍 Search by client name" ) with col2: gender_filter = st.selectbox( "Gender", [ "All", "Male", "Female", "Other" ] ) filtered = clients.copy() if search: filtered = filtered[ filtered["name"] .str.contains(search, case=False) ] if gender_filter != "All": filtered = filtered[ filtered["gender"] == gender_filter ] st.dataframe( filtered, use_container_width=True, hide_index=True ) st.caption( f"Showing {len(filtered)} of {len(clients)} clients." ) elif tab == "Update Client": st.info( "Update Client functionality will be added in Part 3B." ) elif tab == "Delete Client": st.info( "Delete Client functionality will be added in Part 3B." ) elif tab == "Update Client": st.subheader("✏️ Update Client Information") clients = db.get_clients() if clients.empty: st.info("No clients available.") else: client_ids = clients["client_id"].tolist() selected_id = st.selectbox( "Select Client ID", client_ids ) client = clients[ clients["client_id"] == selected_id ].iloc[0] with st.container(border=True): col1, col2 = st.columns(2) with col1: name = st.text_input( "Client Name", value=client["name"] ) age = st.number_input( "Age", min_value=1, max_value=120, value=int(client["age"]) ) gender = st.selectbox( "Gender", ["Male", "Female", "Other"], index=[ "Male", "Female", "Other" ].index(client["gender"]) ) with col2: addiction = st.text_input( "Addiction", value=client["addiction"] ) admission = st.text_input( "Admission Date", value=client["admission_date"] ) sessions = st.number_input( "Total Sessions", min_value=1, value=int(client["total_sessions"]) ) completed = st.number_input( "Completed Sessions", min_value=0, value=int(client["completed_sessions"]) ) if ui.button( text="Update Client", key="update_client" ): db.cursor.execute(""" UPDATE clients SET name=?, age=?, gender=?, addiction=?, admission_date=?, total_sessions=?, completed_sessions=? WHERE client_id=? """, ( name, age, gender, addiction, admission, sessions, completed, selected_id )) db.conn.commit() st.success("✅ Client updated successfully.") st.rerun() elif tab == "Delete Client": st.subheader("🗑 Delete Client") clients = db.get_clients() if clients.empty: st.info("No clients available.") else: options = { f"{row.client_id} - {row.name}": row.client_id for _, row in clients.iterrows() } selected = st.selectbox( "Select Client", list(options.keys()) ) client_id = options[selected] st.warning( "Deleting a client also removes all appointments associated with that client." ) confirm = st.checkbox( "I understand and want to continue." ) if confirm: if ui.button( text="Delete Client", key="delete_client" ): db.delete_client(client_id) st.success("✅ Client deleted successfully.") st.rerun() sort_by = st.selectbox( "Sort By", [ "Client ID", "Name", "Age", "Completed Sessions", "Total Sessions" ] ) sort_columns = { "Client ID": "client_id", "Name": "name", "Age": "age", "Completed Sessions": "completed_sessions", "Total Sessions": "total_sessions" } filtered = filtered.sort_values( by=sort_columns[sort_by] ) st.divider() metric1, metric2, metric3, metric4 = st.columns(4) metric1.metric( "Total Clients", len(filtered) ) metric2.metric( "Average Age", round(filtered["age"].mean(), 1) if len(filtered) else 0 ) metric3.metric( "Average Sessions", round(filtered["total_sessions"].mean(), 1) if len(filtered) else 0 ) metric4.metric( "Completed Sessions", int(filtered["completed_sessions"].sum()) if len(filtered) else 0 ) st.divider() st.dataframe( filtered, use_container_width=True, hide_index=True ) csv = filtered.to_csv(index=False).encode("utf-8") st.download_button( label="📥 Download Client List (CSV)", data=csv, file_name="clients.csv", mime="text/csv" ) st.caption( f"Showing {len(filtered)} client(s)." ) 
    st.divider() if len(filtered): st.subheader("Client Summary") summary = filtered.copy() summary["Progress (%)"] = ( summary["completed_sessions"] / summary["total_sessions"] * 100 ).round(1) st.dataframe( summary[ [ "client_id", "name", "addiction", "completed_sessions", "total_sessions", "Progress (%)" ] ], use_container_width=True, hide_index=True ) else: st.info("No matching clients found.")

import streamlit as st 
import streamlit_shadcn_ui as ui 
db = Database() 
st.set_page_config( page_title="Therapists", page_icon="🩺", layout="wide" ) 
st.title("🩺 Therapist Management")
tab = ui.tabs( options=[ "Add Therapist", "View Therapists", "Update Therapist", "Delete Therapist" ], default_value="Add Therapist", key="therapist_tabs" ) if tab == "Add Therapist": st.subheader("➕ Register Therapist") with st.container(border=True): name = st.text_input("Therapist Name") specialization = st.text_input( "Specialization" ) phone = st.text_input( "Phone Number" ) if ui.button( text="Add Therapist", key="add_therapist" ): if not name.strip(): st.error("Therapist name is required.") elif not specialization.strip(): st.error("Specialization is required.") else: db.add_therapist( name, specialization, phone ) st.success( "✅ Therapist registered successfully." ) st.rerun() elif tab == "View Therapists": st.subheader("📋 Therapist Directory") therapists = db.get_therapists() if therapists.empty: st.info("No therapists registered.") else: search = st.text_input( "🔍 Search Therapist" ) if search: therapists = therapists[ therapists["name"] .str.contains( search, case=False ) ] st.metric( "Total Therapists", len(therapists) ) st.dataframe( therapists, use_container_width=True, hide_index=True ) csv = therapists.to_csv( index=False ).encode("utf-8") st.download_button( "📥 Download Therapist List", csv, "therapists.csv", "text/csv" ) elif tab == "Update Therapist": st.subheader("✏️ Update Therapist") therapists = db.get_therapists() if therapists.empty: st.info("No therapists available.") else: ids = therapists[ "therapist_id" ].tolist() therapist_id = st.selectbox( "Select Therapist", ids ) therapist = therapists[ therapists["therapist_id"] == therapist_id ].iloc[0] name = st.text_input( "Name", therapist["name"] ) specialization = st.text_input( "Specialization", therapist["specialization"] ) phone = st.text_input( "Phone", therapist["phone"] ) if ui.button( text="Update", key="update_therapist" ): db.cursor.execute(""" UPDATE therapists SET name=?, specialization=?, phone=? WHERE therapist_id=? """, ( name, specialization, phone, therapist_id )) db.conn.commit() st.success( "Therapist updated successfully." ) st.rerun() elif tab == "Delete Therapist": st.subheader("🗑 Delete Therapist") therapists = db.get_therapists() if therapists.empty: st.info("No therapists available.") else: options = { f"{row.therapist_id} - {row.name}": row.therapist_id for _, row in therapists.iterrows() } selected = st.selectbox( "Select Therapist", list(options.keys()) ) therapist_id = options[selected] st.warning( "Deleting a therapist will remove future therapist assignments." ) confirm = st.checkbox( "Confirm deletion" ) if confirm: if ui.button( text="Delete Therapist", key="delete_therapist" ): db.cursor.execute( """ DELETE FROM appointments WHERE therapist_id=? """, (therapist_id,) ) db.cursor.execute( """ DELETE FROM therapists WHERE therapist_id=? """, (therapist_id,) ) db.conn.commit() st.success( "Therapist deleted successfully." ) st.rerun()

import streamlit as st 
import streamlit_shadcn_ui as ui 
db = Database() 
st.set_page_config( page_title="Appointments", page_icon="📅", layout="wide" ) 
st.title("📅 Therapy Appointment Management") 
tab = ui.tabs( options=[ "Book Appointment", "View Appointments", "Cancel Appointment" ], default_value="Book Appointment", key="appointment_tabs" ) if tab == "Book Appointment":
st.subheader("➕ Book Therapy Appointment") 
clients = db.get_clients()
therapists = db.get_therapists() 
if clients.empty: st.warning("Please register a client first.") 
elif therapists.empty: st.warning("Please register a therapist first.") 
else: client_options = { f"{row.client_id} - {row.name}": row.client_id for _, row in clients.iterrows() }
therapist_options = { f"{row.therapist_id} - {row.name}": row.therapist_id for _, row in therapists.iterrows() } 
with st.container(border=True): client = st.selectbox( "Client", list(client_options.keys()) ) 
therapist = st.selectbox( "Therapist", list(therapist_options.keys()) ) 
visit_date = st.date_input( "Visit Date" ) 
visit_time = st.time_input( "Visit Time" ) if ui.button( text="Book Appointment", key="book_visit" ): db.book_visit( client_options[client], therapist_options[therapist], str(visit_date), str(visit_time) ) st.success( "✅ Appointment booked successfully." ) st.rerun() elif tab == "View Appointments": st.subheader("📋 Therapy Appointments") appointments = db.get_appointments() if appointments.empty: st.info("No appointments found.") else: search = st.text_input( "🔍 Search by Client ID" ) status = st.selectbox( "Status", [ "All", "Booked", "Cancelled" ] ) filtered = appointments.copy() if search: filtered = filtered[ filtered["client_id"] .astype(str) .str.contains(search) ] if status != "All": filtered = filtered[ filtered["status"] == status ] c1, c2, c3 = st.columns(3) c1.metric( "Appointments", len(filtered) ) c2.metric( "Booked", len( filtered[ filtered["status"] == "Booked" ] ) ) c3.metric( "Cancelled", len( filtered[ filtered["status"] == "Cancelled" ] ) ) st.dataframe( filtered, use_container_width=True, hide_index=True ) csv = filtered.to_csv( index=False ).encode("utf-8") st.download_button( "📥 Download Appointments", csv, "appointments.csv", "text/csv" ) elif tab == "Cancel Appointment": st.subheader("❌ Cancel Therapy Appointment") appointments = db.get_appointments() booked = appointments[ appointments["status"] == "Booked" ] if booked.empty: st.info("No active appointments.") else: options = { f"Appointment {row.appointment_id} | Client {row.client_id} | {row.visit_date}": row.appointment_id for _, row in booked.iterrows() } selected = st.selectbox( "Select Appointment", list(options.keys()) ) appointment_id = options[selected] st.warning( "This appointment will be marked as Cancelled." ) confirm = st.checkbox( "Confirm cancellation" ) if confirm: if ui.button( text="Cancel Appointment", key="cancel_visit" ): db.cancel_visit( appointment_id ) st.success( "Appointment cancelled successfully." ) st.rerun()

import streamlit as st 
import streamlit_shadcn_ui as ui 

db = Database() 
st.set_page_config( page_title="Treatment Progress", page_icon="📈", layout="wide" )
st.title("📈 Treatment Progress")
tab = ui.tabs( options=[ "Update Progress", "View Progress" ], default_value="Update Progress", key="progress_tabs" ) if tab == "Update Progress" :clients = db.get_clients() if clients.empty: st.info("No registered clients.") else: options = { f"{row.client_id} - {row.name}": row.client_id for _, row in clients.iterrows() } selected = st.selectbox( "Select Client", list(options.keys()) ) client_id = options[selected] client = clients[ clients["client_id"] == client_id ].iloc[0] st.write(f"**Client:** {client['name']}") st.write(f"**Total Sessions:** {client['total_sessions']}") completed = st.number_input( "Completed Sessions", min_value=0, max_value=int(client["total_sessions"]), value=int(client["completed_sessions"]) ) if ui.button( text="Update Progress", key="update_progress" ): db.update_progress( client_id, completed ) st.success( "Treatment progress updated successfully." ) st.rerun() elif tab == "View Progress": clients = db.get_clients() if clients.empty: st.info("No registered clients.") else: options = { f"{row.client_id} - {row.name}": row.client_id for _, row in clients.iterrows() } selected = st.selectbox( "Select Client", list(options.keys()) ) client_id = options[selected] result = db.calculate_progress(client_id) if result: col1, col2, col3 = st.columns(3) col1.metric( "Completed", result["completed"] ) col2.metric( "Total Sessions", result["total"] ) col3.metric( "Progress", f"{result['progress']:.1f}%" ) st.progress( result["progress"] / 100 ) if result["progress"] == 100: st.success( "🎉 Treatment Completed" ) elif result["progress"] >= 75: st.success( "Excellent Progress" ) elif result["progress"] >= 50: st.info( "Treatment progressing well." ) elif result["progress"] >= 25: st.warning( "Treatment still in progress." ) else: st.error( "Treatment has just begun." ) report = f""" Treatment Progress Report Client: {result['name']} Completed Sessions: {result['completed']} Total Sessions: {result['total']} Progress: {result['progress']:.2f}% """ st.download_button( "📄 Download Progress Report", report, "progress_report.txt", "text/plain" ) st.divider() st.subheader("Overall Client Progress") clients = db.get_clients() if not clients.empty: summary = clients.copy() summary["Progress (%)"] = ( summary["completed_sessions"] / summary["total_sessions"] * 100 ).round(1) st.dataframe( summary[ [ "client_id", "name", "completed_sessions", "total_sessions", "Progress (%)" ] ], use_container_width=True, hide_index=True ) else: st.info("No client progress available.")

import streamlit as st
import streamlit_shadcn_ui as ui

def metric_cards(clients, therapists, appointments):

    c1, c2, c3 = st.columns(3)

    with c1:
        ui.metric_card(
            title="Clients",
            content=str(clients),
            description="Registered Clients",
            key="clients"
        )

    with c2:
        ui.metric_card(
            title="Therapists",
            content=str(therapists),
            description="Available Therapists",
            key="therapists"
        )

    with c3:
        ui.metric_card(
            title="Appointments",
            content=str(appointments),
            description="Booked Visits",
            key="appointments"
        )
#Sidebar Component
import streamlit as st

def sidebar():

    st.sidebar.image(
        "assets/logo.png",
        use_container_width=True
    )

    st.sidebar.title(
        "Rehabilitation System"
    )

    st.sidebar.success(
        "Manage Clients, Therapists and Appointments"
    )
#Custom CSS



with open("assets/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )
#Dashboard Charts
import plotly.express as px

clients = db.get_clients()

if not clients.empty:

    fig = px.pie(
        clients,
        names="gender",
        title="Client Gender Distribution"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )
#Progress Chart
fig = px.bar(
    clients,
    x="name",
    y="completed_sessions",
    title="Completed Therapy Sessions"
)

st.plotly_chart(
    fig,
    use_container_width=True
)
#Dashboard Tables
#Recent Clients
st.subheader("Recently Registered Clients")

st.dataframe(
    clients.tail(5),
    use_container_width=True
)
#Upcoming Appointments
appointments = db.get_appointments()

st.subheader("Upcoming Appointments")

st.dataframe(
    appointments.head(5),
    use_container_width=True
)
#Footer
st.divider()

st.caption(
    "Rehabilitation Management System © 2026"
)

import streamlit as st 
import streamlit_shadcn_ui as ui 
import plotly.express as px 
db = Database() 
st.set_page_config( page_title="Dashboard", page_icon="🏥", layout="wide" ) 
st.title("🏥 Rehabilitation Management Dashboard") 
clients = db.get_clients() 
therapists = db.get_therapists() 
appointments = db.get_appointments() 
total_clients = len(clients) 
total_therapists = len(therapists) 
total_appointments = len(appointments) 
active = 0 
cancelled = 0 if not appointments.empty: active = len( appointments[ appointments["status"] == "Booked" ] ) cancelled = len( appointments[ appointments["status"] == "Cancelled" ] ) col1, col2, col3, col4 = st.columns(4) with col1: ui.metric_card( title="Clients", content=str(total_clients), description="Registered Clients", key="clients" ) with col2: ui.metric_card( title="Therapists", content=str(total_therapists), description="Available Therapists", key="therapists" ) with col3: ui.metric_card( title="Appointments", content=str(total_appointments), description="Total Visits", key="appointments" ) with col4: ui.metric_card( title="Cancelled", content=str(cancelled), description="Cancelled Visits", key="cancelled" ) st.divider() left, right = st.columns(2) with left: st.subheader("Client Gender Distribution") if not clients.empty: fig = px.pie( clients, names="gender", hole=0.45 ) st.plotly_chart( fig, use_container_width=True ) else: st.info("No client data available.") with right: st.subheader("Addiction Categories") if not clients.empty: addiction = ( clients["addiction"] .value_counts() .reset_index() ) addiction.columns = [ "Addiction", "Clients" ] fig = px.bar( addiction, x="Addiction", y="Clients" ) st.plotly_chart( fig, use_container_width=True ) else: st.info("No addiction data available.") st.divider() st.subheader("Treatment Progress") if not clients.empty: progress = clients.copy() progress["Progress"] = ( progress["completed_sessions"] / progress["total_sessions"] * 100 ).round(1) fig = px.bar( progress, x="name", y="Progress", color="Progress", text="Progress" ) st.plotly_chart( fig, use_container_width=True ) else: st.info("No progress available.") st.divider() left, right = st.columns(2) with left: st.subheader("Recent Clients") if not clients.empty: st.dataframe( clients.tail(5), use_container_width=True, hide_index=True ) else: st.info("No clients registered.") with right: st.subheader("Recent Appointments") if not appointments.empty: st.dataframe( appointments.tail(5), use_container_width=True, hide_index=True ) else: st.info("No appointments available.") st.divider() status1, status2, status3 = st.columns(3) status1.success( f"Registered Clients: {total_clients}" ) status2.success( f"Booked Visits: {active}" ) status3.success( f"Available Therapists: {total_therapists}" ) st.divider() st.caption( "Rehabilitation Management System | Version 1.0 | Built with Streamlit & streamlit-shadcn-ui" )