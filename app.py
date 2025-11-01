"""
app.py - Flask Backend for Emotion Detection Web App

Complete backend with database integration for storing predictions and images.
Configured for sklearn MLPClassifier model with 48x48 grayscale images.
"""
import json
import os
import sqlite3
from datetime import datetime
from io import BytesIO
import base64

import numpy as np
import cv2
from flask import Flask, render_template, request, jsonify, send_file
from PIL import Image
import joblib

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max upload

# Configuration
MODEL_PATH = 'emotion_mlp_model1.pkl'  # Your sklearn model
DB_FILE = 'emotion_detection.db'
IMG_SIZE = (48, 48)  # Model expects 48x48 images

# Emotion labels - UPDATE THIS to match your model's training data
# Your model was trained on 5 emotions
# EMOTION_LABELS = ['angry', 'happy', 'neutral', 'sad', 'surprise']
EMOTION_LABELS = ['angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral']
# EMOTION_LABELS = ['angry', 'fear', 'happy', 'sad', 'surprise']

# Global variables
model = None


def init_database():
    """Initialize SQLite database with required tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table 1: predictions - stores all prediction results with images
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_name TEXT NOT NULL,
            image_path TEXT,
            image_data BLOB NOT NULL,
            predicted_emotion TEXT NOT NULL,
            confidence REAL NOT NULL,
            all_probabilities TEXT,
            timestamp TEXT NOT NULL,
            source TEXT NOT NULL
        )
    """)
    
    # Table 2: users - tracks users (optional, for statistics)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            first_used TEXT NOT NULL,
            total_predictions INTEGER DEFAULT 0
        )
    """)
    
    # Table 3: model_info - stores model training information
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS model_info (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            model_name TEXT NOT NULL,
            created_at TEXT NOT NULL,
            accuracy REAL,
            epochs INTEGER,
            description TEXT
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✅ Database '{DB_FILE}' initialized successfully")


def load_model_and_labels():
    """Load the trained sklearn model."""
    global model
    
    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model file not found: {MODEL_PATH}")
        print("Please ensure emotion_mlp_model1.pkl is in the root directory")
        return False
    
    try:
        model = joblib.load(MODEL_PATH)
        print(f"✅ Model loaded from {MODEL_PATH}")
        print(f"✅ Emotion labels: {EMOTION_LABELS}")
        return True
    except Exception as e:
        print(f"❌ Error loading model: {e}")
        return False


def preprocess_image(img: Image.Image) -> np.ndarray:
    """
    Preprocess PIL image for sklearn model prediction.
    Converts to 48x48 grayscale and flattens to 1D array.
    """
    # Convert PIL image to numpy array
    img_array = np.array(img)
    
    # Convert to grayscale using OpenCV
    if len(img_array.shape) == 3:  # Color image
        img_gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
    else:  # Already grayscale
        img_gray = img_array
    
    # Resize to 48x48
    img_resized = cv2.resize(img_gray, IMG_SIZE)
    
    # Flatten to 1D array (2304 features)
    img_flattened = img_resized.flatten()
    
    # Normalize to 0-1
    img_normalized = img_flattened / 255.0
    
    # Reshape for sklearn (1 sample, 2304 features)
    img_preprocessed = img_normalized.reshape(1, -1)
    
    return img_preprocessed


def predict_emotion(img: Image.Image):
    """Run emotion prediction on image using sklearn model."""
    if model is None:
        return {'error': 'Model not loaded'}
    
    try:
        img_array = preprocess_image(img)
        
        # Get prediction (class index)
        predicted_idx = model.predict(img_array)[0]
        
        # Get probabilities for all classes
        probabilities = model.predict_proba(img_array)[0]
        
        predicted_emotion = EMOTION_LABELS[predicted_idx]
        confidence = float(probabilities[predicted_idx])
        
        # All probabilities
        all_probs = {
            EMOTION_LABELS[i]: float(probabilities[i]) 
            for i in range(len(EMOTION_LABELS))
        }
        
        return {
            'success': True,
            'emotion': predicted_emotion,
            'confidence': confidence,
            'all_probabilities': all_probs
        }
    except Exception as e:
        return {'error': str(e)}


def save_prediction_to_db(user_name: str, image_path: str, image_bytes: bytes,
                          predicted_emotion: str, confidence: float, 
                          all_probs: dict, source: str):
    """Save prediction result to database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        cursor.execute("""
            INSERT INTO predictions 
            (user_name, image_path, image_data, predicted_emotion, 
             confidence, all_probabilities, timestamp, source)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            user_name,
            image_path,
            image_bytes,
            predicted_emotion,
            confidence,
            json.dumps(all_probs),
            timestamp,
            source
        ))
        
        # Update user statistics
        cursor.execute("""
            SELECT id FROM users WHERE name = ?
        """, (user_name,))
        
        user = cursor.fetchone()
        if user:
            cursor.execute("""
                UPDATE users 
                SET total_predictions = total_predictions + 1
                WHERE name = ?
            """, (user_name,))
        else:
            cursor.execute("""
                INSERT INTO users (name, first_used, total_predictions)
                VALUES (?, ?, 1)
            """, (user_name, timestamp))
        
        conn.commit()
        prediction_id = cursor.lastrowid
        conn.close()
        
        return prediction_id
        
    except Exception as e:
        print(f"❌ Database error: {e}")
        return None


# ==================== ROUTES ====================

@app.route('/')
def index():
    """Render main page."""
    return render_template('index.html', emotions=EMOTION_LABELS)


@app.route('/predict', methods=['POST'])
def predict_upload():
    """Handle image upload and prediction."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    user_name = request.form.get('name', 'Anonymous')
    
    try:
        # Load and process image
        img = Image.open(file.stream)
        
        # Convert to grayscale for model (this is what the model expects)
        if img.mode != 'L':
            img_gray = img.convert('L')
        else:
            img_gray = img
        
        # Get prediction on grayscale image
        result = predict_emotion(img_gray)
        
        # Convert grayscale to RGB only for JPEG storage (JPEG doesn't support single-channel grayscale well)
        img_rgb = img_gray.convert('RGB')
        
        # Convert image to bytes for database
        img_byte_arr = BytesIO()
        img_rgb.save(img_byte_arr, format='JPEG')
        img_bytes = img_byte_arr.getvalue()
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Save to database
        prediction_id = save_prediction_to_db(
            user_name=user_name,
            image_path=file.filename,
            image_bytes=img_bytes,
            predicted_emotion=result['emotion'],
            confidence=result['confidence'],
            all_probs=result['all_probabilities'],
            source='upload'
        )
        
        result['prediction_id'] = prediction_id
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/predict_webcam', methods=['POST'])
def predict_webcam():
    """Handle webcam capture prediction."""
    data = request.get_json()
    
    if not data or 'image' not in data:
        return jsonify({'error': 'No image data provided'}), 400
    
    user_name = data.get('name', 'Anonymous')
    
    try:
        # Decode base64 image
        image_data = data['image'].split(',')[1] if ',' in data['image'] else data['image']
        img_bytes = base64.b64decode(image_data)
        img = Image.open(BytesIO(img_bytes))
        
        # Convert to grayscale for model (this is what the model expects)
        if img.mode != 'L':
            img_gray = img.convert('L')
        else:
            img_gray = img
        
        # Get prediction on grayscale image
        result = predict_emotion(img_gray)
        
        # Convert grayscale to RGB only for JPEG storage
        img_rgb = img_gray.convert('RGB')
        
        # Convert to JPEG for consistent storage
        img_byte_arr = BytesIO()
        img_rgb.save(img_byte_arr, format='JPEG')
        stored_img_bytes = img_byte_arr.getvalue()
        
        if 'error' in result:
            return jsonify(result), 500
        
        # Save to database
        prediction_id = save_prediction_to_db(
            user_name=user_name,
            image_path='webcam_capture.jpg',
            image_bytes=stored_img_bytes,
            predicted_emotion=result['emotion'],
            confidence=result['confidence'],
            all_probs=result['all_probabilities'],
            source='webcam'
        )
        
        result['prediction_id'] = prediction_id
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'Processing failed: {str(e)}'}), 500


