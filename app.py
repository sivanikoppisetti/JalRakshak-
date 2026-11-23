

import streamlit as st

st.set_page_config(
    page_title="JalRakshak",
    page_icon="💧",
    layout="wide"
)

# Initialize complaint storage
if "complaints" not in st.session_state:
    st.session_state.complaints = []

st.title("💧 JalRakshak")
st.subheader("Smart Community Water Management System")

st.write(
    "A centralized platform to report, monitor and manage "
    "water-related problems across our college campus."
)

st.divider()

# Dashboard statistics
complaints = st.session_state.complaints

total = len(complaints)
pending = sum(c["status"] == "Pending" for c in complaints)
progress = sum(c["status"] == "In Progress" for c in complaints)
resolved = sum(c["status"] == "Resolved" for c in complaints)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Complaints", total)
col2.metric("Pending", pending)
col3.metric("In Progress", progress)
col4.metric("Resolved", resolved)

st.divider()

# Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Report Water Issue",
        "My Complaints",
        "Admin Dashboard"
    ]
)

# HOME
if menu == "Home":

    st.header("Welcome to JalRakshak 🌱")
    st.write("Together, let's protect every drop of water!")

    st.info(
        "Report water-related problems and help "
        "maintain a water-conscious campus."
    )

    st.subheader("Our Main Features")

    col1, col2, col3 = st.columns(3)

    col1.write("💧 **Report Issues**")
    col1.caption("Submit water-related complaints.")

    col2.write("📋 **Track Complaints**")
    col2.caption("Monitor complaint progress.")

    col3.write("📊 **Admin Management**")
    col3.caption("Manage and resolve reported issues.")

# REPORT WATER ISSUE
elif menu == "Report Water Issue":

    st.header("Report a Water Issue")

    with st.form("complaint_form"):

        name = st.text_input("Your Name")

        category = st.selectbox(
            "Issue Category",
            [
                "Leaking Tap",
                "Overflowing Tank",
                "Damaged Pipeline",
                "Drinking Water Problem",
                "Other"
            ]
        )

        location = st.selectbox(
            "Campus Location",
            [
                "Academic Block",
                "Library",
                "Hostel",
                "Canteen",
                "Laboratory",
                "Other"
            ]
        )

        description = st.text_area("Describe the Problem")

        submitted = st.form_submit_button("Submit Complaint")

        if submitted:

            if name.strip() and description.strip():

                complaint_id = (
                    f"JR{len(st.session_state.complaints) + 1:03d}"
                )

                st.session_state.complaints.append({
                    "id": complaint_id,
                    "name": name,
                    "category": category,
                    "location": location,
                    "description": description,
                    "status": "Pending"
                })

                st.success(
                    f"Complaint submitted successfully! "
                    f"Your ID is {complaint_id}"
                )

            else:
                st.warning("Please enter your name and description.")

# MY COMPLAINTS
elif menu == "My Complaints":

    st.header("Track Your Complaints")

    if complaints:

        for complaint in complaints:

            with st.expander(complaint["id"]):

                st.write("**Name:**", complaint["name"])
                st.write("**Category:**", complaint["category"])
                st.write("**Location:**", complaint["location"])
                st.write("**Description:**", complaint["description"])
                st.write("**Status:**", complaint["status"])

    else:
        st.info("No complaints submitted yet.")

# ADMIN DASHBOARD
elif menu == "Admin Dashboard":

    st.header("🔐 Admin Dashboard")

    st.info("Enter the demo admin passcode to manage complaints.")

    password = st.text_input(
        "Admin Passcode",
        type="password"
    )

    if password == "JalRakshak@2026":

        st.success("Admin access granted!")

        st.subheader("Manage Water Complaints")

        if complaints:

            for complaint in complaints:

                with st.expander(
                    f"{complaint['id']} - {complaint['category']}"
                ):

                    st.write("**Name:**", complaint["name"])
                    st.write("**Location:**", complaint["location"])
                    st.write("**Description:**", complaint["description"])
                    st.write("**Current Status:**", complaint["status"])

                    new_status = st.selectbox(
                        "Update Complaint Status",
                        ["Pending", "In Progress", "Resolved"],
                        index=[
                            "Pending",
                            "In Progress",
                            "Resolved"
                        ].index(complaint["status"]),
                        key=f"status_{complaint['id']}"
                    )

                    if st.button(
                        "Update Status",
                        key=f"update_{complaint['id']}"
                    ):

                        complaint["status"] = new_status

                        st.success(
                            f"{complaint['id']} updated to {new_status}"
                        )

                        st.rerun()

        else:
            st.info("No complaints available to manage.")

    elif password:
        st.error("Incorrect admin passcode.")

st.divider()

st.caption(
    "JalRakshak | Smart Community Water Management System"
)
