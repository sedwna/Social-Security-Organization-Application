# SSO Project

This project is a Django-based web application designed to manage user authentication, cases, and workshops. It includes features such as OTP-based authentication, user registration, case management, and workshop creation.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Models](#models)
- [Admin Interface](#admin-interface)
- [Settings](#settings)
- [Contributing](#contributing)


## Features

- **User Authentication**: OTP-based authentication for secure login.
- **User Registration**: Register new users with unique phone numbers and national IDs.
- **Case Management**: Create and manage cases for individual and legal users.
- **Workshop Management**: Create and manage workshops associated with specific cases.
- **Admin Interface**: Django admin interface for managing users, cases, and workshops.

## Installation

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

## Usage

1. **Access the admin interface**:
   - Navigate to `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

2. **User Registration**:
   - Use the `/api/ssoweb/register/` endpoint to register new users.

3. **OTP Authentication**:
   - Send OTP to a registered phone number using `/api/ssoweb/send-otp/`.
   - Verify OTP using `/api/ssoweb/verify-otp/`.

4. **Case Management**:
   - Create a new case using `/api/ssoweb/create-case/`.
   - List user cases using `/api/ssoweb/cases/`.

5. **Workshop Management**:
   - Create a new workshop using `/api/ssoweb/create-workshop/`.
   - List user workshops using `/api/ssoweb/list-user-workshops/`.

## API Endpoints

- **Send OTP**: `POST /api/ssoweb/send-otp/`
- **Verify OTP**: `POST /api/ssoweb/verify-otp/`
- **Register User**: `POST /api/ssoweb/register/`
- **User Profile**: `GET /api/ssoweb/user-profile/`
- **Create Case**: `POST /api/ssoweb/create-case/`
- **List User Cases**: `GET /api/ssoweb/cases/`
- **Create Workshop**: `POST /api/ssoweb/create-workshop/`
- **List User Workshops**: `GET /api/ssoweb/list-user-workshops/`

## Models

- **CustomUser**: Extends Django's `AbstractUser` to include additional fields like `phone_number`, `national_id`, and `person_type`.
- **Case**: Represents a case with fields for both individual and legal users.
- **Workshop**: Represents a workshop associated with a case.
- **OTP**: Manages OTP codes for user authentication.

## Admin Interface

The Django admin interface allows you to manage:

- **Users**: View and edit user details.
- **Cases**: View and edit case details.
- **Workshops**: View and edit workshop details.
- **OTPs**: View and manage OTP codes.

Access the admin interface at `http://127.0.0.1:8000/admin/`.

## Settings

- **Database**: SQLite is used by default. You can configure other databases in `settings.py`.
- **Authentication**: Custom user model `CustomUser` is used for authentication.
- **Installed Apps**: Includes Django default apps, `rest_framework`, and `rest_framework.authtoken`.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Commit your changes (`git commit -am 'Add some feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a new Pull Request.



