"""
export_images.py

Extract and save images from the emotion_detection database to disk.
"""
import sqlite3
import os
from datetime import datetime

DB_FILE = 'emotion_detection.db'
OUTPUT_DIR = 'exported_images'


def export_all_images():
    """Export all images from database to files."""
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        return
    
    # Create output directory
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"📁 Created directory: {OUTPUT_DIR}")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Get all predictions with images
        cursor.execute("""
            SELECT id, user_name, predicted_emotion, confidence, 
                   timestamp, source, image_data
            FROM predictions
            ORDER BY timestamp DESC
        """)
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print("📭 No predictions found in database")
            return
        
        print(f"\n✅ Found {len(rows)} predictions with images\n")
        print("Exporting images...\n")
        
        for row in rows:
            pred_id, user_name, emotion, confidence, timestamp, source, image_data = row
            
            if not image_data:
                print(f"⚠️  ID {pred_id}: No image data")
                continue
            
            # Create filename with details
            # Format: ID_UserName_Emotion_Timestamp.jpg
            safe_name = user_name.replace(' ', '_')
            time_str = timestamp[:19].replace(':', '-') if timestamp else 'unknown'
            filename = f"{pred_id}_{safe_name}_{emotion}_{confidence:.2f}_{source}_{time_str}.jpg"
            
            filepath = os.path.join(OUTPUT_DIR, filename)
            
            # Write image to file
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            file_size_kb = len(image_data) / 1024
            print(f"✅ ID {pred_id:3d} | {user_name:15s} | {emotion:10s} | {confidence:.2f} | {file_size_kb:6.1f} KB | {filename}")
        
        print(f"\n🎉 Successfully exported {len(rows)} images to: {OUTPUT_DIR}/")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def export_by_emotion(emotion):
    """Export images of a specific emotion only."""
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        return
    
    # Create output directory
    emotion_dir = os.path.join(OUTPUT_DIR, emotion)
    if not os.path.exists(emotion_dir):
        os.makedirs(emotion_dir)
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_name, confidence, timestamp, image_data
            FROM predictions
            WHERE predicted_emotion = ?
            ORDER BY timestamp DESC
        """, (emotion,))
        
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            print(f"📭 No '{emotion}' predictions found")
            return
        
        print(f"✅ Found {len(rows)} '{emotion}' predictions\n")
        
        for row in rows:
            pred_id, user_name, confidence, timestamp, image_data = row
            
            if not image_data:
                continue
            
            filename = f"{pred_id}_{user_name}_{confidence:.2f}.jpg"
            filepath = os.path.join(emotion_dir, filename)
            
            with open(filepath, 'wb') as f:
                f.write(image_data)
            
            print(f"✅ Saved: {filename}")
        
        print(f"\n🎉 Exported to: {emotion_dir}/")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def export_single_image(prediction_id):
    """Export a single image by prediction ID."""
    
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        return
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, user_name, predicted_emotion, confidence, image_data
            FROM predictions
            WHERE id = ?
        """, (prediction_id,))
        
        row = cursor.fetchone()
        conn.close()
        
        if not row:
            print(f"❌ Prediction ID {prediction_id} not found")
            return
        
        pred_id, user_name, emotion, confidence, image_data = row
        
        if not image_data:
            print(f"❌ No image data for ID {prediction_id}")
            return
        
        filename = f"prediction_{pred_id}_{emotion}_{confidence:.2f}.jpg"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        if not os.path.exists(OUTPUT_DIR):
            os.makedirs(OUTPUT_DIR)
        
        with open(filepath, 'wb') as f:
            f.write(image_data)
        
        file_size_kb = len(image_data) / 1024
        print(f"✅ Exported: {filename}")
        print(f"   User: {user_name}")
        print(f"   Emotion: {emotion}")
        print(f"   Confidence: {confidence:.2%}")
        print(f"   Size: {file_size_kb:.1f} KB")
        print(f"   Location: {filepath}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main menu."""
    print("=" * 60)
    print("🖼️  IMAGE EXPORTER - Extract Images from Database")
    print("=" * 60)
    print()
    print("1. Export ALL images")
    print("2. Export images by emotion")
    print("3. Export single image by ID")
    print("4. Exit")
    print()
    
    choice = input("Enter your choice (1-4): ").strip()
    
    if choice == '1':
        export_all_images()
    
    elif choice == '2':
        print("\nAvailable emotions: angry, fear, happy, sad, surprise")
        emotion = input("Enter emotion name: ").strip().lower()
        export_by_emotion(emotion)
    
    elif choice == '3':
        pred_id = input("Enter prediction ID: ").strip()
        if pred_id.isdigit():
            export_single_image(int(pred_id))
        else:
            print("❌ Invalid ID")
    
    elif choice == '4':
        print("👋 Goodbye!")
    
    else:
        print("❌ Invalid choice")


if __name__ == '__main__':
    main()
