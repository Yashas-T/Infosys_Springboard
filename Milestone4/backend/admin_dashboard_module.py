# -*- coding: utf-8 -*-
"""Admin Dashboard Module"""

import json
import os
import logging
from typing import Dict, List, Any, Optional
from collections import Counter

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Resolve paths
CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_DIR, '..'))
STREAMLIT_APP_DIR = os.path.join(PROJECT_ROOT, 'streamlit_app')

def _resolve_log_file(filename: str) -> str:
    """Return an existing path for filename by trying several common locations."""
    candidates = []
    candidates.append(os.path.join(STREAMLIT_APP_DIR, filename))
    candidates.append(os.path.join(os.getcwd(), 'streamlit_app', filename))
    candidates.append(os.path.join(PROJECT_ROOT, filename))
    candidates.append(os.path.join(CURRENT_FILE_DIR, filename))

    tried = []
    for path in candidates:
        p = os.path.normpath(os.path.abspath(path))
        tried.append(p)
        if os.path.exists(p):
            return p

    # Default to streamlit_app dir if not found
    return os.path.normpath(os.path.abspath(os.path.join(STREAMLIT_APP_DIR, filename)))

def load_data():
    """Load data from JSON logs."""
    feedback_file = _resolve_log_file('feedback_log.json')
    history_file = _resolve_log_file('user_history.json')
    users_file = _resolve_log_file('users.json')

    feedback_data = []
    if os.path.exists(feedback_file):
        try:
            with open(feedback_file, 'r', encoding='utf-8') as f:
                feedback_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading feedback: {e}")

    history_data = []
    if os.path.exists(history_file):
        try:
            with open(history_file, 'r', encoding='utf-8') as f:
                history_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading history: {e}")

    users_data = []
    if os.path.exists(users_file):
        try:
            with open(users_file, 'r', encoding='utf-8') as f:
                users_data = json.load(f)
        except Exception as e:
            logger.error(f"Error loading users: {e}")

    return feedback_data, history_data, users_data

def get_dashboard_stats():
    """Compute statistics for the dashboard."""
    feedback_data, history_data, users_data = load_data()

    total_queries = len(history_data)
    total_feedback = len(feedback_data)
    
    ratings = [f['rating'] for f in feedback_data if isinstance(f.get('rating'), (int, float))]
    avg_rating = sum(ratings) / len(ratings) if ratings else 0.0

    # Active users (unique users in history)
    active_users = len(set(h['user_id'] for h in history_data if 'user_id' in h))
    
    # Top languages
    languages = [h.get('language', 'Unknown') for h in history_data]
    lang_counts = Counter(languages)
    top_languages = dict(lang_counts.most_common(5))

    # Recent feedback
    recent_feedback = sorted(feedback_data, key=lambda x: x.get('timestamp', ''), reverse=True)[:5]

    return {
        'total_queries': total_queries,
        'total_feedback': total_feedback,
        'average_rating': round(avg_rating, 2),
        'active_users': active_users,
        'top_languages': top_languages,
        'recent_feedback': recent_feedback,
        'total_users': len(users_data)
    }

def search_global(query: str):
    """Search across users, history, and feedback."""
    feedback_data, history_data, users_data = load_data()
    query = query.lower()
    
    results = {
        'users': [],
        'history': [],
        'feedback': []
    }
    
    # Search users
    for u in users_data:
        if query in str(u.get('username', '')).lower() or query in str(u.get('user_id', '')).lower():
            results['users'].append(u)
            
    # Search history
    for h in history_data:
        if query in str(h.get('query', '')).lower() or query in str(h.get('generated_code', '')).lower():
            results['history'].append(h)
            
    # Search feedback
    for f in feedback_data:
        if query in str(f.get('comments', '')).lower() or query in str(f.get('query', '')).lower():
            results['feedback'].append(f)
            
    return results
