import streamlit as st
import pandas as pd
import random
import re
from datetime import datetime, timedelta

# Page configuration
st.set_page_config(page_title="DriveBD - Smart Driver & Vehicle Portal", page_icon="🚗", layout="wide")

def nav_label(en, key=None):
    """English label for sidebar/nav buttons."""
    return en

# ================= MOCK DATABASE =================
class DriveDB:
    def __init__(self):
        self.users = []
        self.vehicles = []
        self.violations = []
        self.payments = []
        self.notifications = []
        self.documents = []
        self.service = []
        self.appeals = []
        self.activity = []
        self.seq = 1000
        self._seed_data()
    
    def _nid(self, prefix='u'):
        self.seq += 1
        return f"{prefix}{self.seq}"
    
    def _rand(self, arr):
        return arr[random.randint(0, len(arr)-1)]
    
    def _rand_int(self, a, b):
        return random.randint(a, b)
    
    def _fmt_date(self, d):
        return d.strftime("%Y-%m-%d")
    
    def _days_from_now(self, n):
        return datetime.now() + timedelta(days=n)
    
    def _money(self, n):
        return f"৳{n:,}"
    
    def _seed_data(self):
        # Users
        self.users.append({
            'id': 'u1', 'name': 'Rafiq Ahmed', 'email': 'driver@drivebd.gov.bd', 
            'password': 'Demo@123', 'role': 'driver', 'phone': '01711223344',
            'license': 'DHA-0234567', 'nid': '1995123456789', 
            'address': 'House 12, Road 5, Dhanmondi, Dhaka',
            'emergency': '01899887766', 'avatar': 'RA', 'status': 'active',
            'joined': '2025-02-10'
        })
        self.users.append({
            'id': 'u2', 'name': 'Nasrin Sultana', 'email': 'owner@drivebd.gov.bd',
            'password': 'Demo@123', 'role': 'owner', 'phone': '01822334455',
            'license': 'DHA-0987654', 'nid': '1990654321987',
            'address': 'Flat 4B, Gulshan Avenue, Dhaka',
            'emergency': '01911223344', 'avatar': 'NS', 'status': 'active',
            'joined': '2025-04-22'
        })
        self.users.append({
            'id': 'u3', 'name': 'System Admin', 'email': 'admin@drivebd.gov.bd',
            'password': 'Admin@123', 'role': 'admin', 'phone': '01700000000',
            'license': '—', 'nid': '—',
            'address': 'DriveBD HQ, Dhaka', 'emergency': '—',
            'avatar': 'SA', 'status': 'active', 'joined': '2024-11-01'
        })
        
        roles = ['driver', 'owner']
        for i in range(4, 15):
            r = self._rand(roles)
            self.users.append({
                'id': f'u{i}', 'name': f'User {i}', 
                'email': f'user{i}@mail.com', 'password': 'Demo@123',
                'role': r, 'phone': f"017{self._rand_int(10000000, 99999999)}",
                'license': f"DHA-0{self._rand_int(100000, 999999)}",
                'nid': str(self._rand_int(1000000000000, 9999999999999)),
                'address': 'Sample Address, Dhaka',
                'emergency': f"018{self._rand_int(10000000, 99999999)}",
                'avatar': f'U{i}', 'status': 'active' if random.random() > 0.9 else 'suspended',
                'joined': f"2025-0{self._rand_int(1,9)}-1{self._rand_int(0,9)}"
            })
        
        # Vehicles
        vi = ['DHAKA METRO GA 11-2481', 'DHAKA METRO HA 15-7723', 
              'CHATTOGRAM METRO KHA 22-0091', 'DHAKA METRO GA 33-5567',
              'SYLHET METRO GA 09-1234', 'DHAKA METRO LA 44-8890']
        vt = ['Private Car', 'Motorcycle', 'Private Car', 'Bus', 'Truck', 'Motorcycle']
        vo = ['u1', 'u1', 'u2', 'u2', 'u4', 'u5']
        man = ['Toyota', 'Yamaha', 'Toyota', 'Ashok Leyland', 'Tata', 'Bajaj']
        mod = ['Corolla Axio', 'X-Blade', 'Premio', 'Hino300', 'Isuzu', 'Pulsar']
        
        for i in range(6):
            self.vehicles.append({
                'id': f'v{i+1}', 'ownerId': vo[i], 'regNo': vi[i],
                'type': vt[i], 'manufacturer': man[i], 'model': mod[i],
                'engine': f'ENG{self._rand_int(100000, 999999)}',
                'chassis': f'CHS{self._rand_int(100000, 999999)}',
                'fuel': self._rand(['Petrol', 'Octane', 'Diesel', 'CNG']),
                'regDate': f"2022-0{self._rand_int(1,9)}-1{self._rand_int(0,9)}",
                'regExpiry': self._fmt_date(self._days_from_now(self._rand_int(-10, 700))),
                'taxExpiry': self._fmt_date(self._days_from_now(self._rand_int(-15, 120))),
                'fitnessExpiry': self._fmt_date(self._days_from_now(self._rand_int(-5, 90))),
                'insuranceExpiry': self._fmt_date(self._days_from_now(self._rand_int(10, 400))),
                'color': self._rand(['White', 'Black', 'Silver', 'Red', 'Blue']),
                'image': None, 'status': 'active',
                'mileage': self._rand_int(5000, 80000),
                'safety': self._rand_int(62, 98)
            })
        
        # Violations
        vtypes = ["Red Light Crossing", "Speeding", "Wrong Lane", "Illegal Parking",
                  "Helmet Violation", "Seat Belt Violation", "Wrong Direction", "Signal Violation"]
        locs = ["Gulshan Circle 1, Dhaka", "Mirpur 10, Dhaka", "Motijheel C/A, Dhaka",
                "Uttara Sector 7, Dhaka", "GEC Circle, Chattogram", "Zindabazar, Sylhet",
                "Shahbagh, Dhaka", "Farmgate, Dhaka"]
        officers = ["Insp. M. Karim", "Sgt. F. Rahman", "Insp. S. Hossain", "Sgt. A. Islam"]
        
        for i in range(22):
            veh = self._rand(self.vehicles)
            # Only seed 'pending'/'paid' here — 'appealed' status is now only set when a
            # user actually files an appeal (see Violations page), so it always has a
            # matching record in db.appeals for the Appeals page / Admin review to show.
            status = self._rand(['pending', 'pending', 'paid'])
            self.violations.append({
                'id': f'vi{i}', 'violationNo': f'VLN-2026-{1000+i}',
                'vehicleId': veh['id'], 'vehicleNo': veh['regNo'],
                'driverName': next((u['name'] for u in self.users if u['id'] == veh['ownerId']), 'Unknown'),
                'type': self._rand(vtypes),
                'date': self._fmt_date(self._days_from_now(-self._rand_int(1, 90))),
                'time': f"{self._rand_int(6,22)}:{str(self._rand_int(0,59)).zfill(2)}",
                'location': self._rand(locs),
                'lat': f"{23.7 + random.random() * 0.15:.4f}",
                'lng': f"{90.35 + random.random() * 0.15:.4f}",
                'evidence': None,
                'description': 'Detected via traffic monitoring camera at checkpoint.',
                'fine': self._rand([500, 1000, 1500, 2000, 3000]),
                'officer': self._rand(officers),
                'status': status
            })
        
        # Payments
        paid_violations = [v for v in self.violations if v['status'] == 'paid']
        for i, v in enumerate(paid_violations):
            self.payments.append({
                'id': f'p{i}', 'violationId': v['id'],
                'violationNo': v['violationNo'],
                'method': self._rand(['bKash', 'Nagad', 'Card', 'Cash']),
                'amount': v['fine'],
                'date': self._fmt_date(self._days_from_now(-self._rand_int(1, 60))),
                'status': 'completed',
                'receiptNo': f'RCPT-{self._rand_int(100000, 999999)}'
            })
        
        # Notifications
        notifs = [
            ('reminder', 'Road tax expiring soon',
             'Your vehicle DHAKA METRO GA 11-2481 road tax expires in 12 days.'),
            ('violation', 'New violation recorded',
             'A speeding violation was recorded against DHAKA METRO HA 15-7723.'),
            ('payment', 'Payment received',
             'Your payment of ৳1500 for VLN-2026-1004 was confirmed.'),
            ('reminder', 'Fitness certificate due',
             'Fitness certificate for CHATTOGRAM METRO KHA 22-0091 expires soon.'),
            ('system', 'Welcome to DriveBD',
             'Your account has been created successfully.'),
            ('reminder', 'Insurance renewal',
             'Insurance for DHAKA METRO GA 33-5567 renews in 30 days.'),
            ('violation', 'Appeal update',
             'Your appeal for VLN-2026-1002 is under review.'),
            ('payment', 'Receipt available',
             'Download your receipt for RCPT payment anytime from Payments.'),
        ]
        owner_notifs = [
            ('reminder', 'Fitness certificate due',
             'Fitness certificate for one of your vehicles expires soon.'),
            ('payment', 'Payment received',
             'A fine payment on your fleet was confirmed.'),
            ('system', 'Welcome to DriveBD',
             'Your account has been created successfully.'),
        ]
        admin_notifs = [
            ('system', 'New appeal submitted',
             'A driver has submitted an appeal that needs review.'),
            ('system', 'New account registered',
             'A new driver/owner account was created on the platform.'),
            ('system', 'Welcome to DriveBD',
             'Your admin account is ready.'),
        ]
        n_id = 0
        for uid, notif_set in (('u1', notifs), ('u2', owner_notifs), ('u3', admin_notifs)):
            for i, n in enumerate(notif_set):
                self.notifications.append({
                    'id': f'n{n_id}', 'userId': uid, 'category': n[0],
                    'title': n[1], 'message': n[2],
                    'read': i > 4,
                    'date': self._fmt_date(self._days_from_now(-i * 2))
                })
                n_id += 1
        
        # Service history
        for i in range(6):
            veh = self._rand(self.vehicles)
            self.service.append({
                'id': f's{i}', 'vehicleId': veh['id'],
                'vehicleNo': veh['regNo'],
                'type': self._rand(['Oil Change', 'Engine Service', 'Tyre Change',
                                   'Battery Replacement', 'Brake Service']),
                'date': self._fmt_date(self._days_from_now(-self._rand_int(10, 200))),
                'mileage': self._rand_int(5000, 80000),
                'cost': self._rand_int(800, 6000),
                'notes': 'Routine maintenance completed at authorized service center.'
            })
        
        # Activity
        self.activity = [
            {'icon': '🚗', 'text': 'Vehicle DHAKA METRO GA 11-2481 added to your account',
             'time': '2 days ago'},
            {'icon': '🧾', 'text': 'Violation VLN-2026-1004 marked as paid',
             'time': '4 days ago'},
            {'icon': '📄', 'text': 'Insurance document uploaded for HA 15-7723',
             'time': '6 days ago'},
            {'icon': '🔔', 'text': 'Reminder sent: road tax expiring in 12 days',
             'time': '1 week ago'},
        ]

