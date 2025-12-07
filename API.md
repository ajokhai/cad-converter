# API Documentation

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

Complete reference for all endpoints.

## Base URL

```
https://your-service.onrender.com
```

## Authentication

No authentication required for the service itself. However, AI features require an OpenRouter API key that you pass in requests.

---

## Endpoints

### Health Check

**GET** `/health`

Check if the service is running and CAD libraries are installed.

**Response:**
```json
{
  "status": "ok",
  "cadLibraries": true,
  "maxFileSizeMB": 100,
  "authors": "Josh Ayokhai, River",
  "repository": "https://github.com/ajokhai/cad-converter"
}
```

---

### Get Limits

**GET** `/api/limits`

Get service capabilities and limits.

**Response:**
```json
{
  "maxFileSizeMB": 100,
  "supportedFormats": ["step", "stp", "stl"],
  "supportedAIModels": [
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-opus",
    "openai/gpt-4-turbo",
    "openai/gpt-4o",
    "google/gemini-pro-1.5"
  ]
}
```

---

### Convert Single File

**POST** `/api/convert`

Convert a single CAD file to glTF with optional AI analysis.

**Request Body:**
```json
{
  "fileUrl": "https://example.com/part.step",
  "fileType": "step",
  "aiModel": "anthropic/claude-3.5-sonnet",  // optional
  "apiKey": "sk-or-v1-..."  // optional, required for AI
}
```

**Parameters:**
- `fileUrl` (string, required) - Public URL to the CAD file
- `fileType` (string, required) - File type: "step", "stp", or "stl"
- `aiModel` (string, optional) - OpenRouter model identifier
- `apiKey` (string, optional) - Your OpenRouter API key

**Response:**
```json
{
  "success": true,
  "filename": "part.step",
  "gltf": {
    // glTF JSON object
  },
  "metadata": {
    "part_name": "Housing_V2",
    "part_number": "PN-12345",
    "author": "John Doe",
    "organization": "ACME Corp",
    "description": "Main housing",
    "timestamp": "2024-01-15T10:30:00"
  },
  "dimensions": {
    "length": 150.5,
    "width": 75.2,
    "height": 40.0,
    "volume": 452100.5,
    "units": "mm"
  },
  "ai_analysis": {  // Only if apiKey provided
    "part_name": "Main Housing Component",
    "part_number": "HOUS-V2-001",
    "description": "Injection molded housing",
    "category": "mechanical",
    "material": "ABS Plastic",
    "quantity": 1,
    "manufacturer": "TBD",
    "notes": "Requires post-processing",
    "confidence": "high"
  }
}
```

---

### Batch Convert Files

**POST** `/api/batch-convert`

Process multiple CAD files at once, with optional AI-powered BOM generation.

**Request Body:**
```json
{
  "files": [
    {
      "fileUrl": "https://example.com/part1.step",
      "fileType": "step",
      "fileName": "housing.step"  // optional, for better AI analysis
    },
    {
      "fileUrl": "https://example.com/part2.step",
      "fileType": "step",
      "fileName": "bracket.step"
    }
  ],
  "aiModel": "anthropic/claude-3.5-sonnet",  // optional
  "apiKey": "sk-or-v1-...",  // optional
  "extractMetadata": true,  // default: true
  "generatePreview": true,  // default: true, set false to skip 3D
  "generateBOM": false  // default: false, set true for AI BOM generation
}
```

**Parameters:**
- `files` (array, required) - List of files to process
  - `fileUrl` (string) - Public URL to file
  - `fileType` (string) - "step", "stp", or "stl"
  - `fileName` (string, optional) - Override filename
- `aiModel` (string, optional) - OpenRouter model
- `apiKey` (string, optional) - Your OpenRouter API key
- `extractMetadata` (boolean) - Extract raw metadata from files
- `generatePreview` (boolean) - Generate 3D previews (skip for BOM-only)
- `generateBOM` (boolean) - Generate complete BOM using AI

