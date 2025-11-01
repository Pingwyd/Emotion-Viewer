# 🎭 Emotion Detection Web App

A complete emotion detection system with training script and web interface. Detects emotions from uploaded images or live webcam capture.

## 📁 Project Structure

```
root/
├── app.py                    # Flask web application
├── model.py                  # Training script
├── requirements.txt          # Python dependencies
├── templates/
│   └── index.html           # Web UI with upload & webcam support
├── emotion_model.h5         # Trained model (after training)
├── emotion_model_labels.json # Class labels (after training)
└── runs.db                  # SQLite database for predictions
```

## 🚀 Quick Start

### Step 1: Install Dependencies

First, activate your virtual environment (if you have one):

```powershell
.\.venv\Scripts\Activate.ps1
```

Then install required packages (this will take a few minutes as TensorFlow is ~330 MB):

```powershell
python -m pip install -r requirements.txt
```

### Step 2: Train the Model

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
```

Train the model (adjust epochs and batch_size as needed):

```powershell
python model.py --data_dir ..\data --model_out emotion_model.h5 --epochs 10 --batch_size 16
```

**Training options:**
- `--data_dir`: Path to your dataset folder (required)
- `--model_out`: Output model filename (default: `emotion_model.h5`)
- `--epochs`: Number of training epochs (default: 10)
- `--batch_size`: Batch size for training (default: 32)
- `--img_size`: Image size as two integers (default: 224 224)
- `--no_transfer`: Disable transfer learning and use small CNN

**What gets created after training:**
- `emotion_model.h5` - The trained Keras model
- `emotion_model_labels.json` - Class names/labels
- `emotion_model_history.json` - Training metrics and history
- `runs.db` - SQLite database with training run metadata

### Step 3: Run the Web Application

After training is complete, start the Flask server:

```powershell
python app.py
```

Then open your browser and go to:
```
http://localhost:5000
```

## 🎨 Features

### Web Interface
- **Image Upload**: Upload any image to detect emotions
- **Live Webcam**: Capture images in real-time from your webcam
- **User Tracking**: Optional name field to track who used the app
- **Prediction Results**: Shows detected emotion with confidence scores
- **All Probabilities**: Visual bar chart showing all emotion probabilities
- **History**: All predictions are logged to database

### Backend
- **Transfer Learning**: Uses MobileNetV2 pre-trained on ImageNet
- **Real-time Predictions**: Fast inference on uploaded or captured images
- **Database Logging**: SQLite database tracks all predictions with:
  - User name
  - Image filename
  - **Actual image data (BLOB)** - stores the full image
  - Predicted emotion
  - Confidence score
  - All class probabilities
  - Timestamp
  - Source (upload or webcam)

## 📊 Database Schema

The `runs.db` SQLite database contains two tables:

**models table** (from training):
```sql
CREATE TABLE models (
    id INTEGER PRIMARY KEY,
    filename TEXT,
    created_at TEXT,
    epochs INTEGER,
    batch_size INTEGER,
    img_size TEXT,
    training_accuracy REAL,
    validation_accuracy REAL
)
```

**predictions table** (from web app):
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    image_path TEXT,
    image_data BLOB,              -- Stores actual image as binary data
    predicted_label TEXT,
    confidence REAL,
    all_probabilities TEXT,
    created_at TEXT,
    source TEXT
)
```

**Retrieve stored images**: Use the `/image/<id>` endpoint:
```
http://localhost:5000/image/1
```

## 🔧 Advanced Usage

### Custom CNN (no transfer learning)
```powershell
python model.py --data_dir ..\data --model_out custom_model.h5 --no_transfer --epochs 20
```

### Different image size
```powershell
python model.py --data_dir ..\data --img_size 128 128 --epochs 15
```

### Update model path in app.py
If you use a different model name, update these lines in `app.py`:
```python
MODEL_PATH = 'your_model_name.h5'
LABELS_PATH = 'your_model_name_labels.json'
```

## 🌐 Deployment

### For Assignment Submission

1. **GitHub**: Push your code to a repository
2. **Hosting**: Deploy to a free platform:
   - **Render**: https://render.com (recommended for Flask apps)
   - **Railway**: https://railway.app
   - **PythonAnywhere**: https://www.pythonanywhere.com
   - **Heroku**: https://heroku.com (may require credit card)

3. **Save hosting link** in `link_to_my_web_app.txt`:
   ```
   Render - https://your-app-name.onrender.com
   ```

4. **Rename root folder** to: `YOURSURNAME_MATNO_EMOTION_DETECTION_WEB_APP`

5. **Zip and submit** to: odunayo.osofuye@covenantuniversity.edu.ng

## 📦 Requirements

- Python 3.8+
- TensorFlow 2.9+
- Flask
- NumPy
- Pillow
- OpenCV (optional, for advanced image processing)

## 🐛 Troubleshooting

**"Model not found" error:**
- Make sure you've run `model.py` first to train the model
- Check that `emotion_model.h5` and `emotion_model_labels.json` exist

**TensorFlow import error:**
- Install TensorFlow: `pip install tensorflow`
- On Windows, you may need Microsoft Visual C++ Redistributable

**Webcam not working:**
- Check browser permissions for camera access
- Try a different browser (Chrome/Edge recommended)
- HTTPS required for webcam on deployed sites

**Out of memory during training:**
- Reduce batch size: `--batch_size 8`
- Use smaller image size: `--img_size 128 128`
- Reduce dataset size or use fewer epochs

## 📝 Notes

- The model uses transfer learning with MobileNetV2 by default (fast and accurate)
- Training time depends on dataset size and hardware (GPU recommended)
- First training will download ImageNet weights (~14 MB)
- All predictions are logged to the database for tracking and analysis
