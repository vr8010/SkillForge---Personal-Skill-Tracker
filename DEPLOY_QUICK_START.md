# ⚡ Quick Deployment Guide

Deploy SkillForge to Render + Vercel in 15 minutes!

## 🎯 Overview

- **Backend**: Render (Flask API)
- **Frontend**: Vercel (Static Site)
- **Cost**: 100% Free
- **Time**: ~15 minutes

## 📋 Prerequisites

- [x] GitHub account
- [x] Code pushed to GitHub
- [x] Render account (https://render.com)
- [x] Vercel account (https://vercel.com)

## 🚀 Deployment Steps

### Part 1: Deploy Backend to Render (10 min)

1. **Sign up**: https://render.com → Sign up with GitHub

2. **New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your repository
   - Select "SkillForge---Personal-Skill-Tracker"

3. **Configure**:
   ```
   Name: skillforge-api
   Branch: main
   Build Command: pip install -r requirements.txt
   Start Command: gunicorn app:app
   Instance Type: Free
   ```

4. **Environment Variables**:
   ```
   PYTHON_VERSION = 3.11.0
   FLASK_ENV = production
   ```

5. **Deploy**: Click "Create Web Service"

6. **Get URL**: Copy your Render URL (e.g., `https://skillforge-api.onrender.com`)

### Part 2: Update Configuration (2 min)

1. **Update API URL** in `static/config.js`:
   ```javascript
   production: 'https://YOUR-RENDER-URL.onrender.com/api'
   ```

2. **Commit and push**:
   ```bash
   git add static/config.js
   git commit -m "Update API URL"
   git push origin main
   ```

### Part 3: Deploy Frontend to Vercel (3 min)

1. **Sign up**: https://vercel.com → Sign up with GitHub

2. **Import Project**:
   - Click "Add New..." → "Project"
   - Select "SkillForge---Personal-Skill-Tracker"
   - Click "Import"

3. **Configure**:
   ```
   Framework Preset: Other
   Root Directory: (leave empty)
   Build Command: (leave empty)
   Output Directory: static
   ```

4. **Deploy**: Click "Deploy"

5. **Get URL**: Copy your Vercel URL (e.g., `https://skillforge.vercel.app`)

### Part 4: Update CORS (2 min)

1. **Update** `app.py` CORS configuration:
   ```python
   CORS(app, resources={
       r"/api/*": {
           "origins": [
               "https://YOUR-VERCEL-URL.vercel.app",
               "http://localhost:5000"
           ]
       }
   })
   ```

2. **Commit and push**:
   ```bash
   git add app.py
   git commit -m "Update CORS"
   git push origin main
   ```

3. **Wait**: Render auto-deploys (2-3 minutes)

## ✅ Testing

1. **Open**: Your Vercel URL
2. **Add Skill**: Click "Add New Skill"
3. **Check**: Skills should save and load

## 🎉 Done!

Your app is live:
- **Frontend**: https://your-app.vercel.app
- **Backend**: https://your-app.onrender.com/api

## 📝 Important Notes

### Render Free Tier
- ⚠️ Spins down after 15 min inactivity
- ⚠️ First request takes 30-60 seconds
- ⚠️ Data resets on restart (ephemeral storage)

### Vercel Free Tier
- ✅ Always on
- ✅ Fast global CDN
- ✅ Automatic HTTPS

## 🐛 Troubleshooting

### Backend not responding
- Wait 60 seconds (cold start)
- Check Render logs
- Verify build succeeded

### CORS errors
- Update CORS in app.py
- Include your Vercel domain
- Push changes to GitHub

### Skills not saving
- Check browser console (F12)
- Verify API URL in config.js
- Test backend directly

## 📚 Detailed Guides

- Backend: See `DEPLOYMENT_RENDER.md`
- Frontend: See `DEPLOYMENT_VERCEL.md`

## 🔗 Useful Links

- **Render Dashboard**: https://dashboard.render.com
- **Vercel Dashboard**: https://vercel.com/dashboard
- **GitHub Repo**: Your repository URL

## 🎯 Next Steps

1. ✅ Test all features
2. ✅ Share your URL
3. ✅ Add custom domain (optional)
4. ✅ Monitor usage
5. ✅ Add to portfolio

---

**Total Time**: ~15 minutes  
**Total Cost**: $0 (Free)  
**Difficulty**: ⭐⭐ (Easy)

🚀 **Congratulations! Your app is deployed!**
