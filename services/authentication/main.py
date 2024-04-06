from fastapi import FastAPI

app = FastAPI()

@app.get("/auth/ping")
def index():
    return {"ping": "pong"}