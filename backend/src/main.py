from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
import os

app = FastAPI()

UPLOAD_DIRECTORY = "/usr/share/nginx/html/files"

# Asegúrate de que el directorio de subida existe
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    return FileResponse(file_location, filename=filename, media_type='application/octet-stream')
