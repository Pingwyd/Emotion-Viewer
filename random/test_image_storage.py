"""
test_image_storage.py

Quick test to verify images are being stored in the database.
Run this AFTER you've made at least one prediction through the web app.
"""
import sqlite3
import sys

DB_FILE = 'runs.db'

def test_image_storage():
    """Test that images are being stored in the database."""
    print("🔍 Testing Image Storage in Database...\n")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        
        # Check if table exists and has image_data column
        c.execute("PRAGMA table_info(predictions)")
        columns = c.fetchall()
        column_names = [col[1] for col in columns]
        
        print("✅ Database columns:")
        for col in column_names:
            print(f"   - {col}")
        
        if 'image_data' not in column_names:
            print("\n❌ ERROR: image_data column not found!")
            print("   Solution: Delete runs.db and restart the app")
            conn.close()
            return False
        
        print("\n✅ image_data column exists\n")
        
        # Count total predictions
        c.execute("SELECT COUNT(*) FROM predictions")
        total = c.fetchone()[0]
        print(f"📊 Total predictions: {total}")
        
        if total == 0:
            print("\n⚠️  No predictions found yet.")
            print("   Run the web app and make a prediction first!")
            conn.close()
            return True
        
        # Count predictions with images
        c.execute("SELECT COUNT(*) FROM predictions WHERE image_data IS NOT NULL")
        with_images = c.fetchone()[0]
        print(f"📸 Predictions with images: {with_images}")
        
        # Get image sizes
        c.execute("SELECT id, user_name, predicted_label, length(image_data) as img_size FROM predictions WHERE image_data IS NOT NULL LIMIT 5")
        rows = c.fetchall()
        
        print("\n📋 Sample predictions with image sizes:")
        for row in rows:
            img_size_kb = row[3] / 1024 if row[3] else 0
            print(f"   ID {row[0]}: {row[1]} - {row[2]} - Image size: {img_size_kb:.1f} KB")
        
        # Calculate total database size
        c.execute("SELECT SUM(length(image_data)) FROM predictions WHERE image_data IS NOT NULL")
        total_size = c.fetchone()[0] or 0
        total_size_mb = total_size / (1024 * 1024)
        print(f"\n💾 Total images size: {total_size_mb:.2f} MB")
        
        conn.close()
        
        if with_images == total:
            print("\n✅ SUCCESS! All predictions have images stored.")
        elif with_images > 0:
            print(f"\n⚠️  WARNING: Only {with_images}/{total} predictions have images.")
            print("   This is normal if you had predictions before the update.")
        else:
            print("\n❌ ERROR: No images are being stored!")
            print("   Check that app.py has the updated code.")
        
        return True
        
    except sqlite3.Error as e:
        print(f"\n❌ Database error: {e}")
        return False
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


def view_image_by_id(image_id):
    """Extract and save an image from the database."""
    try:
        conn = sqlite3.connect(DB_FILE)
        c = conn.cursor()
        c.execute("SELECT image_data, predicted_label FROM predictions WHERE id = ?", (image_id,))
        row = c.fetchone()
        conn.close()
        
        if row and row[0]:
            filename = f"extracted_image_{image_id}_{row[1]}.jpg"
            with open(filename, 'wb') as f:
                f.write(row[0])
            print(f"\n✅ Image saved as: {filename}")
            return True
        else:
            print(f"\n❌ No image found for ID {image_id}")
            return False
            
    except Exception as e:
        print(f"\n❌ Error: {e}")
        return False


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'extract':
        # Extract specific image: python test_image_storage.py extract 1
        if len(sys.argv) > 2:
            image_id = int(sys.argv[2])
            view_image_by_id(image_id)
        else:
            print("Usage: python test_image_storage.py extract <image_id>")
    else:
        # Run test
        test_image_storage()
        
        print("\n" + "="*60)
        print("TIP: To extract an image from database, run:")
        print("     python test_image_storage.py extract 1")
        print("="*60)
