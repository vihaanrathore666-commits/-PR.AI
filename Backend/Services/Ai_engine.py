import io
import os
from PIL import Image, ImageOps, ImageFilter
from backend.utils.segmentation import LocalSegmentationEngine

class AIEngineService:
    def __init__(self):
        self.processor = LocalSegmentationEngine()

    def remove_background(self, input_image_bytes: bytes) -> Image.Image:
        """
        Routes processing down to our internal isolation engine array module.
        """
        return self.processor.extract_foreground(input_image_bytes)

    def generate_luxury_effects(self, product_image: Image.Image, design_style: str) -> Image.Image:
        """
        Injects reflection matrices, floor lighting vectors, and depth-of-field 
        shadow blurs based on your target marketing style profile configuration.
        """
        product_image = product_image.convert("RGBA")
        w, h = product_image.size
        
        if design_style == "apple":
            # Generate clean mirrored product reflection mapping
            flipped = ImageOps.flip(product_image)
            reflection = flipped.copy()
            
            # Form smooth, realistic alpha attenuation gradients for floor planes
            alpha_gradient = Image.new("L", (w, h), 0)
            for y in range(h):
                # Gradient opacity scales from 20% down to 0% linearly
                opacity = int(255 * (1.0 - (y / h)) * 0.20)
                for x in range(w):
                    alpha_gradient.putpixel((x, y), opacity)
            reflection.putalpha(alpha_gradient)
            
            # Stitch the composition canvas back together safely
            composite = Image.new("RGBA", (w, int(h * 1.45)), (0, 0, 0, 0))
            composite.paste(product_image, (0, 0))
            composite.paste(reflection, (0, h))
            return composite
            
        elif design_style == "dark_luxury":
            # Generate soft, moody under-caravaggio shadow casting pads
            shadow_canvas = Image.new("RGBA", (int(w * 1.3), int(h * 1.2)), (0, 0, 0, 0))
            shadow_vector = Image.new("RGBA", shadow_canvas.size, (10, 10, 12, 255))
            
            # Render floor contact blur profiles
            mask = Image.new("L", shadow_canvas.size, 0)
            from PIL import ImageDraw
            draw = ImageDraw.Draw(mask)
            draw.ellipse([int(w*0.15), int(h*0.95), int(w*1.15), int(h*1.15)], fill=140)
            
            blurred_mask = mask.filter(ImageFilter.GaussianBlur(radius=25))
            shadow_canvas.paste(shadow_vector, (0,0), blurred_mask)
            shadow_canvas.paste(product_image, (int(w * 0.15), 0), product_image)
            return shadow_canvas

        # Default Zara/Minimal setups utilize raw clean drop paddings
        return product_image
