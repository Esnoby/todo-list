# ۰. فراخوانی کتابخانه‌های شبکه، مرورگر و وب‌سرور Uvicorn {#2ecc71, 7}
# ==========================================
import socket
import threading
import time
import webbrowser
import uvicorn
# ==========================================

# ۱. تابع هوشمند یافتن پورت آزاد در سیستم‌عامل {#3498db, 20}
# ==========================================
def find_available_port(preferred_ports: list[int]) -> int:
    """
    بررسی پورت‌های پیشنهادی و انتخاب اولین پورت آزاد و مجاز در سیستم‌عامل
    جهت جلوگیری از خطای PermissionError یا اشغال بودن پورت در ویندوز/لینوکس
    """
    for port in preferred_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            try:
                # آزمایش امکان اتصال سوکت به پورت مورد نظر روی لوکال‌هاست
                sock.bind(("127.0.0.1", port))
                return port
            except OSError:
                continue

    # انتخاب پورت آزاد تصادفی توسط سیستم‌عامل در صورت بسته بودن تمام پورت‌های پیشنهادی
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]
# ==========================================

# ۲. راه‌اندازی سرور برنامه و باز کردن خودکار مرورگر {#1abc9c, 20}
# ==========================================
def main():
    port = find_available_port([8000, 8100, 8080, 5000, 3000])
    url = f"http://127.0.0.1:{port}"

    print("=" * 55)
    print(f"🚀 Todo App Server is starting on: {url}")
    print(f"📘 Swagger API Documentation:      {url}/docs")
    print("=" * 55)

    # باز کردن خودکار آدرس برنامه در مرورگر پیش‌فرض یک ثانیه پس از استارت سرور
    threading.Timer(1.2, lambda: webbrowser.open(url)).start()

    # اجرای سرور FastAPI بر روی پورت آزاد شناسایی‌شده
    uvicorn.run("app.main:app", host="127.0.0.1", port=port, reload=False)


if __name__ == "__main__":
    main()
# ==========================================
