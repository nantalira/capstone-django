# Little Lemon Restaurant Capstone Project

## Project Overview

This is a Django REST API project for Little Lemon Restaurant that implements a complete backend system with user authentication, menu management, and table booking functionality.

## Installation Instructions

### Prerequisites

-   Python 3.8 or higher
-   MySQL Server 5.7 or higher
-   Git

### 1. Clone the Repository

```bash
git clone https://github.com/nantalira/capstone-django.git
cd capstone-django
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv littlelemon-capstone

# Activate virtual environment
# On Windows:
.\Scripts\activate

# On macOS/Linux:
source bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: MySQL (Production)

1. Create MySQL database:

```sql
CREATE DATABASE LittleLemon;
```

2. Update database settings in `littlelemon/littlelemon/settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'LittleLemon',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': '127.0.0.1',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'"
        }
    }
}
```

#### Option B: SQLite (Development)

For quick setup, you can use SQLite by updating `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### 5. Run Migrations

```bash
cd littlelemon
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser

```bash
python manage.py createsuperuser
```

### 7. Run the Server

```bash
python manage.py runserver
```

The application will be available at: `http://localhost:8000`

### 8. Test the Installation

-   Homepage: `http://localhost:8000/restaurant/`
-   Admin panel: `http://localhost:8000/admin/`
-   API endpoints: `http://localhost:8000/restaurant/api/`

## Testing

### Run Unit Tests

```bash
python manage.py test restaurant
```

### API Testing with curl

```bash
# Register user
curl -X POST http://localhost:8000/auth/users/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'

# Login to get token
curl -X POST http://localhost:8000/auth/token/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# Create menu item (replace YOUR_TOKEN with actual token)
curl -X POST http://localhost:8000/restaurant/api/menu-items/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token YOUR_TOKEN" \
  -d '{"title": "Pizza Margherita", "price": "15.99", "inventory": 20}'
```

## Project Structure

```
littlelemon-capstone/
├── littlelemon/                 # Main Django project
│   ├── littlelemon/            # Project settings
│   │   ├── settings.py         # Django settings
│   │   ├── urls.py             # Main URL configuration
│   │   └── wsgi.py             # WSGI configuration
│   ├── restaurant/             # Restaurant app
│   │   ├── models.py           # Database models
│   │   ├── views.py            # API views
│   │   ├── serializers.py      # DRF serializers
│   │   ├── urls.py             # App URL configuration
│   │   ├── admin.py            # Admin configuration
│   │   └── tests.py            # Unit tests
│   ├── templates/              # HTML templates
│   ├── static/                 # Static files (CSS, JS, images)
│   └── manage.py               # Django management script
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Features Implemented

-   ✅ Django REST API with full CRUD operations
-   ✅ User authentication and authorization (Djoser)
-   ✅ MySQL database integration
-   ✅ Static HTML content serving
-   ✅ Comprehensive unit tests
-   ✅ API throttling and security
-   ✅ Admin panel integration
-   ✅ User isolation for bookings

## Grading Criteria Overview

-   ✅ Does the web application use Django to serve static HTML content?
-   ✅ Has the learner committed the project to a Git repository?
-   ✅ Does the application connect the backend to a MySQL database?
-   ✅ Are the menu and table booking APIs implemented?
-   ✅ Is the application set up with user registration and authentication? (with djoser)
-   ✅ Does the application contain unit tests?
-   ✅ Can the API be tested with the Insomnia REST client?

## Troubleshooting

### Common Issues

1. **MySQL Connection Error**

    - Ensure MySQL server is running
    - Check database credentials in settings.py
    - Install mysqlclient: `pip install mysqlclient`

2. **Virtual Environment Issues**

    - Make sure virtual environment is activated
    - Reinstall dependencies if needed

3. **Migration Errors**

    - Delete migration files and recreate: `python manage.py makemigrations`
    - Reset database if necessary

4. **Static Files Not Loading**
    - Run: `python manage.py collectstatic`
    - Check STATIC_URL and STATICFILES_DIRS in settings.py

---

# Little Lemon Restaurant API Documentation

## Base URL

```
http://localhost:8000/restaurant/
```

## Authentication

The API uses Token-based authentication. Most endpoints require authentication except for viewing menu items.

### Get Authentication Token

```
POST /auth/token/login/
Content-Type: application/json

{
    "username": "your_username",
    "password": "your_password"
}
```

### Register New User

```
POST /auth/users/
Content-Type: application/json

{
    "username": "new_username",
    "password": "new_password",
    "email": "user@example.com"
}
```

## Menu Endpoints

### Get All Menu Items (Public)

```
GET /restaurant/api/menu-items/
```

### Create Menu Item (Authenticated)

```
POST /restaurant/api/menu-items/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Pizza Margherita",
    "price": "15.99",
    "inventory": 20
}
```

### Get Single Menu Item (Public)

```
GET /restaurant/api/menu-items/{id}/
```

### Update Menu Item (Authenticated)

```
PUT /restaurant/api/menu-items/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "title": "Updated Pizza",
    "price": "17.99",
    "inventory": 15
}
```

### Delete Menu Item (Authenticated)

```
DELETE /restaurant/api/menu-items/{id}/
Authorization: Token your_token_here
```

## Booking Endpoints (All require authentication)

### Get User Bookings

```
GET /restaurant/api/bookings/
Authorization: Token your_token_here
```

### Create Booking

```
POST /restaurant/api/bookings/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "John Doe",
    "no_of_guest": 4,
    "bookingdate": "2024-12-25T19:00:00Z"
}
```

### Get Single Booking

```
GET /restaurant/api/bookings/{id}/
Authorization: Token your_token_here
```

### Update Booking

```
PUT /restaurant/api/bookings/{id}/
Authorization: Token your_token_here
Content-Type: application/json

{
    "name": "John Smith",
    "no_of_guest": 6,
    "bookingdate": "2024-12-25T20:00:00Z"
}
```

### Delete Booking

```
DELETE /restaurant/api/bookings/{id}/
Authorization: Token your_token_here
```

## Testing with Insomnia

1. **Setup Environment Variables:**

    - Base URL: `http://localhost:8000`
    - Token: `your_authentication_token`

2. **Authentication Flow:**

    - First register a user via `/auth/users/`
    - Then login via `/auth/token/login/` to get token
    - Use token in Authorization header for protected endpoints

3. **Sample Test Requests:**
    - Test public menu access
    - Test authenticated menu creation
    - Test booking CRUD operations
    - Test user isolation (users only see their bookings)

## Error Responses

### 401 Unauthorized

```json
{
    "detail": "Authentication credentials were not provided."
}
```

### 403 Forbidden

```json
{
    "detail": "You do not have permission to perform this action."
}
```

### 404 Not Found

```json
{
    "detail": "Not found."
}
```

### 400 Bad Request

```json
{
    "field_name": ["This field is required."]
}
```
