# 🎸 Guitar Tuner - Web App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://guitar-tuner-web.streamlit.app)
[![GitHub](https://img.shields.io/badge/GitHub-vctmasters1-blue?logo=github)](https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

> **🎵 Try it now:** [Live Demo](https://guitar-tuner-web.streamlit.app)

A real-time guitar tuner web application built with Streamlit. No installation required - just open in your browser!

## ⚡ Quick Start

### Option 1: Use Online (Recommended)
🌐 **[Click here to use the live app](https://guitar-tuner-web.streamlit.app)** - Works on any device with a browser and microphone!

### Option 2: Run Locally (Windows - Easiest!)
After running the setup script once:

1. **Open PowerShell** and run setup:
   ```powershell
   .\setup.ps1
   ```

2. **From now on, just double-click** `run.bat` or `run.ps1` to start!
   - No terminal commands needed
   - Window stays open so you see any errors
   - Browser opens automatically

📖 **Full details:** See [RUN_GUIDE.md](RUN_GUIDE.md) for more options

### Option 3: Run Locally (macOS/Linux/Manual)
```bash
# Setup (one time)
chmod +x setup.sh
./setup.sh

# Run the app
streamlit run app.py
```

📖 **Full setup instructions:** See [SETUP_GUIDE.md](SETUP_GUIDE.md) or [QUICKSTART.md](QUICKSTART.md)

### Option 4: Clone & Manual Setup
```bash
git clone https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB.git
cd PDS-Guitar-Tuner-WEB
python -m venv .venv
# Activate virtual environment (see QUICKSTART.md)
pip install -r requirements.txt
streamlit run app.py
```

## 🎯 How to Use

1. Open the [live app](https://guitar-tuner-web.streamlit.app)
2. **Grant microphone permission** when prompted
3. **Select your tuning reference** (or use default 440 Hz)
4. **Pluck a guitar string**
5. **Watch the live feedback:**
   - 🟢 **Green** = In tune
   - 🟡 **Yellow** = Close
   - 🔴 **Red** = Needs adjustment
6. **Tune until green**
7. **Repeat for all 6 strings**

## ✨ Features

- **Real-time Frequency Detection** - Uses FFT to analyze audio
- **Visual Indicators** - Color-coded feedback and interactive charts
- **Multiple Tuning References** - 432/440/442/444 Hz or custom
- **Temperament Systems** - Equal Temperament & Just Intonation
- **Mobile Friendly** - Works on phones, tablets, and desktops
- **No Installation** - Web-based, runs in any browser
- **Zero Cost** - Free and open source

## 📊 Display Features

| Feature | Description |
|---------|-------------|
| **Frequency Spectrum** | Real-time FFT visualization |
| **Tuner Gauge** | Visual accuracy indicator showing cents deviation |
| **String Status** | Color-coded indicators for all 6 guitar strings |
| **Live Metrics** | Detected frequency, current string, target frequency |
| **Settings Panel** | Adjust reference frequency and temperament on the fly |

## 🎛️ Customization

### Available Tuning References
- 432 Hz (Verdi tuning)
- 440 Hz (Standard A4)
- 442 Hz
- 444 Hz
- Custom frequency (400-460 Hz range)

### Temperament Systems
- **Equal Temperament (12-TET)** - Standard Western music
- **Just Intonation** - Pure harmonic ratios

### Adjustable Settings
- Tuning tolerance (0.1 - 5.0 Hz)
- Reference frequency customization

## 🛠️ Technical Stack

- **Frontend**: Streamlit + Plotly
- **Audio Processing**: NumPy, SciPy (FFT analysis)
- **Real-time Audio**: Streamlit-WebRTC
- **Deployment**: Streamlit Cloud (free)

## 📦 Installation (Local Development)

### Requirements
- Python 3.8+
- Microphone
- Modern web browser

### Setup

```bash
# Clone repository
git clone https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB.git
cd PDS-Guitar-Tuner-WEB

# Create virtual environment (optional)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run application
streamlit run app.py
```

App will open at `http://localhost:8501`

## 🚀 Deployment

### Deploy to Streamlit Cloud (Free & Easy)

1. Fork the repository on GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with GitHub
4. Click "New app" → Select your fork
5. Done! Your app is live

**See [DEPLOYMENT.md](DEPLOYMENT.md) for more options:**
- Heroku (free tier)
- Docker
- AWS/Azure
- Custom server

## 📖 Documentation

- **[QUICKSTART.md](QUICKSTART.md)** - Get running in 5 minutes
- **[DEPLOYMENT.md](DEPLOYMENT.md)** - Deploy online
- **[README.md](README.md)** - Full documentation

## 🎓 How It Works

1. **Audio Capture** - Records audio via your microphone (WebRTC)
2. **FFT Analysis** - Fast Fourier Transform to detect fundamental frequency
3. **String Recognition** - Matches frequency to closest guitar string
4. **Cents Calculation** - Shows deviation from perfect pitch
5. **Visual Feedback** - Real-time displays for tuning guidance

### Guitar String Frequencies (E Standard Tuning @ 440 Hz)

| String | Note | Frequency |
|--------|------|-----------|
| E (6) | E2 | 82.41 Hz |
| A (5) | A2 | 110.00 Hz |
| D (4) | D3 | 146.83 Hz |
| G (3) | G3 | 196.00 Hz |
| B (2) | B3 | 246.94 Hz |
| E (1) | E4 | 329.63 Hz |

## 🆘 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Microphone not working** | Check browser permissions, use HTTPS (live app uses HTTPS automatically) |
| **Wrong frequency detected** | Ensure quiet environment, play one string at a time |
| **Detection lag** | Check internet connection, close other browser tabs |
| **Can't find app online** | Visit [guitar-tuner-web.streamlit.app](https://guitar-tuner-web.streamlit.app) |
| **Local app won't start** | Run `pip install -r requirements.txt` again |

## 📁 Project Structure

```
PDS-Guitar-Tuner-WEB/
├── app.py                 # Main Streamlit app
├── requirements.txt       # Dependencies
├── README.md             # This file
├── QUICKSTART.md         # Quick setup guide
├── DEPLOYMENT.md         # Deployment options
├── Procfile              # Heroku config
├── .gitignore           # Git ignore rules
├── .streamlit/
│   └── config.toml      # Streamlit theme config
└── src/
    ├── core/
    │   ├── config.py     # Configuration
    │   └── tuner.py      # Tuning logic
    └── audio/
        └── capture.py    # Audio FFT analysis
```

## 🤝 Contributing

Found a bug? Have a feature idea? 

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/awesome-feature`)
3. Commit changes (`git commit -m 'Add awesome feature'`)
4. Push to branch (`git push origin feature/awesome-feature`)
5. Open a Pull Request

## 📜 License

MIT License - feel free to use this project for any purpose!

## 🎵 Support

Need help?
- 📖 Check [QUICKSTART.md](QUICKSTART.md)
- 🚀 See [DEPLOYMENT.md](DEPLOYMENT.md) for setup help
- 🐛 Open an [Issue](https://github.com/vctmasters1/PDS-Guitar-Tuner-WEB/issues)

---

**Made with ❤️ for guitarists everywhere** 🎸

### Try it now: [guitar-tuner-web.streamlit.app](https://guitar-tuner-web.streamlit.app)
