# Arquivo: app/route/chat.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.database import SessionLocal
from app.model.documento import Documento
import requests
import os

chat_router = APIRouter()

# Este é o nosso molde. O Front-end será OBRIGADO a mandar o ID do PDF e a Pergunta em texto.
class PerguntaChat(BaseModel):
    documento_id: int
    pergunta: str

@chat_router.post("/chat/")
async def fazer_pergunta(dados: PerguntaChat):
    GROQ_API_KEY = os.getenv("API_KEY")
    if not GROQ_API_KEY:
        raise HTTPException(status_code=500, detail="Chave API_KEY não encontrada no .env")

    # Abre a porta do banco de dados
    banco = SessionLocal()
    
    # Procura na tabela "Documento" a linha onde o ID é igual ao ID que o usuário pediu
    documento = banco.query(Documento).filter(Documento.id == dados.documento_id).first()
    
    # Fecha o banco
    banco.close()

    # Se o usuário mandar um ID fantasma, a gente barra o erro
    if not documento:
        raise HTTPException(status_code=404, detail="Documento não encontrado no banco de dados.")

    # Montamos o comando que a IA vai ler. Ela lê o texto do banco e depois responde a pergunta.
    prompt_inteligente = f"Baseado exclusivamente neste texto: '{documento.texto_extraido}'. Responda de forma clara e direta à seguinte pergunta: {dados.pergunta}"

    # Dispara para a API da Groq exatamente como fizemos na rota de upload
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
    payload = {
        "model": "llama-3.1-8b-instant", 
        "messages": [{"role": "user", "content": prompt_inteligente}], 
        "temperature": 0.3
    }

    resposta = requests.post(url, headers=headers, json=payload)

    # Devolve a resposta final para o Front-end
    if resposta.status_code == 200:
        texto_ia = resposta.json()["choices"][0]["message"]["content"]
        return {"resposta": texto_ia}
    else:
        raise HTTPException(status_code=500, detail="Erro ao consultar a IA da Groq.")