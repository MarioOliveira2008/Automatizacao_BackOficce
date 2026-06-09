from fastapi import APIRouter, UploadFile, File, HTTPException
import pymupdf  # A sua Ferrari
import requests
import os 

upload = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)

# 🚨 Cole a sua chave real da Groq (que começa com gsk_) aqui:
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

@upload.post("/")
async def processar_pdf(arquivo: UploadFile = File(...)):
    if arquivo.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Apenas arquivos PDF são permitidos.")

    try:
        # 1. Leitura do PDF
        conteudo_bytes = await arquivo.read()
        documento = pymupdf.open(stream=conteudo_bytes, filetype="pdf")
        
        total_paginas = len(documento)
        
        texto_completo = ""
        for pagina in documento:
            texto_completo += str(pagina.get_text("text"))
            
        documento.close()

        # 2. Prepara o Prompt para a IA
        prompt = f"Resuma o seguinte texto em uma frase curta:\n\n{texto_completo}"

        # 3. Comunicação com a Groq (Llama 3 na Nuvem)
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "llama-3.1-8b-instant", # O modelo oficial e rápido do Llama 3
            "messages": [
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.3 # Deixa a IA mais focada e menos criativa
        }

        # Dispara o pacote para a IA
        resposta = requests.post(url, headers=headers, json=payload)
        
        # 4. Tratamento da Resposta da Groq
        if resposta.status_code == 200:
            dados_ia = resposta.json()
            # A Groq devolve a resposta aninhada nesta estrutura:
            texto_ia = dados_ia["choices"][0]["message"]["content"]
        else:
            texto_ia = f"Erro na API da IA: {resposta.text}"

        # 5. Retorna para o HTML
        return {
            "mensagem": "Arquivo processado com sucesso!",
            "arquivo": arquivo.filename,
            "total_paginas": total_paginas,
            "resposta_ia": texto_ia
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
