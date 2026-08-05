from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.services.ai_engine import AIEngineService
from backend.services.layout_engine import LayoutEngineService
from backend.utils.enhancement import ProductEnhancementEngine
# NEW: Import your independent diagnostics controller router module cleanly
from backend.services import analytics_router
import io
from PIL import Image

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate architectural services securely
ai_engine = AIEngineService()
layout_engine = LayoutEngineService()

# NEW: Dynamically map and mount your analytics tracker endpoints into the server loop
app.include_router(analytics_router.router)

@app.get("/health")
async def validation_health():
    return {"status": "active", "environment": "minimal_studio_active"}

@app.post("/api/v1/generate")
async def generate_marketing_creative(
    file: UploadFile = File(...),
    brand_name: str = Form("STUDIO"),
    product_name: str = Form("Minimal Object"),
    price: str = Form("$100.00"),
    discount: str = Form(""),
    design_style: str = Form("zara"),
    resolution: str = Form("instagram_feed")
):
    """Generates the premium visual asset composition loop inside server buffer layers."""
    contents = await file.read()
    try:
        # Step 1: Background isolation mapping
        isolated = ai_engine.remove_background(contents)
        
        # Step 2: Texture sharpening and exposure normalization
        enhanced = ProductEnhancementEngine.enhance_studio_lighting(isolated, design_style)
        
        # Step 3: Floor lighting reflections and dropshadow padding passes
        final_asset = ai_engine.generate_luxury_effects(enhanced, design_style)
        
        # Step 4: Typography compilation and composition layout rendering
        output_stream = layout_engine.compose_creative(
            product_layer=final_asset,
            brand_name=brand_name,
            product_name=product_name,
            price=price,
            discount=discount,
            design_style=design_style,
            resolution=resolution
        )
        return StreamingResponse(output_stream, media_type="image/jpeg")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/v1/export")
async def export_format_wrapper(
    file: UploadFile = File(...),
    brand_name: str = Form("STUDIO"),
    product_name: str = Form("Minimal Object"),
    price: str = Form("$100.00"),
    discount: str = Form(""),
    design_style: str = Form("zara"),
    resolution: str = Form("instagram_feed"),
    format_type: str = Form("png")
):
    """
    Phase 11 & 13 Export Module: Converts array data maps dynamically into 
    requested file extension codecs (PNG, JPG, or PDF document layout models).
    """
    contents = await file.read()
    try:
        # Re-execute baseline luxury asset transformation sequence cleanly from file buffers
        isolated = ai_engine.remove_background(contents)
        enhanced = ProductEnhancementEngine.enhance_studio_lighting(isolated, design_style)
        final_asset = ai_engine.generate_luxury_effects(enhanced, design_style)
        
        raw_jpeg_stream = layout_engine.compose_creative(
            product_layer=final_asset, 
            brand_name=brand_name, 
            product_name=product_name,
            price=price, 
            discount=discount, 
            design_style=design_style, 
            resolution=resolution
        )
        
        # Load compiled master buffer image back into PIL to translate formatting layers
        compiled_image = Image.open(raw_jpeg_stream)
        export_buffer = io.BytesIO()
        
        # Parse output data metrics and apply explicit file wrappers
        if format_type.lower() == "png":
            compiled_image.save(export_buffer, format="PNG")
            media_string = "image/png"
        elif format_type.lower() == "pdf":
            # Direct multi-platform printable PDF generation
            compiled_image.convert("RGB").save(export_buffer, format="PDF", resolution=100.0)
            media_string = "application/pdf"
        else:
            compiled_image.save(export_buffer, format="JPEG", quality=98)
            media_string = "image/jpeg"
            
        export_buffer.seek(0)
        return StreamingResponse(export_buffer, media_type=media_string)
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Export transaction failure context: {str(e)}")
