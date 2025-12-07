# Project Summary - CAD Converter API

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

---

## What Changed

This update consolidates all configuration into a single `.env` file, making the project much easier to customize and deploy.

### Before

Configuration was scattered across multiple files:
- Hardcoded URLs in `ai_analysis.py`
- Hardcoded GitHub username in `config.py`
- Multiple files needed editing for customization
- No clear documentation on what to change

### After

**Single source of truth:** `.env` file
- All customizable values in one place
- Clear documentation in `.env.example`
- No need to search through code
- Environment-specific configuration
- Proper attribution to both authors

---

## Project Structure

```
cad-converter/
├── .env.example              ← Copy this to .env and configure
├── .gitignore                ← Prevents .env from being committed
├── main.py                   ← FastAPI application
├── requirements.txt          ← Python dependencies
├── Dockerfile                ← Docker build configuration
├── docker-compose.yml        ← Local development setup
├── render.yaml              ← Render.com deployment config
├── LICENSE                   ← MIT License
│
├── app/                      ← Application code
│   ├── __init__.py          ← Package initialization
│   ├── config.py            ← Reads from .env
│   ├── models.py            ← Request/response schemas
│   ├── metadata.py          ← Metadata extraction
│   ├── converter.py         ← CAD file conversion
│   └── ai_analysis.py       ← AI-powered BOM generation
│
└── docs/                     ← Documentation
    ├── README.md            ← Main documentation
    ├── SETUP.md             ← Setup instructions
    ├── API.md               ← API reference
    ├── DEPLOYMENT.md        ← Deployment guide
    ├── SIMPLE_GUIDE.md      ← Beginner tutorial
    └── CONTRIBUTING.md      ← Contribution guidelines
```

---

## Configuration System

### .env.example (Template)

Contains all configurable variables with:
- Clear descriptions
- Default values
- Usage examples
- Grouping by category

### config.py (Reads .env)

Centralizes all configuration:
- Reads from environment variables
- Provides sensible defaults
- Type conversion (string → int, etc.)
- Exports to rest of application

### Environment Variables

**Required:**
- `SITE_URL` - Your website URL
- `CORS_ORIGINS` - Allowed domains

**Optional:**
- `MAX_FILE_SIZE_MB` - File size limit
- `OPENROUTER_API_KEY` - For AI features
- `DEFAULT_AI_MODEL` - AI model preference
- `GITHUB_USERNAME` - Attribution
- And more...

---

## Key Features

### 1. Environment-Based Configuration

```bash
# Development
CORS_ORIGINS=*
DEBUG=true

# Production
CORS_ORIGINS=https://yourdomain.com
DEBUG=false
```

### 2. No Hardcoded Values

All these are now configurable:
- GitHub username/repo
- Site URLs
- Timeouts
- File size limits
- AI models
- Debug settings

### 3. Easy Deployment

**Render/Railway:**
1. Fork repo
2. Add environment variables from `.env.example`
3. Deploy

**Docker:**
```bash
docker run --env-file .env cad-converter
```

**Local:**
```bash
cp .env.example .env
# Edit .env
uvicorn main:app --reload
```

### 4. Proper Attribution

Both authors credited in:
- All Python files (headers)
- Documentation
- API health endpoint
- Configuration files

---

## Documentation

### README.md
- Quick start guide
- Environment variables reference
- Deployment options
- Usage examples

### SETUP.md
- Detailed setup instructions
- Environment variables explained
- Troubleshooting guide
- Testing procedures

### API.md
- Complete endpoint reference
- Request/response schemas
- Error handling
- Examples

### DEPLOYMENT.md
- Platform-specific deployment guides
- Environment variable configuration
- Monitoring and scaling
- Security best practices

### SIMPLE_GUIDE.md
- Beginner-friendly explanations
- Step-by-step tutorials
- Real-world examples
- Common questions

### CONTRIBUTING.md
- How to contribute
- Development guidelines
- Code style
- Testing procedures

---

## Usage

### Quick Start

```bash
# 1. Copy environment template
cp .env.example .env

# 2. Edit your settings
nano .env

# 3. Run with Docker
docker-compose up -d

# Or run with Python
pip install -r requirements.txt
uvicorn main:app --reload
```

### Example .env

```bash
# Required
SITE_URL=https://familymake.com
CORS_ORIGINS=https://familymake.com,https://app.familymake.com

# Optional
MAX_FILE_SIZE_MB=100
OPENROUTER_API_KEY=sk-or-v1-...
DEFAULT_AI_MODEL=anthropic/claude-3.5-sonnet
GITHUB_USERNAME=ajokhai
```

---

## For Developers

### Adding New Configuration

1. **Add to `.env.example`:**
   ```bash
   # Description
   NEW_CONFIG=default_value
   ```

2. **Add to `config.py`:**
   ```python
   NEW_CONFIG = os.getenv("NEW_CONFIG", "default_value")
   ```

3. **Document in README.md**

4. **Update SETUP.md** if needed

### Code Changes

All Python files now include:
- Author attribution
- Proper imports from config
- No hardcoded values
- Type hints
- Docstrings

---

## Benefits

### For Users

✅ Single file to configure (`.env`)  
✅ Clear documentation  
✅ No code editing required  
✅ Environment-specific settings  
✅ Secure (`.env` not committed)

### For Developers

✅ Centralized configuration  
✅ Easy to extend  
✅ Type-safe  
✅ Well-documented  
✅ Consistent across codebase

### For Deployment

✅ Works with any platform  
✅ Environment variables standard  
✅ Docker-friendly  
✅ Easy to test locally

---

## Migration Guide

If you have an existing deployment:

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Copy your current settings:**
   ```bash
   # If you had these set
   MAX_FILE_SIZE_MB=200
   CORS_ORIGINS=https://myapp.com
   ```

3. **Update deployment:**
   - Render: Add env vars in dashboard
   - Railway: Add in Variables tab
   - Docker: Use `--env-file .env`

4. **Remove old hardcoded values** (if you customized code)

---

## Testing

```bash
# Health check
curl http://localhost:8080/health

# Should show:
{
  "status": "ok",
  "authors": "Josh Ayokhai, River",
  "repository": "https://github.com/ajokhai/cad-converter"
}
```

---

## Next Steps

1. **Review `.env.example`** - Understand all options
2. **Read SETUP.md** - Detailed setup instructions
3. **Check DEPLOYMENT.md** - Deploy to cloud
4. **See SIMPLE_GUIDE.md** - Learn to use the API

---

## Support

- **Issues:** https://github.com/ajokhai/cad-converter/issues
- **Discussions:** https://github.com/ajokhai/cad-converter/discussions
- **Documentation:** All `.md` files in the repo

---

Built with ❤️ by Josh Ayokhai & River

*Making CAD file processing accessible to everyone*
