


import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
from uuid import uuid4
import hmac

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="JalRakshak",
    page_icon="💧",
    layout="wide"
)

# --------------------------------
# SUPABASE CONNECTION
# --------------------------------

@st.cache_resource
def connect_supabase():
    url = st.secrets["supabase"]["url"]
    key = st.secrets["supabase"]["secret_key"]

    return create_client(url, key)


try:
    supabase = connect_supabase()
except Exception as e:
    st.error("Could not connect to Supabase.")
    st.error(str(e))
    st.stop()


# --------------------------------
# DATABASE FUNCTIONS
# --------------------------------

def get_complaints():
    response = (
        supabase.table("complaints")
        .select("*")
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


def generate_complaint_id():
    date_part = datetime.now(timezone.utc).strftime("%Y%m%d")
    random_part = uuid4().hex[:6].upper()

    return f"JR-{date_part}-{random_part}"


def submit_complaint(name, category, location, description):

    complaint_id = generate_complaint_id()

    complaint = {
        "id": complaint_id,
        "name": name,
        "category": category,
        "location": location,
        "description": description,
        "status": "Pending"
    }

    response = (
        supabase.table("complaints")
        .insert(complaint)
        .execute()
    )

    return complaint_id


def update_complaint_status(complaint_id, new_status):

    response = (
        supabase.table("complaints")
        .update({"status": new_status})
        .eq("id", complaint_id)
        .execute()
    )

    return response.data


# --------------------------------
# APPLICATION TITLE
# --------------------------------

st.title("💧 JalRakshak")

st.subheader("Smart Community Water Management System")

st.write(
    "A centralized platform to report, monitor and manage "
    "water-related problems across our college campus."
)

st.divider()


# --------------------------------
# DASHBOARD STATISTICS
# --------------------------------

try:
    complaints = get_complaints()
except Exception as e:
    st.error("Unable to retrieve complaints from the database.")
    st.error(str(e))
    st.stop()


total = len(complaints)

pending = sum(
    c["status"] == "Pending" for c in complaints
)

progress = sum(
    c["status"] == "In Progress" for c in complaints
)

resolved = sum(
    c["status"] == "Resolved" for c in complaints
)

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Complaints", total)
col2.metric("Pending", pending)
col3.metric("In Progress", progress)
col4.metric("Resolved", resolved)

st.divider()


# --------------------------------
# NAVIGATION
# --------------------------------

menu = st.sidebar.selectbox(
    "Navigation",
    [
        "Home",
        "Report Water Issue",
        "My Complaints",
        "Admin Dashboard"
    ]
)


# --------------------------------
# HOME
# --------------------------------

if menu == "Home":

    st.header("Welcome to JalRakshak 🌱")

    st.write(
        "Together, let's protect every drop of water!"
    )

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


# --------------------------------
# REPORT WATER ISSUE
# --------------------------------

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

        description = st.text_area(
            "Describe the Problem"
        )

        submitted = st.form_submit_button(
            "Submit Complaint"
        )

        if submitted:

            if name.strip() and description.strip():

                try:
                    complaint_id = submit_complaint(
                        name.strip(),
                        category,
                        location,
                        description.strip()
                    )

                    st.success(
                        "Complaint submitted successfully!"
                    )

                    st.success(
                        f"Your Complaint ID is: {complaint_id}"
                    )

                    st.info(
                        "Please save your Complaint ID "
                        "to track your complaint later."
                    )

                except Exception as e:
                    st.error("Complaint submission failed.")
                    st.error(str(e))

            else:
                st.warning(
                    "Please enter your name and description."
                )


# --------------------------------
# MY COMPLAINTS
# --------------------------------

elif menu == "My Complaints":

    st.header("Track Your Complaints")

    complaint_id = st.text_input(
        "Enter Complaint ID"
    )

    student_name = st.text_input(
        "Enter Your Name"
    )

    if st.button("Track Complaint"):

        if complaint_id.strip() and student_name.strip():

            try:
                response = (
                    supabase.table("complaints")
                    .select("*")
                    .eq("id", complaint_id.strip().upper())
                    .limit(1)
                    .execute()
                )

                if response.data:

                    complaint = response.data[0]

                    if complaint["name"].casefold() == student_name.strip().casefold():

                        st.success("Complaint Found!")

                        st.write(
                            "**Complaint ID:**",
                            complaint["id"]
                        )

                        st.write(
                            "**Name:**",
                            complaint["name"]
                        )

                        st.write(
                            "**Category:**",
                            complaint["category"]
                        )

                        st.write(
                            "**Location:**",
                            complaint["location"]
                        )

                        st.write(
                            "**Description:**",
                            complaint["description"]
                        )

                        st.write(
                            "**Status:**",
                            complaint["status"]
                        )

                        st.write(
                            "**Created At:**",
                            complaint["created_at"]
                        )

                    else:
                        st.error(
                            "Complaint ID or name does not match."
                        )

                else:
                    st.warning(
                        "No complaint found with this ID."
                    )

            except Exception as e:
                st.error("Unable to track complaint.")
                st.error(str(e))

        else:
            st.warning(
                "Please enter both Complaint ID and Name."
            )


# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

elif menu == "Admin Dashboard":

    st.header("🔐 Admin Dashboard")

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:

        st.info(
            "Enter the admin passcode to manage complaints."
        )

        password = st.text_input(
            "Admin Passcode",
            type="password"
        )

        if st.button("Login"):

            correct_password = st.secrets["auth"]["admin_passcode"]

            if hmac.compare_digest(
                password,
                correct_password
            ):

                st.session_state.admin_authenticated = True

                st.success("Admin access granted!")

                st.rerun()

            else:
                st.error("Incorrect admin passcode.")

    else:

        st.success("Admin access granted!")

        if st.button("Logout"):

            st.session_state.admin_authenticated = False

            st.rerun()

        st.subheader("Manage Water Complaints")

        try:
            admin_complaints = get_complaints()

            if admin_complaints:

                for complaint in admin_complaints:

                    with st.expander(
                        f"{complaint['id']} - {complaint['category']}"
                    ):

                        st.write(
                            "**Name:**",
                            complaint["name"]
                        )

                        st.write(
                            "**Location:**",
                            complaint["location"]
                        )

                        st.write(
                            "**Description:**",
                            complaint["description"]
                        )

                        st.write(
                            "**Current Status:**",
                            complaint["status"]
                        )

                        statuses = [
                            "Pending",
                            "In Progress",
                            "Resolved"
                        ]

                        new_status = st.selectbox(
                            "Update Complaint Status",
                            statuses,
                            index=statuses.index(
                                complaint["status"]
                            ),
                            key=f"status_{complaint['id']}"
                        )

                        if st.button(
                            "Update Status",
                            key=f"update_{complaint['id']}"
                        ):

                            try:
                                update_complaint_status(
                                    complaint["id"],
                                    new_status
                                )

                                st.success(
                                    f"{complaint['id']} updated to {new_status}"
                                )

                                st.rerun()

                            except Exception as e:
                                st.error(
                                    "Status update failed."
                                )
                                st.error(str(e))

            else:
                st.info(
                    "No complaints available to manage."
                )

        except Exception as e:
            st.error(
                "Unable to load admin complaints."
            )
            st.error(str(e))


# --------------------------------
# FOOTER
# --------------------------------

st.divider()

st.caption(
    "JalRakshak | Smart Community Water Management System"
)
