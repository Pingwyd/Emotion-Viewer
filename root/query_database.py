"""
query_database.py

Script to query and view data from the emotion detection database.
"""
import sqlite3
import os
from datetime import datetime

DB_FILE = 'emotion_detection.db'


def check_database_exists():
    """Check if database exists."""
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        print("Run: python init_database.py")
        return False
    return True


def view_all_predictions():
    """View all predictions."""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_name, image_path, predicted_emotion, 
               confidence, timestamp, source
        FROM predictions
        ORDER BY timestamp DESC
    """)
    
    predictions = cursor.fetchall()
    conn.close()
    
    if not predictions:
        print("📭 No predictions found yet")
        return
    
    print(f"\n📊 PREDICTIONS ({len(predictions)} total)\n")
    print("-" * 100)
    print(f"{'ID':<5} {'User':<15} {'Image':<25} {'Emotion':<10} {'Conf.':<8} {'Source':<10} {'Timestamp':<20}")
    print("-" * 100)
    
    for pred in predictions:
        pid, user, img_path, emotion, conf, timestamp, source = pred
        img_name = img_path[:22] + '...' if img_path and len(img_path) > 25 else (img_path or 'N/A')
        time_str = timestamp[:19] if timestamp else 'N/A'
        print(f"{pid:<5} {user:<15} {img_name:<25} {emotion:<10} {conf:.3f}    {source:<10} {time_str:<20}")
    
    print("-" * 100)


def view_users():
    """View all users."""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT name, first_used, total_predictions
        FROM users
        ORDER BY total_predictions DESC
    """)
    
    users = cursor.fetchall()
    conn.close()
    
    if not users:
        print("📭 No users found yet")
        return
    
    print(f"\n👥 USERS ({len(users)} total)\n")
    print("-" * 60)
    print(f"{'Name':<20} {'Total Predictions':<20} {'First Used':<20}")
    print("-" * 60)
    
    for user in users:
        name, first_used, total = user
        time_str = first_used[:19] if first_used else 'N/A'
        print(f"{name:<20} {total:<20} {time_str:<20}")
    
    print("-" * 60)


def view_statistics():
    """View database statistics."""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Total predictions
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total_preds = cursor.fetchone()[0]
    
    # Predictions by emotion
    cursor.execute("""
        SELECT predicted_emotion, COUNT(*) as count
        FROM predictions
        GROUP BY predicted_emotion
        ORDER BY count DESC
    """)
    emotions = cursor.fetchall()
    
    # Total users
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    # Source breakdown
    cursor.execute("""
        SELECT source, COUNT(*) as count
        FROM predictions
        GROUP BY source
    """)
    sources = cursor.fetchall()
    
    # Average confidence
    cursor.execute("SELECT AVG(confidence) FROM predictions")
    avg_conf = cursor.fetchone()[0]
    
    # Database size
    cursor.execute("SELECT SUM(LENGTH(image_data)) FROM predictions")
    total_size = cursor.fetchone()[0] or 0
    
    conn.close()
    
    print("\n📊 DATABASE STATISTICS\n")
    print("=" * 60)
    print(f"Total Predictions:      {total_preds}")
    print(f"Total Users:            {total_users}")
    print(f"Average Confidence:     {avg_conf:.3f}" if avg_conf else "N/A")
    print(f"Total Images Size:      {total_size / (1024*1024):.2f} MB")
    print()
    
    if emotions:
        print("Predictions by Emotion:")
        for emotion, count in emotions:
            percentage = (count / total_preds * 100) if total_preds > 0 else 0
            bar = "█" * int(percentage / 2)
            print(f"  {emotion:<15} {count:>4} ({percentage:>5.1f}%) {bar}")
        print()
    
    if sources:
        print("Predictions by Source:")
        for source, count in sources:
            percentage = (count / total_preds * 100) if total_preds > 0 else 0
            print(f"  {source:<15} {count:>4} ({percentage:>5.1f}%)")
    
    print("=" * 60)


def view_image_info(prediction_id):
    """View information about a specific image."""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_name, image_path, predicted_emotion, confidence,
               all_probabilities, timestamp, source, LENGTH(image_data) as img_size
        FROM predictions
        WHERE id = ?
    """, (prediction_id,))
    
    result = cursor.fetchone()
    conn.close()
    
    if not result:
        print(f"❌ Prediction ID {prediction_id} not found")
        return
    
    pid, user, img_path, emotion, conf, all_probs, timestamp, source, img_size = result
    
    print(f"\n📸 PREDICTION DETAILS (ID: {pid})\n")
    print("=" * 60)
    print(f"User:              {user}")
    print(f"Image Path:        {img_path}")
    print(f"Image Size:        {img_size / 1024:.2f} KB")
    print(f"Predicted Emotion: {emotion}")
    print(f"Confidence:        {conf:.3f} ({conf*100:.1f}%)")
    print(f"Source:            {source}")
    print(f"Timestamp:         {timestamp}")
    print()
    
    if all_probs:
        import json
        probs = json.loads(all_probs)
        print("All Probabilities:")
        for emo, prob in sorted(probs.items(), key=lambda x: x[1], reverse=True):
            bar = "█" * int(prob * 50)
            print(f"  {emo:<15} {prob:.3f} ({prob*100:.1f}%) {bar}")
    
    print("=" * 60)


def export_to_csv():
    """Export predictions to CSV file."""
    if not check_database_exists():
        return
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, user_name, image_path, predicted_emotion, confidence,
               timestamp, source
        FROM predictions
        ORDER BY timestamp DESC
    """)
    
    predictions = cursor.fetchall()
    conn.close()
    
    if not predictions:
        print("📭 No predictions to export")
        return
    
    filename = f"predictions_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    with open(filename, 'w', encoding='utf-8') as f:
        # Header
        f.write("ID,User,Image Path,Emotion,Confidence,Timestamp,Source\n")
        
        # Data
        for pred in predictions:
            f.write(','.join([str(x) for x in pred]) + '\n')
    
    print(f"✅ Exported {len(predictions)} predictions to: {filename}")


def menu():
    """Display interactive menu."""
    while True:
        print("\n" + "=" * 60)
        print("🎭 EMOTION DETECTION - DATABASE VIEWER")
        print("=" * 60)
        print("\n1. View All Predictions")
        print("2. View Users")
        print("3. View Statistics")
        print("4. View Specific Prediction (by ID)")
        print("5. Export to CSV")
        print("6. Exit")
        
        choice = input("\nEnter your choice (1-6): ").strip()
        
        if choice == '1':
            view_all_predictions()
        elif choice == '2':
            view_users()
        elif choice == '3':
            view_statistics()
        elif choice == '4':
            pid = input("Enter prediction ID: ").strip()
            if pid.isdigit():
                view_image_info(int(pid))
            else:
                print("❌ Invalid ID")
        elif choice == '5':
            export_to_csv()
        elif choice == '6':
            print("👋 Goodbye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == '__main__':
    if not check_database_exists():
        print("\nRun this first: python init_database.py")
    else:
        menu()
