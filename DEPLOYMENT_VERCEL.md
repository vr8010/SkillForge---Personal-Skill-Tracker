# 🚀 Deploy SkillForge Frontend to Vercel

## Overview

This guide will help you deploy the SkillForge web frontend to Vercel (free tier).

## Prerequisites

- GitHub account
- Vercel account (sign up at https://vercel.com)
- Backend deployed to Render (see DEPLOYMENT_RENDER.md)
- Your SkillForge repository pushed to GitHub

## Step-by-Step Deployment

### Step 1: Update API Configuration

Before deploying, update `static/config.js` with your Render backend URL:

```javascript
const API_CONFIG = {
    local: 'http://localhost:5000/api',
    production: 'https://YOUR-RENDER-APP.onrender.com/api',  // ← Update this!
    getBaseURL: function() {
        if (window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1') {
            return this.local;
        }
        return this.production;
    }
};
```

**Commit and push this change:**
```bash
git add static/config.js
git commit -m "Update API URL for production"
git push origin main
```

### Step 2: Sign Up for Vercel

1. Go to https://vercel.com
2. Click "Sign Up"
3. Choose "Continue with GitHub" (recommended)
4. Authorize Vercel to access your repositories

### Step 3: Import Project

1. **Dashboard**: Click "Add New..." → "Project"
2. **Import Git Repository**:
   - Find "SkillForge---Personal-Skill-Tracker"
   - Click "Import"

### Step 4: Configure Project

**Framework Preset:**
- Select "Other" (we're using static files)

**Root Directory:**
- Leave as default (root)

**Build Settings:**
- **Build Command**: Leave empty (static site)
- **Output Directory**: `static`
- **Install Command**: Leave empty

### Step 5: Environment Variables

No environment variables needed for frontend!

### Step 6: Deploy

1. Click "Deploy"
2. Wait for deployment (1-2 minutes)
3. Watch the build logs

### Step 7: Get Your URL

Once deployed, you'll get a URL like:
```
https://skillforge-personal-skill-tracker.vercel.app
```

Or a custom domain if configured.

## Testing Your Deployment

### Open Your App

1. Click the deployment URL
2. You should see the SkillForge interface
3. Try adding a skill
4. Check if it connects to your Render backend

### Test Functionality

1. **Add Skill**: Click "Add New Skill"
2. **View Skills**: Should load from backend
3. **Update Progress**: Test progress slider
4. **Log Hours**: Test hour logging
5. **View History**: Check history modal

### Check Browser Console

Press F12 and check for:
- ✅ No CORS errors
- ✅ API calls succeeding
- ✅ Correct API URL being used

## Update Backend CORS

After deployment, update your backend CORS settings in `app.py`:

```python
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://your-vercel-app.vercel.app",  # ← Add your Vercel URL
            "http://localhost:5000"
        ],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type"]
    }
})
```

**Commit and push:**
```bash
git add app.py
git commit -m "Update CORS for Vercel domain"
git push origin main
```

Render will automatically redeploy.

## Custom Domain (Optional)

### Add Custom Domain

1. Go to project settings
2. Click "Domains"
3. Click "Add"
4. Enter your domain
5. Update DNS records as instructed
6. Wait for SSL certificate (automatic)

### Update DNS

Add these records to your domain:

**For apex domain (example.com):**
```
Type: A
Name: @
Value: 76.76.21.21
```

**For subdomain (www.example.com):**
```
Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

## Vercel Configuration

### vercel.json Explained

```json
{
  "version": 2,
  "builds": [
    {
      "src": "static/**",
      "use": "@vercel/static"
    }
  ],
  "routes": [
    {
      "src": "/",
      "dest": "/static/index.html"
    },
    {
      "src": "/(.*)",
      "dest": "/static/$1"
    }
  ]
}
```

This configuration:
- Serves files from `static/` directory
- Routes root to `index.html`
- Routes all other paths to static files

## Troubleshooting

### Build Fails

**Problem**: Deployment fails

**Solutions**:
1. Check `vercel.json` syntax
2. Verify `static/` directory exists
3. Check build logs for errors

### Page Not Loading

**Problem**: Blank page or 404

**Solutions**:
1. Verify `static/index.html` exists
2. Check `vercel.json` routes
3. Clear browser cache
4. Check browser console for errors

### API Not Working

**Problem**: Skills not loading, CORS errors

**Solutions**:
1. Verify API URL in `static/config.js`
2. Check backend is running on Render
3. Update CORS in backend `app.py`
4. Check browser console for errors

### Styles Not Loading

**Problem**: Page loads but looks broken

**Solutions**:
1. Check `static/style.css` exists
2. Verify CSS link in `index.html`
3. Clear browser cache
4. Check Network tab in DevTools

## Monitoring

### View Deployments

1. Go to Vercel dashboard
2. Click your project
3. See all deployments
4. Click any deployment to view details

### Analytics (Optional)

Vercel provides free analytics:
1. Go to project settings
2. Enable "Analytics"
3. View visitor stats

## Updating Your Deployment

### Automatic Deploys

Vercel automatically deploys when you push to GitHub:

```bash
git add .
git commit -m "Update frontend"
git push origin main
```

Vercel will:
1. Detect the push
2. Build and deploy
3. Takes 1-2 minutes

### Preview Deployments

Every branch and PR gets a preview URL:
- Test changes before merging
- Share with team
- Automatic cleanup

### Rollback

If something breaks:
1. Go to deployments
2. Find working version
3. Click "Promote to Production"

## Performance Optimization

### Already Optimized

✅ Static files (fast)  
✅ CDN distribution (global)  
✅ Automatic HTTPS  
✅ Compression enabled  
✅ Caching configured  

### Further Optimization

1. **Minify CSS/JS**: Use build tools
2. **Optimize Images**: Compress images
3. **Lazy Loading**: Load content on demand
4. **Service Worker**: Add PWA support

## Free Tier Limits

### Vercel Free Tier

✅ **Included**:
- Unlimited deployments
- Automatic HTTPS
- Global CDN
- 100 GB bandwidth/month
- Preview deployments
- Custom domains

⚠️ **Limits**:
- 100 GB bandwidth/month
- 100 GB-hours compute/month
- 6,000 build minutes/month

More than enough for personal projects!

## Environment-Specific Configuration

### Development

```javascript
// Local development
API_BASE_URL = 'http://localhost:5000/api'
```

### Production

```javascript
// Vercel production
API_BASE_URL = 'https://your-app.onrender.com/api'
```

### Auto-Detection

Our `config.js` automatically detects:
```javascript
getBaseURL: function() {
    if (window.location.hostname === 'localhost') {
        return this.local;  // Development
    }
    return this.production;  // Production
}
```

## Security Best Practices

### Production Checklist

- [ ] API URL updated in config.js
- [ ] CORS configured on backend
- [ ] HTTPS enabled (automatic)
- [ ] No sensitive data in frontend
- [ ] API keys in backend only
- [ ] Content Security Policy (optional)

### Content Security Policy

Add to `vercel.json` for extra security:

```json
{
  "headers": [
    {
      "source": "/(.*)",
      "headers": [
        {
          "key": "X-Content-Type-Options",
          "value": "nosniff"
        },
        {
          "key": "X-Frame-Options",
          "value": "DENY"
        }
      ]
    }
  ]
}
```

## Multiple Environments

### Production

- Branch: `main`
- URL: `your-app.vercel.app`
- API: Production backend

### Staging (Optional)

- Branch: `staging`
- URL: `your-app-staging.vercel.app`
- API: Staging backend

### Development

- Branch: Any feature branch
- URL: Auto-generated preview
- API: Development backend

## Team Collaboration

### Add Team Members

1. Go to project settings
2. Click "Members"
3. Invite by email
4. Set permissions

### Roles

- **Owner**: Full access
- **Member**: Deploy and view
- **Viewer**: View only

## Cost Optimization

### Stay on Free Tier

- Monitor bandwidth usage
- Optimize assets
- Use CDN caching
- Compress files

### Upgrade When Needed

**Pro Plan** ($20/month):
- More bandwidth
- More build minutes
- Priority support
- Advanced analytics

## Vercel CLI (Optional)

### Install CLI

```bash
npm install -g vercel
```

### Deploy from CLI

```bash
vercel
```

### Production Deploy

```bash
vercel --prod
```

## Success Checklist

- [ ] Vercel account created
- [ ] Repository connected
- [ ] API URL updated in config.js
- [ ] Project deployed
- [ ] Frontend accessible
- [ ] API connection working
- [ ] CORS configured
- [ ] All features tested
- [ ] Custom domain added (optional)

## Testing Checklist

Test all features:
- [ ] Homepage loads
- [ ] Statistics display
- [ ] Add technical skill
- [ ] Add soft skill
- [ ] Update progress
- [ ] Log hours
- [ ] Add application
- [ ] View history
- [ ] Filter skills
- [ ] Mobile responsive

## Next Steps

After frontend is deployed:
1. ✅ Test all functionality
2. ✅ Share your URL
3. ✅ Add to portfolio
4. ✅ Monitor usage
5. ✅ Collect feedback

## Support

### Vercel Documentation

- Docs: https://vercel.com/docs
- Status: https://vercel.com/status
- Community: https://github.com/vercel/vercel/discussions

### SkillForge Issues

- Check browser console
- Verify API connection
- Test backend separately
- Review configuration

## Complete Deployment URLs

After both deployments:

**Frontend (Vercel)**:
```
https://your-app.vercel.app
```

**Backend (Render)**:
```
https://your-app.onrender.com/api
```

**Full Stack Application**: ✅ Live!

---

**Deployment Time**: ~5 minutes  
**Cost**: Free  
**Difficulty**: ⭐ (Very Easy)

🎉 **Your frontend is now live on Vercel!**

## Final Architecture

```
User Browser
     ↓
Vercel (Frontend)
     ↓ API Calls
Render (Backend)
     ↓
JSON Data Storage
```

**Congratulations! Your full-stack SkillForge application is now deployed!** 🚀
