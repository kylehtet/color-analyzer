from fastapi import FastAPI, UploadFile, File, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from color_analyzer import analyze_color
import uvicorn

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def read_index():
    return FileResponse("static/index.html")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


@app.post("/analyze")
async def analyze_endpoint(
    image: UploadFile = File(...),
    hair: str = Form(...),
    eye: str = Form(...)
):

    contents = await image.read()
    

    result = analyze_color(contents, hair, eye)
    
    return result


if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)