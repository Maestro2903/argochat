# ArgoChat Render Deployment Guide

This guide walks you through deploying ArgoChat (Open WebUI) to Render.

## Repository Setup ✅

✅ **GitHub Repository**: https://github.com/Maestro2903/argochat.git
✅ **Configuration Files**: Created render.yaml, build.sh, start.sh

## Render Deployment Steps

### 1. **Create Render Account**
- Go to [render.com](https://render.com)
- Sign up/Login with your GitHub account
- Connect your GitHub repository

### 2. **Deploy Backend Service**

1. **Create New Web Service**:
   - Repository: `Maestro2903/argochat`
   - Environment: `Python`
   - Region: `Oregon`
   - Branch: `main`

2. **Service Configuration**:
   ```
   Name: argochat-backend
   Build Command: pip install -r backend/requirements.txt
   Start Command: cd backend && python -m uvicorn open_webui.main:app --host 0.0.0.0 --port $PORT
   ```

3. **Environment Variables**:
   ```bash
   ENV=prod
   PYTHON_VERSION=3.12.0
   DATA_DIR=./data
   WEBUI_SECRET_KEY=<generate-secure-key>
   CORS_ALLOW_ORIGIN=*
   FORWARDED_ALLOW_IPS=*
   OLLAMA_BASE_URL=https://api.openai.com/v1
   OPENAI_API_BASE_URL=https://api.openai.com/v1
   ```

### 3. **Deploy Frontend Service**

1. **Create New Static Site**:
   - Repository: `Maestro2903/argochat`
   - Environment: `Node.js`
   - Region: `Oregon`
   - Branch: `main`

2. **Build Configuration**:
   ```
   Name: argochat-frontend
   Build Command: npm install --legacy-peer-deps && npm run build
   Publish Directory: build
   ```

3. **Environment Variables**:
   ```bash
   NODE_VERSION=22.12.0
   PUBLIC_API_BASE_URL=https://argochat-backend.onrender.com
   APP_VERSION=0.6.31
   APP_BUILD_HASH=render-build
   ```

### 4. **Optional: Database Service**

For production, you might want a managed database:

1. **Create PostgreSQL Database**:
   - Service Type: `PostgreSQL`
   - Name: `argochat-db`
   - Plan: `Starter` ($7/month)

2. **Update Backend Environment**:
   ```bash
   DATABASE_URL=<postgresql-connection-string>
   ```

## Alternative: Single Service Deployment

If you prefer to deploy as a single service (backend serves frontend):

### 1. **Create Web Service**
```
Repository: Maestro2903/argochat
Environment: Python
Build Command: pip install -r backend/requirements.txt && npm install --legacy-peer-deps && npm run build
Start Command: cd backend && python -m uvicorn open_webui.main:app --host 0.0.0.0 --port $PORT
```

### 2. **Environment Variables**
```bash
ENV=prod
PYTHON_VERSION=3.12.0
NODE_VERSION=22.12.0
WEBUI_SECRET_KEY=<generate-secure-key>
DATA_DIR=./data
CORS_ALLOW_ORIGIN=*
```

## Post-Deployment Setup

### 1. **Initial Admin User**
- Visit your deployed site
- Register the first user (becomes admin)
- Configure settings in Admin Panel

### 2. **Configure AI Models**
- Add OpenAI API key in Settings > Connections
- Or connect to Ollama instance
- Test model connectivity

### 3. **Optional: Custom Domain**
- In Render Dashboard → Settings → Custom Domains
- Add your domain name
- Update CORS settings accordingly

## Environment Variables Reference

### Backend Required:
```bash
ENV=prod
WEBUI_SECRET_KEY=<secure-random-string>
DATA_DIR=./data
CORS_ALLOW_ORIGIN=<frontend-url-or-*>
FORWARDED_ALLOW_IPS=*
```

### Backend Optional:
```bash
OLLAMA_BASE_URL=<ollama-api-url>
OPENAI_API_KEY=<your-openai-key>
OPENAI_API_BASE_URL=https://api.openai.com/v1
DATABASE_URL=<postgres-connection-string>
WEBUI_URL=<frontend-url>
```

### Frontend Required:
```bash
PUBLIC_API_BASE_URL=<backend-service-url>
NODE_VERSION=22.12.0
```

## Troubleshooting

### Build Issues:
1. **Node.js Version**: Ensure using Node.js 22.x
2. **Dependencies**: Use `--legacy-peer-deps` flag
3. **Memory**: Upgrade to Starter plan if build fails

### Runtime Issues:
1. **CORS Errors**: Check CORS_ALLOW_ORIGIN setting
2. **Database**: Ensure migrations run on startup
3. **File Storage**: Use Render disk storage for persistent data

### Performance:
1. **Cold Starts**: Use Starter plan to reduce cold start times
2. **Memory**: Monitor usage in Render dashboard
3. **Database**: Consider upgrading to managed PostgreSQL

## Cost Estimation

### Free Tier:
- Backend: Free tier (sleeps after inactivity)
- Frontend: Free static hosting
- **Total**: $0/month

### Production Ready:
- Backend: Starter plan ($7/month)
- Database: PostgreSQL Starter ($7/month)
- Frontend: Free static hosting
- **Total**: $14/month

## Next Steps

1. **Deploy Backend**: Create Python web service
2. **Deploy Frontend**: Create static site or Node.js service
3. **Configure Environment**: Set all required variables
4. **Test Deployment**: Verify functionality
5. **Set Up Monitoring**: Monitor logs and performance
6. **Configure Domain**: Add custom domain if needed

## Support

If you encounter issues:
1. Check Render logs for error details
2. Verify environment variables
3. Test build locally first
4. Open GitHub issue if needed

---

**Repository**: https://github.com/Maestro2903/argochat.git
**Live Demo**: Will be available after deployment