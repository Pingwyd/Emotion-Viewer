# 🚀 Deployment Guide

Complete guide to deploy your Emotion Detection Web App to a free hosting platform.

## 📋 Pre-Deployment Checklist

Before deploying, ensure you have:

- ✅ Trained model file (`emotion_model.h5`)
- ✅ Labels file (`emotion_model_labels.json`)
- ✅ Working Flask app (`app.py`)
- ✅ `requirements.txt` with all dependencies
- ✅ GitHub repository with your code

## 🌐 Recommended Hosting Platforms

### Option 1: Render (Recommended) ⭐

**Pros:** Free tier, easy setup, auto-deploy from GitHub  
**Cons:** May sleep after inactivity (cold starts)

#### Steps:

1. **Create account** at https://render.com

2. **Create new Web Service:**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select your repo

3. **Configure service:**
   ```
   Name: emotion-detection-app (or your choice)
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   ```

4. **Add to requirements.txt:**
   ```
   gunicorn
   ```

5. **Create `Procfile`** in root folder:
   ```
   web: gunicorn app:app --bind 0.0.0.0:$PORT
   ```

6. **Push changes to GitHub:**
   ```powershell
   git add .
   git commit -m "Add deployment config"
   git push
   ```

7. **Deploy** - Render will auto-deploy your app!

8. **Access your app** at: `https://your-app-name.onrender.com`

---

### Option 2: Railway

**Pros:** Very easy setup, good free tier  
**Cons:** Requires credit card for verification

#### Steps:

1. **Create account** at https://railway.app

2. **New Project:**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

3. **Add environment variables** (if needed):
   ```
   PORT=5000
   ```

4. **Railway auto-detects Python** and deploys automatically

5. **Generate domain:**
   - Go to Settings → Generate Domain

6. **Access your app** at the generated URL

---

### Option 3: PythonAnywhere

**Pros:** Python-specific, very stable  
**Cons:** Manual setup, limited free tier

#### Steps:

1. **Create account** at https://www.pythonanywhere.com

2. **Upload your code:**
   - Use "Files" tab to upload your project
   - Or clone from GitHub using Bash console

3. **Install dependencies:**
   ```bash
   pip install --user -r requirements.txt
   ```

4. **Configure Web App:**
   - Go to "Web" tab → "Add a new web app"
   - Choose "Manual configuration" → Python 3.10
   - Set source code directory
   - Edit WSGI configuration file:
   ```python
   import sys
   path = '/home/yourusername/your-project-folder'
   if path not in sys.path:
       sys.path.append(path)
   
   from app import app as application
   ```

5. **Reload web app** and access at: `yourusername.pythonanywhere.com`

---

### Option 4: Heroku

**Pros:** Popular, well-documented  
**Cons:** Free tier discontinued (requires paid plan or credits)

#### Steps:

1. **Create account** at https://heroku.com

2. **Install Heroku CLI:**
   ```powershell
   # Download from https://devcenter.heroku.com/articles/heroku-cli
   ```

3. **Create `Procfile`:**
   ```
   web: gunicorn app:app
   ```

4. **Create `runtime.txt`:**
   ```
   python-3.10.12
   ```

5. **Add gunicorn to requirements.txt:**
   ```
   gunicorn
   ```

6. **Deploy:**
   ```powershell
   heroku login
   heroku create your-app-name
   git push heroku main
   heroku open
   ```

---

## 📝 Important Files for Deployment

### Procfile (for Render/Heroku)
```
web: gunicorn app:app --bind 0.0.0.0:$PORT
```

### runtime.txt (optional)
```
python-3.10.12
```

### requirements.txt (updated)
Add these if deploying:
```
gunicorn
```

---

## ⚠️ Common Deployment Issues

### Issue: App crashes on startup

**Solution:** Check logs for missing dependencies
```powershell
# On Render: Check "Logs" tab
# On Railway: Check deployment logs
# On Heroku: heroku logs --tail
```

### Issue: Model file too large (>100 MB)

**Solutions:**
1. Use Git LFS (Large File Storage):
   ```powershell
   git lfs install
   git lfs track "*.h5"
   git add .gitattributes
   git commit -m "Track model with LFS"
   ```

2. Or upload model separately and load from cloud storage (Google Drive, Dropbox)

3. Or use a smaller model architecture

### Issue: Cold starts (app sleeps)

**Solution:** 
- Render/Railway free tiers sleep after inactivity
- First request takes ~30 seconds to wake up
- Upgrade to paid tier for always-on service

### Issue: Webcam doesn't work on deployed site

**Solution:**
- Webcam requires HTTPS (not HTTP)
- Most hosting platforms provide HTTPS by default
- If using custom domain, ensure SSL certificate is active

---

## 🔒 Security Considerations

Before deploying:

1. **Never commit sensitive data:**
   - Add `.env` to `.gitignore`
   - Use environment variables for secrets

2. **Create `.gitignore`:**
   ```
   .env
   __pycache__/
   *.pyc
   .venv/
   venv/
   .DS_Store
   *.db
   ```

3. **File upload security:**
   - App already limits uploads to 16 MB
   - Only accepts image files

---

## 📤 Assignment Submission Steps

1. **Train your model locally**
2. **Test app locally** (`python app.py`)
3. **Push to GitHub:**
   ```powershell
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/yourusername/repo-name.git
   git push -u origin main
   ```

4. **Deploy to hosting platform** (follow steps above)

5. **Update `link_to_web_app.txt`** with your deployment URL

6. **Rename root folder:**
   ```
   YOURSURNAME_MATNO_EMOTION_DETECTION_WEB_APP
   ```

7. **Zip the folder** (include everything except `.venv` and large data files)

8. **Email to:** odunayo.osofuye@covenantuniversity.edu.ng

---

## 🎯 Testing Your Deployment

After deployment, test:

1. ✅ Homepage loads correctly
2. ✅ Image upload works
3. ✅ Predictions display correctly
4. ✅ Webcam capture works (requires HTTPS)
5. ✅ All probabilities show in results
6. ✅ Database logging works (check `/history` endpoint)

---

## 📞 Support Resources

- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **PythonAnywhere Help:** https://help.pythonanywhere.com
- **Flask Deployment:** https://flask.palletsprojects.com/en/latest/deploying/

---

**Good luck with your deployment! 🚀**
