"""
Color Analyzer - Analyzes skin tones and recommends colors
"""
import cv2
import numpy as np
from typing import Dict, List, Tuple


def analyze_color(
    image_path: str, 
    style: str = "subtle", 
    formality: str = "casual"
) -> Dict:
    """
    Analyze skin tone from an image and recommend colors.
    
    Args:
        image_path: Path to the image file
        style: Style preference - "subtle" or "bold"
        formality: Formality level - "casual" or "professional"
    
    Returns:
        Dictionary with undertone, colors, and outfit suggestions
    """
    # Load image
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Could not load image")
    
    # Convert to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    # Detect skin tone
    undertone = detect_undertone(img_rgb)
    
    # Get color recommendations
    colors = get_color_palette(undertone, style)
    
    # Get outfit suggestions
    outfits = get_outfit_suggestions(undertone, style, formality)
    
    return {
        "undertone": undertone,
        "colors": colors,
        "outfits": outfits
    }


# Undertone detection thresholds
WARM_THRESHOLD = 10  # Red must exceed blue by this amount for warm undertone
COOL_THRESHOLD = 5   # Blue must exceed red by this amount for cool undertone


def detect_undertone(img_rgb: np.ndarray) -> str:
    """
    Detect skin undertone from RGB image.
    
    Returns:
        "warm", "cool", or "neutral"
    """
    # Simple skin detection using color ranges
    lower_skin = np.array([80, 50, 40], dtype=np.uint8)
    upper_skin = np.array([255, 200, 180], dtype=np.uint8)
    
    # Create mask for skin pixels
    skin_mask = cv2.inRange(img_rgb, lower_skin, upper_skin)
    
    # Get skin pixels
    skin_pixels = img_rgb[skin_mask > 0]
    
    if len(skin_pixels) == 0:
        return "neutral"
    
    # Calculate average RGB values
    avg_r = np.mean(skin_pixels[:, 0])
    avg_g = np.mean(skin_pixels[:, 1])
    avg_b = np.mean(skin_pixels[:, 2])
    
    # Determine undertone based on color balance
    # Warm tones have more red/yellow (higher R, lower B)
    # Cool tones have more blue/pink (higher B, G)
    if avg_r > avg_b + WARM_THRESHOLD:
        if avg_r > avg_g:
            return "warm"
    elif avg_b > avg_r + COOL_THRESHOLD:
        return "cool"
    
    return "neutral"


def get_color_palette(undertone: str, style: str) -> List[Dict[str, str]]:
    """
    Get color palette recommendations based on undertone and style.
    
    Returns:
        List of color dictionaries with name and hex code
    """
    # Color palettes for different undertones
    palettes = {
        "warm": {
            "subtle": [
                {"name": "Warm Beige", "hex": "#D4A574"},
                {"name": "Olive Green", "hex": "#808000"},
                {"name": "Terracotta", "hex": "#E2725B"},
                {"name": "Warm Brown", "hex": "#8B4513"},
                {"name": "Peach", "hex": "#FFDAB9"},
                {"name": "Coral", "hex": "#FF7F50"}
            ],
            "bold": [
                {"name": "Burnt Orange", "hex": "#CC5500"},
                {"name": "Golden Yellow", "hex": "#FFD700"},
                {"name": "Rich Red", "hex": "#DC143C"},
                {"name": "Forest Green", "hex": "#228B22"},
                {"name": "Rust", "hex": "#B7410E"},
                {"name": "Amber", "hex": "#FFBF00"}
            ]
        },
        "cool": {
            "subtle": [
                {"name": "Soft Pink", "hex": "#FFB6C1"},
                {"name": "Powder Blue", "hex": "#B0E0E6"},
                {"name": "Lavender", "hex": "#E6E6FA"},
                {"name": "Cool Gray", "hex": "#A9A9A9"},
                {"name": "Mint", "hex": "#98FF98"},
                {"name": "Silver", "hex": "#C0C0C0"}
            ],
            "bold": [
                {"name": "Royal Blue", "hex": "#4169E1"},
                {"name": "Magenta", "hex": "#FF00FF"},
                {"name": "Purple", "hex": "#800080"},
                {"name": "Emerald", "hex": "#50C878"},
                {"name": "Fuchsia", "hex": "#FF00FF"},
                {"name": "Navy", "hex": "#000080"}
            ]
        },
        "neutral": {
            "subtle": [
                {"name": "Soft Taupe", "hex": "#B38B6D"},
                {"name": "Sage", "hex": "#9DC183"},
                {"name": "Dusty Rose", "hex": "#DCAE96"},
                {"name": "Warm Gray", "hex": "#928E85"},
                {"name": "Cream", "hex": "#FFFDD0"},
                {"name": "Mauve", "hex": "#E0B0FF"}
            ],
            "bold": [
                {"name": "Teal", "hex": "#008080"},
                {"name": "Burgundy", "hex": "#800020"},
                {"name": "Deep Purple", "hex": "#6A0DAD"},
                {"name": "Olive", "hex": "#808000"},
                {"name": "Crimson", "hex": "#DC143C"},
                {"name": "Jade", "hex": "#00A86B"}
            ]
        }
    }
    
    return palettes.get(undertone, {}).get(style, palettes["neutral"]["subtle"])


