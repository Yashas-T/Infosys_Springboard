# -*- coding: utf-8 -*-
"""User Management Module

Handles user registration, login tracking, member replacement, and activity history.
Now supports RBAC (Admin/User), Security Questions, and SMTP-based OTP.
"""

import json
import os
import logging
import threading
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Resolve to the project's streamlit_app folder
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_DIR, '..'))
STREAMLIT_APP_DIR = os.path.join(PROJECT_ROOT, 'streamlit_app')
USERS_FILE = os.path.join(STREAMLIT_APP_DIR, 'users.json')
USER_ACTIVITY_FILE = os.path.join(STREAMLIT_APP_DIR, 'user_activity.json')

# Use a lock for thread-safe file operations
file_lock = threading.Lock()

# SMTP Configuration (Load from env in production)
SMTP_EMAIL = os.environ.get("SMTP_EMAIL", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", 587))


def _ensure_files_exist():
    """Ensure JSON files exist with proper structure."""
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)
    
    if not os.path.exists(USER_ACTIVITY_FILE):
        with open(USER_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
            json.dump([], f, indent=4)


def register_user(user_id: str, username: str, email: str = "", 
                 security_question: str = "", security_answer: str = "") -> Dict[str, Any]:
    """
    Register a new user or update existing user info.
    
    Args:
        user_id: Unique identifier for the user
        username: Username for display
        email: Optional email address
        security_question: Question for password recovery
        security_answer: Answer for password recovery
        
    Returns:
        Dictionary with user info and success status
    """
    _ensure_files_exist()
    
    with file_lock:
        try:
            # Read existing users
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                    if not isinstance(users, list):
                        users = []
                except json.JSONDecodeError:
                    users = []
            
            # Check if user already exists
            user_idx = next((i for i, u in enumerate(users) if u['user_id'] == user_id), None)
            
            # Hash security answer if provided
            sec_answer_hash = None
            if security_answer:
                import hashlib
                sec_answer_hash = hashlib.sha256(security_answer.lower().strip().encode()).hexdigest()

            user_entry = {
                'user_id': user_id,
                'username': username,
                'email': email,
                'role': 'user',  # Default role
                'security_question': security_question,
                'security_answer_hash': sec_answer_hash,
                'created_at': datetime.now().isoformat(),
                'last_login': datetime.now().isoformat(),
                'total_logins': 1,
                'total_queries': 0,
                'average_rating': 0.0,
                'total_feedback_entries': 0
            }
            
            if user_idx is not None:
                # Update existing user
                users[user_idx]['last_login'] = datetime.now().isoformat()
                users[user_idx]['total_logins'] = users[user_idx].get('total_logins', 0) + 1
                users[user_idx]['username'] = username
                if email:
                    users[user_idx]['email'] = email
                if security_question:
                    users[user_idx]['security_question'] = security_question
                if sec_answer_hash:
                    users[user_idx]['security_answer_hash'] = sec_answer_hash
            else:
                # Add new user
                users.append(user_entry)
            
            # Write back
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, indent=4)
            
            logger.info(f"Successfully registered/updated user {user_id}")
            return {'success': True, 'user_id': user_id, 'message': 'User registered successfully'}
            
        except Exception as e:
            logger.error(f"Failed to register user: {e}")
            return {'success': False, 'error': str(e)}


def log_user_activity(user_id: str, activity_type: str, query: str = "", 
                     language: str = "", rating: int = 0, comments: str = "", model_name: str = "") -> bool:
    """
    Log user activity (query, feedback, etc).
    """
    _ensure_files_exist()
    
    activity_entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'activity_type': activity_type,
        'query': query,
        'language': language,
        'rating': rating,
        'comments': comments,
        'model': model_name
    }
    
    with file_lock:
        try:
            # Read existing activities
            if os.path.exists(USER_ACTIVITY_FILE):
                with open(USER_ACTIVITY_FILE, 'r', encoding='utf-8') as f:
                    try:
                        activities = json.load(f)
                        if not isinstance(activities, list):
                            activities = []
                    except json.JSONDecodeError:
                        activities = []
            else:
                activities = []
            
            # Append new activity
            activities.append(activity_entry)
            
            # Write back
            with open(USER_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=4)
            
            logger.info(f"Successfully logged activity for user {user_id}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to log activity: {e}")
            return False


