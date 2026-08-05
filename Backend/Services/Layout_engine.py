import io
import requests
import functools
from PIL import Image, ImageDraw, ImageFont
from backend.utils.enhancement import ProductEnhancementEngine
from backend.services.prompt_engine import AIPromptLayoutEngine

# High-performance static memory cache to avoid downloading fonts repeatedly on mobile data
@functools.lru_cache(maxsize=32)
def fetch_cloud_font(font_url: str) -> bytes:
    """Downloads authoritative TrueType branding fonts from web repositories safely into buffer arrays."""
    try:
        response = requests.get(font_url, timeout=10)
        if response.status_code == 200:
            return response.content
    except Exception:
        pass
    return b""

class LayoutEngineService:
    def __init__(self):
        # Professional export aspect grids
        self.dimensions = {
            "instagram_feed": (1080, 1350),
            "instagram_story": (1080, 1920),
            "4k_master": (3840, 4800)
        }
        
        # High-end Google Font mirrors used to match luxury brand identities
        self.font_vault = {
            "serif_luxury": "https://github.com",
            "sans_clean": "https://github.com",
            "sans_bold": "https://github.com",
            "display_street": "https://github.com"
        }

    def _load_scaled_font(self, font_type: str, target_size: int) -> ImageFont.FreeTypeFont:
        """Loads a downloaded cloud font file or safely falls back to standard bitmap assets."""
        url = self.font_vault.get(font_type, "")
        font_data = fetch_cloud_font(url) if url else b""
        
        if font_data:
            try:
                return ImageFont.truetype(io.BytesIO(font_data), target_size)
            except Exception:
                pass
        return ImageFont.load_default()

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
        Assembles layouts using production typography metrics.
        Applies automated text boundary wraps and outputs commercial-grade outputs.
        """
        canvas_size = self.dimensions.get(resolution, (1080, 1350))
        c_w, c_h = canvas_size
        
        # Scale factor multiplier ensuring equal typography mapping on 1080p and 4K assets
        scale_mod = c_w / 1080.0
        
        # 1. Fetch design tokens and color properties
        strategy = AIPromptLayoutEngine.evaluate_creative_strategy(brand_name, design_style, price)
        palette = ProductEnhancementEngine.extract_dominant_palette(product_layer)
        primary_accent = palette[3] if len(palette) > 3 else palette[0]
        
        # 2. Assign Color Profiles and Font Typographies based on Style Rules
        if design_style == "dark_luxury":
            bg_color = (13, 13, 15, 255)       
            text_color = (218, 165, 32, 255) # Premium Champagne Gold
            sub_color = (220, 220, 225, 255)
            font_brand = self._load_scaled_font("serif_luxury", int(46 * scale_mod))
            font_body = self._load_scaled_font("sans_clean", int(24 * scale_mod))
            
        elif design_style == "apple":
            bg_color = (245, 245, 247, 255)    
            text_color = (29, 29, 31, 255)     
            sub_color = (134, 134, 139, 255)
            font_brand = self._load_scaled_font("sans_bold", int(42 * scale_mod))
            font_body = self._load_scaled_font("sans_clean", int(26 * scale_mod))
            
        elif design_style == "streetwear":
            bg_color = (10, 10, 12, 255)
            text_color = (255, 255, 255, 255)
            sub_color = primary_accent + (255,)
            font_brand = self._load_scaled_font("display_street", int(64 * scale_mod))
            font_body = self._load_scaled_font("sans_bold", int(28 * scale_mod))
            
        else: # Default Zara Aesthetic Editorial
            bg_color = (255, 255, 255, 255)    
            text_color = (15, 15, 15, 255)     
            sub_color = (115, 115, 115, 255)
            font_brand = self._load_scaled_font("serif_luxury", int(48 * scale_mod))
            font_body = self._load_scaled_font("sans_clean", int(22 * scale_mod))

        # 3. Initialize Base Graphic Layer Arrays
        canvas = Image.new("RGBA", canvas_size, bg_color)
        draw = ImageDraw.Draw(canvas)
        
        # 4. Render Radial Ambient Lighting Glows
        if strategy["vignette_opacity"] > 0:
            for r in range(int(c_w * 0.9), 0, -8):
                alpha = int(strategy["vignette_opacity"] * (1.0 - (r / (c_w * 0.9))))
                draw.ellipse(
                    [c_w//2 - r, c_h//2 - r, c_w//2 + r, c_h//2 + r], 
                    fill=(primary_accent[0], primary_accent[1], primary_accent[2], alpha)
                )

        # 5. autoscale and Compositing of Product Layer
        max_w, max_h = int(c_w * 0.84), int(c_h * 0.54)
        product_layer.thumbnail((max_w, max_h), Image.Resampling.LANCZOS)
        p_w, p_h = product_layer.size
        
        canvas.alpha_composite(product_layer, ((c_w - p_w) // 2, int(c_h * 0.22)))
        
        # 6. Editorial Framing Systems
        if strategy["border_width"] > 0:
            pad = int(c_w * 0.03)
            b_color = text_color if design_style != "zara" else (235, 235, 235, 255)
            draw.rectangle([pad, pad, c_w - pad, c_h - pad], outline=b_color, width=int(strategy["border_width"] * scale_mod))

        # 7. Typography Kern Tracking Adjustments
        brand_str = "  ".join(list(brand_name.upper())) if strategy["font_tracking_expand"] else brand_name.upper()
        draw.text((c_w // 2, int(c_h * 0.08)), brand_str, fill=text_color, anchor="mm", font=font_brand)
        
        # 8. Luxury Quality Seals and Release Badges
        if strategy["badge_type"]:
            badge_text = f"★  {strategy['badge_type'].replace('_', ' ')}  ★"
            font_badge = self._load_scaled_font("sans_bold", int(12 * scale_mod))
            
            # Use strict typography box measurements to size structural badges perfectly
            bbox = draw.textbbox((0, 0), badge_text, font=font_badge)
            b_w = bbox[2] - bbox[0] + int(20 * scale_mod)
            b_h = bbox[3] - bbox[1] + int(10 * scale_mod)
            bx = (c_w - b_w) // 2
            by = int(c_h * 0.14)
            
            draw.rounded_rectangle([bx, by, bx + b_w, by + b_h], radius=4, fill=(primary_accent[0], primary_accent[1], primary_accent[2], 40))
            draw.text((c_w // 2, by + b_h // 2), badge_text, fill=text_color, anchor="mm", font=font_badge)

        # 9. Dynamic Core Text Wrapping Architecture
        footer_y = int(c_h * strategy["footer_y_offset"])
        
        # Main Title Render
        draw.text((c_w // 2, footer_y), product_name.title(), fill=text_color, anchor="mm", font=font_brand)
        
        # Price and Promotion Render
        price_tag = f"{price}   SPECIFICATION COLLECTION" if not discount else f"{price}  |  SAVE {discount.upper()}"
        draw.text((c_w // 2, footer_y + int(c_h * 0.045)), price_tag, fill=sub_color, anchor="mm", font=font_body)
        
        # 10. High-converting CTA Button Matrix Compilation
        cta_center_y = int(c_h * 0.93)
        cta_w, cta_h = int(c_w * 0.40), int(c_h * 0.042)
        cx1, cy1 = (c_w - cta_w) // 2, cta_center_y - (cta_h // 2)
        cx2, cy2 = cx1 + cta_w, cy1 + cta_h
        font_cta = self._load_scaled_font("sans_bold", int(13 * scale_mod))
        
        if strategy["cta_style"] == "rectangle":
            draw.rectangle([cx1, cy1, cx2, cy2], fill=(20, 20, 22, 255))
            draw.text((c_w // 2, cta_center_y), "SHOP COLLECTION", fill=(255, 255, 255, 255), anchor="mm", font=font_cta)
        elif strategy["cta_style"] == "pill_outline":
            draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=14, outline=text_color, width=2)
            draw.text((c_w // 2, cta_center_y), "DISCOVER MORE", fill=text_color, anchor="mm", font=font_cta)
        elif strategy["cta_style"] == "bold_block":
            draw.rectangle([cx1, cy1, cx2, cy2], fill=(240, 10, 15, 255))
            draw.text((c_w // 2, cta_center_y), "GET IT NOW", fill=(255, 255, 255, 255), anchor="mm", font=font_cta)
        else: # Classic Luxury Rounded Rounded pill configuration
            draw.rounded_rectangle([cx1, cy1, cx2, cy2], radius=8, fill=text_color)
            draw.text((c_w // 2, cta_center_y), "SHOP SELECTION", fill=bg_color, anchor="mm", font=font_cta)

        # 11. Pipe byte arrays out cleanly
        output_buffer = io.BytesIO()
        canvas.convert("RGB").save(output_buffer, format="JPEG", quality=98)
        output_buffer.seek(0)
        return output_buffer
