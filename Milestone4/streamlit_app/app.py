import streamlit as st
import requests
import json
import os
import sys
import time
from PIL import Image

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.user_management_module import (
    register_user_with_password, verify_user_password, generate_password_reset_otp,
    reset_password_with_otp, reset_password_with_security_question,
    get_user_by_id, get_user_stats, get_user_activity, replace_user, delete_user,
    promote_user_to_admin, get_all_users
)
from backend.feedback_logger_module import log_feedback
from backend.user_history_module import log_user_query
from backend.feedback_analysis_module import (
    generate_avatar_image, save_user_avatar, load_user_avatar,
    pil_image_to_bytes, generate_wordcloud_image, analyze_sentiments
)
from backend.admin_dashboard_module import get_dashboard_stats, search_global

# --- Page Configuration ---
st.set_page_config(
    page_title="CodeGenie AI",
    page_icon="🧞‍♂️",
    layout="wide",
)

# --- Load Custom CSS ---
def local_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        st.warning("Style file not found. Using default theme.")

local_css("streamlit_app/style.css")

# --- Session State Initialization ---
if 'token' not in st.session_state:
    st.session_state.token = None
if 'user' not in st.session_state:
    st.session_state.user = None
if 'messages' not in st.session_state:
    st.session_state.messages = []
if 'page' not in st.session_state:
    st.session_state.page = "Login"

# --- Backend API URL ---
API_URL = "http://localhost:8000"

# --- Helper Functions ---

def login_user(username, password):
    res = verify_user_password(username, password)
    if res['success']:
        st.session_state.token = "dummy_token" # In real app, use JWT from backend
        st.session_state.user = {'user_id': res['user_id'], 'role': res['role']}
        st.session_state.page = "CodeGenie"
        st.success("Logged in successfully!")
        st.rerun()
    else:
        st.error(res.get('error', 'Login failed'))

def logout_user():
    st.session_state.token = None
    st.session_state.user = None
    st.session_state.messages = []
    st.session_state.page = "Login"
    st.rerun()

# --- Views ---

def show_login_page():
    st.title("🧞‍♂️ Welcome to CodeGenie AI")
    
    tab1, tab2, tab3 = st.tabs(["Login", "Sign Up", "Forgot Password"])
    
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username / User ID")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")
            if submitted:
                login_user(username, password)
    
    with tab2:
        with st.form("signup_form"):
            new_user_id = st.text_input("Choose User ID")
            new_username = st.text_input("Choose Username")
            new_email = st.text_input("Email (Optional)")
            new_password = st.text_input("Password", type="password")
            sec_q = st.selectbox("Security Question", [
                "What is your pet's name?",
                "What is your mother's maiden name?",
                "What city were you born in?"
            ])
            sec_a = st.text_input("Answer")
            submitted = st.form_submit_button("Sign Up")
            if submitted:
                if new_user_id and new_username and new_password and sec_a:
                    res = register_user_with_password(new_user_id, new_username, new_password, new_email, sec_q, sec_a)
                    if res['success']:
                        st.success("Account created! Please login.")
                    else:
                        st.error(f"Error: {res.get('error')}")
                else:
                    st.error("Please fill all required fields.")

    with tab3:
        st.subheader("Recover Password")
        method = st.radio("Recovery Method", ["Email OTP", "Security Question"])
        user_id_rec = st.text_input("Enter User ID for Recovery")
        
        if method == "Email OTP":
            if st.button("Send OTP"):
                res = generate_password_reset_otp(user_id_rec)
                if res['success']:
                    st.info(f"OTP generated. (Check logs/console if email not configured). OTP: {res.get('otp')}") # Dev mode hint
                    st.session_state.reset_mode = "otp"
                else:
                    st.error(res.get('error'))
            
            otp_input = st.text_input("Enter OTP")
            new_pass_otp = st.text_input("New Password", type="password", key="new_pass_otp")
            if st.button("Reset with OTP"):
                res = reset_password_with_otp(user_id_rec, otp_input, new_pass_otp)
                if res['success']:
                    st.success("Password reset! Please login.")
                else:
                    st.error(res.get('error'))
                    
        else: # Security Question
            sec_ans_input = st.text_input("Answer to Security Question")
            new_pass_sq = st.text_input("New Password", type="password", key="new_pass_sq")
            if st.button("Reset with Security Question"):
                res = reset_password_with_security_question(user_id_rec, sec_ans_input, new_pass_sq)
                if res['success']:
                    st.success("Password reset! Please login.")
                else:
                    st.error(res.get('error'))


def show_codegenie_page():
    st.header("🧞‍♂️ CodeGenie Workspace")
    
    # Model Selection
    model_choice = st.selectbox("Select Model", ["gemma", "deepseek", "phi-2"])
    language = st.selectbox("Language", ["Python", "JavaScript", "C++", "Java", "SQL", "Go"])
    
    # Chat Interface
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    prompt = st.chat_input("Describe the code you need...")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
            
        with st.chat_message("assistant"):
            with st.spinner("Generating code..."):
                try:
                    # Call Backend API
                    payload = {"prompt": prompt, "language": language, "model": model_choice}
                    response = requests.post(f"{API_URL}/generate", json=payload)
                    if response.status_code == 200:
                        code = response.json().get("code", "")
                        st.code(code, language=language.lower())
                        st.session_state.messages.append({"role": "assistant", "content": f"```\n{code}\n```"})
                        
                        # Log history
                        log_user_query(st.session_state.user['user_id'], prompt, language, code, "", model_choice)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")

    # Feedback
    with st.expander("Give Feedback"):
        f_rating = st.slider("Rating", 1, 5, 5)
        f_comment = st.text_area("Comments")
        if st.button("Submit Feedback"):
            log_feedback(st.session_state.user['user_id'], "General Feedback", f_rating, f_comment)
            st.success("Thank you!")


