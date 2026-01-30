"""
Database Configuration - PostgreSQL + Redis
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager
import os
from typing import Generator
import redis

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:postgres@localhost:5432/wildcodeai"
)

# Redis URL
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create SQLAlchemy engine
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=False  # Set to True for SQL debugging
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db() -> Generator[Session, None, None]:
    """
    Dependency injection for database sessions

    Usage:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            items = db.query(Item).all()
            return items
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_context():
    """
    Context manager for database sessions

    Usage:
        with get_db_context() as db:
            items = db.query(Item).all()
            db.commit()
    """
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    finally:
        db.close()


# Redis connection
redis_client = redis.from_url(
    REDIS_URL,
    decode_responses=True,
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True
)


def get_redis() -> redis.Redis:
    """
    Get Redis client instance

    Usage:
        r = get_redis()
        r.set("key", "value")
        value = r.get("key")
    """
    return redis_client


def init_database():
    """
    Initialize database tables

    Call this on application startup to create all tables
    """
    from models.agent import Agent
    from models.task import Task
    from models.benchmark import AgentBenchmark

    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully")


def test_database_connection():
    """
    Test database connection
    """
    try:
        with engine.connect() as conn:
            conn.execute("SELECT 1")
        print("✅ Database connection successful")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False


def test_redis_connection():
    """
    Test Redis connection
    """
    try:
        r = get_redis()
        r.ping()
        print("✅ Redis connection successful")
        return True
    except Exception as e:
        print(f"❌ Redis connection failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 80)
    print("🗄️  Database Connection Test")
    print("=" * 80)
    print()

    print("Testing PostgreSQL...")
    test_database_connection()

    print()
    print("Testing Redis...")
    test_redis_connection()

    print()
    print("Note: Database and Redis services need to be running")
    print("Use Docker Compose to start services:")
    print("  docker-compose up -d")
