# OiOink - Financial Education Platform for Kids

> **Note**: OiOink APP is in progress.

A comprehensive Django-based web application designed to teach children financial literacy through interactive lessons, virtual wallets, spending tracking, savings goals, achievements, and gamification.

## Table of Contents

- [Features](#features)
- [Technology Stack](#technology-stack)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

### Core Modules

- **Interactive Lessons System**
  - Educational financial literacy lessons for kids
  - Progress tracking and completion certificates
  - Multiple lesson types (content, activities, games, stories)
  - Virtual coin rewards for lesson completion

- **Virtual Wallet System**
  - Multiple wallets per user
  - Income and expense tracking
  - Transaction history
  - Monthly statistics and visualizations

- **Spending Tracking**
  - Categorize expenses with icons and colors
  - Spending dashboard with category analysis
  - Monthly spending reports

- **Savings Goals**
  - Create and manage savings goals
  - Visual progress tracking with progress bars
  - Goal completion tracking
  - Set target amounts and deadlines

- **Achievement System**
  - Unlock achievements by completing various activities
  - Automatic achievement detection
  - Achievement progress tracking
  - Virtual coin rewards

- **Prize Shop**
  - Redeem virtual coins for prizes
  - Digital and physical prize options
  - Redemption history tracking

- **Unified Dashboard**
  - Comprehensive overview of all financial activities
  - Visual progress indicators
  - Quick access to all features
  - Responsive design

## Technology Stack

- **Backend Framework**: Django 6.0
- **Database**: PostgreSQL (production) / SQLite (development)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Python Version**: 3.13+
- **Key Libraries**:
  - `django-decouple` - Environment variable management
  - `psycopg2-binary` - PostgreSQL adapter
  - `django-storages` - Storage backend support

## Installation

### Prerequisites

- Python 3.13 or higher
- PostgreSQL (optional, SQLite works for development)
- pip (Python package manager)

### Step 1: Clone the Repository

```bash
git clone <repository-url>
cd oioink
```

### Step 2: Create Virtual Environment

```bash
python -m venv venv

# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
cd src
pip install -r requirements.txt
```

> **Note**: If `requirements.txt` doesn't exist, install dependencies manually:
> ```bash
> pip install django==6.0 decouple psycopg2-binary django-storages
> ```

### Step 4: Database Setup

#### Option A: Using SQLite (Development - Default)

No additional setup required. Django will create `db.sqlite3` automatically.

#### Option B: Using PostgreSQL (Production)

1. Install PostgreSQL:
   ```bash
   # macOS
   brew install postgresql@16
   brew services start postgresql@16
   ```

2. Create database and user:
   ```bash
   psql postgres
   CREATE DATABASE oioinkdb;
   CREATE USER oioink_user WITH PASSWORD 'your_password';
   GRANT ALL PRIVILEGES ON DATABASE oioinkdb TO oioink_user;
   \q
   ```

## Configuration

### Environment Variables

Create a `.env` file in `src/aienv/config/` by copying the example file:

```bash
cd src/aienv/config/
cp .env.example .env
```

Then edit the `.env` file with your actual values. Required variables:

```bash
# Django Settings
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database Configuration (for PostgreSQL)
USE_POSTGRESQL=False  # Set to True to use PostgreSQL
DB_NAME=oioinkdb
DB_USER=oioink_user
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Email Configuration (optional)
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
EMAIL_USE_TLS=True
```

### Generate Secret Key

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

### Run Migrations

```bash
cd src
python manage.py makemigrations
python manage.py migrate
```

### Create Superuser

```bash
python manage.py createsuperuser
```

## Usage

### Start Development Server

```bash
cd src
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` in your browser.

### Access Admin Panel

Visit `http://127.0.0.1:8000/admin/` and log in with your superuser credentials.

### Management Commands

```bash
# Create default achievements
python manage.py create_default_achievements

# Create sample lesson
python manage.py create_lesson1
```

## Project Structure

```
oioink/
├── src/                          # Main project directory
│   ├── accounts/                 # User authentication and profiles
│   ├── achievements/             # Achievement system
│   ├── lessons/                  # Educational lessons module
│   ├── wallet/                   # Virtual wallet system
│   ├── tracking/                 # Spending and savings tracking
│   ├── prizes/                   # Prize redemption system
│   ├── myhome/                   # Home page and dashboard
│   ├── myapp/                    # Mobile APP API (in development)
│   ├── templates/                # HTML templates
│   ├── static/                   # CSS, JavaScript, images
│   ├── media_cdn/                # User-uploaded media files
│   ├── mysite/                   # Django project settings
│   │   ├── settings.py           # Main settings file
│   │   ├── urls.py               # URL configuration
│   │   └── wsgi.py               # WSGI configuration
│   ├── aienv/                    # Environment configuration
│   │   └── config/               # .env files location
│   │       └── .env.example      # Example environment variables
│   └── manage.py                 # Django management script
├── .gitignore                    # Git ignore rules
├── LICENSE                       # MIT License
└── README.md                     # This file
```

## Key Features Explained

### Virtual Wallet System

Users can create multiple wallets, each with its own currency name and icon. Track income and expenses, view transaction history, and monitor monthly statistics.

### Savings Goals

Set financial goals with target amounts and deadlines. Track progress visually with progress bars and celebrate when goals are completed.

### Achievement System

Earn achievements by:
- Creating wallets
- Tracking spending
- Completing lessons
- Reaching savings goals
- Redeeming prizes

### Lesson System

Interactive financial education lessons designed for kids, featuring:
- Multiple content types (text, activities, games, stories)
- Progress tracking
- Completion certificates
- Virtual coin rewards

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## Notes

- This project uses a custom user model (`accounts.Account`)
- Media files are stored in `media_cdn/` directory
- Static files are collected in `static/` directory
- Database migrations should be run after cloning the repository
- Environment variables are required for proper configuration
- **Mobile APP**: The `myapp/` directory is reserved for future mobile APP API endpoints. Mobile APP version is currently in development.

## Important Security Notes

- **Never commit `.env` files** - They contain sensitive information (API keys, passwords, secrets)
- **Never commit API keys or secrets** - Always use environment variables
- **Change `SECRET_KEY`** in production
- **Set `DEBUG=False`** in production
- **Use strong database passwords** in production
- **Configure `ALLOWED_HOSTS`** properly for production
- **Review `.gitignore`** before committing - Ensure all sensitive files are listed

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Yun Li - [GitHub](https://github.com/lyunify/oioink)

## Acknowledgments

- Django framework and community
- Bootstrap for responsive design
- All contributors and users of this project

---

For more information or support, please open an issue on GitHub.

