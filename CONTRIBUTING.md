# Contributing to CAD Converter API

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

Thank you for considering contributing to this project! 🎉

---

## How to Contribute

### Reporting Bugs

Found a bug? Please [open an issue](https://github.com/ajokhai/cad-converter/issues) with:

- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, Docker version)
- Relevant logs or error messages

### Suggesting Features

Have an idea? [Open an issue](https://github.com/ajokhai/cad-converter/issues) with:

- Clear description of the feature
- Use cases / why it's valuable
- Possible implementation approach (optional)

### Submitting Pull Requests

1. **Fork the repository**
   ```bash
   # Click "Fork" on GitHub, then:
   git clone https://github.com/YOUR-USERNAME/cad-converter.git
   cd cad-converter
   ```

2. **Create a branch**
   ```bash
   git checkout -b feature/your-feature-name
   # or
   git checkout -b fix/your-bug-fix
   ```

3. **Set up development environment**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   
   # Install dependencies
   pip install -r requirements.txt
   ```

4. **Make your changes**
   - Follow existing code style
   - Add comments for complex logic
   - Update documentation if needed

5. **Test your changes**
   ```bash
   # Run the server
   uvicorn main:app --reload --port 8080
   
   # Test manually or write tests
   curl http://localhost:8080/health
   ```

6. **Update configuration if needed**
   - If you add new environment variables, update `.env.example`
   - Document them in README.md
   - Update config.py

7. **Commit your changes**
   ```bash
   git add .
   git commit -m "feat: add support for XYZ format"
   # or
   git commit -m "fix: resolve CORS issue with OPTIONS requests"
   ```

   **Commit message format:**
   - `feat:` - New feature
   - `fix:` - Bug fix
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding tests
   - `chore:` - Maintenance tasks

8. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   
   Then go to GitHub and create a Pull Request with:
   - Clear title and description
   - Reference any related issues
   - Screenshots/examples if applicable

---

## Development Guidelines

### Code Style

- Follow PEP 8 for Python code
- Use type hints where appropriate
- Keep functions focused and small
- Add docstrings to functions/classes

**Example:**
```python
async def process_file(
    file_url: str,
    file_type: str,
    options: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """
    Process a CAD file and return results.
    
    Args:
        file_url: Public URL to the CAD file
        file_type: Type of file (step, stp, stl)
        options: Optional processing options
        
    Returns:
        Dictionary with processing results
        
    Raises:
        HTTPException: If processing fails
    """
    # Implementation...
```

### Adding New Environment Variables

1. **Add to `.env.example`** with documentation:
   ```bash
   # Description of what this does
   NEW_VARIABLE=default_value
   ```

2. **Add to `config.py`**:
   ```python
   NEW_VARIABLE = os.getenv("NEW_VARIABLE", "default_value")
   ```

3. **Document in README.md** under "Environment Variables"

4. **Update SETUP.md** if it affects setup process

### Adding New File Formats

1. **Update `config.py`**:
   ```python
   SUPPORTED_FORMATS = ["step", "stp", "stl", "new_format"]
   ```

2. **Add converter in `converter.py`**:
   ```python
   def convert_new_format_to_stl(input_path, output_path):
       # Implementation
   ```

3. **Update `main.py`** to handle new format

4. **Update documentation** in README.md and API.md

### Adding New AI Features

1. **Add function to `ai_analysis.py`**
2. **Update models in `models.py`** if new request/response fields needed
3. **Update API endpoints in `main.py`**
4. **Document in API.md**

---

## Project Structure

```
├── .env.example          # Environment template (update if adding vars)
├── main.py              # Main FastAPI app (add endpoints here)
├── app/
│   ├── __init__.py
│   ├── config.py        # Configuration (add env vars here)
│   ├── models.py        # Pydantic models (add request/response schemas)
│   ├── metadata.py      # Metadata extraction
│   ├── converter.py     # CAD conversion (add format handlers)
│   └── ai_analysis.py   # AI features (add AI functions)
├── requirements.txt     # Python dependencies
├── Dockerfile           # Docker build config
├── docker-compose.yml   # Local development
├── render.yaml          # Render deployment config
└── docs/
    ├── README.md        # Main documentation
    ├── API.md           # API reference
    ├── DEPLOYMENT.md    # Deployment guide
    ├── SETUP.md         # Setup instructions
    └── SIMPLE_GUIDE.md  # Beginner tutorial
```

---

## Testing

### Manual Testing

```bash
# Start server
uvicorn main:app --reload --port 8080

# Test health endpoint
curl http://localhost:8080/health

# Test conversion (replace with real file URL)
curl -X POST http://localhost:8080/api/convert \
  -H "Content-Type: application/json" \
  -d '{
    "fileUrl": "https://example.com/test.step",
    "fileType": "step"
  }'
```

### Docker Testing

```bash
# Build and run
docker-compose up -d

# Check logs
docker-compose logs -f

# Test
curl http://localhost:8080/health

# Clean up
docker-compose down
```

---

## Documentation

When making changes, update relevant docs:

- **README.md** - Overview, quick start, main features
- **API.md** - Endpoint details, request/response schemas
- **DEPLOYMENT.md** - Deployment instructions
- **SETUP.md** - Setup process
- **SIMPLE_GUIDE.md** - Beginner-friendly explanations
- **.env.example** - New environment variables
- **CONTRIBUTING.md** - This file

---

## Questions?

- Open a [Discussion](https://github.com/ajokhai/cad-converter/discussions)
- Check existing [Issues](https://github.com/ajokhai/cad-converter/issues)
- Read the [documentation](https://github.com/ajokhai/cad-converter)

---

## Code of Conduct

- Be respectful and constructive
- Welcome newcomers and help them learn
- Focus on the problem, not the person
- Give credit where credit is due

---

Thank you for contributing! 🙏

Josh Ayokhai & River