# ================= DATABASE INSTANCE =================
# IMPORTANT: DriveDB() used to be instantiated here directly, which meant a brand
# new (re-randomized) mock database was created on EVERY Streamlit rerun (i.e. on
# every single click/interaction). That wiped out newly registered accounts, reset
# admin changes, and made login state look inconsistent for every user, including
# admin. st.cache_resource makes Streamlit build the DriveDB object exactly once
# per running app process and hand back the SAME instance (kept in server memory)
# on every rerun and for every connected user/session, so data actually persists
# for as long as the app is running.
@st.cache_resource
def get_db():
    return DriveDB()

db = get_db()

# ================= AUTH FUNCTIONS =================
def _normalize_email(email):
    return (email or "").strip().lower()

def login_user(email, password):
    email = _normalize_email(email)
    user = next((u for u in db.users if u['email'].lower() == email), None)
    if not user:
        return False, "No account found with that email."
    if user['password'] != password:
        return False, "Incorrect password."
    if user['status'] != 'active':
        return False, "This account has been suspended. Contact an administrator."
    st.session_state.user = user
    return True, "Logged in successfully!"

def logout_user():
    st.session_state.user = None
    st.session_state.page = 'landing'
    st.rerun()

def register_user(name, email, password, role, phone='', nid=''):
    email = _normalize_email(email)
    if not email:
        return False, "A valid email is required."
    if any(u['email'].lower() == email for u in db.users):
        return False, "An account with this email already exists"
    if len(password) < 6:
        return False, "Password must be at least 6 characters"
    user = {
        'id': db._nid('u'), 'name': name.strip(), 'email': email,
        'password': password, 'role': role, 'phone': phone or '',
        'license': 'PENDING', 'nid': nid or 'PENDING',
        'address': '', 'emergency': '',
        'avatar': ''.join([s[0] for s in name.split()])[:2].upper() if name.strip() else 'U',
        'status': 'active',
        'joined': db._fmt_date(datetime.now())
    }
    db.users.append(user)
    st.session_state.user = user
    return True, "Account created successfully!"

def current_user():
    return st.session_state.get('user')

def is_logged_in():
    return st.session_state.get('user') is not None

# ================= HELPER FUNCTIONS =================
def get_my_vehicles():
    user = current_user()
    if user['role'] == 'admin':
        return db.vehicles
    return [v for v in db.vehicles if v['ownerId'] == user['id']]

def get_vehicle_ids():
    return [v['id'] for v in get_my_vehicles()]

def get_my_violations():
    user = current_user()
    if user['role'] == 'admin':
        return db.violations
    ids = get_vehicle_ids()
    return [v for v in db.violations if v['vehicleId'] in ids]

def get_my_payments():
    vids = [v['id'] for v in get_my_violations()]
    if current_user()['role'] == 'admin':
        return db.payments
    return [p for p in db.payments if p['violationId'] in vids]

def get_my_documents():
    ids = get_vehicle_ids()
    if current_user()['role'] == 'admin':
        return db.documents
    return [d for d in db.documents if d['vehicleId'] in ids]

def get_my_service():
    ids = get_vehicle_ids()
    if current_user()['role'] == 'admin':
        return db.service
    return [s for s in db.service if s['vehicleId'] in ids]

def get_my_appeals():
    vios = [v['id'] for v in get_my_violations()]
    return [a for a in db.appeals if a['violationId'] in vios]

def owner_name(veh_id):
    v = next((v for v in db.vehicles if v['id'] == veh_id), None)
    if v:
        u = next((u for u in db.users if u['id'] == v['ownerId']), None)
        return u['name'] if u else 'Unknown'
    return 'Unknown'

def status_badge(status):
    colors = {
        'pending': 'badge-amber',
        'paid': 'badge-green',
        'appealed': 'badge-navy',
        'waived': 'badge-green',
        'approved': 'badge-green',
        'rejected': 'badge-red'
    }
    return f'<span class="badge {colors.get(status, "badge-navy")}">{status}</span>'

def exp_badge(date_str):
    try:
        days = (datetime.strptime(date_str, "%Y-%m-%d") - datetime.now()).days
        if days < 0:
            return '<span class="badge badge-red">Expired</span>'
        if days < 30:
            return f'<span class="badge badge-amber">{days}d left</span>'
        return '<span class="badge badge-green">OK</span>'
    except:
        return '<span class="badge badge-navy">N/A</span>'

