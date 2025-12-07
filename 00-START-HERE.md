# 🚀 CAD Converter API - Start Here

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

---

## 👋 Welcome!

This is a complete CAD file conversion and BOM generation API with AI capabilities.

**What it does:**
- Converts STEP/STL files to web-viewable 3D (glTF)
- Extracts metadata from CAD files
- Uses AI to generate Bills of Materials
- Processes files in batches

---

## ⚡ Quick Start (3 Steps)

### 1. Copy Configuration Template
```bash
cp .env.example .env
```

### 2. Edit .env File
```bash
# Minimum required:
SITE_URL=https://yourdomain.com
CORS_ORIGINS=*
```

### 3. Choose Deployment

**Local (fastest to test):**
```bash
pip install -r requirements.txt
uvicorn main:app --reload --port 8080
```

**Docker (easiest):**
```bash
docker-compose up -d
```

**Cloud (best for production):**
- See [DEPLOYMENT.md](DEPLOYMENT.md)

---

## 📚 Documentation Guide

### New to the Project?
1. **[README.md](README.md)** - Project overview and quick start
2. **[SETUP.md](SETUP.md)** - Detailed setup instructions
3. **[SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)** - Beginner-friendly tutorial

### Deploying?
1. **[DEPLOYMENT.md](DEPLOYMENT.md)** - Platform-specific guides
2. **[CHECKLIST.md](CHECKLIST.md)** - Quick deployment checklist
3. **[.env.example](.env.example)** - Configuration template

### Using the API?
1. **[API.md](API.md)** - Complete API reference
2. **[SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)** - Easy examples
3. **[README.md](README.md)** - Quick usage examples

### Contributing?
1. **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
2. **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - Project overview
3. **[FILES.md](FILES.md)** - File structure

---

## 🎯 What Changed?

**Before:** Configuration scattered across multiple files  
**After:** Everything in one `.env` file ✨

**Key Improvements:**
- ✅ Single source of truth for configuration
- ✅ No hardcoded values in code
- ✅ Proper attribution to both authors
- ✅ Easy environment-specific settings
- ✅ Better documentation

See [PROJECT_SUMMARY.md](PROJECT_SUMMARY.md) for details.

---

## 🔧 Environment Configuration

All configuration is in `.env` (copy from `.env.example`):

**Required:**
```bash
SITE_URL=https://yourdomain.com
CORS_ORIGINS=*
```

**Optional AI:**
```bash
OPENROUTER_API_KEY=sk-or-v1-...  # Get free at openrouter.ai
DEFAULT_AI_MODEL=anthropic/claude-3.5-sonnet
```

**Optional Limits:**
```bash
MAX_FILE_SIZE_MB=100
GITHUB_USERNAME=ajokhai
```

See `.env.example` for all options with documentation.

---

## 📖 File Index

### Configuration
- **`.env.example`** ← Start here! Copy to `.env`
- `requirements.txt` - Python dependencies
- `Dockerfile` - Docker build config
- `docker-compose.yml` - Local Docker setup
- `render.yaml` - Render.com config

### Documentation  
- **`README.md`** ← Main documentation
- `SETUP.md` - Setup instructions
- `API.md` - API reference
- `DEPLOYMENT.md` - Deployment guides
- `SIMPLE_GUIDE.md` - Beginner tutorial
- `CONTRIBUTING.md` - How to contribute
- `CHECKLIST.md` - Quick reference
- `PROJECT_SUMMARY.md` - What changed
- `FILES.md` - File index

### Code
- `main.py` - FastAPI application
- `app/config.py` - Reads `.env`
- `app/converter.py` - CAD conversion
- `app/ai_analysis.py` - AI features
- `app/metadata.py` - Metadata extraction
- `app/models.py` - Request/response schemas

---

## 🚢 Deployment Options

### Option 1: Render.com (Free)
```
1. Fork repo on GitHub
2. Sign up at render.com
3. New Web Service → select repo
4. Add environment variables
5. Deploy!
```
[Full guide](DEPLOYMENT.md#option-1-rendercom-recommended-free-tier-available)

### Option 2: Railway.app (Free Credits)
```
1. Fork repo
2. Sign up at railway.app
3. Deploy from GitHub
4. Add environment variables
5. Generate domain
```
[Full guide](DEPLOYMENT.md#option-2-railwayapp-simple-free-tier-available)

### Option 3: Docker (Self-Hosted)
```bash
docker-compose up -d
```
[Full guide](DEPLOYMENT.md#option-3-self-hosted-with-docker)

---

## 🧪 Test Your Deployment

```bash
# Health check
curl https://your-api.com/health

# Should return:
{
  "status": "ok",
  "authors": "Josh Ayokhai, River",
  "repository": "https://github.com/ajokhai/cad-converter"
}
```

---

## 💡 Common Use Cases

### 1. Convert Single File
Upload file to S3/R2, then:
```javascript
fetch('https://api.com/api/convert', {
  method: 'POST',
  body: JSON.stringify({
    fileUrl: 'https://storage.com/part.step',
    fileType: 'step'
  })
})
```

### 2. With AI Analysis
```javascript
body: JSON.stringify({
  fileUrl: 'https://storage.com/part.step',
  fileType: 'step',
  aiModel: 'anthropic/claude-3.5-sonnet',
  apiKey: 'sk-or-v1-...'
})
```

### 3. Batch + BOM
```javascript
body: JSON.stringify({
  files: [...],
  generateBOM: true,
  apiKey: 'sk-or-v1-...'
})
```

See [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md) for detailed examples.

---

## 🆘 Need Help?

**Issues?** https://github.com/ajokhai/cad-converter/issues  
**Questions?** https://github.com/ajokhai/cad-converter/discussions

**Common Problems:**
- Can't build? → Check Docker logs
- CORS errors? → Set `CORS_ORIGINS` in `.env`
- AI not working? → Verify OpenRouter API key
- See [SETUP.md](SETUP.md#troubleshooting) for more

---

## 🎁 What You Get

✅ **Fast 3D Conversion** - STEP/STL to glTF  
✅ **AI-Powered BOM** - Smart part categorization  
✅ **Batch Processing** - Handle multiple files  
✅ **Easy Deployment** - Multiple platforms supported  
✅ **Well Documented** - Comprehensive guides  
✅ **Open Source** - MIT License

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📦 What's Included

```
📁 cad-converter/
├── 📄 .env.example          ← Copy to .env
├── 🐳 docker-compose.yml    ← docker-compose up
├── 📝 README.md             ← Main docs
├── 🔧 SETUP.md              ← Setup guide
├── 📡 API.md                ← API reference
├── 🚀 DEPLOYMENT.md         ← Deploy guides
├── 🎓 SIMPLE_GUIDE.md       ← Easy tutorial
├── ✅ CHECKLIST.md          ← Quick reference
├── 💻 main.py               ← FastAPI app
└── 📂 app/                  ← Source code
```

---

## 🎯 Next Steps

1. **Setup:** [SETUP.md](SETUP.md)
2. **Deploy:** [DEPLOYMENT.md](DEPLOYMENT.md)
3. **Use API:** [API.md](API.md)
4. **Learn More:** [SIMPLE_GUIDE.md](SIMPLE_GUIDE.md)

---

**Built with ❤️ by Josh Ayokhai & River**

*Making CAD file processing accessible to everyone*

---

**Last Updated:** December 2024  
**Version:** 1.0.0  
**License:** MIT
