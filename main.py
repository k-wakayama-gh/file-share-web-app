# main.py
from fastapi import FastAPI, UploadFile, File, Request, HTTPException, Form
from fastapi.responses import RedirectResponse, StreamingResponse
from starlette.background import BackgroundTask
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import mimetypes
import uvicorn
import os

from storage.azure import AzureBlobStorage
from storage.local import LocalStorage

app = FastAPI()

templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

STORAGE_TYPE = os.getenv("STORAGE_TYPE", "local")

if STORAGE_TYPE == "azure":
    storage = AzureBlobStorage()
else:
    storage = LocalStorage()



@app.get("/")
async def index(request: Request):
    files = storage.list_files()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "files": files}
    )


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    uploader: str = Form(...)
):
    storage.upload(file.filename, file.file, {"uploader": uploader})
    # return {"message": "uploaded"}
    return RedirectResponse(url="/", status_code=303)


@app.post("/delete/{filename}")
async def delete_file(filename: str):
    try:
        storage.delete(filename)
        # return {"message": "deleted"}
        return RedirectResponse(url="/", status_code=303)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{filename}")
async def download_file(filename: str):
    try:
        fileobj = storage.open(filename)

        media_type, _ = mimetypes.guess_type(filename)
        if media_type is None:
            media_type = "application/octet-stream"

        return StreamingResponse(
            fileobj,
            media_type=media_type,
            headers={
                "Content-Disposition": f'attachment; filename="{filename}"'
            },
            background=BackgroundTask(fileobj.close)
        )
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="File not found")




# Commands must be single quoted
# Type command "python main.py" to activate the server for local testing
if __name__ == "__main__":
    uvicorn.run('main:app', host='localhost', port=8000, reload=True)

