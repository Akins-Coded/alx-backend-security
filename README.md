# ALX Backend Security Project 🔒

This project implements **security and analytics features** in a Django
application.\
The focus is on **IP tracking, rate limiting, anomaly detection, and
secure token handling**.

------------------------------------------------------------------------

## 📂 Project Structure & Features

### `ip_tracking/middleware.py`

-   **IPTrackingMiddleware**
    -   Logs each request by **IP address**.

    -   Tracks **request counts** and **accessed paths** in Redis.

    -   Data expires after **1 hour** (aligned with anomaly detection).

    -   Example stored in Redis:

        ``` json
        {
            "count": 57,
            "paths": ["/login", "/admin"]
        }
        ```

------------------------------------------------------------------------

### `ip_tracking/views.py`

-   **`login_view`**
    -   A dummy login view used for testing.
    -   Protected by **rate limiting**:
        -   Anonymous users → **5 requests/minute**
        -   Authenticated users → **10 requests/minute**
    -   Uses `@ratelimit` decorators with Redis cache.

------------------------------------------------------------------------

### `ip_tracking/utils.py`

-   **`user_or_ip(request)`**
    -   Helper for rate limiting.\
    -   Returns:
        -   `request.user.pk` if authenticated.\
        -   IP address if anonymous.

------------------------------------------------------------------------

### `ip_tracking/tasks.py`

-   **`detect_anomalies()` (Celery task)**
    -   Runs **hourly**.
    -   Flags IPs that:
        -   Exceed **100 requests/hour**.
        -   Access **sensitive paths** like `/admin` or `/login`.
    -   Saves suspicious IPs into the database.

------------------------------------------------------------------------

### `ip_tracking/models.py`

-   **SuspiciousIP**
    -   Fields:
        -   `ip_address`: `CharField` (tracks flagged IPs).
        -   `reason`: `TextField` (explains why flagged).
        -   `created_at`: `DateTimeField` (timestamp).

------------------------------------------------------------------------

## ⚙️ Dependencies

### Django & Core

``` bash
pip install django==5.2.3
```

### Redis Integration

``` bash
pip install django-redis redis
```

### Rate Limiting

``` bash
pip install django-ratelimit
```

### Celery (for background tasks)

``` bash
pip install celery
```

------------------------------------------------------------------------

## 🚀 Setup & Usage

### 1. Clone and Install

``` bash
git clone <repo-url>
cd alx-backend-security
pip install -r requirements.txt
```

### 2. Start Redis (locally)

On **Linux/macOS**:

``` bash
redis-server
```

On **Windows (WSL2/Redis for Windows)**:

``` bash
redis-server.exe
```

### 3. Configure Django Cache (settings.py)

``` python
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        },
    }
}

RATELIMIT_USE_CACHE = "default"
```

### 4. Run Django

``` bash
python manage.py migrate
python manage.py runserver
```

### 5. Run Celery (Worker + Beat)

``` bash
celery -A alx_backend_security worker -l info
celery -A alx_backend_security beat -l info
```

------------------------------------------------------------------------

## ✅ Features Implemented

-   [x] **Access Token Security** → Stored in `.env` using
    `django-environ`.\
-   [x] **IP Tracking Middleware** → Stores requests in Redis with
    counts & paths.\
-   [x] **Rate Limiting** → Per-user/IP with `django-ratelimit`.\
-   [x] **Anomaly Detection** → Celery task detects suspicious IPs.\
-   [x] **Suspicious IP Logging** → Saved into database for later
    review.

------------------------------------------------------------------------

## 🧑‍💻 Author

Developed by **Muheez Akindipe** as part of the **ALX Backend Security
Project**.
