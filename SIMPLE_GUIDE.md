# How to Use This (Explain Like I'm 5)

**Authors:** Josh Ayokhai & River  
**GitHub:** https://github.com/ajokhai/cad-converter

This service turns CAD files into 3D models you can view in a web browser, and can use AI to help you make parts lists (Bills of Materials).

## The Problem This Solves

You have CAD files (`.step` or `.stl`) and you want to:
1. Show them as 3D previews on your website
2. Get information about the parts (names, sizes, materials)
3. Make a parts list (BOM) automatically

Normally this is hard. This service makes it easy.

---

## How It Works (Simple Version)

```
Your CAD file → This Service → 3D model + Part info
```

**Without AI:**
```
your-file.step → [Service] → {
  "Here's your 3D model!",
  "Part name: Housing",
  "Size: 150mm x 75mm x 40mm"
}
```

**With AI:**
```
your-file.step → [Service + AI] → {
  "Here's your 3D model!",
  "Part: Main Housing Component",
  "Category: Mechanical part",
  "Material: Probably ABS plastic",
  "Suggested part number: HOUS-001"
}
```

---

## Step-by-Step Tutorial

### Step 1: Upload Your CAD File Somewhere

Your CAD file needs to be accessible via a URL. Upload it to:
- AWS S3
- Cloudflare R2
- Google Cloud Storage
- Any file hosting service that gives you a public link

**Example:** You upload `bracket.step` and get:
```
https://my-storage.com/files/bracket.step
```

### Step 2: Call the API

**Super Simple (No AI):**

```javascript
fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: 'https://my-storage.com/files/bracket.step',
    fileType: 'step'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Got 3D model:', data.gltf);
  console.log('Part info:', data.metadata);
  console.log('Size:', data.dimensions);
});
```

**With AI (Smarter):**

```javascript
fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: 'https://my-storage.com/files/bracket.step',
    fileType: 'step',
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: 'sk-or-v1-YOUR-KEY-HERE'  // Get from openrouter.ai
  })
})
.then(response => response.json())
.then(data => {
  console.log('AI figured out:', data.ai_analysis);
  // {
  //   "part_name": "L-Bracket Mounting Component",
  //   "category": "mechanical",
  //   "material": "Aluminum 6061",
  //   "confidence": "high"
  // }
});
```

### Step 3: Use the Results

**Show the 3D model** (using Three.js):
```javascript
const loader = new GLTFLoader();
loader.parse(JSON.stringify(data.gltf), '', (gltf) => {
  scene.add(gltf.scene);
});
```

**Fill in a form** with the part info:
```javascript
document.getElementById('partName').value = data.ai_analysis.part_name;
document.getElementById('material').value = data.ai_analysis.material;
document.getElementById('category').value = data.ai_analysis.category;
```

---

## What You Get Back

### Without AI:
```json
{
  "success": true,
  "gltf": { /* 3D model data */ },
  "metadata": {
    "part_name": "bracket",  // From filename
    "part_number": null,     // Usually empty
    "author": null,
    "organization": null
  },
  "dimensions": {
    "length": 50.0,
    "width": 25.0,
    "height": 10.0,
    "volume": 12500.0,
    "units": "mm"
  }
}
```

### With AI:
```json
{
  // ... same as above, plus:
  "ai_analysis": {
    "part_name": "L-Bracket Mounting Component",
    "part_number": "BRKT-L-001",  // AI suggested this
    "description": "Aluminum L-bracket for mounting",
    "category": "mechanical",
    "material": "Aluminum 6061",  // AI guessed from context
    "quantity": 1,
    "manufacturer": "TBD",
    "notes": "Standard right-angle bracket",
    "confidence": "high"  // How sure the AI is
  }
}
```

---

## Processing Multiple Files (Batch)

If you have many parts:

```javascript
fetch('https://your-api.onrender.com/api/batch-convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    files: [
      { fileUrl: 'https://.../part1.step', fileType: 'step' },
      { fileUrl: 'https://.../part2.step', fileType: 'step' },
      { fileUrl: 'https://.../part3.step', fileType: 'step' }
    ],
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: 'sk-or-v1-...',
    generateBOM: true  // ← AI creates complete parts list
  })
})
.then(response => response.json())
.then(data => {
  // data.files = array of processed files
  // data.bom = complete Bill of Materials
  console.log('Complete BOM:', data.bom);
});
```

