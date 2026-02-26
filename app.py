"""
St. George's School Management System
Complete School Administration Platform
Version: 2.0.0
Author: School Administration Team
Last Updated: 2026-02-26
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, date
import hashlib
import hmac
import io
import os
import json
import base64
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import warnings
warnings.filterwarnings('ignore')

# =============================================================================
# PAGE CONFIGURATION
# =============================================================================

st.set_page_config(
    page_title="St. George's School",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'Get Help': 'https://docs.sgs.edu.my',
        'Report a bug': 'mailto:admin@sgs.edu.my',
        'About': '# St. George\'s School Management System\nVersion 2.0.0'
    }
)

# =============================================================================
# CUSTOM CSS FOR MODERN, MINIMALIST DESIGN
# =============================================================================

st.markdown("""
<style>
    /* Import fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
        background-color: #fafbfc;
    }
    
    /* Headers */
    .main-header {
        font-size: 2.2rem;
        font-weight: 500;
        color: #1e293b;
        margin: 0.5rem 0 1.5rem 0;
        padding-bottom: 0.75rem;
        border-bottom: 2px solid #e2e8f0;
        letter-spacing: -0.02em;
    }
    
    .sub-header {
        font-size: 1.4rem;
        font-weight: 500;
        color: #334155;
        margin: 1.5rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .section-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #475569;
        margin: 1rem 0 0.5rem 0;
        text-transform: uppercase;
        letter-spacing: 0.03em;
    }
    
    /* Cards */
    .stat-card {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1);
        border: 1px solid #e9ecef;
        transition: all 0.2s ease;
    }
    
    .stat-card:hover {
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1), 0 2px 4px -1px rgba(0,0,0,0.06);
        transform: translateY(-2px);
    }
    
    .stat-value {
        font-size: 2.2rem;
        font-weight: 600;
        color: #0f172a;
        line-height: 1.2;
    }
    
    .stat-label {
        font-size: 0.9rem;
        color: #64748b;
        margin-top: 0.3rem;
        font-weight: 400;
    }
    
    .stat-icon {
        font-size: 2rem;
        opacity: 0.7;
    }
    
    /* Data cards */
    .data-card {
        background: white;
        padding: 1.2rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
        margin-bottom: 0.8rem;
    }
    
    .data-card-title {
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .data-card-subtitle {
        font-size: 0.85rem;
        color: #64748b;
    }
    
    /* Buttons */
    .stButton > button {
        background: #3b82f6;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1.5rem;
        font-weight: 500;
        font-size: 0.9rem;
        transition: all 0.2s ease;
        border: 1px solid #2563eb;
    }
    
    .stButton > button:hover {
        background: #2563eb;
        border-color: #1d4ed8;
        box-shadow: 0 4px 6px -1px rgba(37, 99, 235, 0.2);
    }
    
    /* Secondary button */
    .stButton > button.secondary {
        background: white;
        color: #1e293b;
        border: 1px solid #cbd5e1;
    }
    
    .stButton > button.secondary:hover {
        background: #f8fafc;
        border-color: #94a3b8;
    }
    
    /* Metrics */
    .metric-container {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #e9ecef;
    }
    
    /* Tables */
    .dataframe {
        font-family: 'Inter', sans-serif;
        border-collapse: collapse;
        width: 100%;
    }
    
    .dataframe th {
        background: #f8fafc;
        color: #1e293b;
        font-weight: 600;
        font-size: 0.9rem;
        padding: 0.75rem;
        text-align: left;
        border-bottom: 2px solid #e2e8f0;
    }
    
    .dataframe td {
        padding: 0.75rem;
        border-bottom: 1px solid #e2e8f0;
        color: #334155;
    }
    
    /* Alerts */
    .alert-success {
        background: #f0fdf4;
        border-left: 4px solid #22c55e;
        padding: 1rem;
        border-radius: 8px;
        color: #166534;
    }
    
    .alert-warning {
        background: #fffbeb;
        border-left: 4px solid #f59e0b;
        padding: 1rem;
        border-radius: 8px;
        color: #92400e;
    }
    
    .alert-info {
        background: #eff6ff;
        border-left: 4px solid #3b82f6;
        padding: 1rem;
        border-radius: 8px;
        color: #1e40af;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Sidebar */
    .css-1d391kg {
        background-color: #ffffff;
        border-right: 1px solid #e9ecef;
    }
    
    /* Input fields */
    .stTextInput > div > div > input {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
        padding: 0.5rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #3b82f6;
        box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.1);
    }
    
    /* Select box */
    .stSelectbox > div > div > select {
        border-radius: 8px;
        border: 1px solid #cbd5e1;
    }
    
    /* Progress bars */
    .stProgress > div > div > div {
        background-color: #3b82f6;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        border-bottom: 1px solid #e2e8f0;
    }
    
    .stTabs [data-baseweb="tab"] {
        color: #64748b;
        font-weight: 500;
    }
    
    .stTabs [aria-selected="true"] {
        color: #3b82f6;
        border-bottom-color: #3b82f6;
    }
</style>
""", unsafe_allow_html=True)

# =============================================================================
# SESSION STATE INITIALIZATION
# =============================================================================

def init_session_state():
    """Initialize all session state variables"""
    
    defaults = {
        'authenticated': False,
        'user_role': None,
        'username': None,
        'user_email': None,
        'login_time': None,
        'current_page': 'Dashboard',
        'data_cache': {},
        'last_refresh': datetime.now(),
        'filters': {},
        'notifications': [],
        'audit_log': []
    }
    
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

init_session_state()

# =============================================================================
# AUTHENTICATION SYSTEM
# =============================================================================

class Authentication:
    """Handle user authentication and session management"""
    
    def __init__(self):
        self.users = {
            'admin': {
                'password': self._hash_password('admin123'),
                'role': 'admin',
                'name': 'System Administrator',
                'email': 'admin@sgs.edu.my',
                'department': 'Administration',
                'avatar': '👨‍💼'
            },
            'principal': {
                'password': self._hash_password('principal123'),
                'role': 'principal',
                'name': 'Dr. Elizabeth Warren',
                'email': 'principal@sgs.edu.my',
                'department': 'Leadership',
                'avatar': '👩‍🏫'
            },
            'james.chen': {
                'password': self._hash_password('teacher123'),
                'role': 'teacher',
                'name': 'Mr. James Chen',
                'email': 'j.chen@sgs.edu.my',
                'department': 'Mathematics',
                'avatar': '👨‍🏫'
            },
            'sarah.lim': {
                'password': self._hash_password('teacher123'),
                'role': 'teacher',
                'name': 'Ms. Sarah Lim',
                'email': 's.lim@sgs.edu.my',
                'department': 'Languages',
                'avatar': '👩‍🏫'
            },
            'linda.tan': {
                'password': self._hash_password('staff123'),
                'role': 'staff',
                'name': 'Ms. Linda Tan',
                'email': 'l.tan@sgs.edu.my',
                'department': 'Administration',
                'avatar': '👩‍💼'
            }
        }
    
    def _hash_password(self, password):
        """Simple password hashing (use bcrypt in production)"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def authenticate(self, username, password):
        """Authenticate user credentials"""
        if username in self.users:
            hashed_input = self._hash_password(password)
            if hashed_input == self.users[username]['password']:
                return True, self.users[username]
        return False, None
    
    def get_user_info(self, username):
        """Get user information"""
        return self.users.get(username, None)

# =============================================================================
# DATA MANAGER
# =============================================================================

class DataManager:
    """Handle all data operations"""
    
    def __init__(self):
        self.data_files = {
            'students': 'STUDENTS',
            'parents': 'PARENTS',
            'teachers': 'TEACHERS',
            'staff': 'STAFF',
            'results': 'ACADEMIC_RESULTS',
            'timetable': 'TIMETABLE'
        }
    
    def load_sample_data(self):
        """Load sample data for demonstration"""
        
        # Students data
        students = pd.DataFrame({
            'StudentID': [f'STU{str(i).zfill(4)}' for i in range(1, 51)],
            'FullName': [
                'Sarah Ali', 'Liyana Lee', 'Ahmad Tan', 'Emily Ong', 'Daniel Chong',
                'Nur Aisyah', 'Raj Kumar', 'Tan Wei Ming', 'Siti Nurhaliza', 'Jason Lim',
                'Hannah Wong', 'Amir Rahman', 'Priya Krishnan', 'Wei Ling', 'Muhammad Faiz',
                'Kavita Raj', 'Ethan Goh', 'Aina Hassan', 'Vicknesh Ganesan', 'Chloe Tan',
                'Danish Irfan', 'Lee Jia Yi', 'Haris Fakhri', 'Tharani Siva', 'Nur Iman',
                'Ryan Tan', 'Aina Maisara', 'Loh Chun Kit', 'Sharifah Nur', 'Vikneswaran Kumar',
                'Cassandra Fernandez', 'Muhammad Haziq', 'Lim Shi Ying', 'Arjun Nair', 'Nurin Qistina',
                'Bryan Koh', 'Nurul Huda', 'Lee Zheng Yang', 'Kavya Ramesh', 'Muhammad Izzat',
                'Amelia Wong', 'Dinesh Kumar', 'Siti Aisyah', 'Isaac Tan', 'Nur Adriana',
                'Muhammad Amin', 'Tan Shi Hui', 'Raj Gopal', 'Nur Fatihah', 'Wong Jun Kit'
            ][:50],
            'IC_Number': [f'01-{np.random.randint(100000, 999999)}' for _ in range(50)],
            'DOB': pd.date_range(start='2010-01-01', periods=50, freq='M').strftime('%d/%m/%Y'),
            'Gender': np.random.choice(['Male', 'Female'], 50),
            'CurrentLevel': np.random.choice(
                ['Year 1', 'Year 2', 'Year 3', 'Year 4', 'Year 5', 'Year 6',
                 'Year 7', 'Year 8', 'Year 9', 'Year 10', 'Year 11'], 50
            ),
            'Class': [f"{np.random.choice(['A', 'B'])}" for _ in range(50)],
            'ParentID': [f'PAR{str(i).zfill(4)}' for i in range(1, 51)],
            'AvgScore': np.random.randint(40, 100, 50),
            'Attendance%': [f"{np.random.randint(75, 100)}%" for _ in range(50)],
            'PromotionStatus': np.random.choice(['Promoted', 'Retained', 'Pending'], 50, p=[0.7, 0.1, 0.2]),
            'NextLevel': ''
        })
        
        # Parents data
        parents = pd.DataFrame({
            'ParentID': [f'PAR{str(i).zfill(4)}' for i in range(1, 51)],
            'ParentName': [f"Parent {i}" for i in range(1, 51)],
            'IC': [f'01-{np.random.randint(100000, 999999)}' for _ in range(50)],
            'Phone': [f'+6012-{np.random.randint(1000000, 9999999)}' for _ in range(50)],
            'Email': [f'parent{i}@email.com' for i in range(1, 51)],
            'Address': ['Kuala Lumpur'] * 50,
            'Occupation': np.random.choice(['Teacher', 'Engineer', 'Doctor', 'Business', 'Government'], 50)
        })
        
        # Teachers data
        teachers = pd.DataFrame({
            'TeacherID': [f'TCH{str(i).zfill(3)}' for i in range(1, 36)],
            'Name': [
                'Emily Ali', 'Bryan Chong', 'Nur Ng', 'Aisyah Lim', 'Chloe Lee',
                'Nur Rahman', 'Bryan Ali', 'Nur Ismail', 'Hafiz Rahman', 'Emily Ong',
                'Amir Rahman', 'Wei Ming Chong', 'Emily Ali', 'Jason Ismail', 'Sarah Ng',
                'Adam Lee', 'Liyana Ng', 'Amir Ismail', 'Zul Rahman', 'Zul Yusof',
                'Hafiz Chong', 'Emily Ismail', 'Daniel Ali', 'Chloe Ali', 'Nur Ong',
                'Amir Ismail', 'Siti Lee', 'Chloe Ali', 'Hafiz Tan', 'Mei Ling Lim',
                'Zul Lee', 'Jason Yusof', 'Hafiz Chong', 'Bryan Ali', 'Ahmad Rahman'
            ],
            'SubjectSpecialty': np.random.choice(
                ['Mathematics', 'English', 'Science', 'History', 'Geography', 
                 'PE', 'ICT', 'Art', 'Malay', 'Business'], 35
            ),
            'EmploymentStatus': np.random.choice(['Permanent', 'Contract'], 35, p=[0.7, 0.3]),
            'AssignedPeriods': np.random.randint(10, 31, 35),
            'WorkloadStatus': ['Balanced'] * 35
        })
        
        # Staff data
        staff = pd.DataFrame({
            'StaffID': [f'STF{str(i).zfill(3)}' for i in range(1, 19)],
            'Name': [
                'Aina Ali', 'Adam Rahman', 'Nur Chong', 'Ahmad Rahman', 'Daniel Lim',
                'Daniel Lim', 'Bryan Ali', 'Adam Chong', 'Emily Ng', 'Hannah Chong',
                'Siti Aminah', 'Jason Fernandez', 'Kavitha Raj', 'Tan Cheng Hoe', 'Norhayati',
                'Ramu Gopal', 'Michelle Wong', 'Azman Hashim'
            ],
            'Role': np.random.choice(['Admin', 'Security', 'Technician', 'Librarian', 'Cleaner'], 18),
            'Phone': [f'+6012-{np.random.randint(1000000, 9999999)}' for _ in range(18)],
            'EmploymentStatus': ['Permanent'] * 18
        })
        
        # Academic results
        results = pd.DataFrame({
            'StudentID': [f'STU{str(i).zfill(4)}' for i in range(1, 51)],
            'Year': [2025] * 50,
            'Level': students['CurrentLevel'].values,
            'Class': students['Class'].values,
            'AverageScore': students['AvgScore'].values,
            'Attendance%': students['Attendance%'].values
        })
        
        # Timetable
        days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        periods = range(1, 6)
        classes = ['1A', '1B', '2A', '2B', '3A', '3B', '4A', '4B', '5A', '5B',
                   '6A', '6B', '7A', '7B', '8A', '8B', '9A', '9B', '10A', '10B', '11A', '11B']
        
        timetable_rows = []
        for class_name in classes[:10]:  # Limit for demo
            for day in days:
                for period in periods:
                    timetable_rows.append({
                        'Class': class_name,
                        'Subject': np.random.choice(['Math', 'English', 'Science', 'History']),
                        'TeacherID': np.random.choice(teachers['TeacherID'].values),
                        'Day': day,
                        'Period': period,
                        'Room': f'R{np.random.randint(1, 21)}'
                    })
        
        timetable = pd.DataFrame(timetable_rows)
        
        return {
            'students': students,
            'parents': parents,
            'teachers': teachers,
            'staff': staff,
            'results': results,
            'timetable': timetable
        }

# =============================================================================
# DASHBOARD COMPONENTS
# =============================================================================

def render_dashboard(data):
    """Render main dashboard"""
    
    st.markdown('<div class="main-header">📊 Dashboard</div>', unsafe_allow_html=True)
    
    # Key metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-value">{len(data['students'])}</div>
            <div class="stat-label">Total Students</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">👨‍🏫</div>
            <div class="stat-value">{len(data['teachers'])}</div>
            <div class="stat-label">Teachers</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">👥</div>
            <div class="stat-value">{len(data['staff'])}</div>
            <div class="stat-label">Staff</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        promoted = len(data['students'][data['students']['PromotionStatus'] == 'Promoted'])
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📈</div>
            <div class="stat-value">{promoted}</div>
            <div class="stat-label">Promoted</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col5:
        avg_attendance = data['results']['Attendance%'].str.rstrip('%').astype(float).mean()
        st.markdown(f"""
        <div class="stat-card">
            <div class="stat-icon">📊</div>
            <div class="stat-value">{avg_attendance:.1f}%</div>
            <div class="stat-label">Avg Attendance</div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="sub-header">Quick Actions</div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📚 View All Students", use_container_width=True):
            st.session_state.current_page = "Students"
            st.rerun()
    
    with col2:
        if st.button("📊 Generate Reports", use_container_width=True):
            st.session_state.current_page = "Reports"
            st.rerun()
    
    with col3:
        if st.button("📅 View Timetable", use_container_width=True):
            st.session_state.current_page = "Timetable"
            st.rerun()
    
    with col4:
        if st.button("📝 Enter Results", use_container_width=True):
            st.session_state.current_page = "Results"
            st.rerun()
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="sub-header">Students by Level</div>', unsafe_allow_html=True)
        level_counts = data['students']['CurrentLevel'].value_counts().sort_index()
        fig = px.bar(
            x=level_counts.index,
            y=level_counts.values,
            title=None,
            labels={'x': 'Year Level', 'y': 'Number of Students'},
            color_discrete_sequence=['#3b82f6']
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family='Inter',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<div class="sub-header">Promotion Status</div>', unsafe_allow_html=True)
        status_counts = data['students']['PromotionStatus'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=status_counts.index,
            values=status_counts.values,
            hole=0.4,
            marker_colors=['#22c55e', '#ef4444', '#f59e0b']
        )])
        fig.update_layout(
            showlegend=True,
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family='Inter',
            height=400,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Recent activity
    st.markdown('<div class="sub-header">Recent Activity</div>', unsafe_allow_html=True)
    
    activities = [
        {"time": "2 minutes ago", "action": "New student enrolled", "user": "Admin"},
        {"time": "15 minutes ago", "action": "Grades updated for Year 6", "user": "Mr. Chen"},
        {"time": "1 hour ago", "action": "Timetable modified", "user": "Principal"},
        {"time": "3 hours ago", "action": "Attendance report generated", "user": "Ms. Lim"},
        {"time": "5 hours ago", "action": "Parent meeting scheduled", "user": "Admin"}
    ]
    
    for activity in activities:
        st.markdown(f"""
        <div class="data-card">
            <div class="data-card-title">{activity['action']}</div>
            <div class="data-card-subtitle">{activity['time']} by {activity['user']}</div>
        </div>
        """, unsafe_allow_html=True)

# =============================================================================
# STUDENTS PAGE
# =============================================================================

def render_students(data):
    """Render students management page"""
    
    st.markdown('<div class="main-header">👥 Student Management</div>', unsafe_allow_html=True)
    
    # Filters
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        search = st.text_input("🔍 Search", placeholder="Name or ID...")
    
    with col2:
        levels = ['All'] + sorted(data['students']['CurrentLevel'].unique().tolist())
        level_filter = st.selectbox("Level", levels)
    
    with col3:
        classes = ['All'] + sorted(data['students']['Class'].unique().tolist())
        class_filter = st.selectbox("Class", classes)
    
    with col4:
        statuses = ['All'] + sorted(data['students']['PromotionStatus'].unique().tolist())
        status_filter = st.selectbox("Status", statuses)
    
    # Apply filters
    filtered_df = data['students'].copy()
    
    if search:
        filtered_df = filtered_df[
            filtered_df['FullName'].str.contains(search, case=False, na=False) |
            filtered_df['StudentID'].str.contains(search, case=False, na=False)
        ]
    
    if level_filter != 'All':
        filtered_df = filtered_df[filtered_df['CurrentLevel'] == level_filter]
    
    if class_filter != 'All':
        filtered_df = filtered_df[filtered_df['Class'] == class_filter]
    
    if status_filter != 'All':
        filtered_df = filtered_df[filtered_df['PromotionStatus'] == status_filter]
    
    # Stats
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Students", len(filtered_df))
    with col2:
        st.metric("Male", len(filtered_df[filtered_df['Gender'] == 'Male']))
    with col3:
        st.metric("Female", len(filtered_df[filtered_df['Gender'] == 'Female']))
    with col4:
        avg_score = filtered_df['AvgScore'].mean()
        st.metric("Avg Score", f"{avg_score:.1f}%")
    
    # Add student button
    if st.button("➕ Add New Student", use_container_width=True):
        st.session_state.show_add_form = True
    
    # Add student form
    if st.session_state.get('show_add_form', False):
        with st.form("add_student_form"):
            st.markdown("### Add New Student")
            
            col1, col2 = st.columns(2)
            
            with col1:
                new_name = st.text_input("Full Name *")
                new_ic = st.text_input("IC Number *")
                new_dob = st.date_input("Date of Birth *")
                new_gender = st.selectbox("Gender *", ["Male", "Female"])
            
            with col2:
                new_level = st.selectbox("Current Level *", 
                    ["Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6",
                     "Year 7", "Year 8", "Year 9", "Year 10", "Year 11"])
                new_class = st.text_input("Class *", placeholder="e.g., 5A")
                new_parent = st.text_input("Parent ID *")
                new_medical = st.text_area("Medical Notes (Optional)")
            
            col1, col2 = st.columns(2)
            with col1:
                submitted = st.form_submit_button("Save Student", use_container_width=True)
            with col2:
                if st.form_submit_button("Cancel", use_container_width=True):
                    st.session_state.show_add_form = False
                    st.rerun()
            
            if submitted and new_name and new_ic and new_parent:
                new_id = f"STU{str(len(data['students']) + 1).zfill(4)}"
                
                new_row = pd.DataFrame({
                    'StudentID': [new_id],
                    'FullName': [new_name],
                    'IC_Number': [new_ic],
                    'DOB': [new_dob.strftime('%d/%m/%Y')],
                    'Gender': [new_gender],
                    'CurrentLevel': [new_level],
                    'Class': [new_class],
                    'ParentID': [new_parent],
                    'AvgScore': [0],
                    'Attendance%': ['0%'],
                    'PromotionStatus': ['Pending'],
                    'NextLevel': ['']
                })
                
                data['students'] = pd.concat([data['students'], new_row], ignore_index=True)
                st.success(f"✅ Student {new_name} added successfully!")
                st.session_state.show_add_form = False
                st.rerun()
    
    # Display students table
    st.markdown('<div class="sub-header">Student Records</div>', unsafe_allow_html=True)
    
    # Format for display
    display_df = filtered_df.copy()
    display_df['IC_Number'] = display_df['IC_Number'].apply(lambda x: f"****{str(x)[-4:]}" if pd.notna(x) else x)
    
    # Color coding
    def color_status(val):
        if val == 'Promoted':
            return 'background-color: #d1fae5'
        elif val == 'Retained':
            return 'background-color: #fee2e2'
        elif val == 'Pending':
            return 'background-color: #fef3c7'
        return ''
    
    styled_df = display_df.style.applymap(color_status, subset=['PromotionStatus'])
    
    st.dataframe(
        styled_df,
        use_container_width=True,
        height=500,
        column_config={
            'StudentID': 'ID',
            'FullName': 'Name',
            'IC_Number': 'IC Number',
            'DOB': 'Birth Date',
            'Gender': 'Gender',
            'CurrentLevel': 'Level',
            'Class': 'Class',
            'ParentID': 'Parent ID',
            'AvgScore': 'Score',
            'Attendance%': 'Attendance',
            'PromotionStatus': 'Status',
            'NextLevel': 'Next Level'
        }
    )

# =============================================================================
# TEACHERS PAGE
# =============================================================================

def render_teachers(data):
    """Render teachers management page"""
    
    st.markdown('<div class="main-header">👨‍🏫 Teacher Management</div>', unsafe_allow_html=True)
    
    # Search and filter
    col1, col2 = st.columns(2)
    
    with col1:
        search = st.text_input("🔍 Search teachers", placeholder="Name or ID...")
    
    with col2:
        subjects = ['All'] + sorted(data['teachers']['SubjectSpecialty'].unique().tolist())
        subject_filter = st.selectbox("Subject", subjects)
    
    # Filter data
    filtered_df = data['teachers'].copy()
    
    if search:
        filtered_df = filtered_df[
            filtered_df['Name'].str.contains(search, case=False, na=False) |
            filtered_df['TeacherID'].str.contains(search, case=False, na=False)
        ]
    
    if subject_filter != 'All':
        filtered_df = filtered_df[filtered_df['SubjectSpecialty'] == subject_filter]
    
    # Statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Teachers", len(filtered_df))
    with col2:
        permanent = len(filtered_df[filtered_df['EmploymentStatus'] == 'Permanent'])
        st.metric("Permanent", permanent)
    with col3:
        avg_load = filtered_df['AssignedPeriods'].mean()
        st.metric("Avg Teaching Load", f"{avg_load:.1f} periods")
    
    # Display table
    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=400,
        column_config={
            'TeacherID': 'ID',
            'Name': 'Name',
            'SubjectSpecialty': 'Subject',
            'EmploymentStatus': 'Status',
            'AssignedPeriods': 'Periods',
            'WorkloadStatus': 'Workload'
        }
    )
    
    # Workload distribution chart
    st.markdown('<div class="sub-header">Workload Distribution</div>', unsafe_allow_html=True)
    
    fig = px.bar(
        filtered_df,
        x='Name',
        y='AssignedPeriods',
        color='SubjectSpecialty',
        title='Teacher Workload',
        labels={'AssignedPeriods': 'Periods per Week', 'Name': 'Teacher'}
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        height=400,
        showlegend=True
    )
    st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# ACADEMIC RESULTS PAGE
# =============================================================================

def render_results(data):
    """Render academic results page"""
    
    st.markdown('<div class="main-header">📚 Academic Results</div>', unsafe_allow_html=True)
    
    # Merge student names with results
    results_df = data['results'].merge(
        data['students'][['StudentID', 'FullName']],
        on='StudentID',
        how='left'
    )
    
    # Filters
    col1, col2, col3 = st.columns(3)
    
    with col1:
        levels = ['All'] + sorted(results_df['Level'].unique().tolist())
        level_filter = st.selectbox("Year Level", levels)
    
    with col2:
        classes = ['All'] + sorted(results_df['Class'].unique().tolist())
        class_filter = st.selectbox("Class", classes)
    
    with col3:
        score_range = st.select_slider(
            "Score Range",
            options=[0, 20, 40, 60, 80, 100],
            value=(0, 100)
        )
    
    # Apply filters
    filtered_df = results_df.copy()
    
    if level_filter != 'All':
        filtered_df = filtered_df[filtered_df['Level'] == level_filter]
    
    if class_filter != 'All':
        filtered_df = filtered_df[filtered_df['Class'] == class_filter]
    
    filtered_df = filtered_df[
        (filtered_df['AverageScore'] >= score_range[0]) &
        (filtered_df['AverageScore'] <= score_range[1])
    ]
    
    # Performance metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        avg_score = filtered_df['AverageScore'].mean()
        st.metric("Average Score", f"{avg_score:.1f}%")
    
    with col2:
        avg_attendance = filtered_df['Attendance%'].str.rstrip('%').astype(float).mean()
        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
    
    with col3:
        passed = len(filtered_df[filtered_df['AverageScore'] >= 50])
        st.metric("Passed", f"{passed}/{len(filtered_df)}")
    
    with col4:
        distinction = len(filtered_df[filtered_df['AverageScore'] >= 80])
        st.metric("Distinction", distinction)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Score distribution
        fig = px.histogram(
            filtered_df,
            x='AverageScore',
            nbins=20,
            title='Score Distribution',
            labels={'AverageScore': 'Score (%)', 'count': 'Number of Students'},
            color_discrete_sequence=['#3b82f6']
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family='Inter',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Top performers
        top_10 = filtered_df.nlargest(10, 'AverageScore')[['FullName', 'AverageScore']]
        fig = px.bar(
            top_10,
            x='AverageScore',
            y='FullName',
            orientation='h',
            title='Top 10 Performers',
            labels={'AverageScore': 'Score (%)', 'FullName': ''},
            color='AverageScore',
            color_continuous_scale='viridis'
        )
        fig.update_layout(
            plot_bgcolor='white',
            paper_bgcolor='white',
            font_family='Inter',
            height=350
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Results table
    st.markdown('<div class="sub-header">Detailed Results</div>', unsafe_allow_html=True)
    
    st.dataframe(
        filtered_df[['StudentID', 'FullName', 'Level', 'Class', 'AverageScore', 'Attendance%']],
        use_container_width=True,
        height=400
    )

# =============================================================================
# TIMETABLE PAGE
# =============================================================================

def render_timetable(data):
    """Render timetable page"""
    
    st.markdown('<div class="main-header">📅 Timetable</div>', unsafe_allow_html=True)
    
    # Class selector
    classes = sorted(data['timetable']['Class'].unique().tolist())
    selected_class = st.selectbox("Select Class", classes)
    
    # Filter for selected class
    class_timetable = data['timetable'][data['timetable']['Class'] == selected_class]
    
    # Merge with teacher names
    class_timetable = class_timetable.merge(
        data['teachers'][['TeacherID', 'Name']],
        on='TeacherID',
        how='left'
    )
    
    # Create weekly view
    days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    periods = sorted(class_timetable['Period'].unique())
    
    # Create timetable matrix
    timetable_data = []
    for period in periods:
        row = {'Period': f'Period {period}'}
        for day in days:
            subject_data = class_timetable[
                (class_timetable['Day'] == day) & 
                (class_timetable['Period'] == period)
            ]
            if not subject_data.empty:
                row[day] = f"{subject_data.iloc[0]['Subject']}\n{subject_data.iloc[0]['Name']}\nRoom {subject_data.iloc[0]['Room']}"
            else:
                row[day] = "—"
        timetable_data.append(row)
    
    # Display timetable
    st.markdown(f"### Class {selected_class} Timetable")
    
    timetable_df = pd.DataFrame(timetable_data)
    st.dataframe(
        timetable_df.set_index('Period'),
        use_container_width=True,
        height=400
    )
    
    # Teacher schedule view
    st.markdown('<div class="sub-header">Teacher Schedule</div>', unsafe_allow_html=True)
    
    teacher_name = st.selectbox(
        "View teacher schedule",
        ['Select a teacher'] + sorted(data['teachers']['Name'].tolist())
    )
    
    if teacher_name != 'Select a teacher':
        teacher_id = data['teachers'][data['teachers']['Name'] == teacher_name]['TeacherID'].iloc[0]
        teacher_schedule = data['timetable'][data['timetable']['TeacherID'] == teacher_id]
        
        if not teacher_schedule.empty:
            teacher_schedule = teacher_schedule.merge(
                data['teachers'][['TeacherID', 'Name']],
                on='TeacherID',
                how='left'
            )
            
            st.dataframe(
                teacher_schedule[['Day', 'Period', 'Class', 'Subject', 'Room']].sort_values(['Day', 'Period']),
                use_container_width=True
            )
        else:
            st.info("No schedule found for this teacher")

# =============================================================================
# REPORTS PAGE
# =============================================================================

def render_reports(data):
    """Render reports generation page"""
    
    st.markdown('<div class="main-header">📑 Reports</div>', unsafe_allow_html=True)
    
    report_type = st.selectbox(
        "Select Report Type",
        [
            "Student Performance Report",
            "Class List Report",
            "Teacher Workload Report",
            "Attendance Summary",
            "Promotion Summary",
            "School Statistics"
        ]
    )
    
    if report_type == "Student Performance Report":
        render_performance_report(data)
    elif report_type == "Class List Report":
        render_class_list(data)
    elif report_type == "Teacher Workload Report":
        render_workload_report(data)
    elif report_type == "Attendance Summary":
        render_attendance_report(data)
    elif report_type == "Promotion Summary":
        render_promotion_report(data)
    elif report_type == "School Statistics":
        render_statistics_report(data)

def render_performance_report(data):
    """Render performance report"""
    
    st.markdown("### Student Performance Report")
    
    col1, col2 = st.columns(2)
    
    with col1:
        level = st.selectbox(
            "Select Level",
            ['All'] + sorted(data['results']['Level'].unique().tolist())
        )
    
    with col2:
        format_type = st.radio("Report Format", ['Summary', 'Detailed'])
    
    # Filter data
    results_df = data['results'].copy()
    if level != 'All':
        results_df = results_df[results_df['Level'] == level]
    
    # Merge with student names
    results_df = results_df.merge(
        data['students'][['StudentID', 'FullName', 'Class']],
        on='StudentID',
        how='left'
    )
    
    if format_type == 'Summary':
        # Summary by class
        summary = results_df.groupby('Class').agg({
            'AverageScore': ['mean', 'min', 'max', 'count'],
            'Attendance%': lambda x: x.str.rstrip('%').astype(float).mean()
        }).round(1)
        
        summary.columns = ['Avg Score', 'Min Score', 'Max Score', 'Students', 'Avg Attendance']
        st.dataframe(summary, use_container_width=True)
        
        # Performance bands
        results_df['Performance Band'] = pd.cut(
            results_df['AverageScore'],
            bins=[0, 40, 50, 60, 70, 80, 90, 100],
            labels=['<40%', '40-50%', '50-60%', '60-70%', '70-80%', '80-90%', '90-100%']
        )
        
        band_dist = results_df['Performance Band'].value_counts().sort_index()
        fig = px.bar(
            x=band_dist.index,
            y=band_dist.values,
            title='Performance Distribution',
            labels={'x': 'Score Range', 'y': 'Number of Students'}
        )
        st.plotly_chart(fig, use_container_width=True)
    
    else:
        # Detailed view
        st.dataframe(
            results_df[['StudentID', 'FullName', 'Class', 'AverageScore', 'Attendance%']],
            use_container_width=True
        )
    
    # Download button
    if st.button("📥 Download Report", use_container_width=True):
        csv = results_df.to_csv(index=False)
        b64 = base64.b64encode(csv.encode()).decode()
        href = f'<a href="data:file/csv;base64,{b64}" download="performance_report.csv">Download CSV</a>'
        st.markdown(href, unsafe_allow_html=True)

def render_class_list(data):
    """Render class list report"""
    
    st.markdown("### Class List Report")
    
    level = st.selectbox("Select Level", sorted(data['students']['CurrentLevel'].unique().tolist()))
    
    if level:
        level_students = data['students'][data['students']['CurrentLevel'] == level]
        classes = sorted(level_students['Class'].unique().tolist())
        
        for class_name in classes:
            with st.expander(f"Class {class_name}"):
                class_students = level_students[level_students['Class'] == class_name]
                
                st.dataframe(
                    class_students[['StudentID', 'FullName', 'Gender']].sort_values('FullName'),
                    use_container_width=True,
                    hide_index=True
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Total Students", len(class_students))
                with col2:
                    boys = len(class_students[class_students['Gender'] == 'Male'])
                    girls = len(class_students[class_students['Gender'] == 'Female'])
                    st.metric("Boys/Girls", f"{boys}/{girls}")

def render_workload_report(data):
    """Render teacher workload report"""
    
    st.markdown("### Teacher Workload Report")
    
    workload_df = data['teachers'].copy()
    
    # Calculate workload status
    workload_df['Status'] = pd.cut(
        workload_df['AssignedPeriods'],
        bins=[0, 15, 25, 50],
        labels=['Underloaded', 'Balanced', 'Overloaded']
    )
    
    # Summary
    col1, col2, col3 = st.columns(3)
    
    with col1:
        avg_load = workload_df['AssignedPeriods'].mean()
        st.metric("Average Load", f"{avg_load:.1f} periods")
    
    with col2:
        overloaded = len(workload_df[workload_df['Status'] == 'Overloaded'])
        st.metric("Overloaded", overloaded)
    
    with col3:
        underloaded = len(workload_df[workload_df['Status'] == 'Underloaded'])
        st.metric("Underloaded", underloaded)
    
    # Distribution chart
    fig = px.bar(
        workload_df.sort_values('AssignedPeriods'),
        x='Name',
        y='AssignedPeriods',
        color='Status',
        title='Teacher Workload Distribution',
        color_discrete_map={
            'Underloaded': '#f59e0b',
            'Balanced': '#22c55e',
            'Overloaded': '#ef4444'
        }
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        height=500,
        xaxis_tickangle=-45
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Detailed table
    st.dataframe(
        workload_df[['TeacherID', 'Name', 'SubjectSpecialty', 'AssignedPeriods', 'Status']],
        use_container_width=True
    )

def render_attendance_report(data):
    """Render attendance report"""
    
    st.markdown("### Attendance Summary Report")
    
    results_df = data['results'].copy()
    results_df['Attendance'] = results_df['Attendance%'].str.rstrip('%').astype(float)
    
    # Summary by level
    level_attendance = results_df.groupby('Level')['Attendance'].agg(['mean', 'min', 'max']).round(1)
    level_attendance.columns = ['Avg Attendance', 'Min', 'Max']
    
    st.dataframe(level_attendance, use_container_width=True)
    
    # Attendance distribution
    results_df['Attendance Band'] = pd.cut(
        results_df['Attendance'],
        bins=[0, 70, 80, 85, 90, 95, 100],
        labels=['<70%', '70-80%', '80-85%', '85-90%', '90-95%', '95-100%']
    )
    
    band_counts = results_df['Attendance Band'].value_counts().sort_index()
    fig = px.pie(
        values=band_counts.values,
        names=band_counts.index,
        title='Attendance Distribution'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Low attendance students
    st.markdown("### Students with Low Attendance (<85%)")
    low_attendance = results_df[results_df['Attendance'] < 85].merge(
        data['students'][['StudentID', 'FullName', 'Class']],
        on='StudentID'
    )
    
    if not low_attendance.empty:
        st.dataframe(
            low_attendance[['StudentID', 'FullName', 'Class', 'Attendance']].sort_values('Attendance'),
            use_container_width=True
        )
    else:
        st.success("No students with low attendance!")

def render_promotion_report(data):
    """Render promotion summary report"""
    
    st.markdown("### Promotion Summary Report")
    
    students_df = data['students'].copy()
    
    # Summary by level
    promotion_summary = pd.crosstab(
        students_df['CurrentLevel'],
        students_df['PromotionStatus'],
        margins=True,
        margins_name='Total'
    )
    
    st.dataframe(promotion_summary, use_container_width=True)
    
    # Promotion rate chart
    promotion_rate = (students_df['PromotionStatus'] == 'Promoted').groupby(
        students_df['CurrentLevel']
    ).mean() * 100
    
    fig = px.bar(
        x=promotion_rate.index,
        y=promotion_rate.values,
        title='Promotion Rate by Level',
        labels={'x': 'Level', 'y': 'Promotion Rate (%)'},
        color_discrete_sequence=['#22c55e']
    )
    fig.update_layout(
        plot_bgcolor='white',
        paper_bgcolor='white',
        font_family='Inter',
        yaxis_range=[0, 100]
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Retained students list
    st.markdown("### Students to be Retained")
    retained = students_df[students_df['PromotionStatus'] == 'Retained'][
        ['StudentID', 'FullName', 'CurrentLevel', 'Class', 'AvgScore', 'Attendance%']
    ]
    
    if not retained.empty:
        st.dataframe(retained, use_container_width=True)
    else:
        st.success("No students to be retained!")

def render_statistics_report(data):
    """Render school statistics report"""
    
    st.markdown("### School Statistics Report")
    
    # Overall statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Enrollment", len(data['students']))
        st.metric("Student-Teacher Ratio", f"{len(data['students'])/len(data['teachers']):.1f}")
    
    with col2:
        st.metric("Total Staff", len(data['teachers']) + len(data['staff']))
        st.metric("Classes", len(data['students']['Class'].unique()))
    
    with col3:
        avg_score = data['results']['AverageScore'].mean()
        st.metric("School Avg Score", f"{avg_score:.1f}%")
        avg_attendance = data['results']['Attendance%'].str.rstrip('%').astype(float).mean()
        st.metric("School Avg Attendance", f"{avg_attendance:.1f}%")
    
    # Gender distribution
    col1, col2 = st.columns(2)
    
    with col1:
        gender_dist = data['students']['Gender'].value_counts()
        fig = go.Figure(data=[go.Pie(
            labels=gender_dist.index,
            values=gender_dist.values,
            hole=0.4
        )])
        fig.update_layout(title='Gender Distribution')
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        level_dist = data['students']['CurrentLevel'].value_counts().sort_index()
        fig = px.bar(
            x=level_dist.index,
            y=level_dist.values,
            title='Students by Level'
        )
        st.plotly_chart(fig, use_container_width=True)

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main():
    """Main application entry point"""
    
    # Initialize data manager
    data_manager = DataManager()
    
    # Load sample data
    data = data_manager.load_sample_data()
    
    # Authentication
    auth = Authentication()
    
    # Sidebar
    with st.sidebar:
        st.image("https://img.icons8.com/ios/100/000000/school.png", width=80)
        st.title("St. George's")
        st.caption("School Management System")
        st.markdown("---")
        
        if not st.session_state.authenticated:
            with st.form("login_form"):
                username = st.text_input("Username", placeholder="Enter username")
                password = st.text_input("Password", type="password", placeholder="Enter password")
                submitted = st.form_submit_button("Login", use_container_width=True)
                
                if submitted:
                    authenticated, user_info = auth.authenticate(username, password)
                    if authenticated:
                        st.session_state.authenticated = True
                        st.session_state.user_role = user_info['role']
                        st.session_state.username = user_info['name']
                        st.session_state.user_email = user_info['email']
                        st.session_state.login_time = datetime.now()
                        st.rerun()
                    else:
                        st.error("Invalid username or password")
        else:
            # User profile
            st.markdown(f"""
            <div style="text-align: center; padding: 1rem;">
                <div style="font-size: 3rem;">{auth.get_user_info(st.session_state.username.split()[-1].lower())['avatar']}</div>
                <div style="font-weight: 600;">{st.session_state.username}</div>
                <div style="color: #666; font-size: 0.9rem;">{st.session_state.user_role}</div>
            </div>
            """, unsafe_allow_html=True)
            
            st.markdown("---")
            
            if st.button("🚪 Logout", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.rerun()
        
        st.markdown("---")
        
        # Navigation
        if st.session_state.authenticated:
            pages = {
                "Dashboard": "📊",
                "Students": "👥",
                "Teachers": "👨‍🏫",
                "Results": "📚",
                "Timetable": "📅",
                "Reports": "📑"
            }
            
            for page, icon in pages.items():
                if st.sidebar.button(
                    f"{icon} {page}",
                    use_container_width=True,
                    key=f"nav_{page}",
                    help=f"Go to {page}"
                ):
                    st.session_state.current_page = page
                    st.rerun()
    
    # Main content
    if not st.session_state.authenticated:
        # Welcome page
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("""
            <div style="text-align: center; padding: 3rem;">
                <h1 style="font-size: 3rem; margin-bottom: 1rem;">🏫</h1>
                <h1 style="font-weight: 400; color: #1e293b;">St. George's School</h1>
                <h3 style="font-weight: 300; color: #64748b; margin: 1rem 0;">Management System</h3>
                <p style="color: #94a3b8; margin: 2rem 0;">Please log in to access the system</p>
                <div style="background: #f8fafc; padding: 1.5rem; border-radius: 12px; margin-top: 2rem;">
                    <p style="color: #475569; margin-bottom: 0.5rem;"><strong>Demo Credentials:</strong></p>
                    <p style="color: #64748b; font-size: 0.9rem;">Admin: admin / admin123</p>
                    <p style="color: #64748b; font-size: 0.9rem;">Principal: principal / principal123</p>
                    <p style="color: #64748b; font-size: 0.9rem;">Teacher: james.chen / teacher123</p>
                </div>
            </div>
            """, unsafe_allow_html=True)
    else:
        # Render selected page
        if st.session_state.current_page == "Dashboard":
            render_dashboard(data)
        elif st.session_state.current_page == "Students":
            render_students(data)
        elif st.session_state.current_page == "Teachers":
            render_teachers(data)
        elif st.session_state.current_page == "Results":
            render_results(data)
        elif st.session_state.current_page == "Timetable":
            render_timetable(data)
        elif st.session_state.current_page == "Reports":
            render_reports(data)

if __name__ == "__main__":
    main()
