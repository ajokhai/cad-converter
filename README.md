# CAD Converter API

Convert CAD files (STEP/STL) to web-viewable 3D formats and generate Bills of Materials with AI.

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

---

## What It Does

- **Converts** STEP/STL files → glTF (viewable in browsers with Three.js)
- **Extracts** metadata from CAD files (part names, numbers, dimensions)
- **AI Analysis** (optional) - Uses AI to intelligently extract BOM data
- **Batch Processing** - Handle multiple files and generate complete BOMs

---

## Quick Start

### 1. Configuration

**Copy the environment template:**
```bash
cp .env.example .env
```

**Edit `.env` and configure your settings:**
```bash
# Required settings
SITE_URL=https://yourdomain.com              # Your website URL
CORS_ORIGINS=https://yourdomain.com          # Allowed domains (or * for dev)

# Optional AI settings (for AI-powered BOM generation)
OPENROUTER_API_KEY=sk-or-v1-...             # Get free key at openrouter.ai
DEFAULT_AI_MODEL=anthropic/claude-3.5-sonnet

# Optional limits
MAX_FILE_SIZE_MB=100
```

**All configurable values are now in `.env`** - no need to search through code files!

### 2. Deploy

#### Option A: Render.com (Recommended, Free Tier)

1. Fork this repo to your GitHub
2. Go to [Render.com](https://render.com) and sign up
3. Click "New +" → "Web Service"
4. Connect your forked repo
5. Render auto-detects settings from `render.yaml`
6. **Add environment variables** in Render dashboard:
   - Go to "Environment" tab
   - Add your variables from `.env`
7. Click "Create Web Service"
8. Wait 5-10 minutes for build
9. Your API is live! 🎉

#### Option B: Railway.app (Simple, Free Credits)

1. Fork this repo
2. Go to [Railway.app](https://railway.app) and sign up
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your forked repo
5. **Add environment variables**:
   - Go to "Variables" tab
   - Add your values from `.env`
6. Click "Settings" → "Generate Domain"
7. Your API is live! 🎉

#### Option C: Local Development

```bash
# Clone the repo
git clone https://github.com/ajokhai/cad-converter.git
cd cad-converter

# Create and configure .env
cp .env.example .env
# Edit .env with your settings

# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn main:app --reload --port 8080
```

#### Option D: Docker

```bash
# Build
docker build -t cad-converter .

# Run (environment variables from .env)
docker run -d \
  -p 8080:8080 \
  --env-file .env \
  --name cad-converter \
  cad-converter
```

---

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SITE_URL` | Yes | - | Your website URL (for OpenRouter attribution) |
| `CORS_ORIGINS` | Yes | `*` | Comma-separated allowed domains |
| `MAX_FILE_SIZE_MB` | No | `100` | Max file size in megabytes |
| `OPENROUTER_API_KEY` | No | - | Your OpenRouter API key (for AI features) |
| `DEFAULT_AI_MODEL` | No | `claude-3.5-sonnet` | Default AI model to use |
| `GITHUB_USERNAME` | No | `ajokhai` | GitHub username |
| `GITHUB_REPO` | No | `cad-converter` | Repository name |
| `PROJECT_AUTHORS` | No | Auto-set | Project authors |
| `DOWNLOAD_TIMEOUT` | No | `120` | File download timeout (seconds) |
| `AI_TIMEOUT` | No | `120` | AI request timeout (seconds) |
| `DEBUG` | No | `false` | Enable debug logging |

See `.env.example` for detailed documentation of all variables.

---

## How to Use

### Simple Example (No AI)

```javascript
const response = await fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: 'https://your-storage.com/part.step',
    fileType: 'step'
  })
});

const data = await response.json();
// Returns:
// - data.gltf (3D model)
// - data.metadata (part info)
// - data.dimensions (size)
```

### With AI Analysis

```javascript
const response = await fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: 'https://your-storage.com/part.step',
    fileType: 'step',
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: 'sk-or-v1-...'  // User's OpenRouter key
  })
});

const data = await response.json();
// Also returns:
// - data.ai_analysis (smart categorization, materials, etc.)
```

### Batch Processing + BOM Generation

```javascript
const response = await fetch('https://your-api.onrender.com/api/batch-convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    files: [
      { fileUrl: 'https://.../part1.step', fileType: 'step' },
      { fileUrl: 'https://.../part2.step', fileType: 'step' }
    ],
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: 'sk-or-v1-...',
    generateBOM: true
  })
});