The AI will:
- Look at all files together
- Find duplicates (e.g., 8 identical screws → 1 line item with quantity: 8)
- Categorize parts
- Suggest part numbers
- Create a proper BOM table

---

## Getting an AI Key (Free)

1. Go to https://openrouter.ai/
2. Click "Sign In" (use Google/GitHub)
3. Go to "Keys" in the menu
4. Click "Create Key"
5. Copy the key (looks like `sk-or-v1-abc123...`)
6. Use it in the `apiKey` field

**Free credits:** You get $1 free credit to try it out.

**Costs after that:**
- ~1-3 cents per file with Claude Sonnet
- ~0.5-1 cent per file with Gemini
- Batch BOM generation: ~5-15 cents per batch

---

## Common Questions

**Q: Do I need AI?**

No! Without AI you still get:
- 3D model conversion ✓
- File metadata ✓
- Dimensions ✓

AI just makes the data smarter and fills in missing info.

**Q: Where does my CAD file go?**

1. You upload it to your storage (S3, etc.)
2. This service downloads it temporarily
3. Processes it
4. Deletes it immediately
5. Sends you back the results

Your file is never permanently stored by this service.

**Q: Can I use this without coding?**

Not directly - this is an API (code-only interface). But you could:
- Use tools like Postman to test it
- Ask ChatGPT to write the code for you
- Use low-code platforms like Zapier/Make.com

**Q: What if my file has no metadata?**

Most CAD files don't have much metadata embedded. That's why AI is helpful - it can:
- Read the filename: `"bracket_aluminum_v2.step"` → material: aluminum
- Look at dimensions: 3mm hole → probably an M3 screw
- Use common patterns: small parts with threads → fasteners

**Q: Is my API key safe?**

- This service never stores your API key
- It only uses it to call OpenRouter
- Each request passes the key, then forgets it
- You can rotate your key anytime at OpenRouter

**Q: What formats are supported?**

**Input:** STEP (.step, .stp), STL (.stl)

**Output:** glTF (for web 3D viewers like Three.js)

---

## Real-World Example

You're building a product catalog website:

```javascript
// User uploads CAD file to your site
const file = document.getElementById('fileInput').files[0];

// Upload to your S3 bucket
const fileUrl = await uploadToS3(file);

// Convert it
const result = await fetch('https://your-api.onrender.com/api/convert', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    fileUrl: fileUrl,
    fileType: 'step',
    aiModel: 'anthropic/claude-3.5-sonnet',
    apiKey: userSettings.openRouterKey
  })
}).then(r => r.json());

// Show 3D preview on product page
loadGLTFInViewer(result.gltf);

// Pre-fill product form with AI data
document.getElementById('name').value = result.ai_analysis.part_name;
document.getElementById('description').value = result.ai_analysis.description;
document.getElementById('category').value = result.ai_analysis.category;
document.getElementById('material').value = result.ai_analysis.material;

// User can edit if needed, then save to database
```

---

## Troubleshooting

**"File size exceeds limit"**
- File is too big (default limit: 100MB)
- Upload a smaller file or ask admin to increase limit

**"CAD libraries not installed"**
- Service didn't deploy correctly
- Check `/health` endpoint
- Redeploy the service

**"AI analysis failed"**
- Check your API key is valid
- Check you have OpenRouter credits
- Try a different AI model

**3D model looks wrong**
- Some STEP files are complex
- Try simplifying in your CAD software first
- Or just use metadata without 3D preview

---

## Tips for Best Results

1. **Name your files well**
   - Good: `housing_abs_plastic_v2.step`
   - Bad: `part1.step`

2. **Process related files together**
   - AI can see patterns across multiple files
   - Better duplicate detection

3. **Pick the right AI model**
   - Just trying it out? → Gemini (cheapest)
   - Production BOM? → Claude Sonnet (best balance)
   - Critical project? → Claude Opus (most capable)

4. **Skip 3D if you don't need it**
   - Set `generatePreview: false` in batch requests
   - Faster + cheaper

5. **Check AI confidence**
   - Look at the `confidence` field
   - "low" = you should double-check it
   - "high" = AI is pretty sure

---

## That's It!

You now know everything you need to use this service. If you get stuck, check the full [API Documentation](API.md) or file an issue on GitHub.
