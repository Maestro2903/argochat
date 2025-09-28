# FLOAT CHAT - Render.com Deployment Guide

Complete guide for deploying FLOAT CHAT to Render.com with production-ready configuration.

## 📋 Prerequisites

### Required Accounts & API Keys
- **Render.com account** (free tier available)
- **GitHub repository** with your FLOAT CHAT code
- **OpenAI API key** (required for AI functionality)
- **Custom domain** (optional, for branding)

### System Requirements
- **Node.js**: 22.12.0 (specified in package.json engines)
- **Python**: 3.12.7 (specified in render.yaml)
- **npm**: >=6.0.0

## 🔧 Pre-Deployment Setup

### 1. Verify Dependencies

**Frontend (Node.js/SvelteKit):**
```json
{
  "engines": {
    "node": ">=18.13.0 <=22.x.x",
    "npm": ">=6.0.0"
  }
}
```

**Backend (Python/FastAPI):**
```toml
requires-python = ">= 3.11, < 3.13.0a1"
```

### 2. Environment Configuration

All environment variables are pre-configured in `render.yaml`. Key variables:

**Backend Environment:**
- `WEBUI_SECRET_KEY`: Auto-generated secure key
- `OPENAI_API_KEY`: **You must provide this**
- `DATABASE_URL`: SQLite by default, PostgreSQL optional
- `CORS_ALLOW_ORIGIN`: Configured for frontend domain

**Frontend Environment:**
- `PUBLIC_API_BASE_URL`: Points to backend service
- `NODE_ENV`: Set to production
- `ORIGIN`: Frontend domain for CORS

## 🚀 Deployment Steps

### Step 1: Prepare Your Repository

1. **Push your code** to GitHub with all recent changes
2. **Verify files** are present:
   ```
   ├── render.yaml                 # Render configuration
   ├── package.json               # Frontend dependencies
   ├── backend/requirements.txt   # Backend dependencies
   ├── pyproject.toml            # Python project config
   ├── svelte.config.js          # SvelteKit config (Node.js adapter)
   └── scripts/
       ├── build-frontend.sh     # Frontend build script
       └── build-backend.sh      # Backend build script
   ```

### Step 2: Deploy to Render

#### Option A: Using Render Blueprint (Recommended)

1. **Go to Render Dashboard**: https://dashboard.render.com
2. **Click "New" → "Blueprint"**
3. **Connect your GitHub repository**
4. **Select repository**: Choose your FLOAT CHAT repository
5. **Blueprint file**: Render will automatically detect `render.yaml`
6. **Review services**:
   - `floatchat-backend` (Python/FastAPI)
   - `floatchat-frontend` (Node.js/SvelteKit)
   - `floatchat-postgres` (PostgreSQL database - optional)

7. **Configure environment variables**:
   - Set `OPENAI_API_KEY` for the backend service
   - All other variables are auto-configured

8. **Deploy**: Click "Apply" to start deployment

#### Option B: Manual Service Creation

If blueprint deployment fails, create services manually:

**Backend Service:**
```
Service Type: Web Service
Environment: Python
Build Command: python3.12 -m pip install --upgrade pip setuptools wheel && pip install -r backend/requirements.txt --no-cache-dir
Start Command: cd backend && python3.12 -m uvicorn open_webui.main:app --host 0.0.0.0 --port $PORT --workers 1 --forwarded-allow-ips '*'
```

**Frontend Service:**
```
Service Type: Web Service
Environment: Node
Build Command: npm ci --legacy-peer-deps && npm run build
Start Command: HOST=0.0.0.0 PORT=$PORT node build
```

### Step 3: Configure Environment Variables

#### Backend Service Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `PYTHON_VERSION` | `3.12.7` | Python runtime version |
| `ENV` | `prod` | Environment mode |
| `WEBUI_SECRET_KEY` | *Auto-generated* | Session security key |
| `OPENAI_API_KEY` | **Your API key** | OpenAI API access |
| `OLLAMA_BASE_URL` | `https://api.openai.com/v1` | AI model endpoint |
| `CORS_ALLOW_ORIGIN` | `https://floatchat-frontend.onrender.com` | Frontend domain |
| `DATABASE_URL` | `sqlite:///./data/webui.db` | Database connection |
| `WEBUI_AUTH` | `true` | Enable authentication |
| `ENABLE_SIGNUP` | `true` | Allow user registration |

#### Frontend Service Environment Variables

| Variable | Value | Description |
|----------|-------|-------------|
| `NODE_VERSION` | `22.12.0` | Node.js runtime version |
| `NODE_ENV` | `production` | Environment mode |
| `PUBLIC_API_BASE_URL` | `https://floatchat-backend.onrender.com` | Backend API URL |
| `ORIGIN` | `https://floatchat-frontend.onrender.com` | Frontend domain |
| `APP_VERSION` | `0.6.31` | Application version |

### Step 4: Update Domain References

After deployment, update these URLs with your actual Render service URLs:

1. **Backend service** → Update `CORS_ALLOW_ORIGIN` and `WEBUI_URL`
2. **Frontend service** → Update `PUBLIC_API_BASE_URL` and `ORIGIN`

