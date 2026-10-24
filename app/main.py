import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.infrastructure.database import Base, engine
from app.api.task_router import router as task_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # مقداردهی اولیه جداول پایگاه‌داده SQLite در زمان شروع به کار برنامه
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="سامانه مدیریت وظایف (Todo App)",
    description="پروژه درس مهندسی نرم‌افزار - فاز اول: اسپرینت اول (توسعه قابلیت‌های پایه بر اساس اسکرام)",
    version="1.0.0",
    lifespan=lifespan
)

# اتصال روتر تسک‌ها
app.include_router(task_router)

# مسیر فایل‌های ایستا (Static Files)
static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir, exist_ok=True)

app.mount("/static", StaticFiles(directory=static_dir), name="static")


@app.get("/", include_in_schema=False)
async def serve_frontend():
    """ارائه صفحه وب اصلی برنامه"""
    index_path = os.path.join(static_dir, "index.html")
    return FileResponse(index_path)
