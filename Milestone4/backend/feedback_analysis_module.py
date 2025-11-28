# -*- coding: utf-8 -*-
"""Feedback Analysis Module"""

import os
import logging
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from PIL import Image, ImageDraw, ImageFont
import io
import random
import string
import hashlib

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

CURRENT_FILE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(CURRENT_FILE_DIR, '..'))
STREAMLIT_APP_DIR = os.path.join(PROJECT_ROOT, 'streamlit_app')
AVATARS_DIR = os.path.join(STREAMLIT_APP_DIR, 'avatars')

analyzer = SentimentIntensityAnalyzer()

def analyze_sentiments(feedback_list):
    """Analyze sentiments of feedback comments."""
    results = []
    for feedback in feedback_list:
        text = feedback.get('comments', '')
        if text:
            score = analyzer.polarity_scores(text)
            results.append({
                'text': text,
                'compound': score['compound'],
                'pos': score['pos'],
                'neu': score['neu'],
                'neg': score['neg']
            })
    return results

def generate_avatar_image(username: str, email: str = None, size: int = 150) -> Image.Image:
    """Generate a default avatar image with initials."""
    # Check Gravatar first if email provided
    if email:
        import requests
        email_hash = hashlib.md5(email.lower().strip().encode()).hexdigest()
        gravatar_url = f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=404"
        try:
            response = requests.get(gravatar_url)
            if response.status_code == 200:
                return Image.open(io.BytesIO(response.content))
        except:
            pass

    # Fallback to generated image
    color = "#" + hashlib.md5(username.encode()).hexdigest()[:6]
    img = Image.new('RGB', (size, size), color=color)
    d = ImageDraw.Draw(img)
    
    initials = "".join([n[0] for n in username.split()[:2]]).upper()
    
    # Try to load a font, fallback to default
    try:
        font = ImageFont.truetype("arial.ttf", size // 2)
    except IOError:
        font = ImageFont.load_default()

    # Center text (approximate)
    d.text((size//3, size//3), initials, fill=(255, 255, 255), font=font)
    return img

def save_user_avatar(user_id: str, image_bytes: bytes) -> bool:
    """Save user uploaded avatar."""
    try:
        os.makedirs(AVATARS_DIR, exist_ok=True)
        path = os.path.join(AVATARS_DIR, f"{user_id}.png")
        with open(path, "wb") as f:
            f.write(image_bytes)
        return True
    except Exception as e:
        logger.error(f"Failed to save avatar: {e}")
        return False

def load_user_avatar(user_id: str) -> Optional[Image.Image]:
    """Load user avatar."""
    path = os.path.join(AVATARS_DIR, f"{user_id}.png")
    if os.path.exists(path):
        try:
            return Image.open(path)
        except:
            pass
    return None

def pil_image_to_bytes(image: Image.Image) -> bytes:
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format='PNG')
    return img_byte_arr.getvalue()

def generate_wordcloud_image(text_list):
    """Generate a simple word cloud image (without wordcloud lib dependency if possible, or using matplotlib)."""
    # Since we can't easily install wordcloud on all systems without C compiler, 
    # we'll use a simple matplotlib based one or just return a placeholder if complex.
    # For this milestone, let's try to use matplotlib to plot text randomly.
    
    import matplotlib.pyplot as plt
    
    text = " ".join(text_list)
    words = text.split()
    
    if not words:
        return Image.new('RGB', (400, 200), color='white')

    fig, ax = plt.subplots(figsize=(8, 4))
    ax.axis('off')
    
    from collections import Counter
    counts = Counter(words)
    
    for word, count in counts.most_common(30):
        size = min(50, max(10, count * 5))
        x = random.random()
        y = random.random()
        ax.text(x, y, word, fontsize=size, ha='center', va='center', rotation=random.choice([0, 90]))
        
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    plt.close(fig)
    buf.seek(0)
    return Image.open(buf)