## 🌐 Custom Domain Setup

### Step 1: Configure Custom Domain in Render

1. **Go to your frontend service** in Render dashboard
2. **Settings → Custom Domains**
3. **Add your domain** (e.g., `chat.yourdomain.com`)
4. **Configure DNS** with your domain provider:
   ```
   Type: CNAME
   Name: chat (or your subdomain)
   Value: floatchat-frontend.onrender.com
   ```

### Step 2: Update Environment Variables

After custom domain is active, update:

**Backend service:**
- `CORS_ALLOW_ORIGIN` → `https://chat.yourdomain.com`
- `WEBUI_URL` → `https://chat.yourdomain.com`

**Frontend service:**
- `ORIGIN` → `https://chat.yourdomain.com`

## 🗃️ Database Configuration

### SQLite (Default)
- **Pros**: Simple setup, included with deployment
- **Cons**: Limited scalability, data resets on service restart
- **Good for**: Testing, small deployments

### PostgreSQL (Recommended for Production)
1. **Enable PostgreSQL** in `render.yaml`:
   ```yaml
   databases:
     - name: floatchat-postgres
       databaseName: floatchat
       user: floatchat_user
       plan: starter
   ```

2. **Update backend environment**:
   ```
   DATABASE_URL=postgresql://user:password@host:5432/floatchat
   ```

## 📊 Service Monitoring

### Health Checks
- **Backend**: `/health` endpoint
- **Frontend**: Default HTTP check on port 10000

### Logs Access
1. **Render Dashboard** → Your service → Logs
2. **Filter by service** (backend/frontend)
3. **Monitor for errors** during startup and runtime

### Performance Monitoring
- **Starter plan**: 0.5 CPU, 512MB RAM
- **Monitor resource usage** in Render dashboard
- **Upgrade plan** if needed for better performance

## 🔧 Troubleshooting

### Common Issues

#### Build Failures

**Frontend build fails:**
```bash
# Check Node.js version
node --version  # Should be 22.x.x

# Clear cache and rebuild
rm -rf node_modules .svelte-kit
npm ci --legacy-peer-deps
npm run build
```

**Backend build fails:**
```bash
# Check Python version
python3.12 --version  # Should be 3.12.x

# Install dependencies manually
pip install -r backend/requirements.txt --no-cache-dir
```

#### Runtime Issues

**CORS errors:**
- Verify `CORS_ALLOW_ORIGIN` matches frontend domain exactly
- Check both HTTP and HTTPS protocols

**Database connection errors:**
- Verify `DATABASE_URL` format
- Check database service is running
- Ensure data directory exists

**Authentication issues:**
- Verify `WEBUI_SECRET_KEY` is set
- Check `WEBUI_AUTH=true` is configured
- Ensure proper session management

### Service URLs

After successful deployment, your services will be available at:

- **Frontend**: `https://floatchat-frontend.onrender.com`
- **Backend API**: `https://floatchat-backend.onrender.com`
- **Custom domain**: `https://your-custom-domain.com` (if configured)

## 🔐 Security Considerations

### Environment Variables
- ✅ All sensitive keys are auto-generated by Render
- ✅ API keys are stored securely in Render environment
- ✅ Database credentials are managed by Render

### HTTPS
- ✅ Automatic SSL certificates for `.onrender.com` domains
- ✅ Custom domains get automatic SSL via Let's Encrypt

### Authentication
- ✅ Built-in user authentication system
- ✅ Configurable signup settings
- ✅ JWT-based session management

## 📈 Scaling & Optimization

### Performance Tips
1. **Use PostgreSQL** for production workloads
2. **Monitor resource usage** and upgrade plan when needed
3. **Enable caching** for frequently accessed data
4. **Optimize frontend bundle size** by removing unused dependencies

### Cost Optimization
- **Free tier limits**: 750 hours/month per service
- **Starter plan**: $7/month per service (recommended for production)
- **Database**: Free PostgreSQL tier available

## ✅ Deployment Checklist

- [ ] Repository pushed to GitHub with latest changes
- [ ] `render.yaml` configuration verified
- [ ] OpenAI API key obtained
- [ ] Render account created and repository connected
- [ ] Blueprint deployment initiated
- [ ] Environment variables configured
- [ ] Custom domain configured (optional)
- [ ] Services tested and accessible
- [ ] Database configured (PostgreSQL recommended)
- [ ] Monitoring and logging verified

## 🆘 Support

### Documentation
- **Render.com docs**: https://render.com/docs
- **SvelteKit docs**: https://kit.svelte.dev/docs
- **FastAPI docs**: https://fastapi.tiangolo.com

### Common Commands

**Local testing:**
```bash
# Frontend
npm run dev

# Backend
cd backend && python3.12 -m uvicorn open_webui.main:app --reload

# Full stack
python3.12 run_servers.py
```

**Build testing:**
```bash
# Test frontend build
./scripts/build-frontend.sh

# Test backend build
./scripts/build-backend.sh
```

---

**FLOAT CHAT** is now ready for production deployment on Render.com! 🚀

For additional support or custom deployment needs, refer to the project documentation or create an issue in the repository.