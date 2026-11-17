# Inventory Management API

A backend API for managing organisational equipment and shared resources. Employees can browse and request resources, resource managers can approve or reject bookings, and the system ensures equipment is never double-booked.

## Features

- JWT-based authentication with role-based access control (Admin, Resource Manager, Employee)
- Resource and category management with availability tracking
- Booking requests with overlap prevention
- Booking approval workflow with rejection reasons and audit trail
- Search, filtering, and pagination on all list endpoints
- Auto-generated Swagger UI documentation

## Tech Stack

- **Framework:** Django + Django REST Framework
- **Database:** PostgreSQL
- **Authentication:** SimpleJWT
- **Documentation:** drf-spectacular (Swagger UI)

---

## Prerequisites

- Python 3.10+
- PostgreSQL 14+

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone <your-repo-url>
cd INVENTORY
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
.\venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example env file and fill in your values:

```bash
cp .env.example .env
```

Open `.env` and update:

```
SECRET_KEY=your-secret-key
DEBUG=True
DB_NAME=inventory_db
DB_USER=inventory_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
```

### 5. Set up the PostgreSQL database

Connect to PostgreSQL as the superuser and run:

```sql
CREATE DATABASE inventory_db;
CREATE USER inventory_user WITH PASSWORD 'your_password';
GRANT ALL PRIVILEGES ON DATABASE inventory_db TO inventory_user;
GRANT ALL ON SCHEMA public TO inventory_user;
ALTER DATABASE inventory_db OWNER TO inventory_user;
```

### 6. Run migrations

```bash
python manage.py migrate
```

### 7. Create a superuser

```bash
python manage.py createsuperuser
```

### 8. Start the development server

```bash
python manage.py runserver
```

---

## API Documentation

Once the server is running, visit:

- **Swagger UI:** http://127.0.0.1:8000/api/docs/
- **Django Admin:** http://127.0.0.1:8000/admin/

---

## API Endpoints

### Authentication
| Method | Endpoint | Access |
|--------|----------|--------|
| POST | `/api/auth/register/` | Public |
| POST | `/api/auth/login/` | Public |
| POST | `/api/auth/token/refresh/` | Public |
| GET/PUT | `/api/auth/profile/` | Authenticated |

### Resources
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/resources/` | Authenticated |
| POST | `/api/resources/` | Admin, Resource Manager |
| GET/PUT/DELETE | `/api/resources/{id}/` | Admin, Resource Manager |
| GET | `/api/resources/categories/` | Authenticated |
| POST | `/api/resources/categories/` | Admin, Resource Manager |

### Bookings
| Method | Endpoint | Access |
|--------|----------|--------|
| GET | `/api/bookings/` | Authenticated |
| POST | `/api/bookings/` | Employee |
| GET | `/api/bookings/{id}/` | Owner, Admin, Resource Manager |
| POST | `/api/bookings/{id}/cancel/` | Owner |
| POST | `/api/bookings/{id}/approve/` | Admin, Resource Manager |
| POST | `/api/bookings/{id}/reject/` | Admin, Resource Manager |

---

## Running Tests

```bash
pytest
```

---

## Environment Variables

See `.env.example` for all required environment variables.
