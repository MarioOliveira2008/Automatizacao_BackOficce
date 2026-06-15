from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.orm import Session

import pymupdf
import requests
import os

from app.database import get_db
from app.model.documento import Documento

upload = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)


@upload.post("/")
async def processar_pdf(
    arquivo: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    GROQ_API_KEY = os.getenv("API_KEY")

    if arquivo.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são permitidos."
        )

    try:
        # Leitura do PDF
        conteudo_bytes = await arquivo.read()

        documento_pdf = pymupdf.open(
            stream=conteudo_bytes,
            filetype="pdf"
        )

        total_paginas = len(documento_pdf)

        texto_completo = ""

        for pagina in documento_pdf:
            texto_completo += str(pagina.get_text("text"))

        documento_pdf.close()

        # Prompt para IA
        prompt = f"""
        Resuma o seguinte texto em uma frase curta:

        {texto_completo}
        """

        # Requisição para Groq
        url = "https://api.groq.com/openai/v1/chat/completions"

        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "llama-3.1-8b-instant",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.3
        }

        resposta = requests.post(
            url,
            headers=headers,
            json=payload
        )

        if resposta.status_code != 200:
            raise HTTPException(
                status_code=500,
                detail=f"Erro na API da IA: {resposta.text}"
            )

        dados_ia = resposta.json()

        texto_ia = dados_ia["choices"][0]["message"]["content"]

        # Salvar no banco
        novo_documento = Documento(
            nome_arquivo=str(arquivo.filename),
            total_paginas=total_paginas,
            texto_extraido=texto_completo,
            resposta_ia=texto_ia
        )

        db.add(novo_documento)
        db.commit()
        db.refresh(novo_documento)

        # Retorno
        return {
            "mensagem": "Arquivo processado com sucesso!",
            "id": novo_documento.id,
            "arquivo": arquivo.filename,
            "total_paginas": total_paginas,
            "resposta_ia": texto_ia
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro interno: {str(e)}"
        )