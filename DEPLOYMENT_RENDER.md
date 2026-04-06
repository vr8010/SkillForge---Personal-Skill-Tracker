# 🚀 Deploy SkillForge Backend to Render

## Overview

This guide will help you deploy the SkillForge Flask backend API to Render.com (free tier).

## Prerequisites

- GitHub account
- Render account (sign up at https://render.com)
- Your SkillForge repository pushed to GitHub

## Step-by-Step Deployment

### Step 1: Prepare Your Repository

✅ Already done! Your repository includes:
- `app.py` - Flask application
- `requirements.txt` - Python dependencies (including gunicorn)
- `runtime.txt` - Python version specification
- `render.yaml` - Render configuration

### Step 2: Sign Up for Render

1. Go to https://render.com
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your repositories

### Step 3: Create New Web Service

1. **Dashboard**: Click "New +" button
2. **Select**: Choose "Web Service"
3. **Connect Repository**:
   - Find "SkillForge---Personal-Skill-Tracker"
   - Click "Connect"

### Step 4: Configure Service

Fill in the following settings:

**Basic Settings:**
- **Name**: `skillforge-api` (or your preferred name)
- **Region**: Choose closest to you (e.g., Oregon)
- **Branch**: `main`
- **Root Directory**: Leave empty
- **Runtime**: `Python 3`

**Build Settings:**
- **Build Command**: 
  ```bash
  pip install -r requirements.txt
  ```

**Start Command**:
```bash
gunicorn app:app
```

**Instance Type:**
- Select **Free** (0.1 CPU, 512 MB RAM)

### Step 5: Environment Variables

Add these environment variables:

| Key | Value |
|-----|-------|
| `PYTHON_VERSION` | `3.11.0` |
| `FLASK_ENV` | `production` |

### Step 6: Deploy

1. Click "Create Web Service"
2. Wait for deployment (5-10 minutes)
3. Watch the logs for any errors

### Step 7: Get Your API URL

Once deployed, you'll get a URL like:
```
https://skillforge-api.onrender.com
```

Your API endpoints will be:
```
https://skillforge-api.onrender.com/api/skills
https://skillforge-api.onrender.com/api/statistics
etc.
```

## Testing Your Deployment

### Test API Endpoints

1. **Get Statistics**:
   ```bash
   curl https://your-app-name.onrender.com/api/statistics
   ```

2. **Get Skills**:
   ```bash
   curl https://your-app-name.onrender.com/api/skills
   ```

3. **Add a Skill**:
   ```bash
   curl -X POST https://your-app-name.onrender.com/api/skills \
     -H "Content-Type: application/json" \
     -d '{
       "skill_type": "technical",
       "name": "Python",
       "category": "Programming",
       "difficulty": 7
     }'
   ```

### Expected Response

```json
{
  "success": true,
  "skills": [],
  "statistics": {...}
}
```

## Update Frontend Configuration

After deployment, update `static/config.js`:

```javascript
const API_CONFIG = {
    local: 'http://localhost:5000/api',
    production: 'https://YOUR-APP-NAME.onrender.com/api',  // ← Update this
    getBaseURL: function() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.local;
        }
        return this.production;
    }
};
```

## Important Notes

### Free Tier Limitations

⚠️ **Render Free Tier**:
- Spins down after 15 minutes of inactivity
- First request after spin-down takes 30-60 seconds
- 750 hours/month free (enough for one service)
- Automatic HTTPS included

### Data Persistence

⚠️ **Important**: Free tier has ephemeral storage
- Data resets when service restarts
- For persistent data, upgrade to paid tier or use external database

### Cold Starts

First request after inactivity will be slow:
- Show loading indicator in frontend
- Consider keeping service warm with cron job

## Troubleshooting

### Build Fails

**Problem**: Build command fails

**Solutions**:
1. Check `requirements.txt` is correct
2. Verify Python version in `runtime.txt`
3. Check build logs for specific errors

### Service Won't Start

**Problem**: Deploy succeeds but service crashes

**Solutions**:
1. Check logs in Render dashboard
2. Verify start command: `gunicorn app:app`
3. Ensure `app.py` has no syntax errors

### CORS Errors

**Problem**: Frontend can't connect to API

**Solutions**:
1. Check CORS configuration in `app.py`
2. Update allowed origins to include your Vercel domain
3. Verify API URL in `config.js`

### 404 Errors

**Problem**: API endpoints return 404

**Solutions**:
1. Verify URL includes `/api/` prefix
2. Check route definitions in `app.py`
3. Test with curl to isolate issue

## Monitoring

### View Logs

1. Go to Render dashboard
2. Click your service
3. Click "Logs" tab
4. Monitor real-time logs

### Check Status

- **Running**: Green indicator
- **Building**: Yellow indicator
- **Failed**: Red indicator

## Updating Your Deployment

### Automatic Deploys

Render automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update backend"
git push origin main
```

Render will:
1. Detect the push
2. Pull latest code
3. Rebuild and redeploy
4. Takes 5-10 minutes

### Manual Deploy

1. Go to Render dashboard
2. Click your service
3. Click "Manual Deploy"
4. Select branch
5. Click "Deploy"

## Custom Domain (Optional)

### Add Custom Domain

1. Go to service settings
2. Click "Custom Domains"
3. Add your domain
4. Update DNS records as instructed
5. Wait for SSL certificate (automatic)

## Scaling (Paid Plans)

### Upgrade Options

- **Starter**: $7/month - Persistent storage
- **Standard**: $25/month - More resources
- **Pro**: $85/month - High performance

## Security Best Practices

### Production Checklist

- [ ] Set `FLASK_ENV=production`
- [ ] Configure specific CORS origins
- [ ] Add rate limiting
- [ ] Use environment variables for secrets
- [ ] Enable HTTPS (automatic on Render)
- [ ] Monitor logs regularly

### Update CORS for Production

In `app.py`, update CORS configuration:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-vercel-app.vercel.app",
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

## Cost Optimization

### Keep Free Tier

- Use only one web service
- Accept cold starts
- No persistent data needed

### Upgrade When Needed

Upgrade if you need:
- Persistent storage
- No cold starts
- More resources
- Custom domain

## Support

### Render Documentation

- Docs: https://render.com/docs
- Status: https://status.render.com
- Community: https://community.render.com

### SkillForge Issues

- Check logs first
- Review this guide
- Test API endpoints with curl
- Verify configuration files

## Success Checklist

- [ ] Render account created
- [ ] Repository connected
- [ ] Service configured
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] API endpoints tested
- [ ] Frontend config updated
- [ ] CORS configured
- [ ] Logs monitored

## Next Steps

After backend is deployed:
1. ✅ Note your Render URL
2. ✅ Update `static/config.js`
3. ✅ Deploy frontend to Vercel (see DEPLOYMENT_VERCEL.md)
4. ✅ Test full application

---

**Deployment Time**: ~10 minutes  
**Cost**: Free (with limitations)  
**Difficulty**: ⭐⭐ (Easy)

🚀 **Your backend is now live on Render!**
