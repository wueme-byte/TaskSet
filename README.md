# TaskSet API

REST API for task management with authentication.

## Tech Stack

- **FastAPI** — web framework
- **PostgreSQL** — database
- **JWT** — authentication
- **Docker** — containerization

## Getting Started
```bash
docker-compose up --build
```

API will be available at `http://localhost:8000`

Swagger docs: `http://localhost:8000/docs`

## Endpoints

| Method | URL | Description |
|--------|-----|-------------|
| POST | /register | Register new user |
| POST | /login | Login, returns JWT token |
| GET | /todos | Get all tasks |
| POST | /todos | Create new task |
| GET | /todos/{id} | Get task by id |