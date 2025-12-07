# Deployment Checklist

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

Quick reference for deploying the CAD Converter API.

---

## Pre-Deployment Checklist

- [ ] Fork repository to your GitHub account
- [ ] Review `.env.example` to understand configuration options
- [ ] Decide on deployment platform (Render/Railway/Docker/Other)
- [ ] (Optional) Get OpenRouter API key from https://openrouter.ai/
- [ ] Prepare file storage (S3/R2/etc.) for CAD files

---

## Configuration Checklist

### Required Environment Variables

- [ ] `SITE_URL` - Set to your website URL
- [ ] `CORS_ORIGINS` - Set allowed domains (or `*` for development)

### Recommended Environment Variables

- [ ] `MAX_FILE_SIZE_MB` - Set appropriate file size limit (default: 100)
- [ ] `GITHUB_USERNAME` - Update to your GitHub username
- [ ] `GITHUB_REPO` - Update to your repo name

### Optional AI Configuration

- [ ] `OPENROUTER_API_KEY` - Add if providing default API key
- [ ] `DEFAULT_AI_MODEL` - Choose default AI model

---

## Render.com Deployment

- [ ] Go to https://render.com and sign in
- [ ] Click "New +" → "Web Service"
- [ ] Connect your GitHub repo
- [ ] Go to "Environment" tab
- [ ] Add required environment variables:
  - [ ] `SITE_URL`
  - [ ] `CORS_ORIGINS`
  - [ ] `GITHUB_USERNAME`
  - [ ] `GITHUB_REPO`
- [ ] (Optional) Add `OPENROUTER_API_KEY`
- [ ] Click "Create Web Service"
- [ ] Wait for build to complete (~5-10 minutes)
- [ ] Test health endpoint: `https://your-service.onrender.com/health`
- [ ] Save your deployment URL

---

## Railway.app Deployment

- [ ] Go to https://railway.app and sign in
- [ ] Click "New Project" → "Deploy from GitHub repo"
- [ ] Select your forked repo
- [ ] Go to "Variables" tab
- [ ] Add required environment variables:
  - [ ] `SITE_URL`
  - [ ] `CORS_ORIGINS`
  - [ ] `GITHUB_USERNAME`
  - [ ] `GITHUB_REPO`
- [ ] (Optional) Add `OPENROUTER_API_KEY`
- [ ] Go to "Settings" → "Generate Domain"
- [ ] Test health endpoint: `https://your-service.railway.app/health`
- [ ] Save your deployment URL

---

## Docker Deployment

- [ ] Clone repository
- [ ] Create `.env` file from `.env.example`
- [ ] Edit `.env` with your configuration
- [ ] Build image: `docker build -t cad-converter .`
- [ ] Run container: `docker run -d -p 8080:8080 --env-file .env cad-converter`
- [ ] Test health endpoint: `http://localhost:8080/health`

### Docker Compose

- [ ] Create `.env` file
- [ ] Run: `docker-compose up -d`
- [ ] Check logs: `docker-compose logs -f`
- [ ] Test health endpoint: `http://localhost:8080/health`

---

## Local Development

- [ ] Clone repository
- [ ] Create `.env` file from `.env.example`
- [ ] Create virtual environment: `python -m venv venv`
- [ ] Activate: `source venv/bin/activate` (macOS/Linux) or `venv\Scripts\activate` (Windows)
- [ ] Install dependencies: `pip install -r requirements.txt`
- [ ] Run server: `uvicorn main:app --reload --port 8080`
- [ ] Test health endpoint: `http://localhost:8080/health`
- [ ] Visit API docs: `http://localhost:8080/docs`

---

## Post-Deployment Checklist

### Testing

- [ ] Health check returns `{"status": "ok"}`
- [ ] `/api/limits` returns supported formats
- [ ] Test file conversion with sample STEP file
- [ ] (If using AI) Test AI analysis with API key
- [ ] Test CORS from your frontend domain

### Security

- [ ] Verify `.env` is in `.gitignore` (not committed)
- [ ] Set `CORS_ORIGINS` to specific domains in production
- [ ] Enable HTTPS (automatic on Render/Railway)
- [ ] (Optional) Add rate limiting at reverse proxy level

### Documentation

- [ ] Update deployment URL in your documentation
- [ ] Document any custom environment variables
- [ ] Share API documentation with team
- [ ] Test API with your frontend application

### Monitoring

- [ ] Set up uptime monitoring (UptimeRobot, etc.)
- [ ] Check logs for errors
- [ ] Monitor API response times
- [ ] Track AI usage costs (if using OpenRouter)

---

## Troubleshooting Quick Checks

### API Not Responding

- [ ] Check service is running (dashboard/logs)
- [ ] Verify port is correct (8080 by default)
- [ ] Check environment variables are set
- [ ] Review build logs for errors

### "CAD libraries not installed"

- [ ] Rebuild Docker image from scratch
- [ ] Check Dockerfile configuration
- [ ] Review build logs for installation errors

### CORS Errors

- [ ] Verify `CORS_ORIGINS` includes your domain
- [ ] Check for trailing slashes in URLs
- [ ] Test with `CORS_ORIGINS=*` to isolate issue

### AI Features Not Working

- [ ] Verify `OPENROUTER_API_KEY` is set (if providing default)
- [ ] Check API key is valid at https://openrouter.ai/
- [ ] Verify you have credits available
- [ ] Check logs for AI-specific errors

---

## Quick Reference Commands

### Health Check
```bash
curl https://your-api-url.com/health
```

### Test Conversion
```bash
curl -X POST https://your-api-url.com/api/convert \
  -H "Content-Type: application/json" \
  -d '{"fileUrl":"https://example.com/file.step","fileType":"step"}'
```

### View Logs (Docker)
```bash
docker logs -f cad-converter
# or
docker-compose logs -f
```

### Restart Service (Docker)
```bash
docker restart cad-converter
# or
docker-compose restart
```

---

## Resources

- **Setup Guide:** [SETUP.md](SETUP.md)
- **API Documentation:** [API.md](API.md)
- **Deployment Guide:** [DEPLOYMENT.md](DEPLOYMENT.md)
- **Simple Tutorial:** [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)
- **GitHub Repo:** https://github.com/ajokhai/cad-converter
- **Issues:** https://github.com/ajokhai/cad-converter/issues

---

Built with ❤️ by Josh Ayokhai & River