def get_outfit_suggestions(undertone: str, style: str, formality: str) -> List[str]:
    """
    Get outfit suggestions based on undertone, style, and formality.
    
    Returns:
        List of outfit suggestion strings
    """
    suggestions = {
        "warm": {
            "casual": {
                "subtle": [
                    "Olive green t-shirt with beige chinos",
                    "Terracotta sweater with brown jeans",
                    "Peach blouse with warm brown pants"
                ],
                "bold": [
                    "Burnt orange hoodie with dark jeans",
                    "Golden yellow shirt with rust-colored jacket",
                    "Rich red top with forest green cardigan"
                ]
            },
            "professional": {
                "subtle": [
                    "Warm beige blazer with olive dress pants",
                    "Terracotta button-up with brown suit",
                    "Peach blouse with neutral skirt and warm brown accessories"
                ],
                "bold": [
                    "Golden yellow blouse with navy suit",
                    "Burnt orange dress shirt with charcoal blazer",
                    "Rich red suit jacket with amber accessories"
                ]
            }
        },
        "cool": {
            "casual": {
                "subtle": [
                    "Powder blue t-shirt with cool gray jeans",
                    "Lavender sweater with silver accessories",
                    "Soft pink top with mint green cardigan"
                ],
                "bold": [
                    "Royal blue hoodie with black jeans",
                    "Magenta shirt with purple jacket",
                    "Emerald green top with navy pants"
                ]
            },
            "professional": {
                "subtle": [
                    "Powder blue blouse with cool gray suit",
                    "Lavender dress shirt with silver accessories",
                    "Soft pink blazer with navy skirt"
                ],
                "bold": [
                    "Royal blue suit with white shirt",
                    "Purple dress with magenta accessories",
                    "Emerald blazer with navy dress pants"
                ]
            }
        },
        "neutral": {
            "casual": {
                "subtle": [
                    "Soft taupe sweater with sage green pants",
                    "Dusty rose top with warm gray jeans",
                    "Cream blouse with mauve cardigan"
                ],
                "bold": [
                    "Teal shirt with burgundy jacket",
                    "Deep purple top with olive pants",
                    "Jade green sweater with crimson accessories"
                ]
            },
            "professional": {
                "subtle": [
                    "Soft taupe suit with cream blouse",
                    "Sage blazer with dusty rose accessories",
                    "Warm gray suit with mauve shirt"
                ],
                "bold": [
                    "Teal blazer with burgundy dress pants",
                    "Deep purple suit with jade accessories",
                    "Olive suit with crimson blouse"
                ]
            }
        }
    }
    
    return suggestions.get(undertone, {}).get(formality, {}).get(style, [
        "Classic white shirt with dark pants",
        "Navy blazer with neutral bottoms",
        "Black dress with colorful accessories"
    ])


if __name__ == "__main__":
    # Test the analyzer
    import sys
    if len(sys.argv) > 1:
        result = analyze_color(sys.argv[1])
        print(f"Undertone: {result['undertone']}")
        print(f"Colors: {result['colors']}")
        print(f"Outfits: {result['outfits']}")