# ================= CSS =================
def load_css():
    st.markdown("""
    <style>
    /* ============ TOKENS ============ */
    :root {
      --navy: #0B2545;
      --navy-2: #123063;
      --green: #046A38;
      --green-l: #0C8A4C;
      --red: #C8102E;
      --amber: #B4740E;
      --paper: #F6F7F5;
      --card: #FFFFFF;
      --ink: #16233A;
      --muted: #5B6B82;
      --border: #E2E6EA;
      --radius: 14px;
      --shadow: 0 1px 2px rgba(11,37,69,.06), 0 8px 24px -12px rgba(11,37,69,.18);
      --font-d: 'Sora', sans-serif;
      --font-b: 'Inter', sans-serif;
      --font-m: 'JetBrains Mono', monospace;
    }
    
    * { box-sizing: border-box; margin: 0; padding: 0; }
    
    .main-header { font-size: 2.4rem; font-weight: 700; color: var(--navy); margin-bottom: 0; font-family: 'Sora', sans-serif; }
    .sub-header { color: #555; font-size: 1.05rem; margin-top: 0; }
    
    .metric-card {
      background: rgba(4,106,56,.06);
      padding: 16px;
      border-radius: 10px;
      border: 1px solid rgba(4,106,56,.18);
    }
    
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 5px;
      padding: 4px 10px;
      border-radius: 100px;
      font-size: 11.5px;
      font-weight: 600;
    }
    .badge-green { background: rgba(4,106,56,.12); color: var(--green); }
    .badge-red { background: rgba(200,16,46,.12); color: var(--red); }
    .badge-amber { background: rgba(180,116,14,.14); color: var(--amber); }
    .badge-navy { background: rgba(11,37,69,.1); color: var(--navy); }
    
    .stat-card {
      background: var(--card);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      padding: 18px;
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
      background: white;
    }
    
    .mono { font-family: 'JetBrains Mono', monospace; }
    
    .panel {
      background: white;
      border: 1px solid #E2E6EA;
      border-radius: 14px;
      padding: 20px;
      margin-bottom: 20px;
    }
    
    .panel-head {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 16px;
    }
    
    .panel-head h3 { font-size: 15.5px; margin: 0; }
    
    .grid-cards {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 16px;
      margin-bottom: 24px;
    }
    
    .two-col {
      display: grid;
      grid-template-columns: 1.6fr 1fr;
      gap: 20px;
    }
    
    .page-head {
      display: flex;
      justify-content: space-between;
      align-items: flex-end;
      margin-bottom: 22px;
      flex-wrap: wrap;
      gap: 12px;
    }
    
    .page-head h2 { font-size: 23px; margin: 0; }
    .page-head p { color: var(--muted); font-size: 13.5px; margin-top: 4px; }
    
    .page-help {
      background: rgba(4,106,56,.05);
      border-left: 3px solid var(--green);
      border-radius: 8px;
      padding: 12px 16px;
      margin-bottom: 20px;
      font-size: 13.5px;
      line-height: 1.55;
      color: var(--ink);
    }
    .page-help b { color: var(--navy); }
    .page-help ul { margin: 6px 0 0 18px; padding: 0; }
    .page-help li { margin-bottom: 3px; }
    
    .toolbar {
      display: flex;
      gap: 10px;
      margin-bottom: 16px;
      flex-wrap: wrap;
    }
    
    .toolbar input, .toolbar select {
      padding: 9px 12px;
      border-radius: 9px;
      border: 1px solid var(--border);
      background: var(--paper);
      color: var(--ink);
      font-size: 13px;
    }
    
    .btn {
      border: none;
      border-radius: 10px;
      padding: 11px 20px;
      font-weight: 600;
      font-size: 14px;
      transition: .2s;
      display: inline-flex;
      align-items: center;
      gap: 8px;
      cursor: pointer;
    }
    .btn-primary { background: var(--green); color: #fff; }
    .btn-primary:hover { background: var(--green-l); }
    .btn-dark { background: var(--navy); color: #fff; }
    .btn-dark:hover { background: var(--navy-2); }
    .btn-outline { background: transparent; border: 1px solid var(--border); color: var(--ink); }
    .btn-outline:hover { border-color: var(--green); color: var(--green); }
    .btn-red { background: var(--red); color: #fff; }
    .btn-red:hover { opacity: .9; }
    .btn-sm { padding: 7px 12px; font-size: 12.5px; border-radius: 8px; }
    .btn-block { width: 100%; justify-content: center; }
    
    .empty {
      text-align: center;
      padding: 50px 20px;
      color: var(--muted);
    }
    
    .vcard {
      width: 100%;
      max-width: 400px;
      aspect-ratio: 1.58/1;
      margin: 0 auto;
      position: relative;
      border-radius: 18px;
      padding: 22px;
      background: linear-gradient(135deg, #0F3D66, #0B2545 60%, #052A44);
      color: #fff;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
    }
    
    .vcard .chip {
      width: 38px;
      height: 28px;
      border-radius: 6px;
      background: linear-gradient(135deg, #E8C36A, #B8933D);
    }
    
    .vcard .num {
      font-family: 'JetBrains Mono', monospace;
      letter-spacing: 3px;
      font-size: 19px;
      margin-top: 18px;
    }
    
    .vcard .row {
      display: flex;
      justify-content: space-between;
      font-size: 11px;
      color: #9FB2CC;
      text-transform: uppercase;
      letter-spacing: .5px;
    }
    
    .vcard .row b {
      display: block;
      color: #fff;
      font-size: 13px;
      text-transform: none;
      font-family: 'Sora', sans-serif;
      margin-top: 2px;
    }
    
    .vcard .top {
      display: flex;
      justify-content: space-between;
      align-items: flex-start;
    }
    
    .flag {
      display: inline-block;
      width: 22px;
      height: 15px;
      border-radius: 2px;
      background: #046A38;
      position: relative;
      overflow: hidden;
      vertical-align: middle;
      margin-right: 4px;
    }
    .flag::after {
      content: '';
      position: absolute;
      width: 9px;
      height: 9px;
      border-radius: 50%;
      background: #C8102E;
      top: 3px;
      left: 5.5px;
    }
    
    .brand {
      font-size: 20px;
      font-weight: 800;
      display: flex;
      align-items: center;
      gap: 8px;
    }
    
    .s-ic {
      width: 38px;
      height: 38px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    
    .stat-card b {
      display: block;
      font-size: 24px;
      font-family: 'Sora', sans-serif;
      margin-top: 10px;
    }
    .stat-card span { font-size: 12.5px; color: var(--muted); }
    
    .doc-grid {
      display: grid;
      grid-template-columns: repeat(4, 1fr);
      gap: 14px;
    }
    
    .doc-card {
      border: 1px solid var(--border);
      border-radius: 12px;
      padding: 14px;
      text-align: center;
      background: white;
    }
    
    .doc-card .thumb {
      height: 90px;
      border-radius: 8px;
      background: var(--paper);
      display: flex;
      align-items: center;
      justify-content: center;
      margin-bottom: 10px;
      overflow: hidden;
    }
    
    .doc-card b { font-size: 12.5px; display: block; }
    .doc-card span { font-size: 11px; color: var(--muted); }
    .doc-actions { display: flex; gap: 6px; margin-top: 10px; justify-content: center; }
    
    .notif-item {
      display: flex;
      gap: 12px;
      padding: 14px 6px;
      border-bottom: 1px solid var(--border);
      align-items: flex-start;
    }
    
    .notif-item.unread { background: rgba(4,106,56,.04); }
    
    .notif-ic {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      display: flex;
      align-items: center;
      justify-content: center;
      flex-shrink: 0;
    }
    
    .notif-item b { font-size: 13.5px; display: block; }
    .notif-item p { font-size: 12.5px; color: var(--muted); margin-top: 2px; }
    .notif-item .time { font-size: 11px; color: var(--muted); margin-left: auto; white-space: nowrap; }
    
    .tabs {
      display: flex;
      gap: 6px;
      border-bottom: 1px solid var(--border);
      margin-bottom: 18px;
    }
    
    .tab {
      padding: 10px 16px;
      font-size: 13.5px;
      font-weight: 600;
      color: var(--muted);
      border-bottom: 2px solid transparent;
      cursor: pointer;
    }
    
    .tab.active { color: var(--green); border-color: var(--green); }
    
    .pager {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-top: 14px;
      font-size: 13px;
      color: var(--muted);
    }
    
    .pbtns { display: flex; gap: 6px; }
    .pbtns button {
      width: 30px;
      height: 30px;
      border-radius: 7px;
      border: 1px solid var(--border);
      background: white;
      color: var(--ink);
      cursor: pointer;
    }
    .pbtns button.active {
      background: var(--green);
      color: #fff;
      border-color: var(--green);
    }
    
    .icon-btn {
      width: 36px;
      height: 36px;
      border-radius: 9px;
      border: 1px solid var(--border);
      background: white;
      color: var(--ink);
      display: inline-flex;
      align-items: center;
      justify-content: center;
      cursor: pointer;
    }
    
    .icon-btn .dot {
      position: absolute;
      top: 6px;
      right: 6px;
      width: 8px;
      height: 8px;
      border-radius: 50%;
      background: var(--red);
      border: 2px solid white;
    }
    
    .role-pick {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 8px;
      margin-bottom: 18px;
    }
    
    .role-opt {
      border: 1px solid var(--border);
      border-radius: 9px;
      padding: 10px 6px;
      text-align: center;
      font-size: 12.5px;
      font-weight: 600;
      color: var(--muted);
      cursor: pointer;
    }
    
    .role-opt.active {
      border-color: var(--green);
      color: var(--green);
      background: rgba(4,106,56,.08);
    }
    
    .timeline {
      list-style: none;
      padding-left: 0;
    }
    
    .timeline li {
      position: relative;
      padding-left: 28px;
      padding-bottom: 20px;
      border-left: 2px solid var(--border);
      margin-left: 8px;
    }
    
    .timeline li:last-child { border-color: transparent; padding-bottom: 0; }
    
    .timeline li::before {
      content: '';
      position: absolute;
      left: -7px;
      top: 0;
      width: 12px;
      height: 12px;
      border-radius: 50%;
      background: var(--green);
      border: 2px solid white;
    }
    
    .timeline b { font-size: 13px; display: block; }
    .timeline span { font-size: 12px; color: var(--muted); }
    
    table {
      width: 100%;
      border-collapse: collapse;
      font-size: 13.5px;
    }
    th {
      text-align: left;
      padding: 10px 12px;
      color: var(--muted);
      font-weight: 600;
      font-size: 11.5px;
      text-transform: uppercase;
      letter-spacing: .4px;
      border-bottom: 1px solid var(--border);
    }
    td {
      padding: 12px;
      border-bottom: 1px solid var(--border);
      vertical-align: middle;
    }
    tr:last-child td { border-bottom: none; }
    tbody tr:hover { background: rgba(4,106,56,.04); }
    
    .form-grid {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 14px;
    }
    
    .field { margin-bottom: 16px; }
    .field label {
      display: block;
      font-size: 13px;
      font-weight: 600;
      margin-bottom: 6px;
    }
    
    .field input, .field select, .field textarea {
      width: 100%;
      padding: 11px 13px;
      border: 1px solid var(--border);
      border-radius: 9px;
      background: var(--paper);
      color: var(--ink);
      font-family: 'Inter', sans-serif;
      font-size: 14px;
    }
    
    .field input:focus, .field select:focus, .field textarea:focus {
      outline: 2px solid var(--green);
      outline-offset: 1px;
    }
    
    .demo-row {
      display: flex;
      gap: 8px;
      margin-top: 18px;
      flex-wrap: wrap;
    }
    
    .demo-chip {
      border: 1px dashed var(--border);
      background: white;
      font-size: 12px;
      padding: 7px 10px;
      border-radius: 8px;
      color: var(--muted);
      cursor: pointer;
      border: 1px solid #E2E6EA;
    }
    
    .demo-chip:hover { border-color: var(--green); color: var(--green); }
    
    .hero-stats {
      display: flex;
      gap: 34px;
      margin-top: 20px;
    }
    
    .hero-stats div b {
      display: block;
      font-family: 'Sora', sans-serif;
      font-size: 24px;
      color: var(--navy);
    }
    .hero-stats div span {
      font-size: 12.5px;
      color: var(--muted);
    }
    
    @media (max-width: 1000px) {
      .grid-cards { grid-template-columns: repeat(2, 1fr); }
      .two-col { grid-template-columns: 1fr; }
      .form-grid { grid-template-columns: 1fr; }
      .doc-grid { grid-template-columns: repeat(2, 1fr); }
    }
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700;800&family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;700&display=swap" rel="stylesheet">
    """, unsafe_allow_html=True)

