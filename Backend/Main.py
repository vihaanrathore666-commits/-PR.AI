from fastapi import FastAPI, UploadFile, File, Form, HTTPException, status
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.services.ai_engine import AIEngineService
from backend.services.layout_engine import LayoutEngineService
from backend.utils.enhancement import ProductEnhancementEngine
import io

app = FastAPI(title=settings.PROJECT_NAME, version=settings.VERSION)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Core Cloud Production Service Frameworks
ai_engine = AIEngineService()
layout_engine = LayoutEngineService()

@app.get("/health")
async def system_health():
    return {"status": "operational", "pipeline_modules": "Loaded", "enhancement_engine": "Active"}

@app.post("/api/v1/generate")
async def generate_marketing_creative(
    file: UploadFile = File(...),
    brand_name: str = Form("PREMIUM"),
    product_name: str = Form("Luxury Asset Item"),
    price: str = Form("$99.00"),
    discount: str = Form(""),
    design_style: str = Form("zara"),
    resolution: str = Form("instagram_feed")
):
    """
    Advanced commercial pipeline executing foreground mask segmentation, auto-color harmonies, 
    studio lighting extraction algorithms, and high-resolution master layout compounding.
    """
    contents = await file.read()
    if len(contents) > settings.MAX_CONTENT_LENGTH:
        raise HTTPException(status_code=413, detail="File metrics break maximum 50MB processing thresholds.")
        
    try:
        # Step 1: Strip image backdrop clusters cleanly
        isolated_product_layer = ai_engine.remove_background(contents)
        
        # Step 2: Inject Phase 6 Studio Lighting Re-balancing & Micro-Contrast pops
        enhanced_product_layer = ProductEnhancementEngine.enhance_studio_lighting(
            isolated_product_layer, 
            design_style
        )
        
        # Step 3: Run floor effects generation layers (Reflections/Shadow Maps)
        final_product_asset = ai_engine.generate_luxury_effects(enhanced_product_layer, design_style)
        
        # Step 4: Map typography metrics, custom badge borders, and output final file
        final_creative_stream = layout_engine.compose_creative(
            product_layer=final_product_asset,
            brand_name=brand_name,
            product_name=product_name,
            price=price,
            discount=discount,
            design_style=design_style,
            resolution=resolution
        )
        
        return StreamingResponse(final_creative_stream, media_type="image/jpeg")
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Pipeline Processing Fault: {str(e)}")
