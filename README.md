# SSO Project 🚀

This repository contains a **Django-based web application** designed for **user authentication**, **case management**, and **workshop management**. It features **OTP-based authentication**, **user registration**, and **modular design** for managing cases and workshops. The project is built to be **scalable**, **secure**, and **easy to integrate** into larger systems.

---

## Table of Contents

1. [Features](#features)
2. [Repository Structure](#repository-structure)
3. [Installation](#installation)
4. [Usage](#usage)
5. [API Endpoints](#api-endpoints)
6. [Models Overview](#models-overview)
7. [Admin Interface](#admin-interface)
8. [Contributing](#contributing)

---

## Features ✨

- **OTP-Based Authentication**: Secure login using One-Time Passwords (OTP) sent to the user's phone number.
- **User Registration**: Register users with unique phone numbers and national IDs.
- **Case Management**: Create and manage cases for both **individual** and **legal** users.
- **Workshop Management**: Create and manage workshops associated with specific cases.
- **Admin Interface**: Django admin panel for managing users, cases, and workshops.
- **RESTful API**: Built with Django REST Framework for seamless integration with front-end applications.

---

## Repository Structure 📂

```
SSO_Project/
├── ssoweb/                    # Main Django app
│   ├── migrations/            # Database migrations
│   ├── admin.py               # Admin interface configurations
│   ├── models.py              # Database models (CustomUser, Case, Workshop, OTP)
│   ├── serializers.py         # Serializers for REST API
│   ├── views.py               # API views (OTP, User Registration, Case, Workshop)
│   ├── urls.py                # URL routing for the app
│   └── tests/                 # Unit tests
├── SSO/                       # Django project settings
│   ├── settings.py            # Django settings
│   ├── urls.py                # Main URL routing
│   └── wsgi.py                # WSGI configuration
├── manage.py                  # Django management script
├── README.md                  # Project documentation
└── requirements.txt           # Python dependencies
```

---

## Installation 🛠️

### Prerequisites

- Python 3.8+
- Django 4.0+
- Django REST Framework
- SQLite (or any other database supported by Django)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/sedwna/Social-Security-Organization-Application.git
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```

---

## Usage 🚀

### 1. **Access the Admin Interface**
   - Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.
   - Manage users, cases, and workshops directly from the admin panel.

### 2. **User Registration**
   - Use the `/api/ssoweb/register/` endpoint to register new users.
   - Required fields: `username`, `phone_number`, `national_id`, `person_type`, `gender`, `province`, `address`, `birth_date`.

### 3. **OTP Authentication**
   - Send OTP to a registered phone number using `/api/ssoweb/send-otp/`.
   - Verify OTP using `/api/ssoweb/verify-otp/`.

### 4. **Case Management**
   - Create a new case using `/api/ssoweb/create-case/`.
   - List user cases using `/api/ssoweb/cases/`.

### 5. **Workshop Management**
   - Create a new workshop using `/api/ssoweb/create-workshop/`.
   - List user workshops using `/api/ssoweb/list-user-workshops/`.

---

## API Endpoints 🌐

| Endpoint                     | Method | Description                                      |
|------------------------------|--------|--------------------------------------------------|
| `/api/ssoweb/send-otp/`      | POST   | Send OTP to a registered phone number.          |
| `/api/ssoweb/verify-otp/`    | POST   | Verify OTP for user authentication.             |
| `/api/ssoweb/register/`      | POST   | Register a new user.                            |
| `/api/ssoweb/user-profile/`  | GET    | Retrieve user profile by phone number.          |
| `/api/ssoweb/create-case/`   | POST   | Create a new case for the authenticated user.   |
| `/api/ssoweb/cases/`         | GET    | List all cases for the authenticated user.      |
| `/api/ssoweb/create-workshop/`| POST  | Create a new workshop for a specific case.      |
| `/api/ssoweb/list-user-workshops/`| GET | List all workshops for the authenticated user. |

---

## Models Overview 📋

### 1. **CustomUser**
   - Extends Django's `AbstractUser`.
   - Fields: `username`, `phone_number`, `national_id`, `person_type`, `gender`, `province`, `address`, `birth_date`.

### 2. **Case**
   - Represents a case for either an individual or legal user.
   - Fields: `user`, `case_number`, `trade_license`, `operation_license`, `person_type`.

### 3. **Workshop**
   - Represents a workshop associated with a case.
   - Fields: `case`, `workshop_code`, `period`, `status`, `activity_type`, `activity_start_date`.

### 4. **OTP**
   - Manages OTP codes for user authentication.
   - Fields: `phone_number`, `code`, `created_at`, `is_valid`.

---

## Admin Interface 🖥️

The Django admin interface allows you to manage:

- **Users**: View and edit user details.
- **Cases**: View and edit case details.
- **Workshops**: View and edit workshop details.
- **OTPs**: View and manage OTP codes.

Access the admin interface at `http://127.0.0.1:8000/admin/`.

---

## Contributing 🤝

We welcome contributions to this project! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push your changes to your fork (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

---


## Acknowledgments 🙏

- **Django Community**: For providing an excellent framework for building web applications.
- **Open Source Contributors**: For inspiring this project with their work.

---

## Contact 📧

For questions or feedback, feel free to reach out:

- **Email**: [sajaddehqan2002@gmail.com]

--- 