# ================= UI ROUTES =================
def render_landing():
    st.markdown("""
    <div style="padding: 40px 0;">
        <div style="display: grid; grid-template-columns: 1.1fr 0.9fr; gap: 60px; align-items: center; max-width: 1280px; margin: 0 auto;">
            <div>
                <div style="display: inline-flex; align-items: center; gap: 8px; background: rgba(4,106,56,.12); border: 1px solid rgba(12,138,76,.3); color: #046A38; font-size: 12.5px; font-weight: 600; padding: 6px 14px; border-radius: 100px; margin-bottom: 22px;">
                    ● Citizen platform · not affiliated with BRTA or Police
                </div>
                <h1 style="font-size: clamp(34px, 4.2vw, 54px); font-weight: 800; line-height: 1.08; letter-spacing: -0.5px; font-family: 'Sora', sans-serif;">
                    Your vehicle, your fines,<br>your papers — <span style="color: #046A38;">in one place.</span>
                </h1>
                <p style="margin-top: 14px; font-size: 17px; color: #5B6B82; max-width: 520px;">
                    DriveBD helps drivers and owners across Bangladesh track violations, store documents, 
                    catch renewal deadlines before they lapse, and pay fines without standing in a line.
                </p>
                <div style="display: flex; gap: 14px; margin-top: 34px; flex-wrap: wrap;">
                    <a href="#get-started" 
                       style="background: #046A38; color: white; border: none; border-radius: 10px; padding: 12px 24px; font-weight: 600; font-size: 14px; cursor: pointer; text-decoration: none; display: inline-block;">
                        Create free account
                    </a>
                </div>
                <div class="hero-stats">
                    <div><b class="mono">150+</b><span>Vehicles tracked</span></div>
                    <div><b class="mono">300+</b><span>Violations logged</span></div>
                    <div><b class="mono">৳12L+</b><span>Fines settled</span></div>
                </div>
            </div>
            <div>
                <div class="vcard">
                    <div class="top">
                        <div class="chip"></div>
                        <b style="font-size:11px; letter-spacing:2px;">DIGITAL VEHICLE CARD</b>
                    </div>
                    <div>
                        <div class="num">DHK · METRO · GA 11‑2481</div>
                        <div class="row" style="margin-top:16px;">
                            <span>Owner<b>Rafiq Ahmed</b></span>
                            <span>Type<b>Private Car</b></span>
                            <span>Valid till<b>Dec 2026</b></span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Features
    st.markdown("""
    <div style="padding: 60px 0;">
        <div style="text-align: center; max-width: 640px; margin: 0 auto 56px;">
            <span style="color: #046A38; font-weight: 700; font-size: 12.5px; letter-spacing: 1.5px; text-transform: uppercase;">Features</span>
            <h2 style="font-size: clamp(26px, 3vw, 38px); margin-top: 10px; letter-spacing: -0.3px; font-family: 'Sora', sans-serif;">
                Everything a vehicle owner actually needs
            </h2>
            <p style="color: #5B6B82; margin-top: 14px; font-size: 15.5px;">
                Built around the paperwork and deadlines that pile up once you own a vehicle in Bangladesh.
            </p>
        </div>
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 22px; max-width: 1200px; margin: 0 auto;">
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">🚗</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Multi‑vehicle registry</h4>
                <p style="font-size: 14px; color: #5B6B82;">Register cars, motorcycles, buses and trucks with full document details in one place.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">⚠</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Violation tracking</h4>
                <p style="font-size: 14px; color: #5B6B82;">See every fine issued against your vehicles with evidence, location and officer details.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">💳</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Instant fine payment</h4>
                <p style="font-size: 14px; color: #5B6B82;">Pay via bKash, Nagad, card or cash and get a receipt immediately.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">📁</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Document vault</h4>
                <p style="font-size: 14px; color: #5B6B82;">Store your licence, registration, fitness and insurance papers securely.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">⏰</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Renewal reminders</h4>
                <p style="font-size: 14px; color: #5B6B82;">Automatic alerts before tax, fitness or insurance expiry dates.</p>
            </div>
            <div style="border: 1px solid #E2E6EA; border-radius: 14px; padding: 26px; background: white;">
                <div style="width: 44px; height: 44px; border-radius: 10px; background: rgba(4,106,56,.12); color: #046A38; display: flex; align-items: center; justify-content: center; margin-bottom: 16px; font-size: 20px;">📊</div>
                <h4 style="font-size: 17px; margin-bottom: 8px;">Service history</h4>
                <p style="font-size: 14px; color: #5B6B82;">Log every oil change, tyre swap and service visit against mileage.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Benefits
    st.markdown("""
    <div style="padding: 60px 0; background: #0B2545; color: white; border-radius: 14px; margin: 20px 0;">
        <div style="text-align: center; max-width: 640px; margin: 0 auto 56px;">
            <span style="color: #8CE0AE; font-weight: 700; font-size: 12.5px; letter-spacing: 1.5px; text-transform: uppercase;">Benefits</span>
            <h2 style="font-size: clamp(26px, 3vw, 38px); margin-top: 10px; letter-spacing: -0.3px; font-family: 'Sora', sans-serif; color: white;">
                Built for how people actually manage vehicles here
            </h2>
        </div>
        <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 20px; max-width: 1200px; margin: 0 auto;">
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">No more paper folders</b>
                <span style="font-size: 13px; color: #AEBEDA;">Every document lives in one secure vault, accessible anywhere.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Never miss a deadline</b>
                <span style="font-size: 13px; color: #AEBEDA;">Reminders arrive weeks before expiry, not the day of.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Pay fines from your phone</b>
                <span style="font-size: 13px; color: #AEBEDA;">No queues — settle a fine in under a minute.</span>
            </div>
            <div style="background: rgba(255,255,255,.05); border: 1px solid rgba(255,255,255,.12); border-radius: 14px; padding: 22px;">
                <b style="display: block; font-family: 'Sora', sans-serif; font-size: 15px; margin-bottom: 6px;">Built around local roads</b>
                <span style="font-size: 13px; color: #AEBEDA;">Violation types and locations reflect real Bangladesh traffic patterns.</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_dashboard():
    user = current_user()
    vehicles = get_my_vehicles()
    violations = get_my_violations()
    pending = [v for v in violations if v['status'] == 'pending']
    paid = [v for v in violations if v['status'] == 'paid']
    # Admins see the platform-wide unread count; everyone else sees their own.
    my_notifs = db.notifications if user['role'] == 'admin' else [n for n in db.notifications if n['userId'] == user['id']]
    notifs = [n for n in my_notifs if not n.get('read', False)]
    docs = get_my_documents()

    first_name = user['name'].split()[0] if user.get('name') else 'there'
    st.markdown(f"""
    <div class="page-head">
        <div>
            <h2>Welcome back, {first_name} 👋</h2>
            <p>Here's a snapshot of your vehicles, fines and paperwork, all in one place.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        This dashboard summarizes everything tied to your account. Use the cards below for a quick health check,
        then jump into a section from the sidebar: <b>My Vehicles</b> to add or review a vehicle, <b>Violations</b>
        to pay a fine or file an appeal, and <b>Documents</b> to keep your papers from expiring unnoticed.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Vehicles</span><b>{len(vehicles)}</b></div>
            <div class="s-ic" style="background: #0B254522; color: #0B2545;">🚗</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Pending Fines</span><b>{len(pending)}</b></div>
            <div class="s-ic" style="background: #C8102E22; color: #C8102E;">⚠</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Paid Fines</span><b>{len(paid)}</b></div>
            <div class="s-ic" style="background: #046A3822; color: #046A38;">✓</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        soon = [v for v in vehicles if any([
            datetime.strptime(v['regExpiry'], "%Y-%m-%d") < datetime.now() + timedelta(days=30),
            datetime.strptime(v['taxExpiry'], "%Y-%m-%d") < datetime.now() + timedelta(days=30),
            datetime.strptime(v['fitnessExpiry'], "%Y-%m-%d") < datetime.now() + timedelta(days=30),
            datetime.strptime(v['insuranceExpiry'], "%Y-%m-%d") < datetime.now() + timedelta(days=30)
        ])]
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Upcoming Renewals</span><b>{len(soon)}</b></div>
            <div class="s-ic" style="background: #B4740E22; color: #B4740E;">⏰</div>
        </div>
        """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Notifications</span><b>{len(notifs)}</b></div>
            <div class="s-ic" style="background: #0B254522; color: #0B2545;">🔔</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Documents Stored</span><b>{len(docs)}</b></div>
            <div class="s-ic" style="background: #046A3822; color: #046A38;">📁</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        total_fine = sum(v['fine'] for v in pending)
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Fine Value</span><b>৳{total_fine:,}</b></div>
            <div class="s-ic" style="background: #C8102E22; color: #C8102E;">৳</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Recent activity
    st.markdown('<div class="two-col">', unsafe_allow_html=True)
    
    col1, col2 = st.columns([1.6, 1])
    with col1:
        st.markdown('<div class="panel"><div class="panel-head"><h3>Recent Activity</h3></div>', unsafe_allow_html=True)
        for act in db.activity:
            st.markdown(f"""
            <div style="display:flex; gap:12px; padding:10px 0; border-bottom:1px solid #E2E6EA;">
                <span style="font-size:18px;">{act['icon']}</span>
                <div>
                    <div style="font-size:13.5px;">{act['text']}</div>
                    <div style="font-size:11.5px; color:#5B6B82;">{act['time']}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="panel"><div class="panel-head"><h3>Upcoming Expiries</h3></div>', unsafe_allow_html=True)
        if soon:
            for v in soon[:5]:
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; padding:10px 0; border-bottom:1px solid #E2E6EA; font-size:13px;">
                    <span class="mono">{v['regNo']}</span>
                    <span class="badge badge-amber">Tax: {v['taxExpiry']}</span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.markdown('<div class="empty">No upcoming expiries 🎉</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="panel-head" style="margin-top:18px;"><h3>Quick Actions</h3></div>', unsafe_allow_html=True)
        col_a, col_b, col_c = st.columns(3)
        with col_a:
            if st.button("+ Add vehicle", use_container_width=True):
                st.session_state.page = 'vehicles'
                st.rerun()
        with col_b:
            if st.button("View violations", use_container_width=True):
                st.session_state.page = 'violations'
                st.rerun()
        with col_c:
            if st.button("Upload document", use_container_width=True):
                st.session_state.page = 'documents'
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def render_vehicles():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>My Vehicles</h2>
            <p>Register and manage every vehicle linked to your account.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Every car, motorcycle, bus or truck registered under your account shows up here as a card with its
        registration, tax, fitness and insurance expiry dates. <b>To add a vehicle</b>, use the "Add Vehicle" form
        on this page and fill in the registration number and basic details. Watch the colored badges — amber means
        a renewal is due soon, red means it has already expired.
    </div>
    """, unsafe_allow_html=True)
    
    vehicles = get_my_vehicles()
    
    # Search/filter
    col1, col2 = st.columns([2, 1])
    with col1:
        search = st.text_input("Search by reg no or model...", key="veh_search", placeholder="Search...")
    with col2:
        type_filter = st.selectbox("Filter by type", ["All types", "Private Car", "Motorcycle", "Bus", "Truck"], key="veh_filter")
    
    filtered = vehicles
    if search:
        filtered = [v for v in filtered if search.lower() in v['regNo'].lower() or search.lower() in v['model'].lower()]
    if type_filter != "All types":
        filtered = [v for v in filtered if v['type'] == type_filter]
    
    if not filtered:
        st.markdown('<div class="empty">No vehicles found. Add your first vehicle to get started.</div>', unsafe_allow_html=True)
    else:
        cols = st.columns(2)
        for i, v in enumerate(filtered):
            with cols[i % 2]:
                st.markdown(f"""
                <div class="panel" style="margin-bottom:0;">
                    <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                        <div>
                            <div class="mono" style="font-weight:700; font-size:14.5px;">{v['regNo']}</div>
                            <div style="font-size:12.5px; color:#5B6B82;">{v['manufacturer']} {v['model']} · {v['color']}</div>
                        </div>
                        <span class="badge badge-navy">{v['type']}</span>
                    </div>
                    <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; margin-top:14px; font-size:12px;">
                        <div>Reg. Expiry <br><b>{v['regExpiry']}</b> {exp_badge(v['regExpiry'])}</div>
                        <div>Road Tax <br><b>{v['taxExpiry']}</b> {exp_badge(v['taxExpiry'])}</div>
                        <div>Fitness <br><b>{v['fitnessExpiry']}</b> {exp_badge(v['fitnessExpiry'])}</div>
                        <div>Insurance <br><b>{v['insuranceExpiry']}</b> {exp_badge(v['insuranceExpiry'])}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_violations():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Traffic Violations</h2>
            <p>Search, review, pay fines or submit an appeal.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Every violation linked to your vehicles appears below with its type, date, location and fine amount.
        <ul>
            <li><b>Pending</b> fines can be paid instantly from this page or appealed if you believe it's a mistake.</li>
            <li><b>Appealed</b> fines are awaiting an admin's decision — check back under Appeals for the outcome.</li>
            <li><b>Paid</b> fines are settled; the receipt is available under Payment History.</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)
    
    violations = get_my_violations()
    
    col1, col2, col3 = st.columns([2, 1.5, 1.5])
    with col1:
        search = st.text_input("Search violation, vehicle, driver...", key="vio_search", placeholder="Search...")
    with col2:
        status_filter = st.selectbox("Status", ["all", "pending", "paid", "appealed", "waived"], key="vio_status")
    with col3:
        types = ["all"] + sorted(set(v['type'] for v in violations))
        type_filter = st.selectbox("Type", types, key="vio_type")
    
    filtered = violations
    if search:
        filtered = [v for v in filtered if search.lower() in v['violationNo'].lower() 
                    or search.lower() in v['vehicleNo'].lower()
                    or search.lower() in v['driverName'].lower()]
    if status_filter != "all":
        filtered = [v for v in filtered if v['status'] == status_filter]
    if type_filter != "all":
        filtered = [v for v in filtered if v['type'] == type_filter]
    
    if not filtered:
        st.markdown('<div class="empty">No violations match your filters.</div>', unsafe_allow_html=True)
        return
    
    # Pagination
    per_page = 6
    total_pages = (len(filtered) - 1) // per_page + 1
    page = st.session_state.get('vio_page', 1)
    if page > total_pages:
        page = total_pages
    start = (page - 1) * per_page
    end = start + per_page
    page_items = filtered[start:end]
    
    st.markdown('<div class="panel"><div style="overflow-x:auto;">', unsafe_allow_html=True)
    
    data = []
    for v in page_items:
        data.append({
            "Violation No": v['violationNo'],
            "Vehicle": v['vehicleNo'],
            "Type": v['type'],
            "Date": v['date'],
            "Location": v['location'],
            "Fine": f"৳{v['fine']:,}",
            "Status": v['status'],
            "Action": "View"
        })
    
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown('</div></div>', unsafe_allow_html=True)

    # ============ Pay a fine / File an appeal ============
    pending_now = [v for v in filtered if v['status'] == 'pending']
    if pending_now:
        st.markdown('<div class="panel"><div class="panel-head"><h3>Pay a fine or file an appeal</h3></div>', unsafe_allow_html=True)
        pick = st.selectbox(
            "Select a violation",
            pending_now,
            format_func=lambda v: f"{v['violationNo']} · {v['vehicleNo']} · {v['type']} · ৳{v['fine']:,}"
        )
        tab_pay, tab_appeal = st.tabs(["💳 Pay fine", "📝 File appeal"])

        with tab_pay:
            method = st.selectbox("Payment method", ["bKash", "Nagad", "Card", "Cash"], key=f"pay_method_{pick['id']}")
            if st.button("Pay now", key=f"pay_btn_{pick['id']}", type="primary"):
                pick['status'] = 'paid'
                db.payments.append({
                    'id': db._nid('p'), 'violationId': pick['id'], 'violationNo': pick['violationNo'],
                    'method': method, 'amount': pick['fine'],
                    'date': db._fmt_date(datetime.now()), 'status': 'completed',
                    'receiptNo': f'RCPT-{random.randint(100000, 999999)}'
                })
                st.success(f"Payment of ৳{pick['fine']:,} confirmed via {method}!")
                st.rerun()

        with tab_appeal:
            reason = st.text_area("Reason for appeal", key=f"appeal_reason_{pick['id']}",
                                   placeholder="Explain why this violation should be reviewed...")
            if st.button("Submit appeal", key=f"appeal_btn_{pick['id']}"):
                if not reason.strip():
                    st.error("Please provide a reason for your appeal.")
                else:
                    pick['status'] = 'appealed'
                    db.appeals.append({
                        'id': db._nid('a'), 'violationId': pick['id'], 'violationNo': pick['violationNo'],
                        'reason': reason.strip(), 'status': 'pending',
                        'submittedDate': db._fmt_date(datetime.now()),
                        'timeline': [{'label': 'Appeal submitted', 'date': db._fmt_date(datetime.now())}],
                        'adminResponse': None
                    })
                    st.success("Appeal submitted! An admin will review it soon.")
                    st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

    # Pagination controls — a windowed pager that scales to any number of pages
    # instead of assuming there are 5 or fewer (which used to overflow every
    # page past #4 into the same column).
    if total_pages > 1:
        window = 5
        half = window // 2
        window_start = max(1, min(page - half, total_pages - window + 1))
        window_start = max(window_start, 1)
        window_end = min(total_pages, window_start + window - 1)
        page_numbers = list(range(window_start, window_end + 1))

        cols = st.columns([1] + [1] * len(page_numbers) + [1])
        with cols[0]:
            if st.button("‹", disabled=page == 1):
                st.session_state.vio_page = page - 1
                st.rerun()
        for idx, i in enumerate(page_numbers, start=1):
            with cols[idx]:
                if st.button(str(i), use_container_width=True, type="primary" if i == page else "secondary"):
                    st.session_state.vio_page = i
                    st.rerun()
        with cols[-1]:
            if st.button("›", disabled=page == total_pages):
                st.session_state.vio_page = page + 1
                st.rerun()

def render_payments():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Payment History</h2>
            <p>All fine payments made across your vehicles.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        This is your receipt log — every completed payment, the method used (bKash, Nagad, Card or Cash), and the
        violation it settled. If a fine is still <b>unpaid</b>, it won't show here yet; pay it first from the
        Violations page and it will automatically appear in this history.
    </div>
    """, unsafe_allow_html=True)
    
    payments = get_my_payments()
    
    if not payments:
        st.markdown('<div class="empty">No payments yet.</div>', unsafe_allow_html=True)
        return
    
    total = sum(p['amount'] for p in payments)
    methods = {}
    for p in payments:
        methods[p['method']] = methods.get(p['method'], 0) + 1
    most_used = max(methods.items(), key=lambda x: x[1])[0] if methods else "—"
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Paid</span><b>৳{total:,}</b></div>
            <div class="s-ic" style="background: #046A3822; color: #046A38;">৳</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Transactions</span><b>{len(payments)}</b></div>
            <div class="s-ic" style="background: #0B254522; color: #0B2545;">🧾</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Most used method</span><b>{most_used}</b></div>
            <div class="s-ic" style="background: #B4740E22; color: #B4740E;">📱</div>
        </div>
        """, unsafe_allow_html=True)
    
    data = []
    for p in payments:
        data.append({
            "Receipt No": p['receiptNo'],
            "Violation": p['violationNo'],
            "Method": p['method'],
            "Amount": f"৳{p['amount']:,}",
            "Date": p['date'],
            "Status": p['status']
        })
    
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_documents():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Document Vault</h2>
            <p>Store and access every vehicle document securely.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Keep your NID, license, registration, fitness, tax token and insurance papers in one place instead of a
        folder at home. <b>To add a document</b>, use the upload form below and pick the correct document type and
        expiry date — DriveBD will flag it as "expiring" as the date gets close, and "expired" once it's passed.
    </div>
    """, unsafe_allow_html=True)
    
    docs = get_my_documents()
    vehicles = get_my_vehicles()
    
    if not vehicles:
        st.markdown('<div class="empty">Add a vehicle first to start uploading documents.</div>', unsafe_allow_html=True)
        return
    
    if not docs:
        st.markdown('<div class="empty">No documents uploaded yet.</div>', unsafe_allow_html=True)
    
    # Upload form
    with st.expander("📤 Upload new document"):
        col1, col2 = st.columns(2)
        with col1:
            doc_type = st.selectbox("Document type", [
                "Driving Licence", "Registration Certificate", "Fitness Certificate",
                "Insurance", "Tax Receipt", "Emission Certificate"
            ])
        with col2:
            vehicle = st.selectbox("Vehicle", vehicles, format_func=lambda v: v['regNo'])
        
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'png', 'jpg', 'jpeg'])
        if st.button("Upload") and uploaded_file:
            # In a real app, we'd save the file
            db.documents.append({
                'id': db._nid('d'),
                'vehicleId': vehicle['id'],
                'type': doc_type,
                'name': doc_type,
                'dataUrl': None,
                'uploadedDate': db._fmt_date(datetime.now())
            })
            st.success("Document uploaded successfully!")
            st.rerun()
    
    # Display documents
    if docs:
        cols = st.columns(4)
        for i, doc in enumerate(docs):
            with cols[i % 4]:
                veh = next((v for v in vehicles if v['id'] == doc['vehicleId']), None)
                st.markdown(f"""
                <div class="doc-card">
                    <div class="thumb">📄</div>
                    <b>{doc['type']}</b>
                    <span>{veh['regNo'] if veh else ''} · {doc['uploadedDate']}</span>
                    <div class="doc-actions">
                        <span style="font-size: 12px; color: #5B6B82;">✓ Stored</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)

