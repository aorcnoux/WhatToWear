# WhatToWear: Interactive Style Recommendation System

## 📖 Overview
WhatToWear is a Python-based interactive desktop application designed to solve the daily dilemma of choosing an outfit. By integrating real-time regional weather data with user-defined styling preferences, the system autonomously generates dynamic clothing combinations and color palette recommendations. 

This project demonstrates practical implementations of API consumption, GUI development, state management, algorithmic image compositing, and structured data handling.

## ✨ Key Features
* **Real-Time Weather Integration:** Fetches live meteorological data (temperature and conditions) via the Central Weather Administration (CWA) Open Data API.
* **Algorithmic 'Paper Doll' Compositing:** Utilizes dynamic alpha-compositing to overlay transparent clothing layers (shoes, bottoms, tops, outerwear, accessories) onto base models.
* **Smart Filtering System:** Categorizes and filters clothing assets through conditional logic driven by datasets (`outfits.csv`), considering gender, style preference (Casual, Formal, Sporty), and dynamic temperature readings.
* **Interactive UI & Audio:** Features a retro pixel-art inspired graphical user interface built with Tkinter, complete with interactive state toggles and asynchronous background audio managed by Pygame.

## 🛠️ Technology Stack
* **Language:** Python 3.x
* **GUI Framework:** Tkinter (`ttk`)
* **Image Processing:** Pillow (`PIL`) for RGBA image manipulation
* **API & Networking:** `requests`, `certifi` (SSL verification)
* **Audio Management:** `pygame` (Mixer)
* **Data Management:** `csv` module for structured outfit database
* **Environment Management:** `python-dotenv`

## 📂 Project Architecture

```text
what-to-wear/
├── main.py                # Core application logic and GUI loop
├── requirements.txt       # Project dependencies list
├── .env.example           # Template for environment variables (API Key)
├── .gitignore             # Git ignore rules for security and clean repo
├── data/                  # Structured datasets
│   ├── outfits.csv        # Core database mapping styles/weather to garments
│   ├── outfits_edit.csv   # Edited/working outfit dataset
│   └── weather.csv        # Historical/fallback weather data
├── clothes/               # Hierarchical database of clothing assets (.png)
│   ├── male/
│   └── female/
│       ├── Casual/
│       ├── Formal/
│       └── Sporty/
├── models/                # Base character models (male.png, female.png)
├── assets/                # UI images and audio files (BGM1.mp3, outfit.ico)
└── README.md              # Project documentation
```

## 🚀 Installation & Setup

Follow these steps to configure the development environment and run the application locally.

### 1. Prerequisites
* **Python 3.8+**: Ensure you have Python installed. You can check your version by running `python --version`.
* **CWA API Key**: A valid API key from the [Central Weather Administration (Taiwan)](https://opendata.cwa.gov.tw/) is required for real-time data fetching.

### 2. Clone the Repository
Clone the project to your local machine:
```bash
git clone [https://github.com/aorcnoux/what-to-wear.git](https://github.com/yourusername/what-to-wear.git)
cd what-to-wear
```

### 3. Set Up a Virtual Environment (Recommended)
This keeps the project dependencies isolated from your global Python installation.
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
Install all required libraries using the requirements.txt file:
```bash
pip install -r requirements.txt
```

### 5. Configure API Credentials

The application requires a private API key to fetch real-time weather data.
1. Locate the .env.example file in the root directory.
2. Rename or copy it to a new file named .env:
```bash
cp .env.example .env
```
3. Open .env and replace your_api_key_here with your actual CWA API Key.

### 6. Run the Application
```bash
python main.py
```

## 📺 Demo Video
Click the image below to watch the project demonstration:

[![Watch the video](https://img.youtube.com/vi/gGs7MIDn7mw/0.jpg)](https://youtu.be/gGs7MIDn7mw)

> *The system demonstrates real-time weather fetching and dynamic outfit layering.*
