# AI Personal Stylist & Color Consultant

![Python](https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![OpenCV](https://img.shields.io/badge/Computer_Vision-OpenCV-5C3EE8?style=for-the-badge&logo=opencv&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Enabled-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![MediaPipe](https://img.shields.io/badge/MediaPipe-Face_Mesh-FFA500?style=for-the-badge&logo=google&logoColor=white)

**Live Demo:** [Insert Your Render URL Here]

![Project Demo](demo.png)
_(A computer vision powered application that determines seasonal color palettes and curates capsule wardrobes)_

## Overview

A professional-grade **Virtual Color Analysis Engine** that utilizes computer vision to determine a user's seasonal color palette. Unlike simple color pickers, this application uses **Google MediaPipe's Face Mesh** technology to perform dermatological skin depth analysis, classifying users into specific sub-seasons (e.g., "Deep Autumn," "Light Summer") based on Lab color space metrics.

The system synthesizes biological features with user inputs to generate a personalized "Capsule Wardrobe"—a curated shopping list of fabrics, metals, and colors tailored to the user's unique phenotype.

## Key Technical Features

- **Geometric Face Segmentation**: Utilizes **MediaPipe** to map 468 3D facial landmarks, isolating specific cheek regions (ROI) for color extraction while ignoring lighting artifacts, shadows, and facial hair.
- **5-Tier Skin Depth Algorithm**: Moves beyond binary "Warm/Cool" logic by implementing a custom algorithm that analyzes the **L-channel** (Lab color space) to classify skin depth into Fair, Light, Medium, Tan, or Deep tiers.
- **Smart Seasonal Logic**: A decision tree that synthesizes biological data (Skin Undertone + Depth) with user inputs (Contrast features) to determine the precise seasonal classification.
- **Robust Image Processing**: Full support for high-efficiency formats (iPhone **.HEIC**) and automatic image normalization using `Pillow-HEIF` and `NumPy`.
- **Capsule Wardrobe Engine**: Dynamic database that serves specific shopping recommendations (Fabrics, Metals, Colors) based on the calculated sub-season.

## 🛠 Tech Stack

| Component           | Technology         | Description                                                         |
| :------------------ | :----------------- | :------------------------------------------------------------------ |
| **Backend**         | FastAPI (Python)   | High-performance async REST API                                     |
| **CV Engine**       | OpenCV & MediaPipe | Facial landmark detection & color space conversion                  |
| **Data Processing** | NumPy              | Matrix operations for pixel averaging and masking                   |
| **Frontend**        | Vanilla JS & CSS   | Lightweight, dependency-free frontend with dynamic DOM manipulation |
| **Deployment**      | Docker             | Containerized environment for consistent CV dependencies            |

## How It Works

1.  **Preprocessing**: User uploads an image (JPG, PNG, HEIC). The backend standardizes the resolution and converts color spaces (BGR to RGB).
2.  **Landmark Detection**: The AI constructs a 3D wireframe of the face.
3.  **Region of Interest (ROI) Masking**: The algorithm mathematically defines a polygon on the user's cheek using specific landmark indices (Points 330, 347, etc.) to extract the purest skin tone.
4.  **Lab Color Analysis**:
    - **b-channel** determines Undertone (Warm vs Cool).
    - **L-channel** determines Depth (Fair to Deep).
5.  **Seasonal Classification**: The system correlates the CV data with user-provided contrast data (Hair/Eye color) to assign a Season.
6.  **Response Generation**: The API returns a tailored JSON object containing Hex palettes, "Avoid" lists, and specific clothing item recommendations.

## 🐳 Installation & Usage

This project uses **Docker** to manage complex Computer Vision dependencies (OpenCV/GL libraries). This is the recommended way to run the application.

### Option 1: Docker (Recommended)

1.  **Build the Container:**

    ```bash
    docker build -t color-stylist .
    ```

2.  **Run the Application:**

    ```bash
    docker run -p 8000:8000 color-stylist
    ```

3.  **Access the App:**
    Open your browser to `http://localhost:8000`

### Option 2: Local Python Environment

If you prefer running locally without Docker:

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/kylehtet/color-analyzer.git](https://github.com/kylehtet/color-analyzer.git)
    cd color-analyzer
    ```

2.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

3.  **Start the server:**
    ```bash
    python app.py
    ```

## 🔌 API Documentation

### `POST /analyze`

Analyzes an uploaded image and user features to return color/wardrobe recommendations.

**Parameters:**

- `image` (file): The selfie image to analyze (.jpg, .png, .heic)
- `hair` (string): User's hair color (e.g., "black", "blonde", "red")
- `eye` (string): User's eye color (e.g., "dark", "blue", "hazel")

**Response Example:**

```json
{
  "success": true,
  "season": "Deep Autumn",
  "undertone": "warm",
  "description": "You are a Deep Autumn. Your deep complexion allows you to...",
  "colors": [
    { "name": "Color", "hex": "#808000" },
    { "name": "Color", "hex": "#B7410E" }
  ],
  "wardrobe": [
    {
      "item": "Leather Jacket",
      "desc": "Espresso leather looks incredibly sleek.",
      "color": "Dark Chocolate"
    }
  ]
}
```
