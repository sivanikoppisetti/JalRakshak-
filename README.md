# JalRakshak – Campus Water Complaint Management System

JalRakshak is a web-based application designed to manage water-related complaints within a college campus. It provides students and campus users with a simple way to report water problems, upload supporting images, and track complaint progress. Administrators can use a separate dashboard to review complaints and update their status.

## Live Application

**[Open JalRakshak](https://k8wdhhjdnm9eau6rkozive.streamlit.app/)**

## Objectives

- Make campus water complaint submission simple and accessible.
- Allow users to track complaints using a unique Complaint ID.
- Provide administrators with a centralized place to review and manage complaints.
- Improve transparency and help campus teams respond to water-related problems systematically.

## Features

### User Features
- User registration and login
- Forgot-password support
- Guest complaint submission
- Submission of water-related complaint details
- Optional image upload as supporting evidence
- Unique Complaint ID generation
- Complaint status tracking
- View previously submitted complaints for registered users

### Administrator Features
- Separate admin dashboard
- View submitted complaints
- View images attached to complaints
- Search and filter complaint records
- Update complaint status:
  - Pending
  - In Progress
  - Resolved

### Interface
- Clean, user-friendly light-mode interface

## Working Process

1. Open the JalRakshak application.
2. Register or log in, or continue as a guest if guest submission is available.
3. Enter the water-related complaint details.
4. Upload a related image if required.
5. Submit the complaint and note the generated Complaint ID.
6. Use the Complaint ID to track its status.
7. Administrators review complaints in the admin dashboard and update their status as action is taken.

## Technologies Used

| Component | Technology |
|---|---|
| Programming language | Python |
| Frontend / application framework | Streamlit |
| Database | Supabase PostgreSQL |
| Authentication | Supabase Authentication |
| File storage | Supabase Storage |
| Data handling | Pandas |
| Data visualization | Plotly |
| PDF generation | ReportLab |
| Deployment | Streamlit Community Cloud |
| Version control | GitHub |

## Installation and Local Setup

### Prerequisites
- Python installed on your computer
- Git installed on your computer
- Access to the Supabase project and its required credentials

### 1. Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd <YOUR_PROJECT_FOLDER>
```

Replace the placeholders with your repository URL and project folder name.

### 2. Create and activate a virtual environment (recommended)

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On macOS or Linux:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Supabase credentials

Add the Supabase project URL and required API key using Streamlit secrets. For local development, create:

`.streamlit/secrets.toml`

Add the configuration keys expected by your application, for example:

```toml
SUPABASE_URL = "your_supabase_project_url"
SUPABASE_KEY = "your_supabase_api_key"
```

Use the exact secret names expected by your Python code. Do not commit real credentials, passwords, or API keys to GitHub.

### 5. Run the application

```bash
streamlit run app.py
```

If your application's main Python file has a different name, replace `app.py` with that filename.

## Complaint Statuses

| Status | Meaning |
|---|---|
| Pending | The complaint is awaiting action. |
| In Progress | The complaint is being addressed. |
| Resolved | The reported issue has been resolved. |

## Future Enhancements

- SMS and WhatsApp notifications
- Mobile application support
- Automatic complaint assignment
- Advanced analytics and reports
- Location-based complaint identification

## Advantages

- Reduces manual complaint handling.
- Saves time and effort for users and administrators.
- Makes complaint tracking easier.
- Centralizes campus water complaint records.
- Supports systematic monitoring and resolution of water problems.

## Conclusion

JalRakshak provides a digital solution for managing water-related complaints within a college campus. It helps users report problems and track progress, while administrators can monitor complaints and update their status through a centralized dashboard. The project aims to support better campus maintenance and responsible water management.

## Project Information

**Project Name:** JalRakshak  
**Project Type:** Campus Water Complaint Management System  
**Deployment:** Streamlit Community Cloud  
**Live URL:** https://k8wdhhjdnm9eau6rkozive.streamlit.app/
