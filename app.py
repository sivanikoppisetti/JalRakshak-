import streamlit as st
from supabase import create_client
from datetime import datetime, timezone
from uuid import uuid4
import hmac
import pandas as pd
from io import BytesIO

# --------------------------------
# PAGE CONFIGURATION
# --------------------------------

st.set_page_config(
    page_title="JalRakshak | Campus Water Management",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --------------------------------
# PROFESSIONAL THEME / CSS
# --------------------------------

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    .stApp {
        background: #f4f8fc;
        color: #172b4d;
    }

    [data-testid="stHeader"] {
        background: rgba(244, 248, 252, 0.92);
    }

    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #073b70 0%, #07558a 58%, #087e9b 100%);
        border-right: 1px solid rgba(255,255,255,0.12);
    }

    [data-testid="stSidebar"] * {
        color: #ffffff !important;
    }

     
    /* Sidebar supporting text */
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #dceeff !important;
    }

    /* SIDEBAR NAVIGATION BUTTONS */
    [data-testid="stSidebar"] div[data-testid="stButton"] {
        width: 100%;
    }

    [data-testid="stSidebar"] div[data-testid="stButton"] > button {
        width: 100% !important;
        min-height: 44px !important;
        display: flex !important;
        justify-content: flex-start !important;
        align-items: center !important;
        background: #ffffff !important;
        color: #173b61 !important;
        -webkit-text-fill-color: #173b61 !important;
        border: 1px solid #dce8f2 !important;
        border-radius: 10px !important;
        padding: 10px 13px !important;
        margin: 0 0 9px 0 !important;
        box-shadow: none !important;
        font-weight: 600 !important;
        text-align: left !important;
    }

    [data-testid="stSidebar"] div[data-testid="stButton"] > button p,
    [data-testid="stSidebar"] div[data-testid="stButton"] > button span {
        color: #173b61 !important;
        -webkit-text-fill-color: #173b61 !important;
    }

    [data-testid="stSidebar"] div[data-testid="stButton"] > button:hover {
        background: #e8f3fb !important;
        border-color: #8bbde0 !important;
        color: #173b61 !important;
    }

    [data-testid="stSidebar"] div[data-testid="stButton"] > button:focus {
        border-color: #69a9d5 !important;
        box-shadow: 0 0 0 2px rgba(105, 169, 213, 0.2) !important;
        color: #173b61 !important;
    }

    .brand-block {
        padding: 8px 4px 22px 4px;
    }

    .brand-icon {
        display: inline-flex;
        width: 48px;
        height: 48px;
        align-items: center;
        justify-content: center;
        background: rgba(255,255,255,0.16);
        border: 1px solid rgba(255,255,255,0.28);
        border-radius: 15px;
        font-size: 27px;
        margin-bottom: 10px;
    }

    .brand-name {
        color: #ffffff;
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -0.7px;
        margin: 0;
    }

    .brand-tagline {
        color: #d7edff;
        font-size: 11px;
        letter-spacing: 1.2px;
        text-transform: uppercase;
        margin-top: 3px;
    }

    .top-label {
        color: #0874a6;
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-bottom: 5px;
    }

    .main-title {
        color: #12345a;
        font-size: 31px;
        line-height: 1.2;
        font-weight: 800;
        letter-spacing: -1px;
        margin: 0 0 6px 0;
    }

    .sub-title {
        color: #63758b;
        font-size: 14px;
        margin-bottom: 22px;
    }

    .hero {
        background: linear-gradient(115deg, #073b70 0%, #0876a5 65%, #16a6b5 100%);
        padding: 27px 30px;
        border-radius: 18px;
        color: white;
        margin: 10px 0 22px 0;
        box-shadow: 0 10px 28px rgba(7, 74, 125, 0.15);
    }

    .hero h2 {
        color: white;
        font-size: 25px;
        font-weight: 800;
        margin: 0 0 8px 0;
    }

    .hero p {
        color: #e2f5ff;
        font-size: 14px;
        margin: 0;
    }

    .hero-tag {
        display: inline-block;
        padding: 6px 11px;
        border: 1px solid rgba(255,255,255,0.35);
        background: rgba(255,255,255,0.12);
        border-radius: 20px;
        color: white;
        font-size: 11px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .section-heading {
        color: #173b61;
        font-size: 19px;
        font-weight: 800;
        margin: 16px 0 12px 0;
    }

    .stat-card {
        background: #ffffff;
        border: 1px solid #e2ebf4;
        border-radius: 15px;
        padding: 17px 18px;
        min-height: 112px;
        box-shadow: 0 4px 14px rgba(26, 67, 105, 0.045);
    }

    .stat-label {
        color: #63758b;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 9px;
    }

    .stat-value {
        color: #12345a;
        font-size: 29px;
        font-weight: 800;
        line-height: 1;
    }

    .stat-icon {
        float: right;
        font-size: 22px;
    }

    .feature-card {
        background: #ffffff;
        border: 1px solid #e2ebf4;
        border-radius: 15px;
        padding: 19px;
        min-height: 145px;
        box-shadow: 0 4px 14px rgba(26, 67, 105, 0.04);
    }

    .feature-icon {
        font-size: 25px;
        margin-bottom: 9px;
    }

    .feature-title {
        color: #173b61;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .feature-text {
        color: #687b90;
        font-size: 12px;
        line-height: 1.6;
    }

    .info-strip {
        background: #e8f5fb;
        border: 1px solid #cde9f5;
        border-radius: 13px;
        padding: 15px 18px;
        color: #245675;
        font-size: 13px;
        margin: 14px 0;
    }

    .status-pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 800;
    }

    div.stButton > button,
    div.stFormSubmitButton > button {
        background: linear-gradient(90deg, #0868a4, #0788ae);
        color: white;
        border: 0;
        border-radius: 9px;
        padding: 9px 18px;
        font-weight: 700;
        min-height: 42px;
    }

    div.stButton > button:hover,
    div.stFormSubmitButton > button:hover {
        background: #064f82;
        color: white;
        border: 0;
    }

    div[data-testid="stForm"] {
        background: #ffffff;
        border: 1px solid #e1eaf3;
        padding: 22px;
        border-radius: 15px;
        box-shadow: 0 4px 14px rgba(26, 67, 105, 0.04);
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextArea"] textarea {
        border-radius: 9px;
    }

    div[data-testid="stSelectbox"] > div > div {
        border-radius: 9px;
    }

    hr {
        border-color: #e2ebf4;
    }

    .footer {
        text-align: center;
        color: #8292a5;
        font-size: 11px;
        padding: 20px 0 5px 0;
    }

    @media (max-width: 700px) {
        .main-title { font-size: 25px; }
        .hero { padding: 22px 20px; }
        .hero h2 { font-size: 21px; }
    }
    
      
    </style>
    """, unsafe_allow_html=True
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
    st.error("Could not connect to Supabase. Please check the app configuration.")
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
        "status": "Pending",
    }
    supabase.table("complaints").insert(complaint).execute()
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
# REUSABLE DISPLAY HELPERS
# --------------------------------

def page_heading(eyebrow, title, description):
    st.markdown(
        f"""
        <div class="top-label">{eyebrow}</div>
        <div class="main-title">{title}</div>
        <div class="sub-title">{description}</div>
        """,
        unsafe_allow_html=True,
    )


def statistic_card(column, label, value, icon):
    column.markdown(
        f"""
        <div class="stat-card">
            <div class="stat-icon">{icon}</div>
            <div class="stat-label">{label}</div>
            <div class="stat-value">{value}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def status_label(status):
    colors = {
        "Pending": ("#fff4d6", "#946200"),
        "In Progress": ("#e4f1ff", "#075da8"),
        "Resolved": ("#e1f7ec", "#137547"),
    }
    background, foreground = colors.get(status, ("#edf1f5", "#526274"))
    st.markdown(
        f'<span class="status-pill" style="background:{background};color:{foreground};">{status}</span>',
        unsafe_allow_html=True,
    )


# --------------------------------
# SIDEBAR BRANDING AND NAVIGATION
# --------------------------------

with st.sidebar:
    st.markdown(
        """
        <div class="brand-block">
            <div class="brand-icon">💧</div>
            <div class="brand-name">JalRakshak</div>
            <div class="brand-tagline">Smart Water Management</div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.caption("MAIN MENU")

    # Keep the selected page between Streamlit reruns.
    if "jr_current_page" not in st.session_state:
        st.session_state["jr_current_page"] = "🏠 Home"

    menu = st.session_state["jr_current_page"]

    if st.button(
        "🏠 Home",
        key="jr_nav_home",
        use_container_width=True,
        type="primary" if menu == "🏠 Home" else "secondary",
    ):
        st.session_state["jr_current_page"] = "🏠 Home"
        st.rerun()

    if st.button(
        "📝 Report Water Issue",
        key="jr_nav_report",
        use_container_width=True,
        type="primary" if menu == "📝 Report Water Issue" else "secondary",
    ):
        st.session_state["jr_current_page"] = "📝 Report Water Issue"
        st.rerun()

    if st.button(
        "🔎 My Complaints",
        key="jr_nav_tracking",
        use_container_width=True,
        type="primary" if menu == "🔎 My Complaints" else "secondary",
    ):
        st.session_state["jr_current_page"] = "🔎 My Complaints"
        st.rerun()

    if st.button(
        "🛡️ Admin Dashboard",
        key="jr_nav_admin",
        use_container_width=True,
        type="primary" if menu == "🛡️ Admin Dashboard" else "secondary",
    ):
        st.session_state["jr_current_page"] = "🛡️ Admin Dashboard"
        st.rerun()

    # Reports is visible only after a successful administrator login.
    if st.session_state.get("admin_authenticated", False):
        if st.button(
            "📊 Reports",
            key="jr_nav_reports",
            use_container_width=True,
            type="primary" if menu == "📊 Reports" else "secondary",
        ):
            st.session_state["jr_current_page"] = "📊 Reports"
            st.rerun()

    st.markdown("---")
    st.markdown(
        """
        <div style="font-size:12px;line-height:1.7;color:#e4f3ff;">
            <b>Every drop matters.</b><br>
            Help us identify water problems early and reduce water wastage across campus.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------
# LOAD DASHBOARD STATISTICS
# --------------------------------

try:
    complaints = get_complaints()
except Exception as e:
    st.error("Unable to retrieve complaints from the database.")
    st.error(str(e))
    st.stop()

total = len(complaints)
pending = sum(c["status"] == "Pending" for c in complaints)
progress = sum(c["status"] == "In Progress" for c in complaints)
resolved = sum(c["status"] == "Resolved" for c in complaints)


# --------------------------------
# SHARED TOP HEADER AND STATISTICS
# --------------------------------

st.markdown(
    """
    <div class="top-label">CAMPUS WATER CARE PORTAL</div>
    <div class="main-title">Water Issue Management</div>
    <div class="sub-title">Report, track and resolve water-related problems in one place.</div>
    """,
    unsafe_allow_html=True,
)


if menu in ["🏠 Home", "🛡️ Admin Dashboard"]:
    c1, c2, c3, c4 = st.columns(4)

    statistic_card(c1, "Total Complaints", total, "📋")
    statistic_card(c2, "Pending", pending, "⏳")
    statistic_card(c3, "In Progress", progress, "🔧")
    statistic_card(c4, "Resolved", resolved, "✅")

    st.write("")


# --------------------------------
# HOME
# --------------------------------

if menu == "🏠 Home":
    st.markdown(
        """
        <div class="hero">
            <div class="hero-tag">💧 SMART COMMUNITY INITIATIVE</div>
            <h2>Protect Every Drop. Improve Every Day.</h2>
            <p>Welcome to JalRakshak — a campus platform to report water issues,
            monitor complaints and support faster maintenance action.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="section-heading">What you can do</div>', unsafe_allow_html=True)
    f1, f2, f3 = st.columns(3)

    with f1:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">💧</div>
                <div class="feature-title">Report Water Issues</div>
                <div class="feature-text">Submit details of leaking taps, overflowing tanks,
                damaged pipelines and other water problems.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f2:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🔎</div>
                <div class="feature-title">Track Complaints</div>
                <div class="feature-text">Use your complaint ID and name to check the
                latest progress of a submitted issue.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with f3:
        st.markdown(
            """
            <div class="feature-card">
                <div class="feature-icon">🛠️</div>
                <div class="feature-title">Maintenance Management</div>
                <div class="feature-text">Authorized administrators can review complaints
                and update their resolution status.</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown(
        """
        <div class="info-strip">
            <b>🌱 Water conservation starts with awareness.</b>
            Reporting a small leak today can help prevent significant water wastage tomorrow.
        </div>
        """,
        unsafe_allow_html=True,
    )


# --------------------------------
# REPORT WATER ISSUE
# --------------------------------

elif menu == "📝 Report Water Issue":
    page_heading(
        "RAISE A REQUEST",
        "Report a Water Issue",
        "Share the problem details so the campus maintenance team can take action.",
    )

    with st.form("complaint_form"):
        name = st.text_input("Your Name", placeholder="Enter your full name")

        col1, col2 = st.columns(2)
        with col1:
            category = st.selectbox(
                "Issue Category",
                [
                    "Leaking Tap",
                    "Overflowing Tank",
                    "Damaged Pipeline",
                    "Drinking Water Problem",
                    "Other",
                ],
            )
        with col2:
            location = st.selectbox(
                "Campus Location",
                [
                    "Academic Block",
                    "Library",
                    "Hostel",
                    "Canteen",
                    "Laboratory",
                    "Other",
                ],
            )

        description = st.text_area(
            "Describe the Problem",
            placeholder="Explain what happened and where the issue can be found...",
            height=130,
        )

        submitted = st.form_submit_button("Submit Complaint", use_container_width=True)

        if submitted:
            if name.strip() and description.strip():
                try:
                    complaint_id = submit_complaint(
                        name.strip(),
                        category,
                        location,
                        description.strip(),
                    )
                    st.success("Complaint submitted successfully!")
                    st.markdown(f"**Your Complaint ID:** `{complaint_id}`")
                    st.info("Please save your Complaint ID to track your complaint later.")
                except Exception as e:
                    st.error("Complaint submission failed.")
                    st.error(str(e))
            else:
                st.warning("Please enter your name and problem description.")


# --------------------------------
# MY COMPLAINTS
# --------------------------------

elif menu == "🔎 My Complaints":
    page_heading(
        "COMPLAINT STATUS",
        "Track Your Complaint",
        "Enter the complaint ID and the name used during submission.",
    )

    with st.container(border=True):
        complaint_id = st.text_input("Complaint ID", placeholder="Example: JR-20261123-ABC123")
        student_name = st.text_input("Your Name", placeholder="Enter your name")

        if st.button("Track Complaint", use_container_width=True):
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
                            st.success("Complaint found!")
                            st.markdown("### Complaint details")

                            d1, d2 = st.columns(2)
                            d1.write(f"**Complaint ID:** {complaint['id']}")
                            d1.write(f"**Category:** {complaint['category']}")
                            d1.write(f"**Location:** {complaint['location']}")
                            d2.write(f"**Name:** {complaint['name']}")
                            d2.write(f"**Created At:** {complaint['created_at']}")

                            st.write("**Problem Description**")
                            st.info(complaint["description"])

                            st.write("**Current Status**")
                            status_label(complaint["status"])
                        else:
                            st.error("Complaint ID or name does not match.")
                    else:
                        st.warning("No complaint found with this ID.")
                except Exception as e:
                    st.error("Unable to track complaint.")
                    st.error(str(e))
            else:
                st.warning("Please enter both Complaint ID and Name.")

# --------------------------------
# ADMIN DASHBOARD
# --------------------------------

elif menu == "🛡️ Admin Dashboard":
    page_heading(
        "AUTHORIZED ACCESS",
        "Admin Dashboard",
        "Review submitted water issues and manage their resolution status.",
    )

    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    if not st.session_state.admin_authenticated:
        with st.container(border=True):
            st.markdown("### 🔐 Administrator Login")
            st.write("Enter the administrator passcode to continue.")

            password = st.text_input("Admin Passcode", type="password")

            if st.button("Login to Dashboard", use_container_width=True):
                correct_password = st.secrets["auth"]["admin_passcode"]

                if hmac.compare_digest(password, correct_password):
                    st.session_state.admin_authenticated = True
                    st.success("Admin access granted!")
                    st.rerun()
                else:
                    st.error("Incorrect admin passcode.")

    else:
        left, right = st.columns([4, 1])
        with left:
            st.success("Administrator access is active.")
        with right:
            if st.button("Logout", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.rerun()

        try:
            admin_complaints = get_complaints()

            # Analytics have moved to the separate, administrator-only Reports page.
            if admin_complaints:
                st.divider()
                st.markdown('<div class="section-heading">Manage Water Complaints</div>', unsafe_allow_html=True)

                for complaint in admin_complaints:
                    with st.expander(
                        f"{complaint['id']}  |  {complaint['category']}  |  {complaint['status']}"
                    ):
                        a1, a2 = st.columns(2)
                        a1.write(f"**Name:** {complaint['name']}")
                        a1.write(f"**Location:** {complaint['location']}")
                        a2.write(f"**Category:** {complaint['category']}")
                        a2.write(f"**Created At:** {complaint['created_at']}")

                        st.write("**Problem Description**")
                        st.info(complaint["description"])

                        statuses = ["Pending", "In Progress", "Resolved"]
                        new_status = st.selectbox(
                            "Update Complaint Status",
                            statuses,
                            index=statuses.index(complaint["status"]),
                            key=f"status_{complaint['id']}",
                        )

                        if st.button(
                            "Save Status",
                            key=f"update_{complaint['id']}",
                        ):
                            try:
                                update_complaint_status(complaint["id"], new_status)
                                st.success(f"{complaint['id']} updated to {new_status}.")
                                st.rerun()
                            except Exception as e:
                                st.error("Status update failed.")
                                st.error(str(e))
            else:
                st.info("No complaints available to manage.")

        except Exception as e:
            st.error("Unable to load admin complaints.")
            st.error(str(e))



# --------------------------------
# REPORTS (ADMIN ONLY)
# --------------------------------

elif menu == "📊 Reports":
    if not st.session_state.get("admin_authenticated", False):
        st.warning("Reports are available to administrators only. Please log in first.")
        st.session_state["jr_current_page"] = "🛡️ Admin Dashboard"
        st.rerun()
    else:
        page_heading(
            "ADMINISTRATOR REPORTS",
            "Reports & Analytics",
            "Analyze water complaints using records stored in Supabase.",
        )

        top_left, top_right = st.columns([5, 1])
        with top_left:
            st.success("Administrator access is active.")
        with top_right:
            if st.button("Logout", key="reports_logout", use_container_width=True):
                st.session_state.admin_authenticated = False
                st.session_state["jr_current_page"] = "🏠 Home"
                st.rerun()

        try:
            report_complaints = get_complaints()

            if not report_complaints:
                st.info("No complaints are available for reporting yet.")
            else:
                report_df = pd.DataFrame(report_complaints)
                report_df["created_at_dt"] = pd.to_datetime(
                    report_df.get("created_at"), utc=True, errors="coerce"
                )
                report_df["resolved_at_dt"] = pd.to_datetime(
                    report_df.get("resolved_at"), utc=True, errors="coerce"
                )

                # Summary counts.
                metric_cols = st.columns(4)
                metric_cols[0].metric("Total Complaints", len(report_df))
                metric_cols[1].metric("Pending", int((report_df["status"] == "Pending").sum()))
                metric_cols[2].metric("In Progress", int((report_df["status"] == "In Progress").sum()))
                metric_cols[3].metric("Resolved", int((report_df["status"] == "Resolved").sum()))

                st.divider()
                st.caption(
                    "All charts are calculated from the complaint records currently stored in Supabase."
                )

                # Download reports. Export only original database columns, not helper columns.
                st.markdown("#### Download Reports")
                export_df = report_df.drop(
                    columns=["created_at_dt", "resolved_at_dt"],
                    errors="ignore",
                )
                csv_data = export_df.to_csv(index=False).encode("utf-8-sig")

                download_col, pdf_col = st.columns(2)
                with download_col:
                    st.download_button(
                        label="⬇️ Download CSV",
                        data=csv_data,
                        file_name="jalrakshak_complaints_report.csv",
                        mime="text/csv",
                        use_container_width=True,
                        key="download_jalrakshak_csv",
                    )

                with pdf_col:
                    try:
                        from reportlab.lib import colors
                        from reportlab.lib.enums import TA_CENTER
                        from reportlab.lib.pagesizes import A4, landscape
                        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                        from reportlab.lib.units import mm
                        from reportlab.platypus import (
                            SimpleDocTemplate,
                            Paragraph,
                            Spacer,
                            Table,
                            TableStyle,
                        )
                        from xml.sax.saxutils import escape

                        pdf_buffer = BytesIO()
                        pdf_doc = SimpleDocTemplate(
                            pdf_buffer,
                            pagesize=landscape(A4),
                            rightMargin=12 * mm,
                            leftMargin=12 * mm,
                            topMargin=12 * mm,
                            bottomMargin=12 * mm,
                        )
                        pdf_styles = getSampleStyleSheet()
                        pdf_title_style = ParagraphStyle(
                            "JalRakshakTitle",
                            parent=pdf_styles["Title"],
                            alignment=TA_CENTER,
                            textColor=colors.HexColor("#07558a"),
                            spaceAfter=8,
                        )
                        pdf_small_style = ParagraphStyle(
                            "JalRakshakSmall",
                            parent=pdf_styles["BodyText"],
                            fontSize=7,
                            leading=9,
                        )

                        
# Calculate complaint counts
pending_reports = int(
    (report_df["status"].astype(str).str.strip().str.lower() == "pending").sum()
)

progress_reports = int(
    (report_df["status"].astype(str).str.strip().str.lower() == "in progress").sum()
)

resolved_reports = int(
    (report_df["status"].astype(str).str.strip().str.lower() == "resolved").sum()
)

# Create PDF report
pdf_story = [
    Paragraph("JalRakshak - Water Issue Report", pdf_title_style),
    Paragraph(
        f"Generated on: {datetime.now().strftime('%d-%m-%Y %H:%M')}",
        pdf_styles["Normal"],
    ),
    Spacer(1, 5 * mm),
    Paragraph(
        f"Total complaints: {len(report_df)}"
        f"&nbsp;&nbsp; Pending: {pending_reports}"
        f"&nbsp;&nbsp; In Progress: {progress_reports}"
        f"&nbsp;&nbsp; Resolved: {resolved_reports}",
        pdf_styles["Normal"],
    ),
    Spacer(1, 4 * mm),
]


                        pdf_columns = [
                            column for column in
                            ["id", "category", "location", "status", "created_at", "resolved_at"]
                            if column in export_df.columns
                        ]
                        if not pdf_columns:
                            pdf_columns = list(export_df.columns[:6])

                        pdf_table_data = [[
                            Paragraph(f"<b>{escape(str(column))}</b>", pdf_small_style)
                            for column in pdf_columns
                        ]]
                        for _, record in export_df[pdf_columns].fillna("").iterrows():
                            pdf_table_data.append([
                                Paragraph(escape(str(value)), pdf_small_style)
                                for value in record.tolist()
                            ])

                        pdf_table = Table(
                            pdf_table_data,
                            repeatRows=1,
                            hAlign="LEFT",
                        )
                        pdf_table.setStyle(TableStyle([
                            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#07558a")),
                            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                            ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#cbd5e1")),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("ROWBACKGROUNDS", (0, 1), (-1, -1),
                             [colors.white, colors.HexColor("#f1f6fa")]),
                            ("LEFTPADDING", (0, 0), (-1, -1), 5),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                            ("TOPPADDING", (0, 0), (-1, -1), 5),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                        ]))
                        pdf_story.append(pdf_table)
                        pdf_doc.build(pdf_story)
                        pdf_data = pdf_buffer.getvalue()

                        st.download_button(
                            label="⬇️ Download PDF",
                            data=pdf_data,
                            file_name="jalrakshak_complaints_report.pdf",
                            mime="application/pdf",
                            use_container_width=True,
                            key="download_jalrakshak_pdf",
                        )
                    except ImportError:
                        st.info(
                            "PDF export needs ReportLab. Install it with: "
                            "`pip install reportlab`"
                        )

                # 1. Monthly complaint trends.
                st.markdown("#### 1. Monthly Complaint Trends")
                monthly_data = (
                    report_df.dropna(subset=["created_at_dt"])
                    .assign(month=lambda data: data["created_at_dt"].dt.strftime("%Y-%m"))
                    .groupby("month")
                    .size()
                    .rename("Complaints")
                    .to_frame()
                    .sort_index()
                )
                if not monthly_data.empty:
                    st.line_chart(monthly_data, use_container_width=True)
                else:
                    st.info("No valid complaint creation dates are available yet.")

                # 2. Category and 3. location analysis.
                category_col, location_col = st.columns(2)
                with category_col:
                    st.markdown("#### 2. Category-wise Analysis")
                    category_data = (
                        report_df["category"].fillna("Not specified")
                        .value_counts()
                        .rename("Complaints")
                        .to_frame()
                    )
                    st.bar_chart(category_data, use_container_width=True)

                with location_col:
                    st.markdown("#### 3. Location-wise Analysis")
                    location_data = (
                        report_df["location"].fillna("Not specified")
                        .value_counts()
                        .rename("Complaints")
                        .to_frame()
                    )
                    st.bar_chart(location_data, use_container_width=True)

                # 4. Complaint status comparison.
                st.markdown("#### 4. Complaint Status Comparison")
                status_order = ["Pending", "In Progress", "Resolved"]
                status_data = (
                    report_df["status"].fillna("Unknown")
                    .value_counts()
                    .reindex(status_order, fill_value=0)
                    .rename("Complaints")
                    .to_frame()
                )
                st.bar_chart(status_data, use_container_width=True)

                # 5. Average resolution time.
                st.markdown("#### 5. Average Complaint Resolution Time")
                valid_resolved = report_df[
                    (report_df["status"] == "Resolved")
                    & report_df["created_at_dt"].notna()
                    & report_df["resolved_at_dt"].notna()
                ].copy()
                valid_resolved["resolution_hours"] = (
                    valid_resolved["resolved_at_dt"] - valid_resolved["created_at_dt"]
                ).dt.total_seconds() / 3600
                valid_resolved = valid_resolved[valid_resolved["resolution_hours"] >= 0]

                if not valid_resolved.empty:
                    average_hours = float(valid_resolved["resolution_hours"].mean())
                    avg_col, count_col = st.columns(2)
                    avg_col.metric("Average Resolution Time", f"{average_hours:.2f} hours")
                    count_col.metric(
                        "Resolved Complaints with Timestamps",
                        int(len(valid_resolved)),
                    )
                    st.caption(
                        f"Approximately {average_hours / 24:.2f} days. "
                        "Records without valid resolved_at timestamps are excluded."
                    )
                else:
                    st.info(
                        "Average resolution time will appear after at least one resolved "
                        "complaint has valid created_at and resolved_at timestamps."
                    )

        except Exception as e:
            st.error("Unable to load reports from Supabase.")
            st.error(str(e))


# --------------------------------
# FOOTER
# --------------------------------

st.markdown("---")
st.markdown(
    """
    <div class="footer">
        💧 <b>JalRakshak</b> · Smart Community Water Management System<br>
        Every drop counts. Together, let's build a water-conscious campus.
    </div>
    """,
    unsafe_allow_html=True,
)


