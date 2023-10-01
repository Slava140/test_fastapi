import uuid

from fastapi import FastAPI, Body
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles


# uvicorn


class User:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
        self.id_ = str(uuid.uuid4())


def find_user_by_id(user_id: str):
    filtered = list(filter(lambda user: user_id == user.id_, users))
    return None if len(filtered) == 0 else filtered[0]


app = FastAPI()
app.mount("/static", StaticFiles(directory="static"))
users = [User("Tom", 12), User("Alex", 19)]


@app.get('/')
def home():
    return FileResponse("static/index.html")


@app.get('/api/users')
def get_users():
    return users


@app.get('/api/users/{user_id}')
def get_user(user_id: str):
    user = find_user_by_id(user_id)
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    return user


@app.post('/api/users')
def create_user(data=Body()):
    user = User(data['name'], data['age'])
    users.append(user)
    return user


@app.put('/api/users')
def edit_user(data=Body()):
    user = find_user_by_id(data['id_'])
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    user.name = data['name']
    user.age = data['age']
    return user


@app.delete('/api/users/{user_id}')
def delete_user(user_id: str):
    user = find_user_by_id(user_id)
    if user is None:
        return JSONResponse(status_code=404, content={"message": "Пользователь не найден"})
    users.remove(user)
    return user
# @app.get("/user/{name}", status_code=200)
# def user(response: Response, name: str):
#     if name not in users:
#         response.status_code = 404
#         return PlainTextResponse(content="Такой пользователь не найден")
#     return PlainTextResponse(content=f"Добро пожаловать, {name}")
#
#
# @app.post("/hello")
# def hello(people: List[User]):
#     return {"message": people}
