# Deployment Guide

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

How to deploy this service to various platforms.

## Before You Deploy

### Configure Your Environment Variables

All configuration is done through environment variables in `.env`. Before deploying:

1. **Copy the template:**
   ```bash
   cp .env.example .env
   ```

2. **Edit `.env` with your values:**
   ```bash
   # Required
   SITE_URL=https://yourdomain.com
   CORS_ORIGINS=https://yourdomain.com
   
   # Optional (for AI features)
   OPENROUTER_API_KEY=sk-or-v1-...
   
   # Optional limits
   MAX_FILE_SIZE_MB=100
   ```

3. **For deployment platforms**, you'll add these as environment variables in their dashboards (don't commit `.env` to git!)

---

## Option 1: Render.com (Recommended, Free Tier Available)

**Why Render:**
- Free tier available
- Auto-deploys from GitHub
- Uses `render.yaml` for config
- Docker support built-in

**Steps:**

1. **Fork this repo** to your GitHub account

2. **Go to Render.com**
   - Sign up at https://render.com (free)
   - Connect your GitHub account

3. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select your forked repo
   - Render auto-detects the `render.yaml` config
   
4. **Configure Environment Variables**
   - Before creating the service, go to "Environment" section
   - Add your variables from `.env.example`:
     ```
     SITE_URL=https://yourdomain.com
     CORS_ORIGINS=https://yourdomain.com
     MAX_FILE_SIZE_MB=100
     GITHUB_USERNAME=ajokhai
     ```
   - (Optional) Add `OPENROUTER_API_KEY` if you want a default key
   
5. **Create and Deploy**
   - Click "Create Web Service"
   - Wait for Build (5-10 minutes for first build)

6. **Your API is Live!**
   - Render gives you a URL like: `https://your-service.onrender.com`
   - Test it: `https://your-service.onrender.com/health`

**Free Tier Limits:**
- Sleeps after 15 mins of inactivity (first request after sleep takes 30-60 seconds)
- 750 hours/month of runtime
- Good for development and light production use

**Upgrade to Paid ($7/mo):**
- No sleeping
- Always-on
- Better performance

---

## Option 2: Railway.app (Simple, Free Tier Available)

**Why Railway:**
- Super simple deployment
- Free $5/month credit (good for ~100 hours)
- Fast builds
- Great for side projects

**Steps:**

1. **Fork this repo**

2. **Go to Railway.app**
   - Sign up at https://railway.app
   - Connect GitHub

3. **Deploy**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your forked repo
   - Railway auto-detects Dockerfile
   
4. **Configure Environment Variables**
   - Go to your service → "Variables" tab
   - Add variables from `.env.example`:
     ```
     SITE_URL=https://yourdomain.com
     CORS_ORIGINS=*
     MAX_FILE_SIZE_MB=100
     GITHUB_USERNAME=ajokhai
     ```
   - Click "Deploy"

5. **Generate Domain**
   - Go to your service
   - Click "Settings" → "Generate Domain"
   - You get: `https://your-service.railway.app`

**Pricing:**
- $5 free credit/month
- Then $0.000463 per GB-hour
- ~$7-10/month for always-on service

---

## Option 3: Self-Hosted with Docker

**Why Self-Host:**
- Full control
- No usage limits
- Run on your own server

**Requirements:**
- Server with Docker installed
- 2GB RAM minimum
- 10GB disk space

**Steps:**

1. **Clone the repo**
   ```bash
   git clone https://github.com/ajokhai/cad-converter.git
   cd cad-converter
   ```

2. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   nano .env  # or use your preferred editor
   ```

3. **Build Docker image**
   ```bash
   docker build -t cad-converter .
   ```

4. **Run container**
   ```bash
   docker run -d \
     -p 8080:8080 \
     --env-file .env \
     --name cad-converter \
     cad-converter
   ```

5. **Test it**
   ```bash
   curl http://localhost:8080/health
   ```

**Production Setup:**

Use docker-compose for easier management:

```yaml
# docker-compose.yml
version: '3.8'

services:
  cad-converter:
    build: .
    ports:
      - "8080:8080"
    env_file:
      - .env
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8080/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

Run with:
```bash
docker-compose up -d
```

**Reverse Proxy (Nginx):**

```nginx
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## Environment Variables

All configuration is done through environment variables. See `.env.example` for the complete list.

**Core Variables:**

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SITE_URL` | Yes | - | Your website URL (for OpenRouter attribution) |
| `CORS_ORIGINS` | Yes | `*` | Comma-separated allowed origins |
| `MAX_FILE_SIZE_MB` | No | `100` | Maximum file size in MB |
| `GITHUB_USERNAME` | No | `ajokhai` | Your GitHub username |
| `GITHUB_REPO` | No | `cad-converter` | Repository name |