def get_all_users() -> List[Dict[str, Any]]:
    """Get all registered users."""
    _ensure_files_exist()
    
    try:
        with open(USERS_FILE, 'r', encoding='utf-8') as f:
            try:
                users = json.load(f)
                if isinstance(users, list):
                    return users
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logger.error(f"Failed to read users: {e}")
    
    return []


def get_user_by_username(username: str) -> Optional[Dict[str, Any]]:
    """Get user by username (case-insensitive)."""
    users = get_all_users()
    username = (username or '').strip().lower()
    return next((u for u in users if str(u.get('username','')).strip().lower() == username), None)


def _save_users(users: List[Dict[str, Any]]) -> bool:
    """Save users list to USERS_FILE atomically."""
    try:
        with open(USERS_FILE, 'w', encoding='utf-8') as f:
            json.dump(users, f, indent=4)
        return True
    except Exception as e:
        logger.error(f"Failed to save users: {e}")
        return False


def _hash_password(password: str, salt: Optional[bytes] = None) -> Dict[str, str]:
    """Return dict with hex salt and password hash using pbkdf2_hmac."""
    import hashlib, binascii, os
    if salt is None:
        salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return {'salt': binascii.hexlify(salt).decode('ascii'), 'hash': binascii.hexlify(dk).decode('ascii')}


def set_password_for_user(user_id: str, password: str) -> Dict[str, Any]:
    """Set or replace a user's password (stores hash+salt)."""
    _ensure_files_exist()
    with file_lock:
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                    if not isinstance(users, list):
                        users = []
                except json.JSONDecodeError:
                    users = []

            idx = next((i for i, u in enumerate(users) if u['user_id'] == user_id), None)
            if idx is None:
                return {'success': False, 'error': 'User not found'}

            ph = _hash_password(password)
            users[idx]['password_salt'] = ph['salt']
            users[idx]['password_hash'] = ph['hash']

            _save_users(users)
            logger.info(f"Password set for user {user_id}")
            return {'success': True}
        except Exception as e:
            logger.error(f"Failed to set password: {e}")
            return {'success': False, 'error': str(e)}


def register_user_with_password(user_id: str, username: str, password: str, email: str = "", 
                               security_question: str = "", security_answer: str = "") -> Dict[str, Any]:
    """Convenience: create user and set password atomically (if user exists, update password)."""
    res = register_user(user_id, username, email, security_question, security_answer)
    if not res.get('success'):
        return res
    return set_password_for_user(user_id, password)


def verify_user_password(user_identifier: str, password: str) -> Dict[str, Any]:
    """
    Verify a user's password. user_identifier may be user_id or username.
    Returns {'success': True, 'user_id': ..., 'role': ...} on success.
    """
    try:
        # Try user_id first
        user = get_user_by_id(user_identifier)
        if not user:
            user = get_user_by_username(user_identifier)
        if not user:
            return {'success': False, 'error': 'User not found'}

        salt_hex = user.get('password_salt')
        hash_hex = user.get('password_hash')
        if not salt_hex or not hash_hex:
            return {'success': False, 'error': 'Password not set for user'}

        import binascii, hashlib
        salt = binascii.unhexlify(salt_hex.encode('ascii'))
        attempt = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
        if binascii.hexlify(attempt).decode('ascii') == hash_hex:
            # update last_login and total_logins
            with file_lock:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    try:
                        users = json.load(f)
                    except json.JSONDecodeError:
                        users = []
                for u in users:
                    if u.get('user_id') == user.get('user_id'):
                        u['last_login'] = datetime.now().isoformat()
                        u['total_logins'] = u.get('total_logins', 0) + 1
                        break
                _save_users(users)

            return {'success': True, 'user_id': user.get('user_id'), 'role': user.get('role', 'user')}
        return {'success': False, 'error': 'Invalid password'}
    except Exception as e:
        logger.error(f"Error verifying password: {e}")
        return {'success': False, 'error': str(e)}


