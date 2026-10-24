/**
 * مدیریت رویدادها و ارتباط با API سامانه مدیریت وظایف
 * پیاده‌سازی منطبق با راهنماهای Modern Web Guidance و استانداردهای دسترس‌پذیری
 */

document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('task-form');
    const titleInput = document.getElementById('task-title');
    const descInput = document.getElementById('task-desc');
    const submitBtn = document.getElementById('submit-btn');
    const tasksContainer = document.getElementById('tasks-container');
    const taskCountBadge = document.getElementById('task-count-badge');
    const emptyState = document.getElementById('empty-state');
    const loadingState = document.getElementById('loading-state');
    const alertBanner = document.getElementById('alert-banner');

    // همگام‌سازی وضعیت ARIA با استایل :user-invalid طبق Modern Web Guidance
    const syncAriaInvalid = (el) => {
        if (!el) return;
        const isInvalid = !el.checkValidity() || !el.value.trim();
        if (isInvalid) {
            el.setAttribute('aria-invalid', 'true');
        } else {
            el.removeAttribute('aria-invalid');
        }
    };

    titleInput.addEventListener('blur', () => syncAriaInvalid(titleInput));
    titleInput.addEventListener('input', () => {
        if (titleInput.hasAttribute('aria-invalid') && titleInput.value.trim().length > 0) {
            titleInput.removeAttribute('aria-invalid');
        }
    });

    // نمایش پیام هشدار / اعلان موقت
    let alertTimeout = null;
    const showAlert = (message, type = 'success') => {
        if (alertTimeout) clearTimeout(alertTimeout);
        alertBanner.className = `alert-banner ${type}`;
        alertBanner.textContent = message;
        alertBanner.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        alertTimeout = setTimeout(() => {
            alertBanner.className = 'alert-banner';
            alertBanner.textContent = '';
        }, 5000);
    };

    // فرمت‌بندی تاریخ و زمان به تقویم شمسی خوانا
    const formatDateTime = (isoDateStr) => {
        try {
            const date = new Date(isoDateStr);
            return new Intl.DateTimeFormat('fa-IR', {
                year: 'numeric',
                month: 'long',
                day: 'numeric',
                hour: '2-digit',
                minute: '2-digit'
            }).format(date);
        } catch {
            return isoDateStr;
        }
    };

    // بارگذاری فهرست وظایف از بک‌اند
    const fetchTasks = async () => {
        loadingState.classList.remove('hidden');
        emptyState.classList.add('hidden');
        tasksContainer.innerHTML = '';

        try {
            const response = await fetch('/api/tasks');
            if (!response.ok) {
                throw new Error('خطا در دریافت لیست وظایف از سرور');
            }
            const tasks = await response.json();
            renderTasks(tasks);
        } catch (err) {
            showAlert(err.message || 'خطایی در برقراری ارتباط با سرور رخ داد.', 'error');
        } finally {
            loadingState.classList.add('hidden');
        }
    };

    // رندر کارت‌های وظایف در صفحه
    const renderTasks = (tasks) => {
        taskCountBadge.textContent = `${tasks.length} وظیفه`;

        if (!tasks || tasks.length === 0) {
            emptyState.classList.remove('hidden');
            tasksContainer.innerHTML = '';
            return;
        }

        emptyState.classList.add('hidden');
        tasksContainer.innerHTML = '';

        tasks.forEach(task => {
            const taskCard = document.createElement('article');
            taskCard.className = 'task-item';
            taskCard.setAttribute('tabindex', '0');

            // هدر کارت وظیفه
            const header = document.createElement('div');
            header.className = 'task-item-header';

            const titleWrap = document.createElement('div');
            titleWrap.className = 'task-item-title-wrap';

            const idSpan = document.createElement('span');
            idSpan.className = 'task-id';
            idSpan.textContent = `#${task.id}`;

            const titleHeading = document.createElement('h3');
            titleHeading.className = 'task-item-title';
            titleHeading.textContent = task.title;

            titleWrap.appendChild(idSpan);
            titleWrap.appendChild(titleHeading);

            const statusBadge = document.createElement('span');
            statusBadge.className = 'task-status-badge';
            statusBadge.textContent = task.status;

            header.appendChild(titleWrap);
            header.appendChild(statusBadge);
            taskCard.appendChild(header);

            // توضیحات در صورت وجود
            if (task.description && task.description.trim()) {
                const descP = document.createElement('p');
                descP.className = 'task-item-desc';
                descP.textContent = task.description;
                taskCard.appendChild(descP);
            }

            // فوتر کارت با زمان ثبت
            const footer = document.createElement('div');
            footer.className = 'task-item-footer';

            const dateSpan = document.createElement('span');
            dateSpan.className = 'task-date';
            dateSpan.innerHTML = `<span aria-hidden="true">🕒</span> <span>زمان ثبت: ${formatDateTime(task.created_at)}</span>`;

            footer.appendChild(dateSpan);
            taskCard.appendChild(footer);

            tasksContainer.appendChild(taskCard);
        });
    };

    // مدیریت ارسال فرم ثبت وظیفه جدید
    taskForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        const rawTitle = titleInput.value;
        const trimmedTitle = rawTitle ? rawTitle.trim() : '';

        // اعتبارسنجی سمت کاربر طبق الزامات اسپرینت اول
        if (!trimmedTitle) {
            titleInput.focus();
            syncAriaInvalid(titleInput);
            showAlert('لطفاً عنوان وظیفه را وارد نمایید. عنوان نمی‌تواند خالی یا شامل صرفاً کاراکترهای فاصله باشد.', 'error');
            return;
        }

        const payload = {
            title: trimmedTitle,
            description: descInput.value ? descInput.value.trim() : null
        };

        submitBtn.disabled = true;
        submitBtn.classList.add('loading');

        try {
            const response = await fetch('/api/tasks', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Accept': 'application/json'
                },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                const errData = await response.json();
                const errMsg = errData.detail || 'ثبت وظیفه با خطا مواجه شد.';
                throw new Error(typeof errMsg === 'string' ? errMsg : JSON.stringify(errMsg));
            }

            const createdTask = await response.json();
            showAlert(`وظیفه «${createdTask.title}» با موفقیت ذخیره شد.`, 'success');

            // پاک‌سازی فرم
            taskForm.reset();
            titleInput.removeAttribute('aria-invalid');

            // به‌روزرسانی مجدد لیست
            await fetchTasks();

        } catch (err) {
            showAlert(err.message || 'خطا در ثبت وظیفه در سرور', 'error');
        } finally {
            submitBtn.disabled = false;
            submitBtn.classList.remove('loading');
        }
    });

    // بارگذاری اولیه هنگام اجرای صفحه
    fetchTasks();
});
