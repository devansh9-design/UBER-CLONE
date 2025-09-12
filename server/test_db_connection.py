"""Test database connection"""
import psycopg2
from sqlalchemy import create_engine, text
from app.core.config import settings

def test_raw_connection():
    """Test raw psycopg2 connection"""
    try:
        conn = psycopg2.connect(
            host=settings.postgres_host,
            database=settings.postgres_db,
            user=settings.postgres_user,
            password=settings.postgres_password,
            port=settings.postgres_port
        )
        cursor = conn.cursor()
        cursor.execute("SELECT version();")
        version = cursor.fetchone()
        print(f"✅ Raw connection successful!")
        print(f"PostgreSQL version: {version[0]}")
        cursor.close()
        conn.close()
        return True
    except Exception as e:
        print(f"❌ Raw connection failed: {e}")
        return False

def test_sqlalchemy_connection():
    """Test SQLAlchemy connection"""
    try:
        engine = create_engine(settings.database_url)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT version();"))
            version = result.fetchone()[0]
            print(f"✅ SQLAlchemy connection successful!")
            print(f"PostgreSQL version: {version}")
        return True
    except Exception as e:
        print(f"❌ SQLAlchemy connection failed: {e}")
        return False

if __name__ == "__main__":
    print("🐘 Testing PostgreSQL Connection...")
    print("=" * 40)
    
    print("\n1. Testing raw psycopg2 connection:")
    raw_success = test_raw_connection()
    
    print("\n2. Testing SQLAlchemy connection:")
    sqlalchemy_success = test_sqlalchemy_connection()
    
    if raw_success and sqlalchemy_success:
        print("\n🎉 All database connections successful!")
        print("You're ready to run the application!")
    else:
        print("\n❌ Some connections failed. Check your configuration.")