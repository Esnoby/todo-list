import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# مسیر پیش‌فرض پایگاه‌داده SQLite محلی
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    """
    تولیدکننده نشست پایگاه‌داده (Database Session Generator)
    جهت تزریق وابستگی امن و بستن خودکار نشست پس از اتمام درخواست
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
