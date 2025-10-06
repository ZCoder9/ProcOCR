import pathlib
from fastapi import FastAPI, Request, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import pytesseract
from PIL import Image
import io

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


BASE_DIR = pathlib.Path(__file__).parent.parent
TEMPLATES_DIR = BASE_DIR / "app" / "templates"
STATIC_DIR = BASE_DIR

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")

templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@app.get("/", response_class=HTMLResponse)
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.post("/extract-text/")
async def extract_text_from_image(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Please upload a valid image file")
    
    try:
        # Read the image file
        image_data = await file.read()
        image = Image.open(io.BytesIO(image_data))
        
        # Extract text using pytesseract
        extracted_text = pytesseract.image_to_string(image)
        
        return {
            "filename": file.filename,
            "extracted_text": extracted_text.strip(),
            "status": "success"
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing image: {str(e)}")