**Optional AI Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `OPENROUTER_API_KEY` | - | Default OpenRouter API key |
| `DEFAULT_AI_MODEL` | `claude-3.5-sonnet` | Default AI model |

**Advanced Variables:**

| Variable | Default | Description |
|----------|---------|-------------|
| `PORT` | `8080` | Server port |
| `DOWNLOAD_TIMEOUT` | `120` | File download timeout (seconds) |
| `AI_TIMEOUT` | `120` | AI request timeout (seconds) |
| `DEBUG` | `false` | Enable debug logging |

**Setting Variables by Platform:**

**Render:**
- Go to service → "Environment" tab
- Add each variable from `.env.example`

**Railway:**
- Go to service → "Variables" tab
- Add each variable from `.env.example`

**Docker/Self-Hosted:**
- Use `--env-file .env` flag
- Or use docker-compose with `env_file: .env`

---

## Monitoring

### Health Checks

All platforms support health checks. Use:
- **Path:** `/health`
- **Method:** GET
- **Expected:** 200 status + `{"status": "ok"}`

### Logs

**Render:**
- View in dashboard → "Logs" tab

**Railway:**
- View in dashboard → "Deployments" → Click deployment

**Docker:**
```bash
docker logs -f cad-converter
```

---

## Scaling

### Vertical Scaling (More Power)

If processing large/complex files:
- Render: Upgrade to larger instance ($7-25/mo)
- Railway: Increase memory/CPU in settings
- Docker: Run on bigger server

### Horizontal Scaling (More Instances)

For high traffic:
1. Deploy multiple instances
2. Use load balancer (nginx, Cloudflare, AWS ALB)
3. Each instance is stateless (no shared state)

---

## Troubleshooting

### Build Fails

**Error:** "Could not find libocct-*"

**Fix:** Docker is having trouble installing OpenCascade. Try:
1. Rebuild from scratch
2. Check if base image changed
3. File an issue on GitHub

### Service Crashes

**Error:** "CAD libraries not installed"

**Fix:** 
1. Check `/health` endpoint
2. Verify Docker build completed successfully
3. Check logs for import errors

### High Memory Usage

**Cause:** Processing large files or many concurrent requests

**Fix:**
1. Reduce `MAX_FILE_SIZE_MB`
2. Increase instance memory
3. Add request queuing

### Slow First Request (Render Free Tier)

**Cause:** Service sleeps after 15 mins inactivity

**Fix:**
- Upgrade to paid tier ($7/mo)
- Or accept 30-60s cold start

---

## Security

### Recommendations

1. **Never commit `.env` to git**
   - Already in `.gitignore`
   - Contains sensitive keys and configuration
   
2. **CORS:** Lock down `CORS_ORIGINS` in production
   ```bash
   CORS_ORIGINS=https://yourapp.com
   ```

3. **File Sources:** Only accept files from trusted storage
   - Use signed URLs (S3, Cloudflare R2)
   - Validate file types
   - Scan for malware if accepting user uploads

4. **Rate Limiting:** Add rate limiting at reverse proxy level
   ```nginx
   limit_req_zone $binary_remote_addr zone=api:10m rate=10r/s;
   limit_req zone=api burst=20;
   ```

5. **API Keys:** Users provide their own OpenRouter keys
   - You never store them permanently
   - Optional: Set `OPENROUTER_API_KEY` for a default key
   - They pay for their own AI usage

6. **HTTPS:** Always use HTTPS in production
   - Render/Railway provide this automatically
   - For self-hosted, use Let's Encrypt + Nginx

---

## Cost Estimates

### Render.com
- **Free:** $0/mo (with sleeping)
- **Starter:** $7/mo (always-on, 512MB RAM)
- **Standard:** $25/mo (2GB RAM)

### Railway.app
- **Free:** $5 credit/mo (~100 hours)
- **Pro:** ~$7-10/mo for always-on

### Self-Hosted (DigitalOcean)
- **Basic:** $6/mo (1GB RAM)
- **Better:** $12/mo (2GB RAM)
- Plus domain, SSL cert (free with Let's Encrypt)

### AI Costs (OpenRouter)
Users pay for their own API usage:
- Claude Sonnet: ~$0.01-0.03 per file
- GPT-4 Turbo: ~$0.02-0.05 per file
- Gemini: ~$0.005-0.01 per file

---

## Next Steps

After deployment:

1. Test all endpoints with real files
2. Set up monitoring/alerts
3. Configure CORS for your domain
4. Add rate limiting if needed
5. Document your deployment URL
6. Consider adding authentication if needed

---

## Need Help?

- **Issues:** https://github.com/ajokhai/cad-converter/issues
- **Render Docs:** https://render.com/docs
- **Railway Docs:** https://docs.railway.app
- **OpenRouter:** https://openrouter.ai/docs

**Authors:** Josh Ayokhai & River
