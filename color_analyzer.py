import cv2
import numpy as np
from PIL import Image
import pillow_heif
import io
import base64
import mediapipe as mp


mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

pillow_heif.register_heif_opener()

def analyze_color(image_bytes, hair_color, eye_color):
    try:
    
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert('RGB')
        img_np = np.array(image)
        img_rgb = img_np.copy()
        img_bgr = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)
        
        undertone = "neutral" 
        skin_tone = "medium"
        
        with mp_face_mesh.FaceMesh(
            static_image_mode=True,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5
        ) as face_mesh:
            results = face_mesh.process(img_rgb)
            
            if results.multi_face_landmarks:
                for face_landmarks in results.multi_face_landmarks:

                    mp_drawing.draw_landmarks(
                        image=img_bgr, 
                        landmark_list=face_landmarks, 
                        connections=mp_face_mesh.FACEMESH_TESSELATION, 
                        landmark_drawing_spec=None, 
                        connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
                    )
                    
                    
                    cheek_indices = [330, 347, 187, 123, 117, 111, 212]
                    height, width, _ = img_rgb.shape
                    mask = np.zeros((height, width), dtype=np.uint8)
                    points = []
                    for index in cheek_indices:
                        pt = face_landmarks.landmark[index]
                        x = int(pt.x * width)
                        y = int(pt.y * height)
                        points.append([x, y])
                    cv2.fillPoly(mask, [np.array(points)], 255)
                    
                    mean_color = cv2.mean(img_bgr, mask=mask)[:3]
                    lab_color = cv2.cvtColor(np.uint8([[mean_color]]), cv2.COLOR_BGR2Lab)[0][0]
                    
             
                    b_channel = lab_color[2]
                    if b_channel > 132: undertone = "warm"
                    elif b_channel < 124: undertone = "cool"
                    else: undertone = "neutral"

          
                    l_channel = lab_color[0]
                    print(f"DEBUG: Skin Lightness = {l_channel}") 

                    if l_channel > 190:
                        skin_tone = "fair"
                    elif l_channel > 155:
                        skin_tone = "light"
                    elif l_channel > 125:
                        skin_tone = "medium"  
                    elif l_channel > 95:
                        skin_tone = "tan"    
                    else:
                        skin_tone = "deep"
        
        
        preview_img = Image.fromarray(cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB))
        preview_img.thumbnail((500, 500))
        buffered = io.BytesIO()
        preview_img.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()

        season = determine_season(undertone, hair_color, eye_color)
        
        return get_professional_results(season, undertone, skin_tone, img_str)
        
    except Exception as e:
        print(f"Error: {e}")
        return {"success": False, "error": str(e)}

def determine_season(undertone, hair, eye):
    is_light_hair = hair in ["blonde", "light_brown", "red", "grey"]
    is_dark_hair = hair in ["black", "dark_brown"]
    if undertone == "cool":
        return "winter" if is_dark_hair else "summer"
    elif undertone == "warm":
        return "spring" if (is_light_hair or hair == "red") else "autumn"
    else:
        return "winter" if is_dark_hair else "spring"

