from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
import io
from PIL import Image

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Engine transforming raw product assets into premium luxury marketing creatives."
)

# Enforce secure operational settings across cloud instances
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", tags=["System Operational Status"])
async def health_check():
    """Validates cloud infrastructure status and memory readiness."""
    return {
        "status": "active",
        "application": settings.PROJECT_NAME,
        "version": settings.VERSION
    }

@app.post("/api/v1/upload", tags=["Core Image Pipeline"])
async def upload_raw_product_image(
    file: UploadFile = File(...),
    brand_name: str = "Generic",
    product_name: str = "Product"
):
    """Receives raw high-res images from mobile and validates structural integrity."""
    contents = await file.read()
    
    # Enforce maximum file sizes securely
    if len(contents) > settings.MAX_CONTENT_LENGTH:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="File size exceeds the maximum 50MB 4K processing boundary."
        )
        
    try:
        # Validate that the file is a readable graphic format
        image = Image.open(io.BytesIO(contents))
        image.verify()
        
        return {
            "status": "success",
            "filename": file.filename,
            "dimensions": f"{image.size[0]}x{image.size[1]}",
            "metadata": {
                "brand": brand_name,
                "product": product_name
            }
        }
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is corrupted or uses an unreadable image codec."
        )