def render_service():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Service History</h2>
            <p>Track maintenance and set reminders by mileage.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        A running log of every oil change, tyre swap or workshop visit for your vehicles, along with cost and
        mileage at the time. Logging service visits consistently makes it easy to spot patterns — like a vehicle
        needing more frequent servicing than expected — and gives you a maintenance record if you ever resell it.
    </div>
    """, unsafe_allow_html=True)
    
    service = get_my_service()
    
    if not service:
        st.markdown('<div class="empty">No service records yet.</div>', unsafe_allow_html=True)
        return
    
    data = []
    for s in service:
        data.append({
            "Vehicle": s['vehicleNo'],
            "Service Type": s['type'],
            "Date": s['date'],
            "Mileage": f"{s['mileage']:,} km",
            "Cost": f"৳{s['cost']:,}",
            "Notes": s['notes'][:30] + "..." if len(s['notes']) > 30 else s['notes']
        })
    
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    df = pd.DataFrame(data)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown('</div>', unsafe_allow_html=True)

def render_appeals():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Appeals</h2>
            <p>Track the status of every violation you've contested.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        If you believe a violation was issued in error, submit an appeal from the Violations page with your reason —
        it lands here as <b>pending</b>. An admin reviews it and either <b>approves</b> it (the fine is waived) or
        <b>rejects</b> it (the fine remains due and payable). You'll see the admin's comment once a decision is made.
    </div>
    """, unsafe_allow_html=True)
    
    appeals = get_my_appeals()
    
    if not appeals:
        st.markdown('<div class="empty">No appeals submitted.</div>', unsafe_allow_html=True)
        return
    
    for a in appeals:
        st.markdown(f"""
        <div class="panel">
            <div class="panel-head">
                <h3 class="mono">{a['violationNo']}</h3>
                {status_badge(a['status'])}
            </div>
            <p style="font-size:13.5px; margin-bottom:14px;"><b>Reason:</b> {a['reason']}</p>
            <ul class="timeline">
                {"".join(f'<li><b>{t["label"]}</b><span>{t["date"]}</span></li>' for t in a.get('timeline', []))}
            </ul>
            {f'<div class="panel" style="background:#F6F7F5; margin-top:10px;"><b style="font-size:12.5px;">Admin response</b><p style="font-size:13px; margin-top:4px;">{a["adminResponse"]}</p></div>' if a.get('adminResponse') else ''}
        </div>
        """, unsafe_allow_html=True)

