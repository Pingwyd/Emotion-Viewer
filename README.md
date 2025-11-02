# 🎭 Emotion Detection Web App

A complete emotion detection system using scikit-learn's MLPClassifier. Detects 5 emotions from uploaded images or live webcam capture with a trained neural network model.

## 🌐 Live Demo

**Deployed App**: https://emotion-viewer.onrender.com

## 📁 Project Structure

```
emotion-viewer/
├── app.py                          # Flask web application
├── model.py                        # Training script for MLP model
├── model.pkl                       # Trained scikit-learn model (19MB)
├── requirements.txt                # Python dependencies
├── runtime.txt                     # Python version for deployment
├── render.yaml                     # Render deployment configuration
├── Procfile                        # Process file for deployment
├── .gitignore                      # Git ignore file
├── templates/
│   └── index.html                  # Web UI with upload & webcam support
├── emotion_detection.db            # SQLite database for predictions (created on first run)
├── init_database.py                # Database initialization script
└──  query_database.py               # Database query utility
```

## 🎯 Emotion Classes

The model detects **5 emotions**:
- Angry
- Fear
- Happy
- Sad
- Suprise *(note: typo preserved for model compatibility)*

## 🚀 Quick Start

### Step 1: Install Dependencies

First, activate your virtual environment:

```powershell
# Windows PowerShell
.\.venv\Scripts\Activate.ps1

# Or if using cmd
.\.venv\Scripts\activate.bat
```

Then install required packages:

```powershell
pip install -r requirements.txt
```

**Key Dependencies:**
- Flask 3.0+ - Web framework
- scikit-learn 1.3+ - Machine learning (MLPClassifier)
- numpy - Numerical operations
- opencv-python-headless - Image processing
- Pillow - Image handling
- joblib - Model serialization
- gunicorn - Production WSGI server

### Step 2: Run the Web Application

The model (`model.pkl`) is already trained and included in the repository.

Start the Flask development server:

```powershell
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

### Step 3: (Optional) Train Your Own Model

If you want to train a new model with your own dataset:

Your dataset should be organized with one folder per emotion class:

```
data/
  Angry/
    img1.jpg
    img2.jpg
  Happy/
    img1.jpg
  Sad/
    img1.jpg
  Fear/
    img1.jpg
  Suprise/
    img1.jpg
```

Then run the training script:

```powershell
python model.py
```

**Note**: The current `model.pkl` was trained on 50000+ emotion images

## 🎨 Features

### Web Interface
- **Image Upload**: Upload any image (JPG, PNG) to detect emotions
- **Live Webcam**: Capture images in real-time from your webcam
- **User Tracking**: Optional name field to track predictions per user
- **Prediction Results**: Shows detected emotion with confidence percentage
- **All Probabilities**: Visual bar chart showing probabilities for all 5 emotions
- **History API**: `/history` endpoint to view last 50 predictions
- **Statistics API**: `/statistics` endpoint for usage analytics
- **Health Check**: `/health` endpoint for monitoring

### Backend (app.py)
- **scikit-learn MLPClassifier**: Fast neural network for image classification
- **Image Preprocessing**: Converts images to 48x48 grayscale, flattens to 2304 features
- **Database Storage**: SQLite database with BLOB storage for images
- **Real-time Predictions**: Instant inference on uploaded or captured images
- **User Statistics**: Tracks total predictions per user
- **Source Tracking**: Distinguishes between upload and webcam predictions
- **Production Ready**: Gunicorn-compatible with proper module-level initialization

### Model (model.py)
- **Algorithm**: MLPClassifier (Multi-layer Perceptron)
- **Input**: 48x48 grayscale images (2304 features)
- **Output**: 5 emotion classes with probabilities
- **Training**: Uses emotion image dataset
- **Serialization**: Saved as `model.pkl` using joblib
- **Size**: ~19MB trained model
  - Confidence score
  - All class probabilities
  - Timestamp
  - Source (upload or webcam)

## 📊 Database Schema

The `emotion_detection.db` SQLite database contains three tables:

**predictions table**:
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_name TEXT NOT NULL,
    image_path TEXT,
    image_data BLOB NOT NULL,           -- Stores actual image as JPEG
    predicted_emotion TEXT NOT NULL,
    confidence REAL NOT NULL,
    all_probabilities TEXT,             -- JSON string of all probabilities
    timestamp TEXT NOT NULL,
    source TEXT NOT NULL                -- 'upload' or 'webcam'
)
```

**users table**:
```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    first_used TEXT NOT NULL,
    total_predictions INTEGER DEFAULT 0
)
```

**model_info table**:
```sql
CREATE TABLE model_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    created_at TEXT NOT NULL,
    accuracy REAL,
    epochs INTEGER,
    description TEXT
)
```

### Database Utilities

**View all predictions**:
```powershell
python query_database.py
```

**Retrieve stored images**: Use the `/image/<id>` endpoint:
```
http://localhost:5000/image/1
```

**View statistics**:
```
http://localhost:5000/statistics
```

## 🔧 API Endpoints

### Main Routes
- `GET /` - Main web interface
- `POST /predict` - Upload image prediction (multipart/form-data)
- `POST /predict_webcam` - Webcam capture prediction (JSON with base64 image)

