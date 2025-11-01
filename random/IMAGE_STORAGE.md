# 📸 Image Storage Feature - Documentation

## ✅ What Was Added

Your app now **stores the actual images** in the database, not just filenames!

### Database Changes

The `predictions` table now includes:
```sql
CREATE TABLE predictions (
    id INTEGER PRIMARY KEY,
    user_name TEXT,
    image_path TEXT,              -- Filename for reference
    image_data BLOB,              -- ✨ NEW: Actual image stored as binary data
    predicted_label TEXT,
    confidence REAL,
    all_probabilities TEXT,
    created_at TEXT,
    source TEXT
)
```

### How It Works

1. **Upload Image**: User uploads image → Image saved as JPEG bytes → Stored in `image_data` column
2. **Webcam Capture**: User captures from webcam → Converted to JPEG bytes → Stored in `image_data` column
3. **Retrieval**: Images can be retrieved via `/image/<id>` endpoint

---

## 🎯 New Endpoints

### 1. `/history` (Updated)
Returns prediction history **without** image data (for performance):
```json
{
  "predictions": [
    {
      "id": 1,
      "user_name": "John",
      "image_path": "photo.jpg",
      "predicted_label": "Happy",
      "confidence": 0.95,
      "all_probabilities": "{...}",
      "created_at": "2025-11-01T10:30:00",
      "source": "upload"
    }
  ]
}
```

### 2. `/image/<prediction_id>` (NEW)
Retrieves the stored image:
```
GET http://localhost:5000/image/1
Returns: JPEG image
```

---

## 💻 Usage Examples

### Get Image in Browser
```
http://localhost:5000/image/1
http://localhost:5000/image/2
```

### Get Image with Python
```python
import requests

response = requests.get('http://localhost:5000/image/1')
with open('retrieved_image.jpg', 'wb') as f:
    f.write(response.content)
```

### View All Predictions with Images (HTML Example)
```html
<div id="predictions"></div>

<script>
fetch('/history')
  .then(r => r.json())
  .then(data => {
    data.predictions.forEach(pred => {
      const html = `
        <div>
          <img src="/image/${pred.id}" width="200">
          <p>${pred.user_name}: ${pred.predicted_label} (${pred.confidence})</p>
        </div>
      `;
      document.getElementById('predictions').innerHTML += html;
    });
  });
</script>
```

---

## 🔍 Testing Image Storage

### Test 1: Upload an Image
```powershell
# Run the app
python app.py

# Upload an image via the web interface
# Check database has image_data
```

### Test 2: View Stored Images
```powershell
# After uploading images, open in browser:
http://localhost:5000/image/1
http://localhost:5000/image/2
```

### Test 3: Check Database
```powershell
# Open SQLite database
sqlite3 runs.db

# Check if images are stored
SELECT id, user_name, length(image_data) as image_size_bytes FROM predictions;

# Should show sizes like: 15234, 23456, etc. (in bytes)
```

---

## 📊 Database Size Considerations

### Image Size
- Average uploaded JPEG: **50-500 KB** per image
- Webcam captures: **20-200 KB** per capture
- Database grows by ~100 KB per prediction on average

### Storage Limits
- SQLite max size: **~281 TB** (practically unlimited)
- For 1000 predictions: ~100 MB database size
- For 10,000 predictions: ~1 GB database size

### Optimization Tips
1. **JPEG quality**: Images are saved as JPEG (good compression)
2. **Resolution**: Images are preprocessed to 224x224 for prediction (can resize before storing)
3. **Cleanup**: Old predictions can be deleted if database gets large

---

## 🔧 Advanced: Resize Images Before Storage

If you want to save disk space, add this to `app.py`:

```python
# After loading image, resize before storing
MAX_STORAGE_SIZE = (400, 400)  # Max width/height for storage
img.thumbnail(MAX_STORAGE_SIZE, Image.Resampling.LANCZOS)

# Then convert to bytes
img_byte_arr = BytesIO()
img.save(img_byte_arr, format='JPEG', quality=85)
img_bytes = img_byte_arr.getvalue()
```

This would reduce storage size by 50-80%.

---

## 🎓 Assignment Requirements

✅ **Requirement Met**: Database now contains:
- User names ✅
- Images (stored as BLOB) ✅
- Predictions and confidence ✅
- Timestamps ✅
- Source (online/offline) ✅

Your database fully satisfies the assignment requirement:
> "a database, name – your choice – this contains names of people that used your app, offline and online, the image, and the result of the model's evaluation"

---

## 🐛 Troubleshooting

### Issue: Database file is getting very large
**Solution**: 
- Add cleanup endpoint to delete old predictions
- Resize images before storage (see above)
- Store thumbnails instead of full images

### Issue: Images not displaying
**Solution**:
- Check that image_data is not NULL: `SELECT COUNT(*) FROM predictions WHERE image_data IS NULL;`
- Verify endpoint returns JPEG: Test with `curl http://localhost:5000/image/1 --output test.jpg`

### Issue: Migration error (if database already exists)
**Solution**:
```powershell
# Option 1: Delete old database (loses data!)
Remove-Item runs.db

# Option 2: Migrate existing database
sqlite3 runs.db "ALTER TABLE predictions ADD COLUMN image_data BLOB;"
```

---

## 📝 Summary

✅ **Images are now stored in the database**
✅ **Both uploaded and webcam images are saved**
✅ **New endpoint to retrieve images: `/image/<id>`**
✅ **History endpoint optimized (excludes image data)**
✅ **Assignment requirements fully met**

**No action needed from you** - this is automatic! Just train and run the app as before. Every prediction now saves the image to the database. 🎉
