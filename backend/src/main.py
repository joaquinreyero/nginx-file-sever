from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
import os

app = FastAPI()

UPLOAD_DIRECTORY = "/usr/share/nginx/html/files"
templates = Jinja2Templates(directory="templates")

# Asegúrate de que el directorio de subida existe
if not os.path.exists(UPLOAD_DIRECTORY):
    os.makedirs(UPLOAD_DIRECTORY)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
    with open(file_location, "wb") as buffer:
        buffer.write(file.file.read())
    return {"info": f"file '{file.filename}' saved at '{file_location}'"}

@app.get("/files", response_class=HTMLResponse)
async def list_files(request: Request):
    files = os.listdir(UPLOAD_DIRECTORY)
    return templates.TemplateResponse("files.html", {"request": request, "files": files})

@app.get("/files/{filename}")
async def get_file(filename: str):
    file_location = os.path.join(UPLOAD_DIRECTORY, filename)
    return FileResponse(file_location, filename=filename, media_type='application/octet-stream')
