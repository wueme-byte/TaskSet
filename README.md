# TaskSet API

A full-stack task management app with authentication, built with FastAPI and deployed on DigitalOcean.

## Live Demo

- **App**: http://178.62.200.90
- **API Docs**: http://178.62.200.90:8000/docs

## Tech Stack

**Backend:**
- FastAPI — web framework
- PostgreSQL — database
- JWT — authentication
- Pydantic — data validation
- Bcrypt — password hashing

**Infrastructure:**
- Docker + docker-compose
- Nginx — reverse proxy & static files
- DigitalOcean — cloud hosting

**Frontend:**
- HTML / CSS / JavaScript

## Features

- User registration with password confirmation
- JWT authentication — stay logged in between sessions
- Create, read, update and delete tasks
- Tasks are private — each user sees only their own
- Responsive dark UI

## Getting Started
```bash
git clone https://github.com/wueme-byte/TaskSet.git
cd TaskSet
docker-compose up --build
```

App will be available at `http://localhost`
API docs at `http://localhost:8000/docs`

## API Endpoints

| Method | URL | Auth | Description |
|--------|-----|------|-------------|
| POST | /register | No | Register new user |
| POST | /login | No | Login, returns JWT token |
| GET | /todos | Yes | Get all user's tasks |
| POST | /todos | Yes | Create new task |
| PUT | /todos/{id} | Yes | Update task |
| DELETE | /todos/{id} | Yes | Delete task |