def show_explainer_page():
    st.header("🧠 Code Explainer")
    
    code_input = st.text_area("Paste code here", height=200)
    style = st.selectbox("Explanation Style", ["Beginner-Friendly", "Technical Deep-Dive", "Step-by-Step Guide"])
    model_choice = st.selectbox("Model", ["deepseek", "gemma", "phi-2"])
    
    if st.button("Explain"):
        if code_input:
            with st.spinner("Analyzing..."):
                try:
                    payload = {"code": code_input, "style": style, "model": model_choice}
                    response = requests.post(f"{API_URL}/explain", json=payload)
                    if response.status_code == 200:
                        explanation = response.json().get("explanation", "")
                        st.markdown(explanation)
                        # Log
                        log_user_query(st.session_state.user['user_id'], "Explain Code", "N/A", code_input, explanation, model_choice)
                    else:
                        st.error(f"Error: {response.text}")
                except Exception as e:
                    st.error(f"Connection Error: {e}")
        else:
            st.warning("Please paste some code first.")


def show_profile_page():
    st.header("👤 My Profile")
    user_id = st.session_state.user['user_id']
    user_stats = get_user_stats(user_id)
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        # Avatar
        avatar_img = load_user_avatar(user_id)
        if not avatar_img:
            avatar_img = generate_avatar_image(user_stats.get('username', user_id), email=user_stats.get('email'))
        st.image(avatar_img, width=150)
        
        uploaded_file = st.file_uploader("Upload Avatar", type=['png', 'jpg', 'jpeg'])
        if uploaded_file:
            bytes_data = uploaded_file.getvalue()
            if save_user_avatar(user_id, bytes_data):
                st.success("Avatar updated!")
                st.rerun()

    with col2:
        st.subheader(f"User: {user_stats.get('username', 'Unknown')}")
        st.write(f"**ID:** {user_id}")
        st.write(f"**Role:** {user_stats.get('role', 'user').upper()}")
        st.write(f"**Email:** {user_stats.get('email', 'N/A')}")
        
        st.metric("Total Queries", user_stats.get('total_queries', 0))
        st.metric("Avg Rating Given", user_stats.get('average_rating', 0.0))

    st.subheader("Activity History")
    history = get_user_activity(user_id)
    if history:
        for item in history[-5:]: # Last 5
            st.text(f"{item['timestamp']} - {item['activity_type']}")
    else:
        st.info("No activity yet.")


def show_admin_dashboard():
    st.header("📊 Admin Dashboard")
    
    # Check permissions
    if st.session_state.user.get('role') != 'admin':
        st.error("Access Denied. Admins only.")
        return

    stats = get_dashboard_stats()
    
    # Metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Total Queries", stats['total_queries'])
    c2.metric("Total Feedback", stats['total_feedback'])
    c3.metric("Avg Rating", stats['average_rating'])
    c4.metric("Active Users", stats['active_users'])
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["Analytics", "User Management", "Global Search"])
    
    with tab1:
        st.subheader("Feedback Word Cloud")
        feedback_texts = [f.get('comments', '') for f in stats['recent_feedback']]
        if feedback_texts:
            wc_img = generate_wordcloud_image(feedback_texts)
            st.image(wc_img, caption="Feedback Word Cloud")
        else:
            st.info("Not enough feedback for word cloud.")
            
        st.subheader("Top Languages")
        st.bar_chart(stats['top_languages'])

    with tab2:
        st.subheader("Manage Users")
        users = get_all_users()
        for u in users:
            with st.expander(f"{u['username']} ({u['user_id']}) - {u['role']}"):
                st.write(u)
                if u['role'] != 'admin':
                    if st.button(f"Promote {u['user_id']}", key=f"prom_{u['user_id']}"):
                        res = promote_user_to_admin(u['user_id'])
                        if res['success']:
                            st.success("Promoted!")
                            st.rerun()
                        else:
                            st.error(res.get('error'))
                    
                    if st.button(f"Delete {u['user_id']}", key=f"del_{u['user_id']}"):
                        res = delete_user(u['user_id'])
                        if res['success']:
                            st.success("Deleted!")
                            st.rerun()
                        else:
                            st.error(res.get('error'))

    with tab3:
        st.subheader("Global Search")
        q = st.text_input("Search Users, History, Feedback")
        if q:
            results = search_global(q)
            st.write(results)


# --- Main Navigation ---

if not st.session_state.token:
    show_login_page()
else:
    with st.sidebar:
        # User Info
        uid = st.session_state.user['user_id']
        avatar = load_user_avatar(uid)
        if not avatar:
            avatar = generate_avatar_image(uid)
        st.image(avatar, width=80)
        st.write(f"Hello, **{uid}**")
        
        if st.button("CodeGenie"):
            st.session_state.page = "CodeGenie"
            st.rerun()
        if st.button("Code Explainer"):
            st.session_state.page = "Explainer"
            st.rerun()
        if st.button("My Profile"):
            st.session_state.page = "Profile"
            st.rerun()
        
        if st.session_state.user.get('role') == 'admin':
            if st.button("Admin Dashboard"):
                st.session_state.page = "Admin"
                st.rerun()
                
        st.divider()
        if st.button("Logout"):
            logout_user()

    # Routing
    if st.session_state.page == "CodeGenie":
        show_codegenie_page()
    elif st.session_state.page == "Explainer":
        show_explainer_page()
    elif st.session_state.page == "Profile":
        show_profile_page()
    elif st.session_state.page == "Admin":
        show_admin_dashboard()
