# 🎸 Quick Start Guide

## 5-Minute Setup

### Prerequisites
- Python 3.8+ installed ([Download Python](https://www.python.org/downloads/))
- Git installed ([Download Git](https://git-scm.com/))
- A working microphone

### Installation

**Step 1: Clone the repository**
```bash
git clone https://github.com/vctmasters1/Guitar-Tuner-WEB.git
cd Guitar-Tuner-WEB
```

**Step 2: Create virtual environment (optional but recommended)**
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

**Step 3: Install dependencies**
```bash
pip install -r requirements.txt
```

**Step 4: Run the app**
```bash
streamlit run app.py
```

**Step 5: Open in browser**
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
| "Microphone not working" | Check browser permissions, refresh page |
| "No frequency detected" | Ensure quiet environment, play louder |
| "Python not found" | [Install Python](https://www.python.org/downloads/) and add to PATH |
| "Module not found" | Run `pip install -r requirements.txt` |
| "Port already in use" | Run `streamlit run app.py --server.port=8502` |

---

## Next Steps

- ✅ Tune your guitar!
- 📖 Read [README.md](README.md) for detailed features
- 🚀 Deploy to [Streamlit Cloud](DEPLOYMENT.md)
- 🤝 Contribute improvements

---

**Questions?** Open an issue on GitHub or check [README.md](README.md)

Happy tuning! 🎸🎵
