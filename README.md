# 🚗 DriveBD: Smart Driver & Vehicle Owner Portal

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.38%2B-FF4B4B)
![License](https://img.shields.io/badge/License-MIT-green)

**DriveBD** is a comprehensive web application designed to simulate the national driver and vehicle management system of Bangladesh. Built with **Python** and **Streamlit**, it provides a centralized platform for vehicle owners, drivers, and administrators to manage registrations, traffic violations, digital documents, vehicle maintenance, and fine payments.

> ⚠️ **Disclaimer:** This is an academic/portfolio capstone project. It is **not affiliated with, endorsed by, or connected to BRTA** (Bangladesh Road Transport Authority), Bangladesh Police, or any government organization. All data, users, and records are synthetically generated for demonstration purposes only.

> 🇧🇩 **Update — Bangladesh-friendly + workable actions added:** Registration now validates a real Bangladeshi mobile number format (`01XXXXXXXXX`) and NID length (10/13/17 digits). The Violations page now has actual **Pay Fine** (bKash/Nagad/Card/Cash) and **File Appeal** actions instead of just a read-only table, "Appeals" was added to the sidebar (it existed as a page but had no nav link), and the Admin → Appeals tab now has real **Approve/Reject** buttons that waive the fine or send it back to pending, so the appeal workflow described in the docs actually works end-to-end.

> 🛠️ **Note on this fixed version:** This copy of the repo runs entirely from the single `app.py` file, which contains its own in-memory mock database and login system. The original `pages/` and `utils/` folders implemented a **second, separate** login system (bcrypt + SQLite) that Streamlit auto-added to the sidebar navigation — clicking those auto-generated links used different session state than `app.py`'s login, which is what caused "please log in" errors for already-logged-in users, including admin. Those folders have been renamed to `legacy_unused_pages/` and `legacy_unused_utils/` so Streamlit no longer picks them up. They're kept only for reference and are not used by the running app. `app.py`'s mock database is now also wrapped in `st.cache_resource`, so it's created once and kept in server memory — registrations, admin edits, etc. now persist across clicks/reruns for as long as the app process stays up, instead of being silently reset on every interaction.

> 🧹 **Note on the latest pass:** The UI is now English-only (the earlier bilingual English/Bangla labels have been removed for consistency). Also fixed: the landing page's "Create free account" button (it targeted a Streamlit internal element that didn't exist, so it silently did nothing — it now scrolls to the login/register section), a duplicate "Dashboard/Vehicles" quick-nav row that redundantly sat under the header, the dashboard's unread-notification count (it was summing every user's notifications instead of the logged-in user's), missing seed notifications for the owner/admin demo accounts, violations pagination (it broke past page 4), and a few smaller polish items — see the CHANGELOG-equivalent commit history for the full list. `requirements.txt` and this README have also been trimmed to match what the running `app.py` actually uses.

---

# 📖 Overview

DriveBD is a full-stack simulation of a national digital driver and vehicle management portal inspired by Bangladesh's transportation ecosystem.

The project demonstrates how a modern e-government service could work by combining:

- Secure authentication
- Role-Based Access Control (RBAC)
- Vehicle Registration
- Traffic Violation Management
- Digital Document Vault
- Service History
- Fine Payment System
- Data Analytics
- Mock BRTA APIs
- AI-based Violation Detection Demo

The system is designed for educational, research, and portfolio purposes while following real-world software engineering practices.

---

# ✨ Key Features

## 🔐 Authentication & RBAC

- Login/Registration (mock, in-memory accounts)
- Session Management (`st.session_state`)
- Three Roles:
  - Admin
  - Vehicle Owner
  - Driver

---

## 📊 Smart Dashboard

Role-based dashboard showing

- Vehicle Count
- Total Violations
- Pending Payments
- Upcoming Expiry Alerts
- Recent Activities
- Quick Navigation Cards

---

## 🚘 Vehicle Management

- Register Vehicle
- Edit Vehicle Information
- Search Vehicles
- Vehicle Ownership
- Registration Status
- Fitness Information

---

## 🚦 Traffic Violation System

- Create Violations
- Automatic Fine Calculation
- Violation Categories
- Payment Status
- Violation History
- Evidence Image Support (Demo)

---

## 💳 Digital Payment Portal

Supported mock payment methods

- bKash
- Nagad
- Debit/Credit Card
- Bank Transfer

Features

- Instant Payment
- Payment History with Receipt Numbers
- Status Tracking

---

## 📂 Digital Document Vault

Store and monitor

- National ID
- Driving License
- Vehicle Registration
- Fitness Certificate
- Tax Token
- Insurance