def render_notifications():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Notification Center</h2>
            <p>Stay on top of renewals, fines and payments.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        DriveBD sends a notification whenever something needs your attention — a new fine, a document about to
        expire, or a payment confirmation. <b>Info</b> notices are routine updates, <b>warning</b> means something
        is approaching a deadline, and <b>alert</b> means action is needed soon.
    </div>
    """, unsafe_allow_html=True)
    
    notifications = db.notifications
    user = current_user()
    user_notifs = [n for n in notifications if n['userId'] == user['id']]
    
    if not user_notifs:
        st.markdown('<div class="empty">No notifications.</div>', unsafe_allow_html=True)
        return
    
    # Filter
    filter_type = st.selectbox("Filter", ["all", "unread", "violation", "payment", "reminder", "system"])
    
    filtered = user_notifs
    if filter_type == "unread":
        filtered = [n for n in filtered if not n['read']]
    elif filter_type != "all":
        filtered = [n for n in filtered if n['category'] == filter_type]
    
    for n in filtered:
        color = {"violation": "#C8102E", "payment": "#046A38", "reminder": "#B4740E", "system": "#0B2545"}.get(n['category'], "#0B2545")
        icon = {"violation": "⚠", "payment": "৳", "reminder": "⏰", "system": "ℹ"}.get(n['category'], "🔔")
        st.markdown(f"""
        <div class="notif-item {'unread' if not n['read'] else ''}">
            <div class="notif-ic" style="background: {color}22; color: {color};">{icon}</div>
            <div style="flex:1;">
                <b>{n['title']}</b>
                <p>{n['message']}</p>
            </div>
            <span class="time">{n['date']}</span>
            <div style="display:flex; gap:4px; margin-left:8px;">
                {f'<span style="font-size: 11px; color: #046A38;">● New</span>' if not n['read'] else ''}
            </div>
        </div>
        """, unsafe_allow_html=True)

def render_brta():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>BRTA Lookup (Mock Service)</h2>
            <p>Simulates GET /api/brta/vehicle, /tax and /fitness endpoints with realistic sample data.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Type in any registration number to see what a real-time BRTA lookup would return: ownership, tax token
        status and fitness certificate validity. This is a <b>mock/demo endpoint</b> — it generates plausible sample
        data for any plate you enter and is not connected to the real BRTA database.
    </div>
    """, unsafe_allow_html=True)
    
    plate = st.text_input("Enter registration number", placeholder="e.g. DHAKA METRO GA 11-2481")
    
    if st.button("Lookup") and plate:
        v = next((v for v in db.vehicles if v['regNo'].lower() == plate.lower()), None)
        if v:
            result = {
                "vehicle": {
                    "plate": v['regNo'],
                    "type": v['type'],
                    "manufacturer": v['manufacturer'],
                    "model": v['model'],
                    "owner": owner_name(v['id']),
                    "engineNo": v['engine'],
                    "chassisNo": v['chassis']
                },
                "tax": {
                    "plate": v['regNo'],
                    "status": "valid" if datetime.strptime(v['taxExpiry'], "%Y-%m-%d") > datetime.now() else "expired",
                    "expiry": v['taxExpiry']
                },
                "fitness": {
                    "plate": v['regNo'],
                    "status": "valid" if datetime.strptime(v['fitnessExpiry'], "%Y-%m-%d") > datetime.now() else "expired",
                    "expiry": v['fitnessExpiry']
                }
            }
        else:
            result = {
                "vehicle": {
                    "plate": plate,
                    "type": "Private Car",
                    "manufacturer": "Toyota",
                    "model": "Axio",
                    "owner": "Unregistered in DriveBD (simulated BRTA record)",
                    "engineNo": f"ENG{random.randint(100000, 999999)}",
                    "chassisNo": f"CHS{random.randint(100000, 999999)}"
                },
                "tax": {
                    "plate": plate,
                    "status": random.choice(["valid", "expired"]),
                    "expiry": db._fmt_date(db._days_from_now(random.randint(-30, 300)))
                },
                "fitness": {
                    "plate": plate,
                    "status": random.choice(["valid", "expired"]),
                    "expiry": db._fmt_date(db._days_from_now(random.randint(-30, 300)))
                }
            }
        
        col1, col2 = st.columns(2)
        with col1:
            st.json(result['vehicle'])
        with col2:
            st.json(result['tax'])
            st.json(result['fitness'])

