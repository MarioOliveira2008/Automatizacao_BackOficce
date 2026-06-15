from fastapi import FastAPI

from app.database import Base, engine
from app.model.documento import Documento
from app.route.upload import upload
from app.route.historico import historico

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(upload)
<<<<<<< HEAD

# Serve a pasta "static" como a interface visual principal
# Coloque isto SEMPRE por baixo das rotas (include_router)
app.mount("/", StaticFiles(directory="static", html=True), name="static")
=======
app.include_router(historico)
>>>>>>> ff19b85 (Criando o historico e arrumando o arquivo upload)