### Data Routes
- `GET /history` - Get last 50 predictions (without image data)
- `GET /image/<id>` - Retrieve stored image by prediction ID
- `GET /statistics` - Get usage statistics (predictions by emotion, top users, etc.)
- `GET /health` - Health check and debugging info

### Example API Usage

**Upload prediction** (using curl):
```bash
curl -X POST -F "image=@photo.jpg" -F "name=John" http://localhost:5000/predict
```

**Webcam prediction** (JavaScript):
```javascript
const response = await fetch('/predict_webcam', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({
        image: canvasElement.toDataURL('image/jpeg'),
        name: 'John'
    })
});
```

## 🌐 Deployment to Render

This app is configured for easy deployment to Render:

### Configuration Files
- **`render.yaml`** - Render service configuration
- **`runtime.txt`** - Specifies Python 3.11.9
- **`requirements.txt`** - All dependencies with compatible versions
- **`Procfile`** - Backup process file (optional)

### Deployment Steps

1. **Push to GitHub**:
   ```powershell
   git add .
   git commit -m "Deploy to Render"
   git push origin main
   ```

2. **Create Render Service**:
   - Go to https://dashboard.render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will auto-detect `render.yaml`

3. **Environment Settings** (auto-configured by render.yaml):
   - **Build Command**: `pip install --upgrade pip && pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Python Version**: 3.11.9
   - **Plan**: Free

4. **Wait for deployment** (3-5 minutes)

5. **Access your app**: `https://your-app-name.onrender.com`

### Important Notes for Deployment
- Model file (`model.pkl`) is tracked in Git (~19MB)
- Database (`emotion_detection.db`) is created on first run
- Render free tier may sleep after inactivity (cold starts ~30 seconds)
- Logs are available in Render dashboard under "Logs" tab

## 📦 Requirements

```txt
# Build Tools
setuptools>=70.0.0
wheel>=0.43.0

# Core ML
numpy>=1.26.0
opencv-python-headless>=4.9.0.80
Pillow>=10.2.0
scikit-learn>=1.4.0
joblib>=1.3.2

# Web Framework
Flask>=3.0.0

# Deployment
gunicorn>=21.2.0
```

**Python Version**: 3.11.9 (specified in `runtime.txt`)

## 🐛 Troubleshooting

### Local Development Issues

**"Model not found" error:**
- Ensure `model.pkl` exists in the root directory
- Check the `MODEL_PATH` variable in `app.py` (line 24)

**Database errors:**
- Delete `emotion_detection.db` and restart the app (it will recreate)
- Run `python init_database.py` to manually initialize

**Import errors:**
- Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

**Webcam not working:**
- Check browser permissions for camera access
- Try Chrome/Edge (better webcam support)
- Webcam requires HTTPS on deployed sites

### Deployment Issues (Render)

**Build failures:**
- Check that `runtime.txt` specifies Python 3.11.9
- Ensure `render.yaml` is in the root directory
- Check Render logs for specific error messages

**"Model not loaded" error on deployed app:**
- Verify `model.pkl` is tracked in Git: `git ls-files | findstr model.pkl`
- Check the file wasn't excluded by `.gitignore`
- Visit `/health` endpoint to see diagnostic info

**App is slow/sleeping:**
- Render free tier sleeps after 15 minutes of inactivity
- First request after sleep takes ~30 seconds (cold start)
- Consider upgrading to paid tier for always-on service

**Scikit-learn version warnings:**
- Model was trained with scikit-learn 1.6.1
- Deployment uses 1.4.0+ (may show compatibility warnings)
- Warnings are safe to ignore if predictions work correctly

## 🔄 Git Repository

**Repository**: https://github.com/Pingwyd/Emotion-Viewer  
**Branch**: main

### Files Excluded from Git (`.gitignore`)
- `.venv/` - Virtual environment
- `__pycache__/` - Python cache
- `*.pyc` - Compiled Python files
- `emotion_detection.db` - Local database
- `data/` - Testing dataset (270+ images)
- `random/` - Random test files
- `exported_images/` - Exported image files
- `export_images.py` - Utility script

### Files Tracked in Git
- ✅ `model.pkl` - Trained model (19MB)
- ✅ `app.py` - Main application
- ✅ All configuration files
- ✅ `templates/` - Web interface
- ✅ README.md

## 📝 Project History & Changes

### Recent Updates
- **Nov 2, 2025**: Fixed gunicorn compatibility - moved model loading to module level
- **Nov 2, 2025**: Added detailed logging and debugging for deployment
- **Nov 2, 2025**: Updated requirements.txt for Python 3.11 compatibility
- **Nov 2, 2025**: Added `render.yaml` for explicit Render configuration
- **Nov 2, 2025**: Cleaned up repository - removed .venv/, data/, random/ from Git
- **Nov 2, 2025**: Renamed main branch from master to main
- **Nov 2, 2025**: Deployed to Render at https://emotion-viewer.onrender.com

### Technology Stack Evolution
- Originally used TensorFlow/Keras with transfer learning
- Switched to scikit-learn MLPClassifier for simpler deployment
- Reduced dependencies from 330MB to ~50MB
- Faster build times and easier maintenance

**Live Demo**: https://emotion-viewer.onrender.com

## 📄 License

This project was created for educational purposes as part of a university assignment.
