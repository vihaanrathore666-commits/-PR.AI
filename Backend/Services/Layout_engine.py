import io
from PIL import Image, ImageDraw, ImageFont, ImageEnhance, ImageFilter
from backend.utils.enhancement import ProductEnhancementEngine

class LayoutEngineService:
    def __init__(self):
        # Master system resolution dictionary configurations
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
        Assembles background colors, borders, typography padding, and badges 
        to output a clean, ultra-expensive looking social ad frame.
        """
        canvas_size = self.dimensions.get(resolution, (1080, 1350))
        c_w, c_h = canvas_size
        
        # 1. Automatically harvest dynamic product palette elements
        palette = ProductEnhancementEngine.extract_dominant_palette(product_layer)
        primary_product_color = palette[0]
        
        # 2. Establish Global Luxury Architecture Layout Styling Parameters
        if design_style == "dark_luxury":
            bg_color = (13, 13, 15, 255)       
            text_color = (218, 165, 32, 255)   # Premium Champagne Luxury Gold Code
            accent_color = (245, 245, 247, 255)
            draw_ambient_gradient = True
        elif design_style == "apple":
            bg_color = (245, 245, 247, 255)    
            text_color = (29, 29, 31, 255)     
            accent_color = (134, 134, 139, 255)
            draw_ambient_gradient = False
        else: # Zara Style (Minimalist Editorial Setup)
            bg_color = (255, 255, 255, 255)    
            text_color = (15, 15, 15, 255)     
            accent_color = (110, 110, 110, 255)
            draw_ambient_gradient = False

        # 3. Instantiate and Draw Background Canvas Array Setup
        canvas = Image.new("RGBA", canvas_size, bg_color)
        draw = ImageDraw.Draw(canvas)
        
        if draw_ambient_gradient:
            # Generate a gorgeous luxury vignette radial flare in back of product layer
            for r in range(int(c_w * 0.8), 0, -4):
                alpha = int(45 * (1.0 - (r / (c_w * 0.8))))
                # Blend subtly into the background color space
                draw.ellipse(
                    [c_w//2 - r, c_h//2 - r, c_w//2 + r, c_h//2 + r], 
                    fill=(primary_product_color[0], primary_product_color[1], primary_product_color[2], alpha)
                )

        # 4. Scale and Position Product Layer Safely
        max_w = int(c_w * 0.80)
        max_h = int(c_h * 0.58)
        product_layer.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        
        prod_w, prod_h = product_layer.size
        prod_x = (c_w - prod_w) // 2
        prod_y = int(c_h * 0.20) # Editorial positioning balance rule
        
        canvas.alpha_composite(product_layer, (prod_x, prod_y))
        
        # 5. Render Geometry Layout Components (Borders & Clean Frames)
        if design_style == "zara":
            # Draw ultra-thin high-end art gallery framing border lines
            padding = int(c_w * 0.03)
            draw.rectangle([padding, padding, c_w - padding, c_h - padding], outline=(230, 230, 230, 255), width=1)

        # 6. High-Fidelity Typography Engine Simulation Core 
        # Standardizes layout rendering without failing on missing external font links
        brand_clean = "  ".join(list(brand_name.upper())) # Elegant spacing expansion
        draw.text((c_w // 2, int(c_h * 0.08)), brand_clean, fill=text_color, anchor="mm", font=None)
        
        # Draw Product Footer Titles Block Layout
        draw.text((c_w // 2, int(c_h * 0.82)), product_name, fill=text_color, anchor="mm", font=None)
        
        # Draw Dynamic Price Presentation and Automated Affiliate Tag Badge Structures
        price_tag_string = f"{price}  |  SPECIAL RELEASE" if not discount else f"{price} ({discount})"
        draw.text((c_w // 2, int(c_h * 0.87)), price_tag_string, fill=accent_color, anchor="mm", font=None)
        
        # Draw Call to Action (CTA) Pill Box Layout Frame
        cta_y = int(c_h * 0.93)
        cta_w, cta_h = int(c_w * 0.35), int(c_h * 0.035)
        cta_x1, cta_y1 = (c_w - cta_w) // 2, cta_y - (cta_h // 2)
        cta_x2, cta_y2 = cta_x1 + cta_w, cta_y1 + cta_h
        
        cta_fill = text_color if design_style != "zara" else (20, 20, 22, 255)
        cta_text_color = bg_color if design_style != "zara" else (255, 255, 255, 255)
        
        draw.rounded_rectangle([cta_x1, cta_y1, cta_x2, cta_y2], radius=6, fill=cta_fill)
        draw.text((c_w // 2, cta_y), "SHOP LINK", fill=cta_text_color, anchor="mm")

        # 7. Convert Output Canvas Stream Layout 
        output_buffer = io.BytesIO()
        canvas.convert("RGB").save(output_buffer, format="JPEG", quality=98)
        output_buffer.seek(0)
        return output_buffer