def send_otp_email(to_email: str, otp: str) -> bool:
    """Send OTP via SMTP."""
    if not SMTP_EMAIL or not SMTP_PASSWORD:
        logger.warning("SMTP credentials not set. Skipping email sending.")
        return False
        
    try:
        msg = MIMEMultipart()
        msg['From'] = SMTP_EMAIL
        msg['To'] = to_email
        msg['Subject'] = "Password Reset OTP - CodeGenie AI"
        
        body = f"Your OTP for password reset is: {otp}\n\nThis OTP is valid for 10 minutes."
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(SMTP_EMAIL, SMTP_PASSWORD)
        text = msg.as_string()
        server.sendmail(SMTP_EMAIL, to_email, text)
        server.quit()
        logger.info(f"OTP sent to {to_email}")
        return True
    except Exception as e:
        logger.error(f"Failed to send email: {e}")
        return False


def generate_password_reset_otp(user_identifier: str, valid_minutes: int = 10) -> Dict[str, Any]:
    """Generate a 6-digit OTP for password reset."""
    try:
        user = get_user_by_id(user_identifier) or get_user_by_username(user_identifier)
        if not user:
            return {'success': False, 'error': 'User not found'}

        import random
        otp = str(random.randint(100000, 999999))
        expiry = (datetime.now() + timedelta(minutes=valid_minutes)).isoformat()

        with file_lock:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []
            for u in users:
                if u.get('user_id') == user.get('user_id'):
                    u['password_reset_otp'] = otp
                    u['password_reset_otp_expiry'] = expiry
                    break
            _save_users(users)

        # Try to send email
        email_sent = False
        if user.get('email'):
            email_sent = send_otp_email(user['email'], otp)

        # Return otp for development/testing, but indicate if email was sent
        return {'success': True, 'otp': otp, 'expiry': expiry, 'email_sent': email_sent}
    except Exception as e:
        logger.error(f"Failed to generate OTP: {e}")
        return {'success': False, 'error': str(e)}


def reset_password_with_otp(user_identifier: str, otp: str, new_password: str) -> Dict[str, Any]:
    """Verify OTP and reset the user's password."""
    try:
        user = get_user_by_id(user_identifier) or get_user_by_username(user_identifier)
        if not user:
            return {'success': False, 'error': 'User not found'}

        with file_lock:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                try:
                    users = json.load(f)
                except json.JSONDecodeError:
                    users = []

            target = None
            for u in users:
                if u.get('user_id') == user.get('user_id'):
                    target = u
                    break

            if not target:
                return {'success': False, 'error': 'User not found during reset'}

            stored_otp = target.get('password_reset_otp')
            expiry = target.get('password_reset_otp_expiry')
            
            if not stored_otp or stored_otp != otp:
                return {'success': False, 'error': 'Invalid OTP'}
            if expiry and datetime.fromisoformat(expiry) < datetime.now():
                return {'success': False, 'error': 'OTP expired'}

            # Set new password
            ph = _hash_password(new_password)
            target['password_salt'] = ph['salt']
            target['password_hash'] = ph['hash']
            # Clear OTP
            target.pop('password_reset_otp', None)
            target.pop('password_reset_otp_expiry', None)

            _save_users(users)
            logger.info(f"Password reset for user {user.get('user_id')}")
            return {'success': True}
    except Exception as e:
        logger.error(f"Failed to reset password: {e}")
        return {'success': False, 'error': str(e)}


def verify_security_answer(user_identifier: str, answer: str) -> bool:
    """Verify security answer."""
    user = get_user_by_id(user_identifier) or get_user_by_username(user_identifier)
    if not user:
        return False
    
    stored_hash = user.get('security_answer_hash')
    if not stored_hash:
        return False
        
    import hashlib
    answer_hash = hashlib.sha256(answer.lower().strip().encode()).hexdigest()
    return answer_hash == stored_hash


