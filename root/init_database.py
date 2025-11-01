"""
init_database.py

Script to initialize the emotion detection database.
Run this to create/reset the database structure.
"""
import sqlite3
import os
from datetime import datetime

DB_FILE = 'emotion_detection.db'


def create_database():
    """Create the database and all required tables."""
    
    # Remove old database if exists (optional - comment out to keep data)
    # if os.path.exists(DB_FILE):
    #     os.remove(DB_FILE)
    #     print(f"🗑️  Removed old database: {DB_FILE}")
    
    print(f"📊 Creating database: {DB_FILE}")
    
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    # Table 1: predictions
    print("Creating table: predictions")
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
    
    # Table 2: users
    print("Creating table: users")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL UNIQUE,
            first_used TEXT NOT NULL,
            total_predictions INTEGER DEFAULT 0
        )
    """)
    
    # Table 3: model_info
    print("Creating table: model_info")
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
    
    # Create indexes for better performance
    print("Creating indexes...")
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_predictions_timestamp 
        ON predictions(timestamp DESC)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_predictions_user 
        ON predictions(user_name)
    """)
    
    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_predictions_emotion 
        ON predictions(predicted_emotion)
    """)
    
    conn.commit()
    conn.close()
    
    print("✅ Database created successfully!\n")
    
    # Display table information
    display_database_info()


def display_database_info():
    """Display information about the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("=" * 60)
    print("📊 DATABASE STRUCTURE")
    print("=" * 60)
    
    # Get all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    for table_name in tables:
        table = table_name[0]
        print(f"\n📋 Table: {table}")
        
        # Get column info
        cursor.execute(f"PRAGMA table_info({table})")
        columns = cursor.fetchall()
        
        for col in columns:
            col_id, name, type_, notnull, default, pk = col
            nullable = "NOT NULL" if notnull else "NULL"
            primary = "PRIMARY KEY" if pk else ""
            print(f"   {name:20} {type_:10} {nullable:10} {primary}")
        
        # Get row count
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        count = cursor.fetchone()[0]
        print(f"   Rows: {count}")
    
    conn.close()
    print("\n" + "=" * 60)


def add_sample_data():
    """Add sample data for testing (optional)."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    
    print("\n📝 Adding sample data...")
    
    # Add sample model info
    cursor.execute("""
        INSERT INTO model_info (model_name, created_at, accuracy, epochs, description)
        VALUES (?, ?, ?, ?, ?)
    """, (
        'emotion_model_v1',
        datetime.utcnow().isoformat(),
        0.85,
        10,
        'Initial emotion detection model trained on FER2013 dataset'
    ))
    
    print("✅ Sample data added")
    
    conn.commit()
    conn.close()


def verify_database():
    """Verify database is working correctly."""
    print("\n🔍 Verifying database...")
    
    try:
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()
        
        # Test query
        cursor.execute("SELECT COUNT(*) FROM predictions")
        count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM users")
        users_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM model_info")
        models_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"✅ Database is working!")
        print(f"   Predictions: {count}")
        print(f"   Users: {users_count}")
        print(f"   Models: {models_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database verification failed: {e}")
        return False


if __name__ == '__main__':
    print("=" * 60)
    print("🎭 EMOTION DETECTION - DATABASE INITIALIZATION")
    print("=" * 60)
    print()
    
    # Create database
    create_database()
    
    # Optional: Add sample data
    # Uncomment the line below to add sample model info
    # add_sample_data()
    
    # Verify it works
    verify_database()
    
    print("\n" + "=" * 60)
    print("✅ DATABASE READY!")
    print("=" * 60)
    print("\nNext steps:")
    print("1. Run your Flask app: python app.py")
    print("2. Make predictions through the web interface")
    print("3. Data will be automatically stored in the database")
    print("\nDatabase file: emotion_detection.db")
    print("=" * 60)
