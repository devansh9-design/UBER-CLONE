"""Initialize database with sample data"""
import sys
import os
from sqlalchemy.orm import Session
from sqlalchemy import text

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database.connection import SessionLocal, engine, Base
from app.database.models import User, Ride, PingLog
from app.models.user import UserCreate
from app.services.user_services import UserService

def test_connection():
    """Test database connection"""
    try:
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            print("✅ Database connection successful!")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def create_tables():
    """Create all database tables"""
    try:
        print("Creating database tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully!")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def init_db():
    """Initialize database with sample data"""
    db: Session = SessionLocal()
    
    try:
        # Check if users already exist
        existing_users = db.query(User).first()
        if existing_users:
            print("✅ Database already has data!")
            return True
        
        # Create sample users
        users_data = [
            UserCreate(
                email="john.rider@miniuber.com",
                username="john_rider",
                full_name="John Doe",
                phone_number="+1234567890",
                is_driver=False
            ),
            UserCreate(
                email="jane.driver@miniuber.com",
                username="jane_driver",
                full_name="Jane Smith",
                phone_number="+1234567891",
                is_driver=True
            ),
            UserCreate(
                email="bob.both@miniuber.com",
                username="bob_both",
                full_name="Bob Johnson",
                phone_number="+1234567892",
                is_driver=True
            ),
            UserCreate(
                email="alice.rider@miniuber.com",
                username="alice_rider",
                full_name="Alice Wilson",
                phone_number="+1234567893",
                is_driver=False
            )
        ]
        
        print("Creating sample users...")
        created_users = []
        for user_data in users_data:
            user = UserService.create_user(db, user_data)
            created_users.append(user)
            print(f"  ✅ Created: {user.full_name} ({user.email})")
        
        print(f"\n🎉 Database initialized successfully!")
        print(f"Created {len(created_users)} sample users")
        print("\nSample users:")
        for user in created_users:
            role = "Driver" if user.is_driver else "Rider"
            print(f"  - {user.full_name} ({role}) - ID: {user.id}")
            
        return True
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def verify_setup():
    """Verify database setup"""
    db: Session = SessionLocal()
    try:
        # Count users
        user_count = db.query(User).count()
        rider_count = db.query(User).filter(User.is_driver == False).count()
        driver_count = db.query(User).filter(User.is_driver == True).count()
        
        print(f"\n📊 Database Status:")
        print(f"  Total Users: {user_count}")
        print(f"  Riders: {rider_count}")
        print(f"  Drivers: {driver_count}")
        
        # List all users
        users = db.query(User).all()
        print(f"\n👥 All Users:")
        for user in users:
            role = "🚗 Driver" if user.is_driver else "🙋 Rider"
            print(f"  {role} - {user.full_name} ({user.email}) - ID: {user.id}")
            
    except Exception as e:
        print(f"❌ Error verifying setup: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    print("🐘 Initializing Mini-Uber Database")
    print("=" * 50)
    
    # Step 1: Test connection
    if not test_connection():
        print("💡 Check your .env file and database credentials")
        sys.exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        print("💡 Check database permissions")
        sys.exit(1)
    
    # Step 3: Initialize data
    if not init_db():
        print("💡 Check database setup")
        sys.exit(1)
    
    # Step 4: Verify setup
    verify_setup()
    
    print("\n🚀 Ready to start the server!")
    print("Run: python run.py")