# ⚡ Quick Start Guide

Get your Emotion Detection app running in 3 steps!

## 🎯 What You Need

- Python 3.8 or higher
- Your dataset in the `data` folder (Angry, Happy, Sad folders)
- About 5-10 minutes

## 📝 Step-by-Step Instructions

### Step 1️⃣: Install Dependencies

Open PowerShell in the project folder and run:

```powershell
# Activate virtual environment (if you have one)
.\.venv\Scripts\Activate.ps1

# Install required packages (this takes 3-5 minutes)
python -m pip install -r requirements.txt
```

**Note:** TensorFlow is ~330 MB, so the download may take a few minutes depending on your internet speed.

---

### Step 2️⃣: Train Your Model

Run the training script with your dataset:

```powershell
python model.py --data_dir ..\data --model_out emotion_model.h5 --epochs 10 --batch_size 16
```

**What this does:**
- Loads images from `../data` folder
- Trains for 10 epochs (adjust based on your dataset size)
- Saves the trained model as `emotion_model.h5`
- Creates `emotion_model_labels.json` with class names
- Logs training metrics to `runs.db` database

**Training time:**
- Small dataset (100-500 images): 2-5 minutes
- Medium dataset (500-2000 images): 5-15 minutes
- Large dataset (2000+ images): 15-60 minutes

**Adjust settings if needed:**
- Low memory? Use `--batch_size 8`
- Quick test? Use `--epochs 3`
- Different size? Use `--img_size 128 128`

---

### Step 3️⃣: Run the Web App

Start the Flask server:

```powershell
python app.py
```

You should see:
```
Loading model and labels...
Model loaded from emotion_model.h5
Labels loaded: ['Angry', 'Happy', 'Sad']
Ready! Starting Flask server...
 * Running on http://0.0.0.0:5000
```

**Open your browser** and go to:
```
http://localhost:5000
```

---

## 🎨 Using the Web App

### Upload Image Tab:
1. (Optional) Enter your name
2. Click "Choose an image" and select a photo
3. Click "Detect Emotion"
4. See the detected emotion with confidence score!

### Live Webcam Tab:
1. (Optional) Enter your name
2. Click "Start Webcam" (allow camera access if prompted)
3. Position yourself in the frame
4. Click "Capture & Detect"
5. See the detected emotion!

---

## ✅ Verify Everything Works

Test these features:

- [ ] Upload an image → Get emotion prediction
- [ ] Start webcam → Capture → Get prediction
- [ ] Check different images show different emotions
- [ ] View prediction history at: `http://localhost:5000/history`

---

## 🐛 Troubleshooting

### Problem: "Model file not found"
**Solution:** Make sure you completed Step 2 (training). Check that `emotion_model.h5` exists.

### Problem: "Import tensorflow could not be resolved"
**Solution:** Install TensorFlow: `pip install tensorflow`

### Problem: Training is very slow
**Solution:** 
- Reduce batch size: `--batch_size 8`
- Use fewer epochs for testing: `--epochs 3`
- GPU highly recommended for large datasets

### Problem: Webcam doesn't work
**Solution:**
- Check browser permissions (allow camera access)
- Try Chrome or Edge browser
- On deployed site, HTTPS is required for webcam

### Problem: Out of memory error
**Solution:**
- Reduce batch size: `--batch_size 4`
- Use smaller images: `--img_size 128 128`
- Close other applications

---

## 📚 Next Steps

Once everything works locally:

1. **Test thoroughly** with different images
2. **Push to GitHub** (see DEPLOYMENT_GUIDE.md)
3. **Deploy to web** (Render, Railway, etc.)
4. **Update link_to_web_app.txt** with your URL
5. **Prepare for submission:**
   - Rename folder: `SURNAME_MATNO_EMOTION_DETECTION_WEB_APP`
   - Zip the project
   - Email to instructor

---

## 📞 Need Help?

Check these files for detailed information:
- `README.md` - Complete documentation
- `DEPLOYMENT_GUIDE.md` - Hosting instructions
- `model.py` - Training script with comments
- `app.py` - Web app with comments

---

**You're all set! Happy coding! 🚀**
