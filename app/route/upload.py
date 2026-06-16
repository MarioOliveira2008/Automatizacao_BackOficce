from fastapi import APIRouter, UploadFile, File, HTTPException
import pymupdf  
import requests
import os

upload = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)

@upload.post("/")
async def processar_pdf(arquivo: UploadFile = File(...)):
    GROQ_API_KEY = os.getenv("API_KEY")
    
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Chave da Groq não encontrada no .env")

    if arquivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    try:
        conteudo_bytes = await arquivo.read()
        documento = pymupdf.open(stream=conteudo_bytes, filetype="pdf")
        
        total_paginas = len(documento)
        texto_completo = ""
        for pagina in documento:
            texto_completo += str(pagina.get_text("text"))
        documento.close()

        prompt = f"Resuma o seguinte texto em uma frase curta:\n\n{texto_completo}"
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": prompt}], "temperature": 0.3}

        resposta = requests.post(url, headers=headers, json=payload)
        
        if resposta.status_code == 200:
            texto_ia = resposta.json()["choices"][0]["message"]["content"]
        else:
            texto_ia = f"Erro na IA: {resposta.text}"

        return {
            "mensagem": "Sucesso", 
            "arquivo": arquivo.filename, 
            "total_paginas": total_paginas, 
            "resposta_ia": texto_ia
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))