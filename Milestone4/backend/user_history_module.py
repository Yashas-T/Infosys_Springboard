# -*- coding: utf-8 -*-
"""User History Module"""

import json
import os
import logging
import threading
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_DIR, '..'))
STREAMLIT_APP_DIR = os.path.join(PROJECT_ROOT, 'streamlit_app')
HISTORY_FILE = os.path.join(STREAMLIT_APP_DIR, 'user_history.json')
file_lock = threading.Lock()

def log_user_query(user_id: str, query: str, language: str, generated_code: str, explanation: str, model_name: str) -> None:
    """
    Logs user query and generated response to history.
    """
    entry = {
        'timestamp': datetime.now().isoformat(),
        'user_id': user_id,
        'query': query,
        'language': language,
        'generated_code': generated_code,
        'explanation': explanation,
        'model': model_name
    }

    with file_lock:
        try:
            if os.path.exists(HISTORY_FILE):
                with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                    try:
                        data = json.load(f)
                        if not isinstance(data, list):
                            data = []
                    except json.JSONDecodeError:
                        data = []
            else:
                data = []

            data.append(entry)

            os.makedirs(os.path.dirname(HISTORY_FILE), exist_ok=True)
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4)
            
            # Also log to activity
            try:
                import sys
                if PROJECT_ROOT not in sys.path:
                    sys.path.append(PROJECT_ROOT)
                from backend.user_management_module import log_user_activity
                log_user_activity(user_id, 'query', query, language, 0, "", model_name)
            except Exception as e:
                logger.warning(f"Could not log to user activity: {e}")

        except Exception as e:
            logger.error(f"Failed to log history: {e}")
