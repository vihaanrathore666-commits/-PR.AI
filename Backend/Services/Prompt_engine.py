class AIPromptLayoutEngine:
    """
    Intelligent layout selector and prompt generation engine. Analyzes marketing intent 
    and converts metadata parameters into explicit visual style layout tokens.
    """
    
    @staticmethod
    def evaluate_creative_strategy(brand_name: str, design_style: str, user_price: str) -> dict:
        """
        Parses branding parameters to determine spacing geometry, font scale, 
        vignette densities, and structural alignment fields for the rendering engine.
        """
        # 1. Base Strategy Tokens Architecture
        tokens = {
            "font_tracking_expand": True,
            "vignette_opacity": 35,
            "border_width": 0,
            "cta_style": "pill",
            "alignment": "center",
            "footer_y_offset": 0.82,
            "badge_type": None
        }
        
        # Clean price evaluations for high-value badge distribution
        is_luxury_price = False
        try:
            numeric_price = ''.join(c for c in user_price if c.isdigit() or c == '.')
            if numeric_price and float(numeric_price) >= 150.0:
                is_luxury_price = True
        except ValueError:
            pass

        # 2. Dynamic Layout Matrix Evaluations
        if design_style == "zara":
            tokens["font_tracking_expand"] = True
            tokens["vignette_opacity"] = 0
            tokens["border_width"] = 1
            tokens["cta_style"] = "rectangle"
            tokens["footer_y_offset"] = 0.80
            if is_luxury_price:
                tokens["badge_type"] = "EDITORIAL_LIMITED"
                
        elif design_style == "apple":
            tokens["font_tracking_expand"] = False
            tokens["vignette_opacity"] = 15
            tokens["border_width"] = 0
            tokens["cta_style"] = "pill_outline"
            tokens["footer_y_offset"] = 0.84
            
        elif design_style == "dark_luxury":
            tokens["font_tracking_expand"] = True
            tokens["vignette_opacity"] = 65
            tokens["border_width"] = 0
            tokens["cta_style"] = "pill"
            tokens["footer_y_offset"] = 0.82
            tokens["badge_type"] = "PREMIUM_COLLECTION"
            
        elif design_style == "streetwear":
            tokens["font_tracking_expand"] = False
            tokens["vignette_opacity"] = 40
            tokens["border_width"] = 3
            tokens["cta_style"] = "bold_block"
            tokens["footer_y_offset"] = 0.78
            tokens["badge_type"] = "DROP_ACTIVE"

        return tokens
