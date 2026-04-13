# Gaming Platform - Django Web Application

A simple Django-based gaming platform featuring FizzBuzz, TicTacToe, and Chess with user authentication and leaderboard.

## Features

- **User Authentication**: Register, Login, and Logout functionality
- **FizzBuzz Game**: User vs Computer and User vs User modes
- **TicTacToe Game**: User vs Computer and User vs User modes
- **Chess Game**: Full legal-move Chess in User vs Computer and User vs User modes
- **Leaderboard**: Track top players by total score
- **Session-Based Game State**: Game progress stored in Django sessions

## Technology Stack

- **Backend**: Django 4.2 (Python)
- **Database**: MySQL
- **Frontend**: Django Templates (HTML + CSS)
- **No JavaScript**: All logic handled server-side

## Project Structure

```
game_platform/
├── manage.py
├── requirements.txt
├── game_platform/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── games/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── forms.py
    ├── services.py
    └── templates/
        ├── base.html
        ├── home.html
        ├── login.html
        ├── register.html
        ├── fizzbuzz.html
        ├── tictactoe.html
        ├── chess.html
        └── leaderboard.html
```

## Setup Instructions

### 1. Create MySQL Database

Open MySQL Workbench and create a new database:

```sql
CREATE DATABASE game_platform_db;
```

### 2. Configure Database Settings

Edit `game_platform/settings.py` and update the database configuration:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'game_platform_db',  # Your database name
        'USER': 'root',  # Your MySQL username
        'PASSWORD': 'your_password',  # Your MySQL password
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```

### 3. Create Virtual Environment

```powershell
python -m venv venv
venv\Scripts\activate
```

### 4. Install Dependencies

```powershell
pip install -r requirements.txt
```

Note: If you encounter issues installing `mysqlclient`, you may need to install it via wheel file or use `mysql-connector-python` as an alternative:

```powershell
pip install mysql-connector-python
```

Then update `settings.py`:
```python
'ENGINE': 'mysql.connector.django',
```

### 5. Run Migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 6. Create Superuser (Optional)

```powershell
python manage.py createsuperuser
```

### 7. Run Development Server

```powershell
python manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Game Rules

### FizzBuzz
- Enter numbers sequentially
- If divisible by 3 → enter "FIZZ"
- If divisible by 5 → enter "BUZZ"
- If divisible by both → enter "FIZZBUZZ"
- Otherwise → enter the number itself
- **Scoring**: +10 points per correct answer
- Game ends on wrong answer

### TicTacToe
- Player vs Computer
- You are X, Computer is O
- Click empty cells to make your move
- **Scoring**: Win (+50), Draw (+10), Loss (0)

## URL Routes

- `/` - Home page
- `/register/` - User registration
- `/login/` - User login
- `/logout/` - User logout
- `/games/fizzbuzz/` - FizzBuzz game
- `/games/tictactoe/` - TicTacToe game
- `/leaderboard/` - View leaderboard
- `/admin/` - Django admin panel

    - User vs Computer or User vs User
    - In CPU mode: You are X, Computer is O
### PlayerProfile
- `user` - OneToOne relationship with Django User
- `total_score` - Total accumulated score
    ### Chess
    - User vs Computer or User vs User
    - Supports SAN input (e4, Nf3) and UCI input (e2e4)
    - Computer plays simple legal moves as Black in CPU mode
    - **Scoring**:
      - CPU mode: Win (+100), Draw (+30), Loss (0)
      - PvP mode: Win (+70), Draw (+30)
- `games_played` - Number of games played

### GameScore
- `user` - ForeignKey to Django User
- `game_name` - Name of the game (fizzbuzz/tictactoe)
- `score` - Score achieved in the game
- `played_at` - Timestamp of when game was played

## Admin Panel

Access the admin panel at http://127.0.0.1:8000/admin/ to manage users, player profiles, and game scores.

## Notes

- All game logic is handled server-side using Django views and services
- Game state is stored in Django sessions
- No JavaScript is used - all interactions use form submissions
- Simple CSS styling is included in base template

## License

This project is for educational purposes.

## Vercel Deployment Checklist

Use this checklist before and after deployment to keep the flow clean and error-free.

### 1. Required Files

- `vercel.json` should exist in project root.
- `api/index.py` should expose the Django WSGI app.
- `requirements.txt` should include deployment dependencies:
    - `dj-database-url`
    - `psycopg2-binary`
    - `whitenoise`

### 2. Vercel Environment Variables

Set these in Vercel Project Settings -> Environment Variables:

- `SECRET_KEY`: long random string
- `DEBUG`: `False`
- `ALLOWED_HOSTS`: your domain list (comma-separated)
    - Example: `your-app.vercel.app`
- `CSRF_TRUSTED_ORIGINS`: full https origins (comma-separated)
    - Example: `https://your-app.vercel.app`
- `DATABASE_URL`: managed database connection string

### 3. Database Migration Step

Migrations must be applied to production database whenever models change:

```powershell
python manage.py migrate
```

Check migration status anytime:

```powershell
python manage.py showmigrations
```

### 4. Static Files Step

Before release verification, ensure static files collect without warnings:

```powershell
python manage.py collectstatic --noinput
```

### 5. Health Check Commands

Run these locally before pushing:

```powershell
python manage.py check
python manage.py showmigrations games
```

All migrations should show `[X]` and `check` should report no issues.

## Best Free Cloud Database Options

### Recommended (best fit for Vercel + Django)

1. **Vercel Postgres (Neon-backed)**
     - Easy integration with Vercel
     - Good free starter tier
2. **Neon Postgres (direct)**
     - Very solid free tier
     - Fast and easy to connect via `DATABASE_URL`
3. **Supabase Postgres**
     - Good dashboard and free tier
     - Works well with Django

### Does Vercel provide database?

Yes. Vercel offers managed database products (including Postgres). For this project, Postgres is the easiest production path.

### Important note

For production on Vercel, prefer **Postgres** over local MySQL configuration unless you already manage an external MySQL service.
