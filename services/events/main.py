from fastapi import FastAPI

app = FastAPI()

@app.get("/events/ping")
def index():
    return {"ping": "pong"}