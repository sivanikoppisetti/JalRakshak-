
import streamlit as st

st.set_page_config(
    page_title="JalRakshak",
    page_icon="💧",
    layout="wide"
)

# Store complaints during the current session
if "complaints" not in st.session_state:
    st.session_state.complaints = []

st.title("💧 JalRakshak")
st.subheader("Smart Community Water Management System")

st.write(
    "A centralized platform to report, monitor and manage "
    "water-related problems across our college campus."
)

st.divider()

# Dashboard summary
col1, col2, col3 = st.columns(3)

total = len(st.session_state.complaints)
pending = sum(
    c["status"] == "Pending"
    for c in st.session_state.complaints
)
resolved = sum(
    c["status"] == "Resolved"
    for c in st.session_state.complaints
)

col1.metric("Total Complaints", total)
col2.metric("Pending Complaints", pending)
col3.metric("Resolved Complaints", resolved)

st.divider()

# Navigation
menu = st.sidebar.selectbox(
    "Navigation",
    ["Home", "Report Water Issue", "My Complaints"]
)

if menu == "Home":
    st.header("Welcome to JalRakshak 🌱")
    st.write("Together, let's protect every drop of water!")
    st.info(
        "Use the sidebar to report a water issue "
        "or track your submitted complaints."
    )

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
            if name and description:
                complaint_id = f"JR{len(st.session_state.complaints) + 1:03d}"

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

elif menu == "My Complaints":
    st.header("Track Your Complaints")

    if st.session_state.complaints:
        for complaint in st.session_state.complaints:
            with st.expander(complaint["id"]):
                st.write("**Name:**", complaint["name"])
                st.write("**Category:**", complaint["category"])
                st.write("**Location:**", complaint["location"])
                st.write("**Description:**", complaint["description"])
                st.write("**Status:**", complaint["status"])
    else:
        st.info("No complaints submitted yet.")

st.divider()
st.caption("JalRakshak | Smart Water Management for a Better Campus")