const data = await response.json();
// Returns:
// - data.files (array of processed files)
// - data.bom (complete Bill of Materials)
```

---

## API Endpoints

### `GET /health`
Check service status
```json
{
  "status": "ok",
  "cadLibraries": true,
  "maxFileSizeMB": 100,
  "authors": "Josh Ayokhai, River",
  "repository": "https://github.com/ajokhai/cad-converter"
}
```

### `GET /api/limits`
Get service capabilities
```json
{
  "maxFileSizeMB": 100,
  "supportedFormats": ["step", "stp", "stl"],
  "supportedAIModels": [...]
}
```

### `POST /api/convert`
Convert single file

### `POST /api/batch-convert`
Convert multiple files + generate BOM

### `POST /api/metadata`
Extract metadata only (faster, no 3D)

See [API.md](API.md) for complete endpoint documentation.

---

## Supported Formats

- **Input:** STEP (.step, .stp), STL (.stl)
- **Output:** glTF (for 3D viewing in browsers)

---

## AI Models (via OpenRouter)

Configure in `.env` with `DEFAULT_AI_MODEL`:

- `anthropic/claude-3.5-sonnet` ⭐ Recommended (best balance)
- `anthropic/claude-3-opus` (Best quality, slower/expensive)
- `openai/gpt-4-turbo` (Good alternative)
- `openai/gpt-4o` (Latest GPT-4)
- `google/gemini-pro-1.5` (Cheapest option)

Get your free OpenRouter API key: https://openrouter.ai/

**Cost:** ~$0.01-0.05 per file (you pay OpenRouter directly)

---

## Project Structure

```
├── .env.example          # Environment configuration template
├── main.py              # FastAPI application
├── app/
│   ├── __init__.py
│   ├── config.py        # Configuration (reads from .env)
│   ├── models.py        # Request/response schemas
│   ├── metadata.py      # Metadata extraction
│   ├── converter.py     # CAD conversion
│   └── ai_analysis.py   # AI-powered analysis
├── requirements.txt
├── Dockerfile
├── render.yaml          # Render deployment config
├── README.md            # This file
├── API.md               # Complete API reference
├── DEPLOYMENT.md        # Deployment guide
└── SIMPLE_GUIDE.md      # Beginner-friendly tutorial
```

---

## Tech Stack

- **FastAPI** - Web framework
- **CadQuery** - STEP file processing
- **Trimesh** - Mesh processing & glTF export
- **OpenRouter** - AI model access (optional)
- **Python 3.11+**

---

## Security Best Practices

1. **Never commit `.env`** - It's in `.gitignore` by default
2. **Lock down CORS in production** - Set specific domains in `CORS_ORIGINS`
3. **Users provide their own AI keys** - You never store them
4. **Use signed URLs** for file storage (S3, Cloudflare R2)
5. **Enable HTTPS** in production (automatic on Render/Railway)

---

## Common Issues

### "CAD libraries not installed"
- Check `/health` endpoint
- Rebuild Docker image from scratch
- Verify `render.yaml` build configuration

### "File size exceeds limit"
- Increase `MAX_FILE_SIZE_MB` in `.env`
- Or compress your CAD files

### Service sleeps on Render free tier
- First request takes 30-60s after inactivity
- Upgrade to paid tier ($7/mo) for always-on

---

## Cost Estimates

### Hosting
- **Render Free:** $0/mo (sleeps after 15min)
- **Render Starter:** $7/mo (always-on)
- **Railway Free:** $5 credit/mo (~100 hours)
- **Railway Paid:** ~$7-10/mo

### AI (via OpenRouter)
- **Claude Sonnet:** ~$0.01-0.03 per file
- **GPT-4 Turbo:** ~$0.02-0.05 per file
- **Gemini:** ~$0.005-0.01 per file

---

## Contributing

PRs welcome! Please:

1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Update `.env.example` if adding new config
5. Test locally
6. Submit PR

---

## License

MIT License - see [LICENSE](LICENSE) file

---

## Support

- **Issues:** https://github.com/ajokhai/cad-converter/issues
- **Discussions:** https://github.com/ajokhai/cad-converter/discussions
- **Documentation:** See `API.md`, `DEPLOYMENT.md`, `SIMPLE_GUIDE.md`

---

## Acknowledgments

Built with ❤️ by Josh Ayokhai & River

Special thanks to:
- The CadQuery community
- OpenRouter for AI access
- Anthropic for Claude
- Everyone building open CAD tools
