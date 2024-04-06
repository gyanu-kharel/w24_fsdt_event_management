from fastapi import FastAPI

app = FastAPI()

@app.get("/notifications/ping")
def index():
    return {"ping": "pong"}