from fastapi import APIRouter, UploadFile, File, HTTPException
import os
import shutil

upload = APIRouter(
    prefix="/uploads",
    tags=["Uploads"]
)

UPLOAD_FOLDER = "upload"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@upload.post("/")
async def upload_pdf(arquivo: UploadFile = File(...)):

    # Verifica se o arquivo é PDF
    if arquivo.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Apenas arquivos PDF são permitidos."
        )

    caminho = f"{UPLOAD_FOLDER}/{arquivo.filename}"

    # Salva o arquivo
    with open(caminho, "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return {
        "mensagem": "Upload realizado com sucesso",
        "arquivo": arquivo.filename
    }