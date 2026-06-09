from fastapi import FastAPI
from app.route.upload import upload

app = FastAPI()

app.include_router(upload)

@app.get("/")
def home():
    return {"mensagem": "API funcionando"}