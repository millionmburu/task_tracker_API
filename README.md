# Task Tracker API

A secure RESTful Flask API for tracking personal tasks. Built with JWT authentication, allowing users to sign up, log in, and manage their own tasks — with strict ownership rules ensuring no user can view or modify another user's data.

## 🔗 Live Deployment

**Base URL:** `https://task-tracker-api-jinb.onrender.com`

The API is fully deployed and live — no local setup is required to test it. You can interact with it directly using Postman, curl, or any HTTP client. See the **Endpoints** section below for full usage details.

> Note: This is a JSON API, not a browsable website. Visiting the base URL in a browser will show a 404 — that's expected, since there's no root route. Use the specific endpoints below instead.

## Tech Stack

- **Flask** — web framework
- **Flask-RESTful** — resource-based routing
- **Flask-SQLAlchemy** — ORM
- **Flask-Migrate** — database migrations
- **Flask-Bcrypt** — password hashing
- **Flask-JWT-Extended** — JWT-based authentication
- **PostgreSQL** — production database (Render)
- **SQLite** — local development database
- **Gunicorn** — production WSGI server
- **Faker** — seed data generation

## Getting Started (Local Setup)

### Prerequisites
- Python 3.12+
- pipenv (`pip install pipenv` or `sudo apt install pipenv`)

### Installation

```bash
git clone https://github.com/millionmburu/task_tracker_API.git
cd task_tracker_API
pipenv install
pipenv shell
```

### Environment Variables

Create a `.env` file in the project root:
-You'll create a .env file and put a variable called JWT_SECRET_KEY with your key
JWT_SECRET_KEY=<place your random JWT SECRET KEY HERE> 


Generate a secure key with:
```bash
python3 -c "import secrets; print(secrets.token_hex(32))"
```

### Set Up the Database

```bash
export FLASK_APP=app.py
flask db upgrade
```

### Seed Sample Data (optional)

```bash
python seed.py
```

This creates 3 sample users, each with 5 randomly generated tasks. All seeded users share the same password for easy testing:

| Password |
|---|
| `password123` |

(Usernames are randomly generated each time you seed — check the terminal output after running `seed.py` for the exact usernames created.)

### Run the App

```bash
python app.py
```

The API will be available locally at `http://127.0.0.1:5555`.

## Authentication

This API uses **JWT (JSON Web Token)** authentication. After signing up or logging in, you'll receive an `access_token`. Include it in the `Authorization` header for any protected route:

Authorization: Bearer <your_access_token>


Tokens expire after 15 minutes by default — simply log in again to get a new one.

## API Endpoints

### Auth

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| POST | `/signup` | No | Create a new user account. Returns the user object and an access token. |
| POST | `/login` | No | Log in with username and password. Returns the user object and an access token. |
| GET | `/me` | Yes | Returns the currently authenticated user's profile. |

**POST /signup — Request body:**
```json
{
  "username": "alice",
  "password": "securepassword"
}
```

**POST /signup — Response (201):**
```json
{
  "user": { "id": 1, "username": "alice" },
  "access_token": "eyJhbGci..."
}
```

**POST /login — Request body:**
```json
{
  "username": "alice",
  "password": "securepassword"
}
```

**POST /login — Response (200):** same shape as signup.

**GET /me — Response (200):**
```json
{ "id": 1, "username": "alice" }
```

---

### Tasks

All task endpoints require a valid JWT in the `Authorization` header. Users can only view or modify their own tasks — attempting to access another user's task returns a `404`.

| Method | Endpoint | Auth Required | Description |
|---|---|---|---|
| GET | `/tasks?page=1&per_page=10` | Yes | Returns a paginated list of the current user's tasks. |
| POST | `/tasks` | Yes | Creates a new task owned by the current user. |
| PATCH | `/tasks/<id>` | Yes | Partially updates a task (only fields provided are changed). Must be owned by the current user. |
| DELETE | `/tasks/<id>` | Yes | Deletes a task. Must be owned by the current user. |

**GET /tasks — Query parameters:**
- `page` (optional, default `1`)
- `per_page` (optional, default `10`)

**GET /tasks — Response (200):**
```json
{
  "tasks": [
    {
      "id": 1,
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-09-11T16:54:13.384357",
      "user_id": 1
    }
  ],
  "total": 3,
  "page": 1,
  "pages": 1,
  "per_page": 10
}
```

**POST /tasks — Request body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```
`description` is optional. `completed` defaults to `false` if not provided.

**POST /tasks — Response (201):** returns the created task object.

**PATCH /tasks/<id> — Request body (send only the fields you want to update):**
```json
{
  "completed": true
}
```

**PATCH /tasks/<id> — Response (200):** returns the updated task object.

**DELETE /tasks/<id> — Response (204):** empty body, no content.

---

## Testing the Live API (Example with curl)

```bash
# 1. Sign up
curl -X POST https://task-tracker-api-jinb.onrender.com/signup \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'

# 2. Copy the access_token from the response above, then create a task
curl -X POST https://task-tracker-api-jinb.onrender.com/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <ACCESS_TOKEN>" \
  -d '{"title": "My first task"}'

# 3. View your tasks
curl https://task-tracker-api-jinb.onrender.com/tasks \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

## Project Structure

task_tracker_API/
├── app.py # App entry point, route registration
├── config.py # Flask app + extensions configuration
├── models.py # User and Task database models
├── seed.py # Database seeding script
├── resources/
│ ├── auth.py # Signup, Login, Me endpoints
│ └── tasks.py # Task CRUD endpoints
├── migrations/ # Flask-Migrate migration history
├── Pipfile # Project dependencies
└── Procfile # Production start command (for Render)


## Security Notes

- Passwords are hashed with bcrypt before storage — plaintext passwords are never saved.
- JWT secret key is stored as an environment variable.
- All task routes verify ownership at the database query level (`filter_by(user_id=...)`), not just at the application layer.
- Ownership violations return `404` rather than `403`, to avoid confirming the existence of other users' resources.

