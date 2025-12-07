# Setup Guide

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

Complete step-by-step setup instructions for the CAD Converter API.

---

## Quick Setup (5 minutes)

### 1. Clone the Repository

```bash
git clone https://github.com/ajokhai/cad-converter.git
cd cad-converter
```

### 2. Configure Environment Variables

```bash
# Copy the template
cp .env.example .env

# Edit with your settings
nano .env  # or use your preferred editor
```

**Minimum required configuration:**

```bash
# In .env file
SITE_URL=https://yourdomain.com
CORS_ORIGINS=*  # Use specific domains in production
```

**Optional AI configuration:**

```bash
# Get a free API key at https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-...
DEFAULT_AI_MODEL=anthropic/claude-3.5-sonnet
```

### 3. Choose Your Deployment Method

Pick one:

**A) Local Development**
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

**B) Docker**
```bash
docker-compose up -d
```

**C) Deploy to Cloud** (see [DEPLOYMENT.md](DEPLOYMENT.md))
- Render.com (free tier)
- Railway.app (free credits)

### 4. Test It

```bash
curl http://localhost:8080/health
```

You should see:
```json
{
  "status": "ok",
  "cadLibraries": true,
  "authors": "Josh Ayokhai, River"
}
```

---

## Detailed Setup

### Environment Variables Explained

Open `.env` and configure these variables:

#### Required Variables

```bash
# Your website URL (used for OpenRouter attribution)
SITE_URL=https://yourdomain.com

# Allowed origins for CORS
# Development: Use "*"
# Production: Use specific domains
CORS_ORIGINS=https://yourdomain.com,https://app.yourdomain.com
```

#### Optional Variables

```bash
# File size limit (default: 100MB)
MAX_FILE_SIZE_MB=100

# Your GitHub info (for attribution)
GITHUB_USERNAME=ajokhai
GITHUB_REPO=cad-converter

# Server port (default: 8080)
PORT=8080
```

#### AI Features (Optional)

```bash
# Get free key at https://openrouter.ai/
OPENROUTER_API_KEY=sk-or-v1-...

# Default AI model
DEFAULT_AI_MODEL=anthropic/claude-3.5-sonnet

# Options:
# - anthropic/claude-3.5-sonnet (recommended)
# - anthropic/claude-3-opus (best quality)
# - openai/gpt-4-turbo
# - google/gemini-pro-1.5 (cheapest)
```

#### Advanced Settings

```bash
# Enable debug logging
DEBUG=false

# Timeouts (in seconds)
DOWNLOAD_TIMEOUT=120
AI_TIMEOUT=120

# Supported formats (comma-separated)
SUPPORTED_FORMATS=step,stp,stl
```

---

## Local Development Setup

### Prerequisites

- Python 3.11 or higher
- pip (Python package manager)
- (Optional) Docker & Docker Compose

### Install Python Dependencies

```bash
# Create virtual environment (recommended)
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Development Server

```bash
# With auto-reload
uvicorn main:app --reload --port 8080

# Or specify host
uvicorn main:app --reload --host 0.0.0.0 --port 8080
```

Visit: `http://localhost:8080/docs` for interactive API documentation

---

## Docker Setup

### Using Docker Compose (Recommended)

```bash
# Build and start
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

### Using Docker Directly

```bash
# Build image
docker build -t cad-converter .

# Run with .env file
docker run -d \
  -p 8080:8080 \
  --env-file .env \
  --name cad-converter \
  cad-converter

# View logs
docker logs -f cad-converter

# Stop
docker stop cad-converter
docker rm cad-converter
```

---

## Cloud Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed instructions for:

- **Render.com** - Free tier, auto-deploy from GitHub
- **Railway.app** - Free credits, simple deployment
- **Self-hosted** - VPS/dedicated server

### Quick Deploy to Render

1. Fork this repo on GitHub
2. Sign up at [Render.com](https://render.com)
3. Click "New +" → "Web Service"
4. Select your repo
5. Add environment variables from `.env.example`
6. Click "Create Web Service"

---

## Testing Your Deployment

### Health Check

```bash
curl https://your-api-url.com/health
```

Expected response:
```json
{
  "status": "ok",
  "cadLibraries": true,
  "maxFileSizeMB": 100,
  "authors": "Josh Ayokhai, River",
  "repository": "https://github.com/ajokhai/cad-converter"
}
```

### Test File Conversion

1. Upload a test STEP file to a public URL (e.g., S3, R2)
2. Make a request:

```bash
curl -X POST https://your-api-url.com/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://your-storage.com/test.step",
    "fileType": "step"
  }'
```

### Test with AI (Optional)

```bash
curl -X POST https://your-api-url.com/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://your-storage.com/test.step",
    "fileType": "step",
    "aiModel": "anthropic/claude-3.5-sonnet",
    "apiKey": "sk-or-v1-YOUR-KEY"
  }'
```

---

## Troubleshooting

### "CAD libraries not installed"

**Cause:** Docker build failed or Python packages not installed correctly

**Fix:**
```bash
# Docker: Rebuild from scratch
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Python: Reinstall dependencies
pip install --force-reinstall -r requirements.txt
```

### "ModuleNotFoundError: No module named 'app'"

**Cause:** Running from wrong directory

**Fix:**
```bash
# Make sure you're in the project root
cd /path/to/cad-converter
python -m uvicorn main:app --reload
```

### ".env not found" or environment variables not loading

**Cause:** `.env` file missing or not in the right place

**Fix:**
```bash
# Verify .env exists
ls -la .env

# If not, create it
cp .env.example .env
nano .env
```

### CORS errors in browser

**Cause:** `CORS_ORIGINS` not configured for your domain

**Fix:**
```bash
# In .env
CORS_ORIGINS=https://yourfrontend.com,https://app.yourfrontend.com
```

### Port already in use

**Cause:** Another service using port 8080

**Fix:**
```bash
# Use a different port
PORT=8081

# Or find and kill the process
lsof -ti:8080 | xargs kill -9
```

---

## Next Steps

1. **Read the API docs:** [API.md](API.md)
2. **Learn deployment options:** [DEPLOYMENT.md](DEPLOYMENT.md)
3. **See usage examples:** [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)
4. **Get OpenRouter key:** https://openrouter.ai/ (for AI features)

---

## Getting Help

- **Issues:** https://github.com/ajokhai/cad-converter/issues
- **Discussions:** https://github.com/ajokhai/cad-converter/discussions
- **OpenRouter Docs:** https://openrouter.ai/docs

---

Built with ❤️ by Josh Ayokhai & River
