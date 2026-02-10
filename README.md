# 🎸 Guitar Tuner - Web App

A modern, real-time guitar tuner web application built with **Streamlit**. Easily accessible from any browser, perfect for sharing live on GitHub Pages or deploying to cloud platforms.

## ✨ Features

- **Real-time Frequency Detection**: Uses FFT (Fast Fourier Transform) to analyze audio input from your microphone
- **Visual Feedback**: 
  - Frequency spectrum visualization
  - Tuner gauge showing cents deviation
  - Color-coded string status indicators (Green = In Tune, Yellow = Close, Red = Off)
- **Multiple Tuning References**: 432 Hz, 440 Hz, 442 Hz, 444 Hz, or custom frequency
- **Temperament Systems**:
  - Equal Temperament (12-TET) - Standard tuning
  - Just Intonation - Harmonic tuning
- **Adjustable Tolerance**: Fine-tune the sensitivity of the tuner
- **No Installation Required**: Works directly in your web browser
- **Mobile Friendly**: Can be used on tablets and mobile devices with microphone access

## 🚀 Quick Start

### Option 1: Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/vctmasters1/Guitar-Tuner-WEB.git
   cd Guitar-Tuner-WEB
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the app:**
   ```bash
   streamlit run app.py
   ```

4. **Open in browser:**
   The app will automatically open at `http://localhost:8501`

### Option 2: Deploy Online (Recommended for GitHub Sharing)

#### Deploy to Streamlit Cloud (Free & Easy)

1. Fork this repository on GitHub
2. Go to [Streamlit Cloud](https://streamlit.io/cloud)
3. Sign in with your GitHub account
4. Click "New app"
5. Select your forked repository
6. Choose the branch and file: `app.py`
7. Click "Deploy"

Your app will be live at: `https://<username>-guitar-tuner-web.streamlit.app`

#### Deploy to Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --logger.level=error
   ```

2. Create a `.streamlit/config.toml`:
   ```toml
   [server]
   headless = true
   port = $PORT
   enableCORS = false
   
   [client]
   showErrorDetails = false
   ```

3. Deploy:
   ```bash
   git push heroku main
   ```

## 📖 How to Use

1. **Grant Microphone Access**: Click "Allow" when your browser asks for microphone permission
2. **Configure Settings**:
   - Select or enter your reference tuning frequency
   - Choose temperament system (Equal or Just Intonation)
   - Adjust tolerance as needed
3. **Tune Your Guitar**:
   - Pluck one string at a time
   - Watch the real-time feedback:
     - **Green ✓** = String is in tune
     - **Yellow ~** = String is close
     - **Red ✗** = String needs adjustment
   - Adjust the string until it shows green
4. **Repeat** for all 6 strings

## 🎛️ Settings Explained

- **Tuning Reference (Hz)**: The frequency standard (440 Hz is standard A4)
- **Temperament System**: Musical scale system for frequency calculation
  - Equal Temperament: Standard Western music
  - Just Intonation: Pure harmonic ratios
- **Tolerance (Hz)**: How strict the "in tune" detection should be

## 🛠️ Technical Details

### How It Works

1. **Audio Capture**: Records audio from your microphone using WebRTC
2. **FFT Analysis**: Applies Fast Fourier Transform to detect the fundamental frequency
3. **String Recognition**: Matches detected frequency to the closest guitar string
4. **Cents Calculation**: Shows deviation from target in cents (100 cents = 1 semitone)
5. **Visual Display**: Real-time charts and indicators for feedback

### Architecture

```
Guitar-Tuner-WEB/
├── app.py                 # Main Streamlit application
├── src/
│   ├── core/
│   │   ├── config.py     # Configuration constants
│   │   └── tuner.py      # Core tuning logic
│   └── audio/
│       └── capture.py    # Audio processing & FFT
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 📦 Dependencies

- **Streamlit**: Web framework
- **Streamlit-WebRTC**: Real-time audio capture
- **NumPy & SciPy**: Audio signal processing
- **Plotly**: Interactive charts

## 🎓 Guitar String Frequencies (E Standard Tuning)

| String | Note | Frequency (Hz) |
|--------|------|---|
| E (6) | E2 | 82.41 |
| A (5) | A2 | 110.00 |
| D (4) | D3 | 146.83 |
| G (3) | G3 | 196.00 |
| B (2) | B3 | 246.94 |
| E (1) | E4 | 329.63 |

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| No microphone input | Check browser permissions, grant microphone access |
| Wrong frequency detected | Ensure only one string is playing, reduce background noise |
| Detection lag | Check internet connection, ensure sufficient system resources |
| App crashes | Refresh the page, check browser console for errors |

## 🤝 Contributing

Found a bug? Have an improvement idea?

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the MIT License.

## 📧 Support

Need help? Create an issue on GitHub or contact the maintainers.

---

**Made with ❤️ for guitarists everywhere** 🎸
