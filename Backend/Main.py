from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.services.ai_engine import AIEngineService
from backend.services.layout_engine import LayoutEngineService
import io

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Instantiate Core Design Engine Services
ai_engine = AIEngineService()
layout_engine = LayoutEngineService()

@app.get("/health")
async def health():
    return {"status": "active", "engine": "SAM2 and Layout Engine Loaded"}

@app.post("/api/v1/generate")
async def generate_marketing_creative(
    file: UploadFile = File(...),
    brand_name: str = Form("Premium Brand"),
    product_name: str = Form("Luxury Asset"),
    price: str = Form("$99.00"),
    discount: str = Form(""),
    design_style: str = Form("zara"),
    resolution: str = Form("instagram_feed")
):
    """
    The main execution route. Takes your phone's photo, isolates the product, 
    applies professional studio enhancement reflections, and generates the layout.
    """
    contents = await file.read()
    if len(contents) > settings.MAX_CONTENT_LENGTH:
        raise HTTPException(status_code=413, detail="File too large for 4K rendering window.")
        
    try:
        # Step 1: Strip background and isolate core foreground item geometry
        isolated_product = ai_engine.remove_background(contents)
        
        # Step 2: Inject reflections, dynamic ambient lighting overlays and drop shadows
        enhanced_product = ai_engine.generate_luxury_effects(isolated_product, design_style)
        
        # Step 3: Run Layout composition (Inject editorial spacing borders, typography alignment & price badges)
        final_creative_stream = layout_engine.compose_creative(
            product_layer=enhanced_product,
            brand_name=brand_name,
            product_name=product_name,
            price=price,
            discount=discount,
            design_style=design_style,
            resolution=resolution
        )
        
        # Stream the actual rendered JPEG image file straight back to your smartphone web screen
        return StreamingResponse(final_creative_stream, media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI pipeline failure details: {str(e)}")
