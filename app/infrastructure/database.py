# ۰. فراخوانی کتابخانه‌های سیستم‌عامل و SQLAlchemy {#2ecc71, 5}
# ==========================================
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
# ==========================================

# ۱. پیکربندی موتور پایگاه‌داده و کارخانه نشست‌ها {#3498db, 15}
# ==========================================
# پشتیبانی از تغییر محیط اجرایی: دریافت آدرس دیتابیس از متغیر محیطی یا استفاده از SQLite محلی
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./todo.db")

# جلوگیری از خطای چندریسمانی در SQLite: غیرفعال‌سازی بررسی ریسمان یکسان در درخواست‌های وب
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# مدیریت دستی تراکنش‌ها: غیرفعال‌سازی کامیت خودکار برای کنترل دقیق‌تر ذخیره‌سازی
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
# ==========================================

# ۲. تولیدکننده نشست پایگاه‌داده برای تزریق وابستگی {#1abc9c, 14}
# ==========================================
def get_db():
    """
    تولیدکننده نشست پایگاه‌داده (Database Session Generator)
    جهت تزریق وابستگی امن و بستن خودکار نشست پس از اتمام درخواست
    """
    db = SessionLocal()
    try:
        # تحویل نشست فعال به اندپوینت درخواست‌دهنده: حفظ اتصال در طول پردازش HTTP
        yield db
    finally:
        # پیشگیری از نشت منابع و قفل شدن دیتابیس: بستن قطعی نشست پس از پایان درخواست
        db.close()
# ==========================================
