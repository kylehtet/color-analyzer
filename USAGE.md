# Usage Guide

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/kylehtet/color-analyzer.git
cd color-analyzer
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

### Running the Application

Start the server:
```bash
python app.py
```

The application will be available at `http://localhost:8000`

## Using the Web Interface

1. **Upload a Selfie**: Click the "Choose File" button and select a selfie image from your device
2. **Select Style Preference**: Choose between "Subtle" or "Bold" colors
3. **Select Formality Level**: Choose between "Casual" or "Professional" outfits
4. **Click "Analyze My Colors"**: The app will analyze your skin tone and display results

### Results Include:
- **Undertone**: Your skin's undertone (Warm, Cool, or Neutral)
- **Perfect Colors**: 6 color recommendations with names and hex codes
- **Outfit Suggestions**: 3 outfit combinations tailored to your preferences

## Using the Python API

### Direct Script Usage

```python
from color_analyzer import analyze_color

# Analyze an image
result = analyze_color("path/to/selfie.jpg", style="subtle", formality="casual")

print(f"Undertone: {result['undertone']}")
print(f"Colors: {result['colors']}")
print(f"Outfits: {result['outfits']}")
```

### HTTP API Usage

#### Analyze Endpoint

**Endpoint**: `POST /analyze`

**Parameters**:
- `image` (file): The selfie image to analyze
- `style` (form): "subtle" or "bold"
- `formality` (form): "casual" or "professional"

**Example with cURL**:
```bash
curl -X POST http://localhost:8000/analyze \
  -F "image=@selfie.jpg" \
  -F "style=subtle" \
  -F "formality=casual"
```

**Response**:
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

#### Health Check Endpoint

**Endpoint**: `GET /health`

**Response**:
```json
{
  "status": "healthy"
}
```

## Tips for Best Results

1. **Use clear, well-lit photos**: Natural lighting works best
2. **Face should be clearly visible**: Avoid shadows or filters
3. **Try different combinations**: Experiment with style and formality options
4. **Save your favorite colors**: Note down the hex codes for future reference

## Troubleshooting

### Server won't start
- Ensure all dependencies are installed: `pip install -r requirements.txt`
- Check if port 8000 is already in use
- Try running on a different port: `uvicorn app:app --host 0.0.0.0 --port 8080`

### Image upload fails
- Ensure the image is in a supported format (JPEG, PNG)
- Check that the image file is not corrupted
- Verify the file size is reasonable (< 10MB recommended)

### No skin detected
- Use a clearer photo with better lighting
- Ensure your face is visible in the image
- Try a different photo

## Advanced Usage

### Running in Production

For production deployment, consider:

1. **Use a production WSGI server**: Gunicorn or similar
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker app:app
```

2. **Configure CORS properly**: Update `allow_origins` in `app.py` with your domain
```python
allow_origins=["https://yourdomain.com"]
```

3. **Use HTTPS**: Set up SSL certificates
4. **Add authentication**: Protect the API endpoints if needed
5. **Set up monitoring**: Use the `/health` endpoint for health checks

### Customizing Color Palettes

To add or modify color palettes, edit the `get_color_palette()` function in `color_analyzer.py`:

```python
palettes = {
    "warm": {
        "subtle": [
            {"name": "Your Color", "hex": "#HEXCODE"},
            # Add more colors
        ]
    }
}
```

### Customizing Outfit Suggestions

To modify outfit suggestions, edit the `get_outfit_suggestions()` function in `color_analyzer.py`:

```python
suggestions = {
    "warm": {
        "casual": {
            "subtle": [
                "Your custom outfit suggestion",
                # Add more suggestions
            ]
        }
    }
}
```
