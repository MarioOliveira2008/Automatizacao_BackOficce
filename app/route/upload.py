from fastapi import APIRouter, UploadFile, File, HTTPException
from app.database import SessionLocal
from app.model.documento import Documento
import pymupdf  
import requests
import os

upload = APIRouter()

@upload.post("/uploads/")
async def processar_pdf(arquivo: UploadFile = File(...)):
    GROQ_API_KEY = os.getenv("API_KEY") 
    
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Chave API_KEY não encontrada no .env")

    if arquivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    try:
        conteudo_bytes = await arquivo.read()
        documento_pdf = pymupdf.open(stream=conteudo_bytes, filetype="pdf")
        total_paginas = len(documento_pdf)
        texto_completo = ""
        for pagina in documento_pdf:
            texto_completo += str(pagina.get_text("text"))
        documento_pdf.close()

        prompt = f"Resuma o seguinte texto em uma frase curta:\n\n{texto_completo}"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}

        resposta = requests.post(url, headers=headers, json=payload)
        
        if resposta.status_code == 200:
            texto_ia = resposta.json()["choices"][0]["message"]["content"]
        else:
            texto_ia = f"Erro na IA: {resposta.text}"

        # Salva usando SessionLocal
        banco = SessionLocal() 
        novo_doc = Documento(
            nome_arquivo=arquivo.filename,
            total_paginas=total_paginas,
            texto_extraido=texto_completo,
            resposta_ia=texto_ia
        )
        banco.add(novo_doc) 
        banco.commit()      
        banco.close()       

        return {
            "mensagem": "Sucesso", 
            "arquivo": arquivo.filename, 
            "total_paginas": total_paginas, 
            "resposta_ia": texto_ia
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))