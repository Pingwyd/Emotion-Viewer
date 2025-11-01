# 🎯 Command Reference - Quick Copy/Paste

All the commands you need, ready to copy and paste!

## 📦 Installation

```powershell
# Activate virtual environment (if you have one)
.\.venv\Scripts\Activate.ps1

# Install all dependencies
python -m pip install -r requirements.txt

# Install just TensorFlow (if you want to install separately)
python -m pip install tensorflow

# Update pip (optional but recommended)
python -m pip install --upgrade pip
```

---

## 🤖 Training Commands

```powershell
# Basic training (recommended)
python model.py --data_dir ..\data --model_out emotion_model.h5 --epochs 10 --batch_size 16

# Quick test (3 epochs)
python model.py --data_dir ..\data --epochs 3 --batch_size 16

# Low memory training
python model.py --data_dir ..\data --batch_size 8 --img_size 128 128

# Custom CNN (no transfer learning)
python model.py --data_dir ..\data --no_transfer --epochs 20

# Different model name
python model.py --data_dir ..\data --model_out my_custom_model.h5 --epochs 15

# Full training with all options
python model.py --data_dir ..\data --model_out emotion_v2.h5 --epochs 20 --batch_size 32 --img_size 224 224
```

---

## 🌐 Running the Web App

```powershell
# Start the Flask server
python app.py

# Then open in browser: http://localhost:5000
```

---

## 🔍 Testing & Verification

```powershell
# Check Python version
python --version

# Check if TensorFlow is installed
python -c "import tensorflow as tf; print(tf.__version__)"

# Check if Flask is installed
python -c "import flask; print(flask.__version__)"

# List installed packages
python -m pip list

# Check model file exists
dir emotion_model.h5

# Check database exists
dir runs.db

# Run Python import test
python -c "import sys; sys.path.insert(0, '.'); import model; print('Import OK')"
```

---

## 📂 Git Commands

```powershell
# Initialize Git repository
git init

# Add all files
git add .

# Commit changes
git commit -m "Initial commit - Emotion Detection App"

# Set main branch
git branch -M main

# Add remote repository (replace with your URL)
git remote add origin https://github.com/yourusername/emotion-detection.git

# Push to GitHub
git push -u origin main

# Check status
git status

# View commit history
git log --oneline

# Create .gitignore
echo "__pycache__/" > .gitignore
echo ".venv/" >> .gitignore
echo "*.pyc" >> .gitignore
```

---

## 🚀 Deployment Commands (Render)

```powershell
# Add gunicorn to requirements
echo "gunicorn" >> requirements.txt

# Create Procfile
echo "web: gunicorn app:app --bind 0.0.0.0:$PORT" > Procfile

# Commit deployment files
git add requirements.txt Procfile
git commit -m "Add deployment configuration"
git push

# Then deploy on Render.com using their web interface
```

---

## 📊 Database Commands

```powershell
# Open SQLite database (if you have sqlite3 installed)
sqlite3 runs.db

# Inside SQLite shell:
.tables                          # List all tables
.schema models                   # Show models table schema
.schema predictions              # Show predictions table schema
SELECT * FROM models;            # View all training runs
SELECT * FROM predictions;       # View all predictions
SELECT COUNT(*) FROM predictions; # Count predictions
.exit                            # Exit SQLite

# Python one-liner to view database
python -c "import sqlite3; conn = sqlite3.connect('runs.db'); print(conn.execute('SELECT * FROM predictions').fetchall())"
```

---

## 🧹 Cleanup Commands

```powershell
# Remove Python cache
Remove-Item -Recurse -Force __pycache__

# Remove generated model files (careful!)
Remove-Item emotion_model.h5
Remove-Item emotion_model_labels.json
Remove-Item emotion_model_history.json

# Remove database (careful!)
Remove-Item runs.db

# Clean virtual environment (careful!)
Remove-Item -Recurse -Force .venv

# Start fresh (recreate venv)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 📦 Creating Submission ZIP

```powershell
# Rename folder first (replace with your details)
cd ..
Rename-Item "root" "SURNAME_MATNO_EMOTION_DETECTION_WEB_APP"

# Create ZIP using PowerShell (Windows 10+)
Compress-Archive -Path "SURNAME_MATNO_EMOTION_DETECTION_WEB_APP" -DestinationPath "SURNAME_MATNO_EMOTION_DETECTION_WEB_APP.zip"

