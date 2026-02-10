# 🚀 Deployment Guide

This guide shows how to deploy the Guitar Tuner web app online so you can share it with others.

## Option 1: Streamlit Cloud (Easiest - FREE)

### Step-by-Step

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Initial commit: Guitar Tuner Web App"
   git push origin main
   ```

2. **Go to Streamlit Cloud:**
   - Visit https://streamlit.io/cloud
   - Click "Sign in" and authenticate with GitHub

3. **Deploy Your App:**
   - Click "New app"
   - Select your repository and branch
   - Specify the main file: `app.py`
   - Click "Deploy"

4. **Share Your Link:**
   - Your app will be live at `https://<username>-guitar-tuner-web.streamlit.app`
   - Share this URL with anyone to use your tuner!

### Features:
- ✅ Free hosting
- ✅ Automatic updates when you push to GitHub
- ✅ Custom domain support (paid)
- ✅ SSL/HTTPS by default
- ✅ Scales automatically

---

## Option 2: GitHub Pages (Static Site Alternative)

If you want to use GitHub Pages, you'll need to build a React version. For now, Streamlit Cloud is recommended.

---

## Option 3: Heroku Deployment

### Step-by-Step

1. **Install Heroku CLI:**
   ```bash
   # Windows (via Chocolatey)
   choco install heroku-cli
   
   # Or download from https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Create Heroku App:**
   ```bash
   heroku login
   heroku create your-guitar-tuner
   ```

3. **Configure Procfile** (already created in repo):
   ```
   web: streamlit run app.py --logger.level=error
   ```

4. **Configure Streamlit** (already created):
   Create `.streamlit/config.toml` with server settings for Heroku

5. **Deploy:**
   ```bash
   git push heroku main
   ```

6. **View Logs:**
   ```bash
   heroku logs --tail
   ```

### Cost:
- Free tier available (with limitations)
- Paid plans start at $7/month

---

## Option 4: Docker (Advanced)

### Create Dockerfile:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Build and Run:
```bash
docker build -t guitar-tuner .
docker run -p 8501:8501 guitar-tuner
```

---

## Comparing Deployment Options

| Option | Cost | Ease | Cold Start | Custom Domain |
|--------|------|------|-----------|---------------|
| Streamlit Cloud | FREE | ⭐⭐⭐⭐⭐ | <2s | Paid |
| Heroku | FREE tier | ⭐⭐⭐⭐ | ~30s | Included |
| Docker (DigitalOcean) | $5-12/month | ⭐⭐⭐ | <5s | Yes |
| AWS/Azure | Varies | ⭐⭐ | Variable | Yes |

---

## Troubleshooting Deployment

### App won't load
- Check that all files are in GitHub
- Verify `requirements.txt` has all dependencies
- Check Streamlit Cloud logs

### Microphone not working
- Only works with HTTPS (Streamlit Cloud provides this)
- Browser must have microphone permission
- Check browser console for errors (F12)

### Performance issues
- Streamlit Cloud handles scaling automatically
- If needed, upgrade Streamlit Cloud tier

---

## Sharing Your App

Once deployed, share the URL:
- 📱 Works on desktop, tablet, and mobile
- 🔗 No installation required
- 👥 Anyone can use it with a link

### Share on Social Media:
```
Check out my Guitar Tuner Web App! 🎸
[Your App URL]
No installation needed - just open and tune!
```

---

## Next Steps

1. ✅ Deploy to Streamlit Cloud
2. Test microphone permissions
3. Share with friends
4. Gather feedback
5. Consider enhancements (see ROADMAP.md)

Happy tuning! 🎸