def get_capsule_wardrobe(season, skin_tone):
    
    advice = {
        "autumn": {
            "fair": [
                {"item": "Soft Contrast", "color": "Soft Teal / Peach", "desc": "Avoid harsh dark browns. Soft, muted warm tones make you glow."},
                {"item": "Knitwear", "color": "Oatmeal", "desc": "A light, warm neutral is better than stark camel."},
                {"item": "Metal", "color": "Rose Gold", "desc": "Adds warmth without being too yellow/harsh."}
            ],
            "light": [
                {"item": "Warm Layers", "color": "Camel / Sage", "desc": "Classic Autumn tones work perfectly. Avoid neon brights."},
                {"item": "Outerwear", "color": "Trench Coat", "desc": "The quintessential item for your skin tone."},
                {"item": "Metal", "color": "Gold", "desc": "Standard gold jewelry looks natural on you."}
            ],
            "medium": [
                {"item": "Rich Definition", "color": "Rust / Terracotta", "desc": "Your medium contrast shines in rich, spicy colors."},
                {"item": "Essential Jacket", "color": "Cognac Leather", "desc": "A reddish-brown leather adds life to your complexion."},
                {"item": "Shirt", "color": "Olive Green", "desc": "Brings out the warm highlights in your skin."},
                {"item": "Metal", "color": "Brass / Gold", "desc": "Textured, antique metals look sophisticated."}
            ],
            "tan": [
                {"item": "Bold Earth", "color": "Burnt Orange", "desc": "Your rich skin tone can handle the most saturated Autumn colors."},
                {"item": "Contrast Piece", "color": "Cream / Off-White", "desc": "Creates a stunning, expensive contrast against tan skin."},
                {"item": "Statement", "color": "Forest Green", "desc": "Deep greens look majestic against bronze skin tones."},
                {"item": "Metal", "color": "Burnished Gold", "desc": "Heavy, rich gold jewelry pops."}
            ],
            "deep": [
                {"item": "High Intensity", "color": "Dark Chocolate", "desc": "Deep brown acts as a powerful neutral for you."},
                {"item": "Vibrant Pop", "color": "Mustard Yellow", "desc": "While risky for others, this looks golden and regal on deep skin."},
                {"item": "Outerwear", "color": "Espresso Leather", "desc": "Monochrome dark layers look incredibly sleek."},
                {"item": "Metal", "color": "Bright Gold", "desc": "High-shine gold creates beautiful contrast."}
            ]
        },
        "winter": {
            "fair": [
                {"item": "High Contrast", "color": "True Black", "desc": "The 'Snow White' effect. Black hair + Fair skin = Iconic contrast."},
                {"item": "Accent", "color": "Ruby Red", "desc": "A clear, cool red looks stunning against pale skin."},
                {"item": "Metal", "color": "Shiny Silver", "desc": "Icy metals complement your cool undertone."}
            ],
            "light": [
                {"item": "Balance", "color": "Navy Blue", "desc": "A classic cool dark that isn't as harsh as black."},
                {"item": "Shirt", "color": "Icy Pink", "desc": "Pastels must be icy and sharp, not dusty."},
                {"item": "Metal", "color": "Platinum", "desc": "Elegant and high-shine."}
            ],
            "medium": [
                {"item": "Cool Definition", "color": "Royal Blue", "desc": "A strong primary color that balances your medium contrast."},
                {"item": "Suiting", "color": "Charcoal Grey", "desc": "Softer than black but still sharp and commanding."},
                {"item": "Metal", "color": "White Gold", "desc": "Perfect balance for medium cool skin."}
            ],
            "tan": [
                {"item": "Vibrant Cool", "color": "Electric Blue", "desc": "Bright, cool neon tones pop incredibly against tan skin."},
                {"item": "Staple", "color": "Crisp White", "desc": "White creates a clean, fresh contrast with bronze skin."},
                {"item": "Metal", "color": "Silver", "desc": "Provides a striking cool contrast to your tan."}
            ],
            "deep": [
                {"item": "Boldest Cold", "color": "Icy White", "desc": "Stark white looks incredible against deep skin."},
                {"item": "Statement", "color": "Fuchsia / Magenta", "desc": "High-impact pinks and purples look amazing."},
                {"item": "Metal", "color": "High-Shine Silver", "desc": "Go for maximum reflectivity."}
            ]
        },
        "spring": {
            "fair": [
                {"item": "Delicate Warmth", "color": "Peach / Ivory", "desc": "Keep colors light and warm. Avoid harsh black."},
                {"item": "Dress", "color": "Soft Coral", "desc": "A gentle pop of color that brightens your complexion."},
                {"item": "Metal", "color": "Light Gold", "desc": "Subtle gold jewelry."}
            ],
            "light": [
                {"item": "Fresh Pop", "color": "Aqua / Mint", "desc": "Energetic light colors look fresh on you."},
                {"item": "Jacket", "color": "Camel", "desc": "A classic light warm neutral."},
                {"item": "Metal", "color": "Shiny Gold", "desc": "Polished gold matches your brightness."}
            ],
            "medium": [
                {"item": "Golden Glow", "color": "Turquoise", "desc": "Balances your medium depth with vibrant energy."},
                {"item": "Staple", "color": "Warm Navy", "desc": "A navy with yellow undertones (marine blue)."},
                {"item": "Metal", "color": "Yellow Gold", "desc": "Standard gold is perfect."}
            ],
            "tan": [
                {"item": "Tropical", "color": "Hot Pink / Orange", "desc": "You can wear the brightest tropical colors with ease."},
                {"item": "Statement", "color": "Lime Green", "desc": "High energy colors match your tan glow."},
                {"item": "Metal", "color": "Rose Gold", "desc": "Highlights the bronze tones in your skin."}
            ],
            "deep": [
                {"item": "Vivid Contrast", "color": "Bright Purple", "desc": "Spring purples (warm violets) look regal on deep skin."},
                {"item": "Essential", "color": "Kelly Green", "desc": "A bold, grassy green pops against deep skin."},
                {"item": "Metal", "color": "Bright Gold", "desc": "Maximum shine to match color intensity."}
            ]
        },
        "summer": {
            "fair": [
                {"item": "Ethereal", "color": "Powder Blue", "desc": "Very light cool tones look angelic on you."},
                {"item": "Essential", "color": "Soft Lavender", "desc": "Avoid heavy darks; stick to airy pastels."},
                {"item": "Metal", "color": "Matte Silver", "desc": "Brushed or matte metals are best."}
            ],
            "light": [
                {"item": "Dusty Tones", "color": "Sage Green", "desc": "Muted, greyed-out greens work perfectly."},
                {"item": "Jacket", "color": "Cool Grey", "desc": "Your best neutral. Much better than black."},
                {"item": "Metal", "color": "White Gold", "desc": "Soft and cool."}
            ],
            "medium": [
                {"item": "Muted Depth", "color": "Slate Blue", "desc": "Dusty, soft cool colors that aren't too pale."},
                {"item": "Staple", "color": "Raspberry", "desc": "A muted red-pink that adds color without being neon."},
                {"item": "Metal", "color": "Pewter", "desc": "Darker silver metals work well here."}
            ],
            "tan": [
                {"item": "Cool Contrast", "color": "Cocoa Brown", "desc": "A cool-toned brown (rosy brown) works for summers."},
                {"item": "Essential", "color": "Soft White", "desc": "Not stark white, but a soft milk white."},
                {"item": "Metal", "color": "Rose Gold", "desc": "Can work well if it leans pink/cool."}
            ],
            "deep": [
                {"item": "Rich Mute", "color": "Plum / Burgundy", "desc": "Deep cool purples look sophisticated."},
                {"item": "Jacket", "color": "Charcoal", "desc": "Dark grey is your power color."},
                {"item": "Metal", "color": "Silver", "desc": "Classic silver."}
            ]
        }
    }
    
   
    season_data = advice.get(season.lower(), {})
    
    return season_data.get(skin_tone, season_data.get("medium", []))