@app.route('/history')
def get_history():
    """Get prediction history (without image data for performance)."""
    try:
        conn = sqlite3.connect(DB_FILE)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_name, image_path, predicted_emotion, 
                   confidence, all_probabilities, timestamp, source
            FROM predictions
            ORDER BY timestamp DESC
            LIMIT 50
        """)
        
        predictions = [dict(row) for row in cursor.fetchall()]
        conn.close()
        
        return jsonify({'predictions': predictions})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/image/<int:prediction_id>')
def get_image(prediction_id):
    """Retrieve stored image from database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT image_data FROM predictions WHERE id = ?
        """, (prediction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if row and row[0]:
            return send_file(BytesIO(row[0]), mimetype='image/jpeg')
        else:
            return jsonify({'error': 'Image not found'}), 404
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/statistics')
def get_statistics():
    """Get statistics about predictions and users."""
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Total predictions
        cursor.execute("SELECT COUNT(*) FROM predictions")
        total_predictions = cursor.fetchone()[0]
        
        # Predictions by emotion
        cursor.execute("""
            SELECT predicted_emotion, COUNT(*) as count
            FROM predictions
            GROUP BY predicted_emotion
        """)
        emotions_count = dict(cursor.fetchall())
        
        # Total users
        cursor.execute("SELECT COUNT(*) FROM users")
        total_users = cursor.fetchone()[0]
        
        # Top users
        cursor.execute("""
            SELECT name, total_predictions
            FROM users
            ORDER BY total_predictions DESC
            LIMIT 10
        """)
        top_users = [{'name': row[0], 'predictions': row[1]} for row in cursor.fetchall()]
        
        # Upload vs Webcam
        cursor.execute("""
            SELECT source, COUNT(*) as count
            FROM predictions
            GROUP BY source
        """)
        source_count = dict(cursor.fetchall())
        
        conn.close()
        
        return jsonify({
            'total_predictions': total_predictions,
            'emotions_count': emotions_count,
            'total_users': total_users,
            'top_users': top_users,
            'source_count': source_count
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'running',
        'model_loaded': model is not None,
        'database': os.path.exists(DB_FILE),
        'emotions': EMOTION_LABELS
    })


# ==================== MAIN ====================

if __name__ == '__main__':
    print("=" * 60)
    print("🎭 EMOTION DETECTION WEB APP - BACKEND")
    print("=" * 60)
    
    # Initialize database
    print("\n📊 Initializing database...")
    init_database()
    
    # Load model
    print("\n🤖 Loading emotion detection model...")
    model_loaded = load_model_and_labels()
    
    if model_loaded:
        print("\n✅ Backend ready!")
        print(f"📁 Database: {DB_FILE}")
        print(f"🎯 Emotions: {EMOTION_LABELS}")
        print(f"🌐 Starting Flask server on http://localhost:5000")
        print("=" * 60)
        
        app.run(debug=True, host='127.0.0.1', port=5000)
    else:
        print("\n❌ Failed to load model!")
        print("\nTo fix this:")
        print("1. Train a model first: python model.py")
        print("2. Or update MODEL_PATH in app.py to point to your model")
        print("=" * 60)
