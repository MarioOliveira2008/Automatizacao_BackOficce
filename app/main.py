
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from dotenv import load_dotenv
from app.route.historico import historico
from app.route.upload import upload
from app.database import Base, engine

load_dotenv()

# Importa as configurações do banco


# Importa as rotas separadas que vocês criaram


# Garante que o banco.db e as tabelas sejam criadas na pasta data
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Inclui as duas rotas no sistema
app.include_router(upload)
app.include_router(historico)

app.mount("/", StaticFiles(directory="static", html=True), name="static")