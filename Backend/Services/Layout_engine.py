from PIL import Image, ImageDraw, ImageFont
import io

class LayoutEngineService:
    def __init__(self):
        # Base design dimensions mapping standard premium Instagram configurations
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
        # Determine canvas size
        canvas_size = self.dimensions.get(resolution, (1080, 1350))
        
        # 1. Establish Style Palette Configs
        if design_style == "dark_luxury":
            bg_color = (15, 15, 17, 255)       # Rich Charcoal
            text_color = (212, 175, 55, 255)   # Premium Champagne Gold
            accent_color = (255, 255, 255, 255)
        elif design_style == "apple":
            bg_color = (245, 245, 247, 255)    # Clean Apple White
            text_color = (29, 29, 31, 255)     # Deep Onyx Black
            accent_color = (110, 110, 115, 255)
        else: # Zara Style (Minimalist Editorial)
            bg_color = (255, 255, 255, 255)    # Stark Gallery White
            text_color = (0, 0, 0, 255)        # Sharp Editorial Black
            accent_color = (100, 100, 100, 255)

        # 2. Render Main Canvas Canvas Background Layer
        canvas = Image.new("RGBA", canvas_size, bg_color)
        draw = ImageDraw.Draw(canvas)
        
        # 3. Position and Resize Isolated Product Layer Autoscale
        # Ensure the product scales elegantly within the upper/middle frame region
        max_prod_w = int(canvas_size[0] * 0.75)
        max_prod_h = int(canvas_size[1] * 0.55)
        
        product_layer.thumbnail((max_prod_w, max_prod_h), Image.Resampling.LANCZOS)
        
        # Center horizontally, place slightly above vertical center to save space for luxury text layout
        prod_x = (canvas_size[0] - product_layer.size[0]) // 2
        prod_y = int(canvas_size[1] * 0.22)
        
        canvas.alpha_composite(product_layer, (prod_x, prod_y))
        
        # 4. Render Editorial Typography and Badges
        # Note: In standard python setups, default system fonts are used unless .ttf handles are passed
        # We design structured geometric text alignments to mimic luxury advertisements
        
        # Draw Brand Title (Top Centered or Bottom Minimal)
        brand_clean = brand_name.upper()
        draw.text(((canvas_size[0] // 2), int(canvas_size[1] * 0.08)), brand_clean, fill=text_color, anchor="mm")
        
        # Draw Product Details Footer Block
        draw.text(((canvas_size[0] // 2), int(canvas_size[1] * 0.82)), product_name, fill=text_color, anchor="mm")
        
        # Draw Luxury Price Matrix & CTA Badge Elements
        price_display = f"{price} - Limited Release" if not discount else f"{price} ({discount})"
        draw.text(((canvas_size[0] // 2), int(canvas_size[1] * 0.88)), price_display, fill=accent_color, anchor="mm")
        
        # Export master processed asset frame as raw data stream
        output_buffer = io.BytesIO()
        canvas.convert("RGB").save(output_buffer, format="JPEG", quality=95)
        output_buffer.seek(0)
        return output_buffer
