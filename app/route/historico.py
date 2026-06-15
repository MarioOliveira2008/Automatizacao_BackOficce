from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.model.documento import Documento

historico = APIRouter(
    prefix="/historico",
    tags=["Historico"]
)

@historico.get("/")
def listar_historico(
    db: Session = Depends(get_db)
):
    return db.query(Documento).all()