# Or use 7-Zip if installed
7z a SURNAME_MATNO_EMOTION_DETECTION_WEB_APP.zip SURNAME_MATNO_EMOTION_DETECTION_WEB_APP
```

---

## 🐛 Debugging Commands

```powershell
# Check which Python is being used
where python

# Check Python path
python -c "import sys; print(sys.executable)"

# Check if GPU is available (TensorFlow)
python -c "import tensorflow as tf; print('GPU Available:', tf.config.list_physical_devices('GPU'))"

# Check Flask app in debug mode
$env:FLASK_APP = "app.py"
$env:FLASK_DEBUG = "1"
flask run

# Test single prediction (after model is trained)
python -c "from app import predict_emotion; from PIL import Image; img = Image.open('test.jpg'); print(predict_emotion(img))"

# View Flask routes
python -c "from app import app; print([str(rule) for rule in app.url_map.iter_rules()])"
```

---

## 🔧 Troubleshooting Commands

```powershell
# Reinstall TensorFlow (if having issues)
pip uninstall tensorflow
pip install tensorflow

# Install specific TensorFlow version
pip install tensorflow==2.15.0

# Check for pip issues
python -m pip check

# Upgrade all packages (careful!)
pip list --outdated
pip install --upgrade package_name

# Clear pip cache
pip cache purge

# Install from requirements without cache
pip install --no-cache-dir -r requirements.txt
```

---

## 📊 Performance Testing

```powershell
# Time model training
Measure-Command { python model.py --data_dir ..\data --epochs 1 }

# Check model size
dir emotion_model.h5 | Select-Object Name, Length

# Monitor memory usage while running
Get-Process python | Select-Object Name, CPU, WorkingSet

# Test prediction speed
python -c "import time; from app import model, preprocess_image; from PIL import Image; img = Image.open('test.jpg'); start = time.time(); predictions = model.predict(preprocess_image(img)); print(f'Inference time: {time.time()-start:.3f}s')"
```

---

## 🌐 Network Testing

```powershell
# Check if Flask is running
curl http://localhost:5000

# Test prediction endpoint (PowerShell)
$form = @{
    image = Get-Item -Path "test.jpg"
    name = "TestUser"
}
Invoke-WebRequest -Uri "http://localhost:5000/predict" -Method Post -Form $form

# Check if port is in use
netstat -ano | findstr :5000

# Kill process on port 5000 (if needed)
Stop-Process -Id (Get-NetTCPConnection -LocalPort 5000).OwningProcess -Force
```

---

## 📝 Documentation Generation

```powershell
# Generate requirements.txt from current environment
pip freeze > requirements.txt

# Count lines of code
Get-ChildItem -Recurse -Include *.py | Get-Content | Measure-Object -Line

# Find TODO comments
Select-String -Path *.py -Pattern "TODO|FIXME|HACK"

# List all Python files
Get-ChildItem -Recurse -Include *.py | Select-Object FullName
```

---

## 🎓 Useful One-Liners

```powershell
# Quick syntax check (no execution)
python -m py_compile model.py app.py

# Format Python code (if you have black installed)
pip install black
black model.py app.py

# Check code style (if you have flake8 installed)
pip install flake8
flake8 model.py app.py

# Generate project tree
tree /F

# Count files in project
(Get-ChildItem -Recurse -File).Count

# Total project size
"{0:N2} MB" -f ((Get-ChildItem -Recurse | Measure-Object -Property Length -Sum).Sum / 1MB)
```

---

## 🆘 Emergency Quick Fixes

```powershell
# If training crashes, reduce batch size
python model.py --data_dir ..\data --batch_size 4 --epochs 3

# If app won't start, check if model exists
Test-Path emotion_model.h5

# If port is busy, use different port
# Edit app.py: app.run(debug=True, port=5001)

# If import errors, reinstall package
pip uninstall package_name
pip install package_name

# If Git issues, force push (careful!)
git push -f origin main

# If virtual environment issues, recreate it
Remove-Item -Recurse -Force .venv
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

---

## 💡 Pro Tips

```powershell
# Create alias for common commands (add to PowerShell profile)
Set-Alias train "python model.py --data_dir ..\data --epochs 10"
Set-Alias serve "python app.py"

# Create batch file for training
echo "python model.py --data_dir ..\data --epochs 10 --batch_size 16" > train.bat

# Create batch file for running app
echo "python app.py" > run.bat

# Then just run:
.\train.bat
.\run.bat
```

---

**Copy and paste these commands as needed! 📋✨**