Includes automatic expiry reminders.

---

## 🔧 Vehicle Service History

Maintain

- Oil Changes
- Repairs
- Servicing
- Cost Tracking
- Workshop Details
- Service Timeline

---

## 📝 Appeals Management

Drivers may

- Submit Appeals
- Track Appeal Status
- View Decisions
- Upload Supporting Information

Admins can

- Approve Appeals
- Reject Appeals
- Add Comments

---

## 👨‍💼 Admin Control Panel

Administrator capabilities include

- User Management
- Role Management
- System Logs
- Dashboard Analytics
- Approve Appeals
- Edit Configuration
- Database Overview

---

## 📈 Data Analytics

The Admin panel includes summary tables and totals (revenue, violation counts, vehicle/user breakdowns). Interactive charting (e.g. Plotly) isn't wired into the running app yet — see Future Improvements.

---

## 📑 Report Generation

Not currently implemented in the running app (no CSV/PDF export buttons) — listed here as a planned feature. See Future Improvements.

---

## 🌐 Mock BRTA API

Simulation of

- Driving License Verification
- Vehicle Fitness Verification
- Registration Lookup

No real government APIs are used.

---

## 🤖 AI Violation Detection Demo

Concept demonstration using rule-based AI.

Simulates

- Helmet Detection
- Seatbelt Detection
- Number Plate Reading
- Speed Violation Detection

*(Educational demonstration only—not actual computer vision.)*

---

## 🔔 Notification Center

Receive alerts for

- New Violations
- Expiring Documents
- Successful Payments
- Admin Notices
- Appeal Updates

---

# 🛠️ Technology Stack

This section describes what `app.py` (the version that actually runs) uses. The `legacy_unused_pages/` and `legacy_unused_utils/` folders reference a different, unused stack — see the note above.

## Frontend & App Framework

- Streamlit

## Backend

- Python

## Data Processing

- Pandas

## Data Storage

- In-memory only (a Python object cached with `st.cache_resource`). Nothing is written to disk, so all data resets when the app process restarts. The `data/*.csv` files in this repo are reference samples, not a live database.

## PDF / Export

- Not currently implemented in `app.py` (see Future Improvements below).

---

# 🚀 Quick Start

## Prerequisites

- Python 3.10+
- pip

---

## 1️⃣ Clone Repository

```bash
git clone https://github.com/rahanul089/drivebd.git

cd drivebd
```

---

## 2️⃣ Create Virtual Environment

### Windows

```bash
python -m venv venv

venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv venv

source venv/bin/activate
```

---

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4️⃣ Run Application

```bash
streamlit run app.py
```

Open

```
http://localhost:8501
```

The app seeds its own demo data (users, vehicles, violations, payments, etc.) in memory on startup — no separate database initialization step is needed.

---

# 🔐 Demo Credentials

These accounts are created automatically in memory the first time the app starts — no setup step is required.

| Role | Email | Password |
|------|--------|----------|
| Admin | admin@drivebd.gov.bd | Admin@123 |
| Driver | driver@drivebd.gov.bd | Demo@123 |
| Owner | owner@drivebd.gov.bd | Demo@123 |

(These match the accounts actually seeded in `app.py`'s `DriveDB._seed_data()`. The table previously listed `demo@drivebd.gov.bd`, which doesn't exist — that mismatch was itself a source of "login failures".)

Additional randomly generated demo users (`user4@mail.com` … `user14@mail.com`, all password `Demo@123`) are created automatically on first run — a few are randomly marked "suspended" to demonstrate that status check.

---

# ☁️ Deploy to Streamlit Community Cloud

DriveBD is deployment-ready.

## Step 1

Push the project to GitHub.

---

## Step 2

Login to

https://share.streamlit.io/

---

## Step 3

Select your repository.

---

## Step 4

No extra setup is needed for storage — `app.py`'s mock database lives entirely in memory (wrapped in `st.cache_resource`) and seeds itself automatically on first load. Just be aware that on Streamlit Community Cloud, that memory is cleared whenever the app sleeps/restarts, so registrations and other changes won't survive a redeploy or a long idle period. For data that needs to persist, see the Production Tip below.

---

## Step 5

Deploy

Main file

```
app.py
```

---

### 💡 Production Tip

The current `app.py` has no persistence layer at all — everything lives in server memory and resets on restart. If you want data to survive restarts, the most realistic path is to add a real datastore (e.g. SQLite, or a hosted Postgres provider like Neon, Supabase, or Railway) and swap the in-memory `DriveDB` class for one that reads/writes to it. That's a genuine code change, not a config toggle.

---

# 📂 Project Structure

