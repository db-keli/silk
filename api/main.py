from fastapi import FastAPI

app = FastAPI()

app.get('/')
def boilerplate():
    return 'boilerplate'