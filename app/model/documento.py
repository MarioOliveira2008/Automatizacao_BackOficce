from sqlalchemy import Column, Integer, String, Text
from app.database import Base

class Documento(Base):
    __tablename__ = "documentos"

    id = Column(Integer, primary_key=True, index=True)
    nome_arquivo = Column(String(255))
    total_paginas = Column(Integer)
    texto_extraido = Column(Text)
    resposta_ia = Column(Text)