# from fastapi import FastAPI
# app = FastAPI()
# @app.get('/')
# def root():
#     return {'message': 'Hello FastAPI'}


from routers import tasks, users, auth
from fastapi import FastAPI
from routers.graphql import create_graphql_app 
app = FastAPI(title="мое айпи", description="Пример API с разделением на модули")


app.include_router(tasks.router)
app.include_router(users.router)
app.include_router(auth.router)

app.include_router(
    create_graphql_app(),
    prefix = "/graphql"
)


@app.get("/")
async def root():
    return {
        "message": "welcome to api",
        "endpoints":{
            "tasks": "/tasks",
            "users": "/users",
            "auth": "/auth",
        },
        "graphql": "/graphql"
    }