def render_aidemo():
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>AI Plate Recognition — Demo</h2>
            <p>Upload a vehicle photo to simulate automatic plate detection and violation generation.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Upload any photo containing a vehicle and this demo will simulate what an automated traffic camera pipeline
        might detect — a plate number, vehicle type, and a possible violation. <b>This is an educational, rule-based
        demonstration only</b> — it does not perform real computer-vision plate recognition.
    </div>
    """, unsafe_allow_html=True)
    
    uploaded = st.file_uploader("Upload vehicle image", type=['jpg', 'jpeg', 'png'])
    
    if uploaded:
        st.image(uploaded, width=300)
        
        if st.button("Run detection"):
            confidence = random.randint(82, 98)
            plate = f"DHAKA METRO GA {random.randint(10,99)}-{random.randint(1000,9999)}"
            vtype = random.choice(["Red Light Crossing", "Speeding", "Wrong Lane", "Illegal Parking",
                                   "Helmet Violation", "Seat Belt Violation"])
            
            st.markdown(f"""
            <div class="panel" style="background: #F6F7F5;">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <div><b>Detected plate:</b> <span class="mono">{plate}</span></div>
                    <span class="badge badge-green">{confidence}% confidence</span>
                </div>
                <p style="font-size:13px; color:#5B6B82; margin-top:10px;">
                    Suggested violation: <b>{vtype}</b>. Evidence image stored to vault.
                </p>
            </div>
            """, unsafe_allow_html=True)

def render_profile():
    user = current_user()
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Profile Settings</h2>
            <p>Manage your personal information and security.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        Keep your contact details accurate so renewal reminders and fine notices reach you. Use the password
        section to change your login password — you'll need to enter your current password first as a security check.
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        name = st.text_input("Full name", user['name'])
        phone = st.text_input("Phone", user['phone'])
        license_no = st.text_input("Driving Licence No.", user['license'])
        nid = st.text_input("NID Number", user['nid'])
        emergency = st.text_input("Emergency Contact", user['emergency'])
        address = st.text_area("Address", user['address'])
        
        if st.button("Save changes"):
            user['name'] = name
            user['phone'] = phone
            user['license'] = license_no
            user['nid'] = nid
            user['emergency'] = emergency
            user['address'] = address
            st.success("Profile updated!")
            st.rerun()
    
    with col2:
        st.markdown(f"""
        <div class="panel" style="text-align:center;">
            <div style="width:70px; height:70px; border-radius:50%; background:#0B2545; color:white; 
                        display:flex; align-items:center; justify-content:center; margin:0 auto 12px; 
                        font-size:22px; font-weight:700;">
                {user['avatar']}
            </div>
            <b>{user['name']}</b><br>
            <span style="color:#5B6B82; font-size:13px;">
                {user['role'].title()} · joined {user['joined']}
            </span>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="panel"><div class="panel-head"><h3>Change Password</h3></div>', unsafe_allow_html=True)
        cur = st.text_input("Current password", type="password")
        new = st.text_input("New password", type="password")
        if st.button("Update password") and cur and new:
            if cur == user['password']:
                if len(new) >= 6:
                    user['password'] = new
                    st.success("Password updated successfully!")
                else:
                    st.error("New password must be at least 6 characters")
            else:
                st.error("Current password is incorrect")
        st.markdown('</div>', unsafe_allow_html=True)

