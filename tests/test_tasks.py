# ۰. فراخوانی ابزارهای آزمون Pytest، کلاینت تست و ماژول‌های برنامه {#2ecc71, 13}
# ==========================================
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.infrastructure.database import Base, get_db
from app.domain.entities import TaskEntity
from app.domain.interfaces import ITaskRepository
from app.services.task_service import TaskService
# ==========================================

# ۱. پیکربندی پایگاه‌داده ایزوله در حافظه و فیکسچرهای تست {#3498db, 32}
# ==========================================
# جلوگیری از آلوده شدن دیتابیس اصلی پروژه: استفاده از SQLite موقت در حافظه رم
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)


@pytest.fixture(autouse=True)
def setup_test_db():
    # تضمین استقلال هر تست از تست‌های دیگر: بازسازی و پاک‌سازی کامل جداول در هر آزمون
    Base.metadata.create_all(bind=test_engine)
    yield
    Base.metadata.drop_all(bind=test_engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# جایگزینی وابستگی دیتابیس اصلی با دیتابیس تستی در کلاینت FastAPI
app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)
# ==========================================

# ۲. پیاده‌سازی مخزن تستی در حافظه جهت ارزیابی اصل لیسکوف (LSP) {#f1c40f, 25}
# ==========================================
class InMemoryTaskRepository(ITaskRepository):
    """
    پیاده‌سازی تستی در حافظه جهت نمایش اصل جانشینی لیسکوف (LSP) و تفکیک تست از دیتابیس
    """
    def __init__(self):
        # شبیه‌سازی جدول دیتابیس با لیست پایتون: حذف وابستگی تست واحد به موتور SQL
        self._items = []
        self._counter = 1

    def create(self, task: TaskEntity) -> TaskEntity:
        task.id = self._counter
        self._counter += 1
        self._items.append(task)
        return task

    def get_all(self):
        return list(reversed(self._items))

    def get_by_id(self, task_id: int):
        for item in self._items:
            if item.id == task_id:
                return item
        return None
# ==========================================

# ۳. آزمون‌های واحد لایه دامنه و سرویس بیزینس (Unit Tests) {#9b59b6, 30}
# ==========================================
def test_domain_entity_validation_empty_title():
    """تست سطح دامنه: جلوگیری از ایجاد وظیفه با عنوان خالی"""
    # اطمینان از پرتاب خطا در هسته دامنه هنگام دریافت رشته تهی
    with pytest.raises(ValueError):
        TaskEntity(id=None, title="")


def test_domain_entity_validation_whitespace_title():
    """تست سطح دامنه: جلوگیری از ایجاد وظیفه با عنوان شامل صرفاً فاصله"""
    # اطمینان از رد شدن رشته‌های متشکل از کاراکترهای فاصله
    with pytest.raises(ValueError):
        TaskEntity(id=None, title="     ")


def test_service_with_in_memory_repo_lsp():
    """تست لایه سرویس با استفاده از مخزن تستی در حافظه (تایید اصل لیسکوف)"""
    # اثبات کارکرد صحیح سرویس با هر پیاده‌سازی از اینترفیس ITaskRepository
    repo = InMemoryTaskRepository()
    service = TaskService(repository=repo)

    created = service.create_task("تسک تستی", "توضیحات تست")
    assert created.id == 1
    assert created.title == "تسک تستی"
    assert created.status == "انجام‌نشده"

    tasks = service.list_tasks()
    assert len(tasks) == 1
    assert tasks[0].title == "تسک تستی"
# ==========================================

# ۴. آزمون‌های یکپارچگی اندپوینت‌های وب و اعتبارسنجی (Integration Tests) {#e67e22, 64}
# ==========================================
def test_api_create_task_success():
    """تست ثبت موفق وظیفه جدید از طریق API"""
    # بررسی صحت کد وضعیت ۲۰۱ و ساختار JSON بازگشتی پس از ثبت وظیفه
    response = client.post(
        "/api/tasks",
        json={"title": "یادگیری اسکرام", "description": "مطالعه کتاب راهنمای اسکرام"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["id"] is not None
    assert data["title"] == "یادگیری اسکرام"
    assert data["description"] == "مطالعه کتاب راهنمای اسکرام"
    assert data["status"] == "انجام‌نشده"
    assert "created_at" in data


def test_api_create_task_optional_description():
    """تست ثبت وظیفه بدون توضیحات (اختیاری بودن فیلد توضیحات)"""
    # اطمینان از ثبت موفق وظیفه در صورت عدم ارسال فیلد اختیاری توضیحات
    response = client.post(
        "/api/tasks",
        json={"title": "خرید کتاب مهندسی نرم‌افزار"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "خرید کتاب مهندسی نرم‌افزار"
    assert data["description"] is None
    assert data["status"] == "انجام‌نشده"


def test_api_create_task_validation_empty_title():
    """تست جلوگیری از ثبت وظیفه با عنوان خالی (Input Validation)"""
    # بررسی بازگشت کد خطای ۴۲۲ توسط Pydantic در برابر عنوان خالی
    response = client.post(
        "/api/tasks",
        json={"title": ""}
    )
    assert response.status_code == 422


def test_api_create_task_validation_whitespace_only():
    """تست جلوگیری از ثبت وظیفه با عنوان فقط فاصله"""
    # بررسی بازگشت کد خطای ۴۲۲ در برابر عنوان شامل صرفاً فاصله سفید
    response = client.post(
        "/api/tasks",
        json={"title": "    "}
    )
    assert response.status_code == 422


def test_api_list_tasks():
    """تست مشاهده لیست وظایف ثبت‌شده"""
    # بررسی ترتیب نزولی نمایش وظایف (قرارگیری جدیدترین وظیفه در ابتدای لیست)
    client.post("/api/tasks", json={"title": "وظیفه ۱"})
    client.post("/api/tasks", json={"title": "وظیفه ۲"})

    response = client.get("/api/tasks")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) == 2
    assert tasks[0]["title"] == "وظیفه ۲"
    assert tasks[1]["title"] == "وظیفه ۱"
# ==========================================
