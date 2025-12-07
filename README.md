# CAD Converter Microservice for FamilyMake

Converts CAD files (STEP/STP) to glTF for 3D preview and extracts metadata for BOM generation.

## Features

- **3D Conversion**: STEP → STL → glTF for web rendering
- **Metadata Extraction**: Part name, number, author, organization, description
- **Dimension Calculation**: Length, width, height, volume
- **File Size Limits**: Configurable (default 100MB)
- **Two Endpoints**: Full conversion or metadata-only (faster)

## API Endpoints

### POST `/api/convert`
Full conversion with 3D preview + metadata

**Request:**
```json
{
  "fileUrl": "https://example.com/part.step",
  "fileType": "step"
}
```

**Response:**
```json
{
  "success": true,
  "gltf": { /* glTF JSON for Three.js */ },
  "metadata": {
    "part_name": "Housing_V2",
    "part_number": "PN-12345",
    "author": "John Doe",
    "organization": "ACME Corp",
    "description": "Main housing component",
    "timestamp": "2024-01-15T10:30:00"
  },
  "dimensions": {
    "length": 150.5,
    "width": 75.2,
    "height": 40.0,
    "volume": 452100.5,
    "units": "mm"
  },
  "fileSize": 2.3
}
```

### POST `/api/metadata`
Metadata extraction only (no 3D conversion, faster/cheaper)

**Request:**
```json
{
  "fileUrl": "https://example.com/part.step",
  "fileType": "step"
}
```

**Response:**
```json
{
  "success": true,
  "metadata": {
    "part_name": "Housing_V2",
    "part_number": "PN-12345",
    "author": "John Doe",
    "organization": "ACME Corp",
    "description": "Main housing component"
  },
  "filename": "part.step"
}
```

### GET `/health`
Health check endpoint

### GET `/api/limits`
Returns service limits and supported formats

## Deployment

### Render.com
1. Push to GitHub
2. Connect to Render
3. Render will use `render.yaml` automatically
4. Build takes ~5-10 minutes (installing OpenCascade)

### Local Development
```bash
docker build -t cad-converter .
docker run -p 8080:8080 cad-converter
```

## Environment Variables

- `MAX_FILE_SIZE_MB`: Maximum file size in MB (default: 100)

## Usage in FamilyMake

### For 3D Preview + BOM:
```javascript
const response = await fetch('https://your-render-url.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: uploadedFileUrl,
    fileType: 'step'
  })
});

const { gltf, metadata, dimensions } = await response.json();
// Load gltf in Three.js
// Use metadata for BOM generation
```

### For BOM Only (faster):
```javascript
const response = await fetch('https://your-render-url.onrender.com/api/metadata', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: uploadedFileUrl,
    fileType: 'step'
  })
});

const { metadata } = await response.json();
// Generate BOM row with metadata
```

## BOM Generation Strategy

**What you'll get from files:**
- ✅ Part name (often from filename or FILE_NAME entity)
- ✅ Dimensions (calculated from geometry)
- ✅ Author/Organization (if embedded)
- ⚠️ Part number (sometimes embedded, often missing)
- ❌ Manufacturer ID (rarely embedded)
- ❌ Product URL (never embedded)
- ❌ Unit cost (never embedded)

**Recommended BOM workflow:**
1. Extract what's available from CAD files
2. Use filename parsing as fallback for part name
3. Provide manual input fields for missing data
4. Store user's manual entries for future uploads
5. Future: AI-powered part recognition from geometry

## Notes

- STEP files are text-based ISO 10303 format
- Metadata availability varies widely by CAD software
- SolidWorks, Fusion 360, OnShape typically have better metadata
- Generic STEP exporters often strip custom properties
- Many files will require manual BOM data entry
