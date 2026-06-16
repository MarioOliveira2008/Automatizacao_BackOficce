from fastapi import APIRouter
from app.database import SessionLocal
from app.model.documento import Documento

historico = APIRouter()

@historico.get("/historico/")
async def listar_historico():
    banco = SessionLocal()
    documentos_salvos = banco.query(Documento).all() 
    banco.close()
    return documentos_salvos

@historico.get("/limpar-historico/")
async def apagar_historico():
    banco = SessionLocal()
    banco.query(Documento).delete()
    banco.commit()
    banco.close()
    return {"status": "Histórico apagado"}