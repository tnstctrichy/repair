import streamlit as st
import pandas as pd
import sqlite3

# Create or connect to the database
conn = sqlite3.connect('repair_management.db')
c = conn.cursor()

# Create a table to store repair requests if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS repair_requests (
        id INTEGER PRIMARY KEY,
        received_date DATE,
        received_dsrr_number TEXT,
        depot TEXT,
        item TEXT,
        make TEXT,
        serial_number TEXT,
        problem_description TEXT,
        solved_description TEXT,
        send_date DATE,
        send_dsrr_number TEXT
    )
''')
conn.commit()

# Function to add a repair request
def add_repair_request(data):
    c.execute('''
        INSERT INTO repair_requests (received_date, received_dsrr_number, depot, item, make, serial_number, problem_description, solved_description, send_date, send_dsrr_number)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', data)
    conn.commit()

# Function to update a repair request
def update_repair_request(data, request_id):
    c.execute('''
        UPDATE repair_requests
        SET received_date=?, received_dsrr_number=?, depot=?, item=?, make=?, serial_number=?, problem_description=?, solved_description=?, send_date=?, send_dsrr_number=?
        WHERE id=?
    ''', (*data, request_id))
    conn.commit()

# Function to delete a repair request
def delete_repair_request(request_id):
    c.execute('DELETE FROM repair_requests WHERE id=?', (request_id,))
    conn.commit()

# Function to fetch repair requests
def fetch_repair_requests():
    c.execute('SELECT * FROM repair_requests')
    data = c.fetchall()
    return data

# Streamlit UI
st.set_page_config(layout="wide", page_title="Repair Management System", page_icon="🔧")
st.title("Repair Management System")

# Sidebar for navigation
page = st.sidebar.selectbox("Select an option", ["Add Repair", "Update Repair", "Delete Repair", "View Repair", "Exit"])

if page == "Add Repair":
    st.header("Add Repair Request")

    received_date = st.date_input("Received Date")
    received_dsrr_number = st.text_input("Received DSRR Number")
    depot = st.text_input("Depot")
    item = st.text_input("Item")
    make = st.text_input("Make")
    serial_number = st.text_input("Serial Number")
    problem_description = st.text_area("Problem Description")
    solved_description = st.text_area("Solved Repair Description")
    send_date = st.date_input("Send Date")
    send_dsrr_number = st.text_input("Send DSRR Number")

    if st.button("Submit"):
        if received_date and received_dsrr_number and depot and item and make and serial_number:
            data = (received_date, received_dsrr_number, depot, item, make, serial_number, problem_description, solved_description, send_date, send_dsrr_number)
            add_repair_request(data)
            st.success("Repair request submitted successfully!")
        else:
            st.error("Please fill in all mandatory fields.")

elif page == "Update Repair":
    st.header("Update Repair Request")

    repair_requests = fetch_repair_requests()
    request_ids = [str(request[0]) for request in repair_requests]
    selected_request_id = st.selectbox("Select a repair request to update", request_ids)

    index = request_ids.index(selected_request_id)
    selected_request = repair_requests[index]

    received_date = st.date_input("Received Date", pd.to_datetime(selected_request[1]))
    received_dsrr_number = st.text_input("Received DSRR Number", selected_request[2])
    depot = st.text_input("Depot", selected_request[3])
    item = st.text_input("Item", selected_request[4])
    make = st.text_input("Make", selected_request[5])
    serial_number = st.text_input("Serial Number", selected_request[6])
    problem_description = st.text_area("Problem Description", selected_request[7])
    solved_description = st.text_area("Solved Repair Description", selected_request[8])
    send_date = st.date_input("Send Date", pd.to_datetime(selected_request[9]))
    send_dsrr_number = st.text_input("Send DSRR Number", selected_request[10])

    if st.button("Update"):
        data = (received_date, received_dsrr_number, depot, item, make, serial_number, problem_description, solved_description, send_date, send_dsrr_number)
        update_repair_request(data, int(selected_request_id))
        st.success("Repair request updated successfully!")

elif page == "Delete Repair":
    st.header("Delete Repair Request")

    repair_requests = fetch_repair_requests()
    request_ids = [str(request[0]) for request in repair_requests]
    selected_request_id = st.selectbox("Select a repair request to delete", request_ids)

    selected_request = None
    for request in repair_requests:
        if request[0] == int(selected_request_id):
            selected_request = request
            break

    if selected_request:
        st.subheader("Details of Repair Request:")
        st.write(f"ID: {selected_request[0]}")
        st.write(f"Received Date: {selected_request[1]}")
        st.write(f"Depot: {selected_request[2]}")
        st.write(f"Received DSRR Number: {selected_request[3]}")
        st.write(f"Item: {selected_request[4]}")
        st.write(f"Make: {selected_request[5]}")
        st.write(f"Serial Number: {selected_request[6]}")
        st.write(f"Problem Description: {selected_request[7]}")
        st.write(f"Solved Repair Description: {selected_request[8]}")
        st.write(f"Send Date: {selected_request[9]}")
        st.write(f"Send DSRR Number: {selected_request[10]}")

        if st.button("Delete"):
            delete_repair_request(int(selected_request_id))
            st.success("Repair request deleted successfully!")
    else:
        st.error("Invalid request ID. Please select a valid repair request to delete.")


elif page == "View Repair":
    st.header("View Repair Requests")

    repair_requests = fetch_repair_requests()
    
    if not repair_requests:
        st.info("No repair requests found.")
    else:
        df = pd.DataFrame(repair_requests, columns=["ID", "Received Date", "Received DSRR Number", "Depot", "Item", "Make", "Serial Number", "Problem Description", "Solved Repair Description", "Send Date", "Send DSRR Number"])
        st.dataframe(df)

elif page == "Exit":
    conn.close()
    st.stop()
