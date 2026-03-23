import os   
from dotenv import load_dotenv
load_dotenv() 
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from jose import JWTError, jwt
from passlib.context import CryptContext
import psycopg2

app = FastAPI()

#подключаемся к базе данных 


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://macbook@localhost/todo_db")

conn = psycopg2.connect(DATABASE_URL)

cursor = conn.cursor()

# Создаём таблицы если не существуют
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        password VARCHAR(200) NOT NULL
    )
""")
cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
        id SERIAL PRIMARY KEY,
        title VARCHAR(200) NOT NULL,
        done BOOLEAN DEFAULT FALSE
    )
""")
conn.commit()

# настройкт JWT
SECRET_KEY = os.getenv("SECRET_KEY", "supersecretkey")
ALGORITHM = "HS256"

# шифрование паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


# МОДЕЛИ Описываем схему — как ДОЛЖНА выглядеть задача
class Todo(BaseModel):
    title: str
    done: bool=False

class UserRegister(BaseModel):
    username: str
    password: str

# функции для работы с паролями и токенами
def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed: str):
    return pwd_context.verify(plain_password, hashed)

def create_token(username: str):
    return jwt.encode({"sub": username}, SECRET_KEY, algorithm=ALGORITHM)

def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="неверный токен")
        return username
    except JWTError:
        raise HTTPException(status_code=401, detail="неверный токен")


# Регистрация
@app.post("/register")
def register(user: UserRegister):
    hashed = hash_password(user.password)
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (user.username, hashed))
        conn.commit()
        return {"message": "Пользователь зарегистрирован"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=400, detail=str(e))


# логин - возвращает токен
@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT password FROM users WHERE username = %s", (form_data.username,))
    row = cursor.fetchone()
    if not row or not verify_password(form_data.password, row[0]):
        raise HTTPException(status_code=401, detail="Неверные log or password")
    token = create_token(form_data.username)
    return {"access_token": token, "token_type": "bearer"}

@app.post("/token")
def token(form: OAuth2PasswordRequestForm = Depends()):
    cursor.execute("SELECT password FROM users WHERE username = %s", (form.username,))
    row = cursor.fetchone()
    if not row or not verify_password(form.password, row[0]):
        raise HTTPException(status_code=401, detail="Неверный логин или пароль")
    token = create_token(form.username)
    return {"access_token": token, "token_type": "bearer"}



# задачи - только для авторизованых пользователей
@app.get("/todos")
def get_todos(current_user: str = Depends(get_current_user)):
    cursor.execute("SELECT id, title, done FROM todos")
    rows = cursor.fetchall()
    return [{"id": row[0], "title": row[1], "done": row[2]} for row in rows]

@app.get("/todos/{todo_id}")
def get_todo(todo_id: int):
    cursor.execute("SELECT id, title, done FROM todos WHERE id = %s", (todo_id,))
    row = cursor.fetchone()
    if row:
        return {"id": row[0], "title": row[1], "done": row[2]}
    return {"error": "Задача todo не найдена"}


@app.post("/todos")
def create_todo(todo: Todo, current_user: str = Depends(get_current_user)):  # теперь принимает только Todo
    cursor.execute(
        "INSERT INTO todos (title, done) VALUES (%s, %s) RETURNING id",
        (todo.title, todo.done)
     )
    new_id = cursor.fetchone()[0]
    conn.commit()
    return {"id": new_id, "title": todo.title, "done": todo.done}