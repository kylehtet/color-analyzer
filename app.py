"""
FastAPI backend for Color Analyzer
"""
from fastapi import FastAPI, File, UploadFile, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
import tempfile
from color_analyzer import analyze_color

app = FastAPI(title="Color Analyzer API")

# Enable CORS for frontend
# Note: In production, replace ["*"] with specific allowed origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure with specific domains in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    """Serve the main page"""
    if os.path.exists("static/index.html"):
        return FileResponse("static/index.html")
    return {"message": "Color Analyzer API", "docs": "/docs"}


@app.post("/analyze")
async def analyze(
    image: UploadFile = File(...),
    style: str = Form("subtle"),
    formality: str = Form("casual")
):
    """
    Analyze a selfie image and return color recommendations.
    
    Args:
        image: Uploaded image file
        style: Style preference - "subtle" or "bold"
        formality: Formality level - "casual" or "professional"
    
    Returns:
        JSON with undertone, colors, and outfit suggestions
    """
    # Validate inputs
    if style not in ["subtle", "bold"]:
        raise HTTPException(status_code=400, detail="Style must be 'subtle' or 'bold'")
    
    if formality not in ["casual", "professional"]:
        raise HTTPException(status_code=400, detail="Formality must be 'casual' or 'professional'")
    
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as temp_file:
        content = await image.read()
        temp_file.write(content)
        temp_path = temp_file.name
    
    try:
        # Analyze the image
        result = analyze_color(temp_path, style, formality)
        
        return {
            "success": True,
            "undertone": result["undertone"],
            "colors": result["colors"],
            "outfits": result["outfits"]
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"An error occurred during analysis: {str(e)}")
    finally:
        # Clean up temporary file
        if os.path.exists(temp_path):
            os.unlink(temp_path)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
