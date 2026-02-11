# 🎸 Quick Start Guide

## 🚀 Fastest Setup (Recommended)

We provide automated setup scripts for your convenience.

### Prerequisites
- Python 3.9+ installed ([Download Python](https://www.python.org/downloads/))
- A working microphone

### Automated Setup

**Windows (PowerShell):**
```powershell
.\setup.ps1
```

**macOS/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

**Cross-platform (Python):**
```bash
python setup.py
```

The script will:
- ✓ Create a virtual environment
- ✓ Install all dependencies
- ✓ Verify the installation
- ✓ Check your project structure

Once complete, it will show you how to activate the environment and run the app.

---

## 📖 Manual Setup (If Scripts Don't Work)

If you prefer manual setup or the scripts encounter issues:

**Step 1: Create virtual environment**
```bash
# Windows
python -m venv .venv
.venv\Scripts\activate

# Mac/Linux
python3 -m venv .venv
source .venv/bin/activate
```

**Step 2: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 3: Run the app**
```bash
streamlit run app.py
```

**Step 4: Open in browser**
- Your browser will automatically open to `http://localhost:8501`
- If not, manually navigate to that address

---

## Using the App

1. **Grant Microphone Access**: Click "Allow" when prompted
2. **Choose Tuning**: Select your reference frequency (default: 440 Hz)
3. **Play a String**: Pluck a guitar string
4. **Watch the Feedback**: 
   - Green ✓ = In tune
   - Yellow ~ = Close
   - Red ✗ = Needs adjustment
5. **Tune**: Adjust until green
6. **Repeat** for all 6 strings

---

## Deploy Online (Optional)

Want to share with others without them installing anything?

**Best Option: Streamlit Cloud (FREE)**

1. Fork this repo on GitHub
2. Go to https://streamlit.io/cloud
3. Sign in with GitHub
4. Click "New app"
5. Select your fork and click "Deploy"
6. Share the generated URL!

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment options.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Script won't run | See [SETUP_GUIDE.md](SETUP_GUIDE.md) for detailed instructions |
| "Microphone not working" | Check browser permissions, refresh page, try different browser |
| "No frequency detected" | Ensure quiet environment, play louder/closer to mic |
| "Python not found" | [Install Python 3.9+](https://www.python.org/downloads/) and add to PATH |
| "Module not found" | Run `pip install -r requirements.txt` with venv activated |
| "Port already in use" | Run `streamlit run app.py --server.port=8502` |

**Need more help?** Check [SETUP_GUIDE.md](SETUP_GUIDE.md) for comprehensive troubleshooting.

---

## Next Steps

- 🎸 Tune your guitar!
- 📖 Read [README.md](README.md) for detailed features
- 📚 Full setup help: [SETUP_GUIDE.md](SETUP_GUIDE.md)
- 🏗️ Architecture details: [AI-Instruct.md](AI-Instruct.md)
- 🚀 Deploy online: [DEPLOYMENT.md](DEPLOYMENT.md)
- 🤝 Contribute: [CONTRIBUTING.md](CONTRIBUTING.md)

---

**Questions?** Check [SETUP_GUIDE.md](SETUP_GUIDE.md) or open an issue on GitHub.

Happy tuning! 🎸🎵
