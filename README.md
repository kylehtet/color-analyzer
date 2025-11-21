# Color Analyzer 🎨

A web application that analyzes your skin tone from a selfie and recommends personalized colors and outfit combinations.

## Features

- **Skin Tone Analysis**: Upload a selfie and get your undertone (warm, cool, or neutral) detected using computer vision
- **Color Recommendations**: Get a personalized color palette with hex codes based on your undertone and style preferences
- **Outfit Suggestions**: Receive tailored outfit recommendations based on your preferences (style and formality)
- **Interactive Web Interface**: Easy-to-use frontend with file upload and dropdown selections

## Tech Stack

- **Backend**: FastAPI (Python)
- **Frontend**: HTML, CSS, JavaScript
- **Image Processing**: OpenCV, NumPy
- **API**: RESTful API with `/analyze` endpoint

## Installation

1. Clone the repository:
```bash
git clone https://github.com/kylehtet/color-analyzer.git
cd color-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the server:
```bash
python app.py
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

3. Upload a selfie, select your style preference (subtle/bold) and formality level (casual/professional), then click "Analyze My Colors"

## API Endpoints

### `POST /analyze`

Analyzes an uploaded image and returns color recommendations.

**Parameters:**
- `image` (file): The selfie image to analyze
- `style` (form): Style preference - "subtle" or "bold"
- `formality` (form): Formality level - "casual" or "professional"

**Response:**
```json
{
  "success": true,
  "undertone": "warm",
  "colors": [
    {"name": "Warm Beige", "hex": "#D4A574"},
    {"name": "Olive Green", "hex": "#808000"}
  ],
  "outfits": [
    "Olive green t-shirt with beige chinos",
    "Terracotta sweater with brown jeans"
  ]
}
```

### `GET /health`

Health check endpoint.

**Response:**
```json
{
  "status": "healthy"
}
```

## Python Script Usage

You can also use the color analyzer as a standalone Python script:

```python
from color_analyzer import analyze_color

result = analyze_color("selfie.jpg", style="subtle", formality="casual")
print(f"Undertone: {result['undertone']}")
print(f"Colors: {result['colors']}")
print(f"Outfits: {result['outfits']}")
```

## Project Structure

```
color-analyzer/
├── app.py                 # FastAPI backend
├── color_analyzer.py      # Color analysis logic
├── requirements.txt       # Python dependencies
├── static/
│   └── index.html        # Frontend interface
└── README.md             # This file
```

## How It Works

1. **Image Upload**: User uploads a selfie through the web interface
2. **Skin Detection**: OpenCV detects skin pixels in the image
3. **Undertone Analysis**: RGB values are analyzed to determine undertone (warm/cool/neutral)
4. **Color Matching**: Based on undertone and preferences, matching color palettes are selected
5. **Outfit Suggestions**: Personalized outfit combinations are generated
6. **Results Display**: Undertone, color chips with hex codes, and outfit suggestions are shown

## License

MIT