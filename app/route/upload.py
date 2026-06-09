from fastapi import APIRouter, UploadFile, File
import shutil

upload = APIRouter()

@upload.post("/")
async def upload_pdf(arquivo: UploadFile = File(...)):
    with open(f"upload/{arquivo.filename}", "wb") as buffer:
        shutil.copyfileobj(arquivo.file, buffer)

    return {
        "mensagem": "Upload realizado com sucesso",
        "arquivo": arquivo.filename
    }
    