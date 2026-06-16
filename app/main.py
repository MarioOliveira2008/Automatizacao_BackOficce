from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv

# Carrega as variáveis (como a API KEY)
load_dotenv()

# Importa apenas a rota de upload
from app.route.upload import upload

app = FastAPI()

app.include_router(upload)

# Roda o seu HTML
app.mount("/", StaticFiles(directory="static", html=True), name="static")