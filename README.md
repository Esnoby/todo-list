# سامانه مدیریت وظایف (Todo App) — فاز اول: اسپرینت اول

> **پروژه درس مهندسی نرم‌افزار**  
> **اعضای تیم:** رضا (Product Owner & Frontend) و آنتی (System Architect & Backend)  
> **متدولوژی توسعه:** چابک (Scrum)  

---

## ۱. معرفی پروژه
این پروژه نسخه اولیه یک سامانه مدیریت وظایف تحت وب است که در قالب **اسپرینت اول** از فاز اول درس مهندسی نرم‌افزار توسعه یافته است. تمرکز این اسپرینت بر توسعه قابلیت‌های پایه (ثبت وظیفه، مشاهده وظایف، اعتبارسنجی دقیق ورودی، ماندگاری پایگاه داده) همراه با رعایت کامل **اصول طراحی شی‌گرا (OOP)** و **اصول پنج‌گانه SOLID** بوده است.

---

## ۲. تکنولوژی‌ها و ابزارهای مورد استفاده (Tech Stack)
* **بک‌اند:** Python 3.11 + FastAPI (سریع، امن و مدرن)
* **پایگاه داده:** SQLite + SQLAlchemy ORM (ماندگاری داده محلی و مستقل)
* **اعتبارسنجی داده:** Pydantic V2 (اعتبارسنجی دوطرفه ورودی‌ها و جلوگیری از مقادیر نامعتبر یا فاصله خالی)
* **فرانت‌اند:** HTML5 معنایی، CSS3 مدرن (استفاده از کلاس `:user-invalid` و `:has()` طبق استانداردهای Modern Web Guidance)، جاوااسکریپت ماژولار و رابط کاربری راست‌چین (RTL) با فونت Vazirmatn
* **تست خودکار:** Pytest و FastAPI TestClient
* **کنترل نسخه:** Git با تاریخچه کامیت‌های استاندارد

---

## ۳. معماری سیستم و رعایت اصول SOLID

پروژه به صورت لایه‌ای (Layered Architecture) طراحی شده است:

```
app/
├── domain/                  # موجودیت‌ها و قراردادهای مستقل بیزینس
│   ├── entities.py          # موجودیت خالص TaskEntity
│   └── interfaces.py        # قراردادهای انتزاعی ITaskRepository و ITaskService
├── infrastructure/          # ارتباط با پایگاه داده و ابزارهای خارجی
│   ├── database.py          # پیکربندی اتصال SQLite
│   ├── models.py            # مدل جدول وظایف در SQLAlchemy
│   └── sqlite_repository.py # پیاده‌سازی ملموس مخزن داده (Repository Pattern)
├── services/
│   └── task_service.py      # لایه منطق بیزینس (Business Logic)
├── schemas/
│   └── task_schema.py       # DTOها و قوانین اعتبارسنجی ورودی Pydantic
├── api/
│   ├── dependencies.py      # تزریق وابستگی‌ها (Dependency Injection)
│   └── task_router.py       # اندپوینت‌های RESTful
├── static/                  # رابط کاربری وب، استایل‌ها و اسکریپت‌ها
│   ├── index.html
│   ├── css/style.css
│   └── js/app.js
└── main.py                  # نقطه ورود اصلی برنامه FastAPI
```

### نحوه رعایت اصول پنج‌گانه SOLID:
1. **Single Responsibility Principle (SRP):** هر ماژول تنها یک مسئولیت دارد (مدل فقط ساختار جدول است، اسکیما فقط اعتبارسنجی، سرویس فقط منطق، و روتر فقط پروتکل HTTP).
2. **Open/Closed Principle (OCP):** سیستم از طریق اینترفیس‌های انتزاعی (`ITaskRepository`) قابل توسعه است؛ برای مثال تغییر دیتابیس به PostgreSQL بدون تغییر کدهای لایه سرویس یا کنترلر امکان‌پذیر است.
3. **Liskov Substitution Principle (LSP):** پیاده‌سازی‌های مختلف از `ITaskRepository` (نظیر `SQLiteTaskRepository` یا `InMemoryTaskRepository` در تست‌ها) کاملاً بدون خطا جایگزین یکدیگر می‌شوند.
4. **Interface Segregation Principle (ISP):** اینترفیس‌ها متمرکز و بدون تحمیل متدهای اضافی تعریف شده‌اند.
5. **Dependency Inversion Principle (DIP):** لایه‌های بالا به لایه‌های پایین وابسته نیستند؛ هر دو به واسطه انتزاع (اینترفیس‌ها) به هم متصل شده و توسط FastAPI Dependency Injection تزریق می‌شوند.

---

## ۴. اقلام تحویلی اسکرام (Scrum Deliverables)
تمام مستندات تحویلی در پوشه `docs/` با جزئیات کامل تدوین شده‌اند:
* [مستند ۱: فهرست محصول (Product Backlog)](file:///C:/ME/computer/mohandsi%20narm/docs/1_product_backlog.md)
* [مستند ۲: فهرست اسپرینت اول و DoD (Sprint Backlog)](file:///C:/ME/computer/mohandsi%20narm/docs/2_sprint_backlog.md)
* [مستند ۳: گزارش ۴ جلسه هماهنگی (Sync Meetings)](file:///C:/ME/computer/mohandsi%20narm/docs/3_sync_meetings.md)
* [مستند ۴: گزارش جلسه بازبینی اسپرینت اول (Sprint Review)](file:///C:/ME/computer/mohandsi%20narm/docs/4_sprint_review.md)
* [مستند ۵: گزارش جلسه بازنگری عملکرد و اقدام اصلاحی (Sprint Retrospective)](file:///C:/ME/computer/mohandsi%20narm/docs/5_sprint_retrospective.md)

---

## ۵. راهنمای نصب و راه‌اندازی پروژه

### پیش‌نیازها:
* پایتون نسخه 3.10 به بالا

### گام اول: فعال‌سازی محیط مجازی پایتون
در محیط ترمینال (PowerShell یا CMD) در ریشه پروژه:
```powershell
# در ویندوز
.\.venv\Scripts\Activate.ps1

# در لینوکس یا مک
source .venv/bin/activate
```

*(در صورت نیاز به نصب مجدد وابستگی‌ها)*:
```bash
pip install -r requirements.txt
```

---

### گام دوم: اجرای برنامه
دستور زیر را در ترمینال اجرا کنید:
```powershell
.venv\Scripts\uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

سپس مرورگر خود را باز کرده و به آدرس زیر بروید:
👉 **[http://127.0.0.1:8000](http://127.0.0.1:8000)**

---

### گام سوم: مستندات تعاملی API (Swagger UI)
FastAPI به صورت خودکار مستندات تعاملی API را تولید می‌کند که در آدرس زیر قابل مشاهده و تست است:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## ۶. اجرای تست‌های خودکار (Automated Tests)
برای اجرای تمام ۸ تست واحد و یکپارچگی پروژه:
```powershell
.venv\Scripts\python -m pytest -v
```

تمام تست‌ها مربوط به اعتبارسنجی ورودی، صحت عملکرد دیتابیس و رفتار شی‌گرا بوده و در کسری از ثانیه اجرا می‌شوند.
