
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.route.upload import upload
import app.database # Importa apenas para garantir que a base de dados inicializa

app = FastAPI()

# Rotas de Backend
app.include_router(upload)

# Serve a pasta "static" como a interface visual principal
# Coloque isto SEMPRE por baixo das rotas (include_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")