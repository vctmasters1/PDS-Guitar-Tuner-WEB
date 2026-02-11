# 🎸 Guitar Tuner - Web App

[![GitHub Pages](https://img.shields.io/badge/Live-GitHub%20Pages-brightgreen)](https://vctmasters1.github.io/PDS-Guitar-Tuner-WEB/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-blue)]()

A real-time guitar tuner that runs entirely in your browser. **No installation, no server, no dependencies** - just open and tune!

## 🎵 Try It Now

**[Open Guitar Tuner](https://vctmasters1.github.io/PDS-Guitar-Tuner-WEB/)** ← Click to use immediately!

Or download `index.html` and open it directly in your browser.

## ⚡ Quick Start

### Option 1: Use Online (Recommended)
Click the link above. That's it!

### Option 2: Run Locally
1. Download or clone this repository
2. Open `index.html` in any modern browser
3. Done!

```bash
git clone https://github.com/vctmasters1/Guitar-Tuner-WEB.git
cd Guitar-Tuner-WEB
# Open index.html in your browser - no build step needed!
```

## 🎯 How to Use

1. **Open the app** in your browser
2. **Click "Start Microphone"** and grant permission
3. **Pluck a guitar string**
4. **Watch the visual feedback:**
   - 🟢 **Green** = In tune (±5 cents)
   - 🟠 **Orange** = Close (±15 cents)
   - 🔴 **Red** = Needs adjustment
5. **Adjust until the needle is centered**
6. **Repeat for all 6 strings**

## ✨ Features

- **Real-time Pitch Detection** - Uses Web Audio API autocorrelation
- **Visual Tuning Gauges** - Individual needle for each string
- **Interactive Piano** - Click keys to hear reference tones
- **Multiple Reference Frequencies** - 432/440/442/444 Hz
- **Adjustable Sensitivity** - dB threshold slider
- **Mobile Friendly** - Responsive design works on all devices
- **Fully Offline** - Works without internet after loading
- **Zero Dependencies** - Pure HTML/CSS/JavaScript

## 📊 Display Features

| Feature | Description |
|---------|-------------|
| **Hz Display** | Real-time detected frequency |
| **dB Level** | Input volume meter |
| **String Gauges** | Visual cents deviation for each string |
| **Piano Keyboard** | Interactive vertical keyboard (D2-A4) |
| **Status Indicators** | IN TUNE / CLOSE / FLAT / SHARP |

## 🎛️ Settings

### Reference Frequency
- 432 Hz
- 440 Hz (Standard - default)
- 442 Hz
- 444 Hz

### Sensitivity
Adjust the dB threshold (-60 to -20 dB) to filter out background noise.

## 🎸 Guitar Strings

| String | Note | Frequency (440 Hz ref) |
|--------|------|------------------------|
| 6 (thickest) | E2 | 82.41 Hz |
| 5 | A2 | 110.00 Hz |
| 4 | D3 | 146.83 Hz |
| 3 | G3 | 196.00 Hz |
| 2 | B3 | 246.94 Hz |
| 1 (thinnest) | E4 | 329.63 Hz |

## 🔧 Technical Details

### How It Works
1. **Microphone Access** - Uses `navigator.mediaDevices.getUserMedia()`
2. **Audio Analysis** - Web Audio API `AnalyserNode` with 4096 FFT size
3. **Pitch Detection** - Autocorrelation algorithm finds fundamental frequency
4. **Harmonic Filtering** - Prevents octave jumps
5. **Visual Feedback** - Updates at 10Hz (100ms intervals)

### Formula
All frequencies calculated using Equal Temperament (12-TET):
```
frequency = reference_freq × 2^(semitones_from_A4 / 12)
```

### Browser Support
- Chrome/Edge: ✅ Full support
- Firefox: ✅ Full support
- Safari: ✅ Full support (iOS 14.5+)

**Note:** HTTPS is required for microphone access. GitHub Pages provides this automatically.

## 📁 Project Structure

```
Guitar-Tuner-WEB/
├── index.html          # HTML structure
├── css/
│   └── styles.css      # All styling
├── js/
│   ├── config.js       # Configuration & constants
│   ├── audio.js        # Web Audio API & pitch detection
│   ├── ui.js           # UI rendering
│   └── app.js          # Main initialization
├── README.md           # This file
└── LICENSE             # MIT License
```

Industry-standard separation of concerns:

## 🚀 Deployment

### GitHub Pages (Free Hosting)
1. Push `index.html` to your repository
2. Go to **Settings** → **Pages**
3. Source: **Deploy from a branch**
4. Branch: **master**, Folder: **/ (root)**
5. Your app is live at `https://<username>.github.io/<repo>/`

### Any Static Host
Just upload `index.html` to any web server. No configuration needed.

## 📄 License

MIT License - See [LICENSE](LICENSE) for details.

## 🤝 Contributing

1. Fork the repository
2. Make your changes to `index.html`
3. Test locally by opening in browser
4. Submit a pull request

Keep everything in the single `index.html` file unless there's a specific reason to split.
