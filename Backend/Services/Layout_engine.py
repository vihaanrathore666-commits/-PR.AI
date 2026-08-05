import io
from PIL import Image, ImageDraw, ImageFont
from backend.utils.enhancement import ProductEnhancementEngine
from backend.services.prompt_engine import AIPromptLayoutEngine

class LayoutEngineService:
    def __init__(self):
        self.dimensions = {
            "instagram_feed": (1080, 1350),
            "instagram_story": (1080, 1920),
            "4k_master": (3840, 4800)
        }

    def compose_creative(
        self, 
        product_layer: Image.Image, 
        brand_name: str, 
        product_name: str, 
        price: str, 
        discount: str, 
        design_style: str, 
        resolution: str
    ) -> io.BytesIO:
        """
        Assembles layout geometries, typography spacing matrices, and dynamic badges 
        driven by the structural prompt token architecture matrix.
        """
        canvas_size = self.dimensions.get(resolution, (1080, 1350))
        c_w, c_h = canvas_size
        
        # 1. Pull dynamic AI layout rules tokens
        strategy = AIPromptLayoutEngine.evaluate_creative_strategy(brand_name, design_style, price)
        
        # 2. Harvest product color palette metadata
        palette = ProductEnhancementEngine.extract_dominant_palette(product_layer)
        primary_accent_color = palette[0]
        
        # 3. Dynamic Base Palette Assignment Engine
        if design_style == "dark_luxury":
            bg_color = (13, 13, 15, 255)       
            text_color = (218, 165, 32, 255) # Luxury Gold Champagne Code
            sub_color = (245, 245, 247, 255)
        elif design_style == "apple":
            bg_color = (245, 245, 247, 255)    
            text_color = (29, 29, 31, 255)     
            sub_color = (134, 134, 139, 255)
        elif design_style == "streetwear":
            bg_color = (10, 10, 12, 255)
            text_color = (255, 255, 255, 255)
            sub_color = primary_accent_color + (255,)
        else: # Default Zara Minimalist
            bg_color = (255, 255, 255, 255)    
            text_color = (15, 15, 15, 255)     
            sub_color = (110, 110, 110, 255)

        # 4. Canvas Initialization & Vignette Rendering
        canvas = Image.new("RGBA", canvas_size, bg_color)
        draw = ImageDraw.Draw(canvas)
        
        if strategy["vignette_opacity"] > 0:
            for r in range(int(c_w * 0.85), 0, -6):
                alpha = int(strategy["vignette_opacity"] * (1.0 - (r / (c_w * 0.85))))
                draw.ellipse(
                    [c_w//2 - r, c_h//2 - r, c_w//2 + r, c_h//2 + r], 
                    fill=(primary_accent_color[0], primary_accent_color[1], primary_accent_color[2], alpha)
                )

        # 5. Core Product Geometry Alignment
        max_w, max_h = int(c_w * 0.82), int(c_h * 0.55)
        product_layer.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        prod_w, prod_h = product_layer.size
        
        prod_x = (c_w - prod_w) // 2
        prod_y = int(c_h * 0.22)
        canvas.alpha_composite(product_layer, (prod_x, prod_y))
        
        # 6. Framing Borders Engine Pass
        if strategy["border_width"] > 0:
            pad = int(c_w * 0.03)
            border_color = text_color if design_style != "zara" else (235, 235, 235, 255)
            draw.rectangle([pad, pad, c_w - pad, c_h - pad], outline=border_color, width=strategy["border_width"])

        # 7. Intelligent Typography Distribution Engine
        if strategy["font_tracking_expand"]:
            brand_display = "  ".join(list(brand_name.upper()))
        else:
            brand_display = brand_name.upper()
            
        draw.text((c_w // 2, int(c_h * 0.08)), brand_display, fill=text_color, anchor="mm")
        
        # 8. Dynamic Retail Badge Ingestion Pass
        if strategy["badge_type"]:
            badge_y = int(c_h * 0.14)
            badge_txt = strategy["badge_type"].replace("_", " ")
            draw.text((c_w // 2, badge_y), f"★ {badge_txt} ★", fill=sub_color, anchor="mm")

        # Footer Copy blocks
        footer_base_y = int(c_h * strategy["footer_y_offset"])
        draw.text((c_w // 2, footer_base_y), product_name, fill=text_color, anchor="mm")
        
        price_string = f"{price}  -  ARRIVING NOW" if not discount else f"{price} ({discount})"
        draw.text((c_w // 2, footer_base_y + int(c_h * 0.045)), price_string, fill=sub_color, anchor="mm")
        
        # 9. Smart CTA Generation Execution Blocks
        cta_y = int(c_h * 0.93)
        cta_w, cta_h = int(c_w * 0.38), int(c_h * 0.038)
        cx1, cy1 = (c_w - cta_w) // 2, cta_y - (cta_h // 2)
        cx2, cy2 = cx1 + cta_w, cy1 + cta_h
        
        if strategy["cta_style"] == "rectangle":
            draw.rectangle([cx1, cy1, cx2, cy2], fill=(18, 18, 20, 255))
            draw.text((c_w // 2, cta_y), "SHOP SELECTION", fill=(255, 255, 255, 255), anchor="mm")
        elif strategy["cta_style"] == "pill_outline":
            draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=12, outline=text_color, width=1)
            draw.text((c_w // 2, cta_y), "DISCOVER MORE", fill=text_color, anchor="mm")
        elif strategy["cta_style"] == "bold_block":
            draw.rectangle([cx1, cy1, cx2, cy2], fill=sub_color)
            draw.text((c_w // 2, cta_y), "GET IT NOW", fill=bg_color, anchor="mm")
        else: # Standard Premium Pill
            draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=8, fill=text_color)
            draw.text((c_w // 2, cta_y), "SHOP COLLECTION", fill=bg_color, anchor="mm")

        # 10. Frame Buffer Assembly
        output_buffer = io.BytesIO()
        canvas.convert("RGB").save(output_buffer, format="JPEG", quality=98)
        output_buffer.seek(0)
        return output_buffer