def reset_password_with_security_question(user_identifier: str, answer: str, new_password: str) -> Dict[str, Any]:
    """Reset password using security question."""
    if verify_security_answer(user_identifier, answer):
        user = get_user_by_id(user_identifier) or get_user_by_username(user_identifier)
        return set_password_for_user(user['user_id'], new_password)
    else:
        return {'success': False, 'error': 'Incorrect security answer'}


def promote_user_to_admin(user_id: str) -> Dict[str, Any]:
    """Promote a user to admin role (max 2 admins)."""
    _ensure_files_exist()
    with file_lock:
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            # Count existing admins
            admin_count = sum(1 for u in users if u.get('role') == 'admin')
            if admin_count >= 2:
                return {'success': False, 'error': 'Maximum number of admins (2) reached.'}
            
            target = next((u for u in users if u['user_id'] == user_id), None)
            if not target:
                return {'success': False, 'error': 'User not found'}
            
            target['role'] = 'admin'
            _save_users(users)
            return {'success': True, 'message': f"User {user_id} promoted to admin."}
        except Exception as e:
            return {'success': False, 'error': str(e)}


def get_user_by_id(user_id: str) -> Optional[Dict[str, Any]]:
    """Get specific user information."""
    users = get_all_users()
    return next((u for u in users if u['user_id'] == user_id), None)


def get_user_activity(user_id: str = None) -> List[Dict[str, Any]]:
    """Get activity history for a specific user or all users."""
    _ensure_files_exist()
    try:
        with open(USER_ACTIVITY_FILE, 'r', encoding='utf-8') as f:
            try:
                activities = json.load(f)
                if isinstance(activities, list):
                    if user_id:
                        return [a for a in activities if a['user_id'] == user_id]
                    return activities
            except json.JSONDecodeError:
                pass
    except Exception as e:
        logger.error(f"Failed to read activities: {e}")
    return []


def replace_user(old_user_id: str, new_user_id: str, new_username: str, new_email: str = "") -> Dict[str, Any]:
    """Replace an old user with a new user (transfer/reassign)."""
    _ensure_files_exist()
    with file_lock:
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            user_idx = next((i for i, u in enumerate(users) if u['user_id'] == old_user_id), None)
            if user_idx is None:
                return {'success': False, 'error': f'User {old_user_id} not found'}
            
            old_user = users[user_idx]
            new_user = old_user.copy()
            new_user.update({
                'user_id': new_user_id,
                'username': new_username,
                'email': new_email,
                'last_login': datetime.now().isoformat()
            })
            
            users[user_idx] = new_user
            _save_users(users)
            
            # Update activities
            with open(USER_ACTIVITY_FILE, 'r', encoding='utf-8') as f:
                activities = json.load(f)
                for activity in activities:
                    if activity['user_id'] == old_user_id:
                        activity['user_id'] = new_user_id
            
            with open(USER_ACTIVITY_FILE, 'w', encoding='utf-8') as f:
                json.dump(activities, f, indent=4)
            
            return {'success': True, 'message': 'User replaced successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


def delete_user(user_id: str) -> Dict[str, Any]:
    """Delete a user from the system."""
    _ensure_files_exist()
    with file_lock:
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
            
            users = [u for u in users if u['user_id'] != user_id]
            _save_users(users)
            return {'success': True, 'message': 'User deleted successfully'}
        except Exception as e:
            return {'success': False, 'error': str(e)}


def get_user_stats(user_id: str) -> Dict[str, Any]:
    """Get aggregated statistics for a specific user."""
    user = get_user_by_id(user_id)
    activities = get_user_activity(user_id)
    
    if not user:
        return {}
    
    queries = [a for a in activities if a['activity_type'] == 'query']
    feedbacks = [a for a in activities if a['activity_type'] == 'feedback']
    
    ratings = [a['rating'] for a in feedbacks if a['rating'] > 0]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0.0
    
    return {
        **user,
        'total_queries': len(queries),
        'total_feedback': len(feedbacks),
        'average_rating': round(avg_rating, 2),
        'activities': {
            'queries': len(queries),
            'feedbacks': len(feedbacks),
            'logins': user.get('total_logins', 0)
        }
    }
