# Arquivo: app/route/upload.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from app.database import SessionLocal
from app.model.documento import Documento
import pymupdf
import requests
import os

upload = APIRouter()

@upload.post("/uploads/")
async def processar_pdf(arquivo: UploadFile = File(...), pergunta: str = Form(...)):
    # 1. Verifica se a chave da API existe
    GROQ_API_KEY = os.getenv("API_KEY")
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Chave API_KEY não encontrada no .env")

    try:
        # 2. Lê o PDF de forma blindada (sem dar erro de +=)
        conteudo_arquivo = await arquivo.read()
        doc_pdf = pymupdf.open(stream=conteudo_arquivo, filetype="pdf")
        
        textos_das_paginas = [] 
        total_paginas = len(doc_pdf)

        for pagina in doc_pdf:
            # Força o resultado a ser texto e guarda na lista
            texto = str(pagina.get_text())
            textos_das_paginas.append(texto)

        # Junta todas as páginas de uma vez só
        texto_completo = "\n".join(textos_das_paginas)

        # 3. O Prompt Livre (Junta o seu comando com o texto do PDF)
        prompt_inteligente = f"{pergunta}\n\n--- CONTEÚDO DO DOCUMENTO ---\n{texto_completo}"

        # 4. Envia para a API da Groq
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}", 
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant", 
            "messages": [{"role": "user", "content": prompt_inteligente}], 
            "temperature": 0.3
        }

        resposta = requests.post(url, headers=headers, json=payload)

        # 5. Desempacota a resposta da IA
        if resposta.status_code == 200:
            texto_ia = resposta.json()["choices"][0]["message"]["content"]
        else:
            raise HTTPException(status_code=500, detail="Erro ao consultar a IA da Groq.")

        # 6. Salva as informações no Banco de Dados SQLite
        banco = SessionLocal() 
        novo_doc = Documento(
            nome_arquivo=arquivo.filename,
            total_paginas=total_paginas,
            texto_extraido=texto_completo,
            resposta_ia=texto_ia
        )
        banco.add(novo_doc) 
        banco.commit()
        banco.refresh(novo_doc) 
        
        # Guarda o ID antes de fechar o banco para devolver ao Front-end
        id_gerado = novo_doc.id 
        banco.close()       

        # 7. Retorna o sucesso para o JavaScript (Front-end)
        return {
            "mensagem": "Sucesso", 
            "arquivo": arquivo.filename, 
            "total_paginas": total_paginas, 
            "resposta_ia": texto_ia,
            "documento_id": id_gerado
        }

    except Exception as e:
        # Se qualquer coisa der errado, avisa o Front-end para não ficar travado
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")