def render_admin():
    if current_user()['role'] != 'admin':
        st.error("Admin access required")
        return
    
    st.markdown("""
    <div class="page-head">
        <div>
            <h2>Admin Panel</h2>
            <p>Platform-wide statistics and management tools.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    <div class="page-help">
        This panel is only visible to <b>admin</b> accounts. Use the <b>Users</b> tab to review or change a user's
        role, <b>Vehicles</b> and <b>Violations</b> to see platform-wide activity, and <b>Appeals</b> to approve
        (waive the fine) or reject pending appeals — the citizen who filed it will see your decision immediately.
    </div>
    """, unsafe_allow_html=True)
    
    total_fines = sum(p['amount'] for p in db.payments)
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Users</span><b>{len(db.users)}</b></div>
            <div class="s-ic" style="background: #0B254522; color: #0B2545;">👤</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Vehicles</span><b>{len(db.vehicles)}</b></div>
            <div class="s-ic" style="background: #046A3822; color: #046A38;">🚗</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Violations</span><b>{len(db.violations)}</b></div>
            <div class="s-ic" style="background: #C8102E22; color: #C8102E;">⚠</div>
        </div>
        """, unsafe_allow_html=True)
    with col4:
        st.markdown(f"""
        <div class="stat-card">
            <div><span>Total Revenue</span><b>৳{total_fines:,}</b></div>
            <div class="s-ic" style="background: #B4740E22; color: #B4740E;">৳</div>
        </div>
        """, unsafe_allow_html=True)
    
    tab1, tab2, tab3, tab4 = st.tabs(["Users", "Vehicles", "Violations", "Appeals"])
    
    with tab1:
        data = []
        for u in db.users:
            data.append({
                "Name": u['name'],
                "Email": u['email'],
                "Role": u['role'],
                "Status": u['status'],
                "Joined": u['joined']
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    
    with tab2:
        data = []
        for v in db.vehicles:
            data.append({
                "Reg No": v['regNo'],
                "Owner": owner_name(v['id']),
                "Type": v['type'],
                "Status": v['status'],
                "Insurance": v['insuranceExpiry']
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    
    with tab3:
        data = []
        for v in db.violations:
            data.append({
                "No": v['violationNo'],
                "Vehicle": v['vehicleNo'],
                "Type": v['type'],
                "Fine": f"৳{v['fine']:,}",
                "Status": v['status']
            })
        st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)
    
    with tab4:
        if not db.appeals:
            st.markdown('<div class="empty">No appeals submitted yet.</div>', unsafe_allow_html=True)
        else:
            data = []
            for a in db.appeals:
                data.append({
                    "Violation": a['violationNo'],
                    "Reason": a['reason'][:50] + "..." if len(a['reason']) > 50 else a['reason'],
                    "Status": a['status'],
                    "Submitted": a['submittedDate']
                })
            st.dataframe(pd.DataFrame(data), use_container_width=True, hide_index=True)

            pending_appeals = [a for a in db.appeals if a['status'] == 'pending']
            if pending_appeals:
                st.markdown('<div class="panel-head" style="margin-top:16px;"><h3>Review a pending appeal</h3></div>', unsafe_allow_html=True)
                pick = st.selectbox(
                    "Select appeal",
                    pending_appeals,
                    format_func=lambda a: f"{a['violationNo']} · {a['reason'][:40]}"
                )
                comment = st.text_area("Admin comment", key=f"admin_comment_{pick['id']}")
                col_a, col_b = st.columns(2)
                with col_a:
                    if st.button("✅ Approve (waive fine)", key=f"approve_{pick['id']}", type="primary", use_container_width=True):
                        pick['status'] = 'approved'
                        pick['adminResponse'] = comment.strip() or "Appeal approved. The fine has been waived."
                        pick.setdefault('timeline', []).append({'label': 'Approved', 'date': db._fmt_date(datetime.now())})
                        vio = next((v for v in db.violations if v['id'] == pick['violationId']), None)
                        if vio:
                            vio['status'] = 'waived'
                        st.success("Appeal approved and fine waived.")
                        st.rerun()
                with col_b:
                    if st.button("❌ Reject", key=f"reject_{pick['id']}", use_container_width=True):
                        pick['status'] = 'rejected'
                        pick['adminResponse'] = comment.strip() or "Appeal rejected. The fine remains due."
                        pick.setdefault('timeline', []).append({'label': 'Rejected', 'date': db._fmt_date(datetime.now())})
                        vio = next((v for v in db.violations if v['id'] == pick['violationId']), None)
                        if vio:
                            vio['status'] = 'pending'
                        st.warning("Appeal rejected.")
                        st.rerun()

# ================= MAIN APP =================
def main():
    load_css()
    
    # Initialize session state
    if 'user' not in st.session_state:
        st.session_state.user = None
    if 'page' not in st.session_state:
        st.session_state.page = 'landing'
    
    if not is_logged_in():
        # Landing page
        render_landing()
        
        st.divider()
        st.markdown('<p style="text-align:center; color: #5B6B82; font-size: 14px;">DriveBD Capstone Project · Built with Streamlit · Not affiliated with BRTA · All data is mock/demo data</p>', unsafe_allow_html=True)

        st.markdown('<div id="get-started"></div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="page-head" style="display:block; margin-bottom: 6px;">
            <h2>Get started</h2>
            <p>Log in to an existing account, or create a free driver/owner account below. Registration takes less than a minute — no document upload is required to get started, and you can add vehicles once you're in.</p>
        </div>
        """, unsafe_allow_html=True)

        with st.expander("🔑 Need a quick demo login? Click here for test credentials"):
            st.markdown("""
            Use any of these to explore the portal without registering:

            | Role | Email | Password |
            |---|---|---|
            | Admin | `admin@drivebd.gov.bd` | `Admin@123` |
            | Driver | `driver@drivebd.gov.bd` | `Demo@123` |
            | Owner | `owner@drivebd.gov.bd` | `Demo@123` |

            Admin can manage users, review appeals, and adjust system settings. Driver and Owner accounts show the day-to-day citizen experience.
            """)

        # Login/Register tabs
        tab1, tab2 = st.tabs(["Log In", "Create Account"])
        
        with tab1:
            st.markdown('<p style="color: var(--muted); font-size: 13.5px; margin-bottom: 10px;">Enter the email and password for your account. Use the demo credentials above if you just want to look around.</p>', unsafe_allow_html=True)
            with st.form("login_form"):
                email = st.text_input("Email", placeholder="you@example.com")
                password = st.text_input("Password", type="password", placeholder="Your password")
                if st.form_submit_button("Log In", use_container_width=True):
                    if not email.strip() or not password:
                        st.error("Please enter both your email and password.")
                    else:
                        ok, msg = login_user(email, password)
                        if ok:
                            st.session_state.page = 'dashboard'
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
        
        with tab2:
            st.markdown('<p style="color: var(--muted); font-size: 13.5px; margin-bottom: 10px;">Create a free account as a <b>Driver</b> (you drive but may not own the vehicle) or an <b>Owner</b> (you own one or more vehicles). Admin accounts cannot be self-registered for security reasons.</p>', unsafe_allow_html=True)
            with st.form("register_form"):
                name = st.text_input("Full name", placeholder="e.g. Rafiq Ahmed")
                email = st.text_input("Email", placeholder="you@example.com")
                phone = st.text_input("Phone number", placeholder="e.g. 01712345678")
                nid = st.text_input("NID number", placeholder="10/13/17-digit National ID (optional)")
                role = st.selectbox("Account type", ["driver", "owner"], help="Driver: you operate a vehicle. Owner: you own one or more vehicles and manage their paperwork.")
                password = st.text_input("Password", type="password", placeholder="At least 6 characters")
                confirm_password = st.text_input("Confirm password", type="password", placeholder="Re-enter your password")
                
                if st.form_submit_button("Create Account", use_container_width=True):
                    name = (name or "").strip()
                    email = (email or "").strip()
                    phone = (phone or "").strip()
                    nid = (nid or "").strip()
                    if not all([name, email, password]):
                        st.error("Name, email and password are required.")
                    elif "@" not in email or "." not in email.split("@")[-1]:
                        st.error("Please enter a valid email address.")
                    elif phone and not re.match(r'^01[3-9]\d{8}$', phone):
                        st.error("Please enter a valid Bangladeshi mobile number (e.g. 01712345678).")
                    elif nid and not re.match(r'^\d{10}$|^\d{13}$|^\d{17}$', nid):
                        st.error("NID should be 10, 13 or 17 digits, matching Bangladesh's NID formats.")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters.")
                    elif password != confirm_password:
                        st.error("Passwords do not match. Please re-type them.")
                    else:
                        ok, msg = register_user(name, email, password, role, phone, nid)
                        if ok:
                            st.session_state.page = 'dashboard'
                            st.success(msg)
                            st.rerun()
                        else:
                            st.error(msg)
    else:
        # App layout
        user = current_user()
        
        # Header
        col1, col2, col3 = st.columns([2, 3, 1])
        with col1:
            st.markdown(f'<p class="main-header">🚗 DriveBD</p>', unsafe_allow_html=True)
        with col2:
            st.markdown(f'<p class="sub-header">Smart Driver & Vehicle Owner Portal</p>', unsafe_allow_html=True)
        with col3:
            st.markdown(f"""
            <div style="text-align: right; padding-top: 8px;">
                <span style="font-weight: 600;">{user['name']}</span>
                <span style="color: #5B6B82; font-size: 12px; display: block;">{user['role'].title()}</span>
            </div>
            """, unsafe_allow_html=True)
        
        # Sidebar navigation
        with st.sidebar:
            st.markdown(f"""
            <div style="text-align: center; padding: 16px 0; border-bottom: 1px solid #E2E6EA;">
                <div style="width: 56px; height: 56px; border-radius: 50%; background: #0B2545; color: white; 
                            display: flex; align-items: center; justify-content: center; margin: 0 auto 8px; 
                            font-size: 20px; font-weight: 700;">
                    {user['avatar']}
                </div>
                <div style="font-weight: 600;">{user['name']}</div>
                <div style="color: #5B6B82; font-size: 12px;">{user['role'].title()}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("### Overview")
            if st.button(nav_label("📊 Dashboard", 'dashboard'), use_container_width=True, type="primary" if st.session_state.page == 'dashboard' else "secondary"):
                st.session_state.page = 'dashboard'
                st.rerun()
            
            st.markdown("### Manage")
            if st.button(nav_label("🚗 My Vehicles", 'my_vehicles'), use_container_width=True, type="primary" if st.session_state.page == 'vehicles' else "secondary"):
                st.session_state.page = 'vehicles'
                st.rerun()
            if st.button(nav_label("⚠ Violations", 'violations'), use_container_width=True, type="primary" if st.session_state.page == 'violations' else "secondary"):
                st.session_state.page = 'violations'
                st.rerun()
            if st.button(nav_label("💰 Payments", 'payments'), use_container_width=True, type="primary" if st.session_state.page == 'payments' else "secondary"):
                st.session_state.page = 'payments'
                st.rerun()
            if st.button(nav_label("📁 Documents", 'documents'), use_container_width=True, type="primary" if st.session_state.page == 'documents' else "secondary"):
                st.session_state.page = 'documents'
                st.rerun()
            if st.button(nav_label("🔧 Service", 'service'), use_container_width=True, type="primary" if st.session_state.page == 'service' else "secondary"):
                st.session_state.page = 'service'
                st.rerun()
            if st.button(nav_label("📝 Appeals", 'appeals'), use_container_width=True, type="primary" if st.session_state.page == 'appeals' else "secondary"):
                st.session_state.page = 'appeals'
                st.rerun()
            
            st.markdown("### Tools")
            if st.button(nav_label("🔎 BRTA Lookup", 'brta'), use_container_width=True, type="primary" if st.session_state.page == 'brta' else "secondary"):
                st.session_state.page = 'brta'
                st.rerun()
            if st.button(nav_label("✦ AI Demo", 'aidemo'), use_container_width=True, type="primary" if st.session_state.page == 'aidemo' else "secondary"):
                st.session_state.page = 'aidemo'
                st.rerun()
            if st.button(nav_label("🔔 Notifications", 'notifications'), use_container_width=True, type="primary" if st.session_state.page == 'notifications' else "secondary"):
                st.session_state.page = 'notifications'
                st.rerun()
            
            st.markdown("### Account")
            if st.button(nav_label("⚙ Profile", 'profile'), use_container_width=True, type="primary" if st.session_state.page == 'profile' else "secondary"):
                st.session_state.page = 'profile'
                st.rerun()
            
            if user['role'] == 'admin':
                st.markdown("### Administration")
                if st.button(nav_label("🛡 Admin Panel", 'admin'), use_container_width=True, type="primary" if st.session_state.page == 'admin' else "secondary"):
                    st.session_state.page = 'admin'
                    st.rerun()
            
            st.divider()
            if st.button(nav_label("🚪 Log out", 'logout'), use_container_width=True):
                logout_user()
        
        # Main content
        # Safety net: if the requested page doesn't exist, or a non-admin somehow
        # ends up with 'admin' as their page (e.g. role changed mid-session), fall
        # back to the dashboard instead of showing a blank screen or restricted page.
        valid_pages = {'dashboard', 'vehicles', 'violations', 'payments', 'documents',
                       'service', 'appeals', 'brta', 'aidemo', 'notifications', 'profile', 'admin'}
        if st.session_state.page not in valid_pages or (
            st.session_state.page == 'admin' and user['role'] != 'admin'
        ):
            st.session_state.page = 'dashboard'

        if st.session_state.page == 'dashboard':
            render_dashboard()
        elif st.session_state.page == 'vehicles':
            render_vehicles()
        elif st.session_state.page == 'violations':
            render_violations()
        elif st.session_state.page == 'payments':
            render_payments()
        elif st.session_state.page == 'documents':
            render_documents()
        elif st.session_state.page == 'service':
            render_service()
        elif st.session_state.page == 'appeals':
            render_appeals()
        elif st.session_state.page == 'brta':
            render_brta()
        elif st.session_state.page == 'aidemo':
            render_aidemo()
        elif st.session_state.page == 'notifications':
            render_notifications()
        elif st.session_state.page == 'profile':
            render_profile()
        elif st.session_state.page == 'admin':
            render_admin()

if __name__ == "__main__":
    main()