**Response:**
```json
{
  "success": true,
  "total_files": 2,
  "processed": 2,
  "failed": 0,
  "files": [
    {
      "filename": "housing.step",
      "file_type": "step",
      "success": true,
      "metadata": { /* ... */ },
      "dimensions": { /* ... */ },
      "gltf": { /* ... */ },
      "ai_analysis": { /* ... */ }  // if apiKey provided
    },
    // ... more files
  ],
  "bom": {  // Only if generateBOM: true
    "bom_name": "Main Assembly BOM",
    "total_parts": 2,
    "parts": [
      {
        "line_number": 1,
        "part_number": "HOUS-001",
        "part_name": "Main Housing",
        "description": "Injection molded housing",
        "quantity": 1,
        "category": "mechanical",
        "material": "ABS Plastic",
        "manufacturer": "TBD",
        "estimated_cost": null,
        "notes": "Primary structural component"
      },
      // ... more parts
    ],
    "assembly_notes": "Notes about the assembly",
    "missing_information": ["List of missing data"]
  }
}
```

---

### Extract Metadata Only

**POST** `/api/metadata`

Extract metadata without 3D conversion. Much faster if you only need BOM data.

**Request Body:**
```json
{
  "fileUrl": "https://example.com/part.step",
  "fileType": "step",
  "aiModel": "anthropic/claude-3.5-sonnet",  // optional
  "apiKey": "sk-or-v1-..."  // optional
}
```

**Response:**
```json
{
  "success": true,
  "filename": "part.step",
  "metadata": {
    "part_name": "Housing_V2",
    "part_number": "PN-12345",
    // ... more metadata
  },
  "ai_analysis": {  // Only if apiKey provided
    // ... AI-extracted data
  }
}
```

---

## Error Responses

All endpoints return errors in this format:

```json
{
  "detail": "Error message here"
}
```

**Common Status Codes:**
- `400` - Bad request (invalid parameters)
- `413` - File too large
- `500` - Server error (conversion failed, AI error, etc.)

---

## AI Analysis Details

When you provide an `apiKey`, the service sends file data to OpenRouter AI which:

1. Analyzes raw metadata, filename, and dimensions
2. Makes intelligent inferences about missing data
3. Categorizes parts (mechanical, fastener, electronic, etc.)
4. Suggests materials based on typical use cases
5. Proposes part numbers if missing
6. Returns confidence level (high/medium/low)

**What AI Can Infer:**
- Part categories from filenames and dimensions
- Materials from naming conventions
- Whether parts are fasteners (based on size)
- Reasonable part number formats
- Part relationships (in batch mode)

**What AI Cannot Do:**
- Access manufacturer databases
- Verify if part numbers are real
- Get real-time pricing
- Determine exact materials without specs

---

## Rate Limits

No rate limits on the service itself.

OpenRouter has its own rate limits per API key (check OpenRouter docs).

---

## File Size Limits

Default: 100MB per file

Can be configured with `MAX_FILE_SIZE_MB` environment variable.

---

## Tips for Best Results

1. **Use descriptive filenames** - AI uses these heavily
   - Good: `bracket_aluminum_v2.step`
   - Bad: `part1.step`

2. **Batch related files together** - AI can detect duplicates and relationships

3. **Skip 3D if only need BOM** - Set `generatePreview: false` for faster processing

4. **Use metadata endpoint for speed** - If you don't need 3D at all

5. **Choose AI model wisely**:
   - Sonnet: Best balance of speed/quality
   - Opus: Best quality, slower, more expensive
   - GPT-4: Good alternative to Claude
   - Gemini: Cheapest option

---

## Example Integration

```javascript
// Upload file to your storage
const fileUrl = await uploadToS3(file);

// Convert with AI
const response = await fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: fileUrl,
    fileType: 'step',
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: user.openRouterKey
  })
});

const result = await response.json();

// Use the results
displayIn3DViewer(result.gltf);  // Three.js viewer
populateBOMTable(result.ai_analysis);  // BOM form
```

---

## OpenRouter Setup

1. Go to https://openrouter.ai/
2. Sign up (free)
3. Go to "Keys" → "Create Key"
4. Copy your API key (starts with `sk-or-v1-`)
5. Pass it in the `apiKey` parameter

**Costs** (approximate):
- Claude Sonnet: $3 per million tokens (~$0.01-0.03 per file)
- Claude Opus: $15/$75 per million tokens (~$0.05-0.15 per file)
- GPT-4 Turbo: $10/$30 per million tokens
- Gemini Pro: $0.125/$0.375 per million tokens (cheapest)
