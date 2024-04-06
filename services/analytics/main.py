from fastapi import FastAPI

app = FastAPI()

@app.get("/analytics/ping")
def index():
    return {"ping": "pong"}