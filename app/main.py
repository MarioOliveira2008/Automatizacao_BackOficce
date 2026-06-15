from fastapi import FastAPI

from app.database import Base, engine
from app.model.documento import Documento
from app.route.upload import upload
from app.route.historico import historico

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload)
app.include_router(historico)