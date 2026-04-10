import streamlit as st
import requests

st.title("Leave Management System")

BASE_URL = "http://127.0.0.1:8000"

# 👇 Employee Input
employee_id = int(st.number_input("Employee ID", min_value=1, step=1))
leave_type = st.text_input("Leave Type")
reason = st.text_input("Reason")

start_date = st.date_input("Start Date")
end_date = st.date_input("End Date")

# Apply Leave
if st.button("Apply Leave"):
    data = {
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": str(start_date),
        "end_date": str(end_date),
        "reason": reason
    }

    try:
        res = requests.post(f"{BASE_URL}/leave/", json=data)

        if res.status_code == 200:
            st.success("Leave Applied Successfully ✅")
            st.write(res.json())
        else:
            st.error(f"Error: {res.status_code}")
            st.write(res.text)

    except Exception as e:
        st.error(f"Connection Error: {e}")

# Show Leaves
if st.button("Show All Leaves"):
    try:
        res = requests.get(f"{BASE_URL}/leave/")

        if res.status_code == 200:
            st.write(res.json())
        else:
            st.error(f"Error: {res.status_code}")
            st.write(res.text)

    except Exception as e:
        st.error(f"Connection Error: {e}")

# Approve / Reject Section
st.subheader("Approve / Reject Leave")

leave_id = int(st.number_input("Leave ID", min_value=1, step=1))

if st.button("Approve Leave"):
    try:
        res = requests.put(f"{BASE_URL}/leave/approve/{leave_id}")

        if res.status_code == 200:
            st.success("Leave Approved ✅")
            st.write(res.json())
        else:
            st.error(f"Error: {res.status_code}")
            st.write(res.text)

    except Exception as e:
        st.error(f"Connection Error: {e}")

if st.button("Reject Leave"):
    try:
        res = requests.put(f"{BASE_URL}/leave/reject/{leave_id}")

        if res.status_code == 200:
            st.success("Leave Rejected ❌")
            st.write(res.json())
        else:
            st.error(f"Error: {res.status_code}")
            st.write(res.text)

    except Exception as e:
        st.error(f"Connection Error: {e}")