```text
drivebd/
│
├── app.py                    # The actual running app — everything else below is legacy/unused
├── requirements.txt
├── README.md
│
├── .streamlit/
│   └── config.toml
│
├── .devcontainer/
│   └── devcontainer.json
│
├── data/                     # Reference CSV samples, not a live database
│   ├── users.csv
│   ├── vehicles.csv
│   ├── violations.csv
│   ├── payments.csv
│   ├── documents.csv
│   ├── service_history.csv
│   ├── appeals.csv
│   ├── notifications.csv
│   ├── activity_logs.csv
│   └── settings.csv
│
├── legacy_unused_pages/      # Old Streamlit multipage app, not loaded by app.py
│   ├── 1_Dashboard.py
│   ├── 2_Vehicles.py
│   ├── 3_Violations.py
│   ├── 4_Payments.py
│   ├── 5_Documents.py
│   ├── 6_Service_History.py
│   ├── 7_Notifications.py
│   ├── 8_Appeals.py
│   ├── 9_Admin.py
│   ├── 10_Reports.py
│   ├── 11_Analytics.py
│   ├── 12_Mock_BRTA_API.py
│   └── 13_AI_Demo.py
│
└── legacy_unused_utils/      # Old SQLAlchemy/bcrypt backend, not used by app.py
    ├── auth.py
    ├── db.py
    ├── pdf_utils.py
    └── seed.py
```

---

# 📸 Screenshots

You can include screenshots here after deployment.

```text
assets/
├── dashboard.png
├── vehicles.png
├── violations.png
├── analytics.png
├── payments.png
```

Example:

```md
## Dashboard

![Dashboard](assets/dashboard.png)

## Analytics

![Analytics](assets/analytics.png)
```

---

# 🔒 Security Notes

This is a demo/portfolio app, not a hardened production system. Specifically:

- Passwords are stored and compared in **plaintext** in the in-memory mock database — fine for a demo with fake accounts, but not something to copy into a real app.
- There's no real backend or database, so there's nothing to SQL-inject and no ORM layer to speak of.
- Access to admin-only pages is gated by a role check in `app.py` (`user['role'] == 'admin'`), not by any server-side enforcement — it's a UI-level guard suitable for a demo, not a security boundary.
- Session state is Streamlit's built-in `st.session_state`, scoped to the browser session; there's no token-based auth, expiry, or CSRF protection.
- Basic input validation exists for things like phone number and NID format on registration.

If you build on this for something real, add proper password hashing, a real datastore, and server-side authorization checks before deploying it anywhere with real user data.

---

# 🧪 Future Improvements

- Interactive Charts/Analytics (e.g. Plotly)
- CSV/PDF Report Export
- Downloadable PDF Payment Receipts
- Persistent Storage (SQLite/Postgres instead of in-memory)
- Real Password Hashing
- OCR-based License Verification
- Real AI Computer Vision
- Live Camera Integration
- BRTA API Integration
- Bangladesh Police API Integration
- SMS Notifications
- Email Verification
- Two-Factor Authentication (2FA)
- Mobile Application (Flutter)
- GPS Vehicle Tracking
- Online Vehicle Tax Payment
- Cloud Storage for Documents

---

# 📄 License

This project is licensed under the **MIT License**.

---

# 🙏 Acknowledgments

- Real-world Bangladesh transportation concepts inspired by public BRTA guidelines and transport policies.
- Streamlit for the interactive web framework.
- Pandas for data handling and display.
- The Python open-source community for excellent libraries and tooling.

---

# 📬 Contact

**Maintainer:** Rahanul

**GitHub:** https://github.com/rahanul089

**Project Repository:**

https://github.com/rahanul089/drivebd

---

# ⭐ Show Your Support

If you found this project useful, educational, or inspiring, please consider:

- ⭐ Starring the repository on GitHub
- 🍴 Forking the project
- 🐛 Reporting bugs or suggesting improvements
- 💡 Opening feature requests
- 🤝 Contributing through pull requests

Your support helps improve the project and encourages future open-source development.

---

## ❤️ Made with Passion

Made with ❤️ for the people of Bangladesh 🇧🇩

Designed and developed as a portfolio project demonstrating modern software engineering, database design, UI/UX, analytics, and full-stack development using Python and Streamlit.

---

## 📌 Project Status

> 🚀 **Status:** Production-Ready Portfolio Project

Current Version:

```
v1.0.0
```

Last Updated:

```
August 2026
```

Maintained by:

**Rahanul**

---

## 🌟 If you like this project...

```
⭐ Star the repository
🍴 Fork it
📢 Share it
💙 Happy Coding!
```