def get_professional_results(season, undertone, skin_tone, user_image_base64):
    palettes = {
        "winter": {"colors": ["#000000", "#FFFFFF", "#2B4C7E", "#50C878", "#E0115F"], "avoid": ["#F5F5DC", "#FFA500"]},
        "summer": {"colors": ["#B0E0E6", "#E6E6FA", "#DCAE96", "#708090", "#98FF98"], "avoid": ["#000000", "#FFA500"]},
        "autumn": {"colors": ["#808000", "#B7410E", "#FFDB58", "#FFFDD0", "#4B3621"], "avoid": ["#FFD1DC", "#F0FFFF"]},
        "spring": {"colors": ["#FF7F50", "#40E0D0", "#FFD700", "#FFE5B4", "#4CBB17"], "avoid": ["#000000", "#808000"]}
    }
    
    wardrobe_items = get_capsule_wardrobe(season, skin_tone)
    p_data = palettes.get(season.lower())
    
    formatted_colors = [{"hex": c, "name": "Color"} for c in p_data["colors"]]
    formatted_avoid = [{"hex": c, "name": "Avoid"} for c in p_data["avoid"]]


    display_title = f"{skin_tone.capitalize()} {season.capitalize()}"

    return {
        "success": True,
        "season": display_title,
        "undertone": undertone,
        "description": f"You are a {display_title}. This combination means you need colors that complement your {skin_tone} depth.",
        "colors": formatted_colors,
        "avoid": formatted_avoid,
        "wardrobe": wardrobe_items,
        "user_image": user_image_base64
    }