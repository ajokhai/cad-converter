from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import tempfile
import os
import json

# Use cadquery for STEP conversion
try:
    import cadquery as cq
    import trimesh
    CAD_AVAILABLE = True
except ImportError:
    CAD_AVAILABLE = False

app = FastAPI(title="CAD Conversion Service")

# Configurable via environment variable
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Lock down to your domain in production
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

class ConversionRequest(BaseModel):
    fileUrl: str
    fileType: str  # "step" or "iges"

@app.post("/api/convert")
async def convert_cad(request: ConversionRequest):
    if not CAD_AVAILABLE:
        raise HTTPException(500, "CAD libraries not installed")
    
    try:
        # Download with size check
        async with httpx.AsyncClient() as client:
            # First, HEAD request to check size without downloading
            head_response = await client.head(request.fileUrl, timeout=10.0)
            content_length = head_response.headers.get('content-length')
            
            if content_length:
                file_size_mb = int(content_length) / 1024 / 1024
                if int(content_length) > MAX_FILE_SIZE:
                    raise HTTPException(
                        413,  # Payload Too Large
                        f"File size ({file_size_mb:.1f}MB) exceeds limit of {MAX_FILE_SIZE_MB}MB. "
                        "Larger files require enterprise tier."
                    )
            
            # Download the file
            response = await client.get(
                request.fileUrl, 
                timeout=120.0,  # 2 minutes for download
                follow_redirects=True
            )
            response.raise_for_status()
            file_content = response.content
            
            # Double-check actual size
            actual_size_mb = len(file_content) / 1024 / 1024
            if len(file_content) > MAX_FILE_SIZE:
                raise HTTPException(
                    413,
                    f"File size ({actual_size_mb:.1f}MB) exceeds limit of {MAX_FILE_SIZE_MB}MB"
                )
        
        # Create temp files
        with tempfile.NamedTemporaryFile(
            suffix=f".{request.fileType}", 
            delete=False
        ) as tmp_input:
            tmp_input.write(file_content)
            input_path = tmp_input.name
        
        stl_path = input_path.replace(f".{request.fileType}", ".stl")
        gltf_path = input_path.replace(f".{request.fileType}", ".gltf")
        
        try:
            # Import the STEP file (IGES support can be added if needed)
            if request.fileType.lower() in ["step", "stp"]:
                result = cq.importers.importStep(input_path)
            else:
                raise HTTPException(400, f"File type '{request.fileType}' not supported yet")
            
            # Export to STL first (intermediate format)
            cq.exporters.export(result, stl_path)
            
            # Load STL with trimesh
            mesh = trimesh.load(stl_path)
            
            # Convert to GLTF
            mesh.export(gltf_path, file_type='gltf')
            
            # Read the GLTF file
            with open(gltf_path, 'r') as f:
                gltf_json = json.load(f)
            
            return {
                "success": True,
                "gltf": gltf_json,
                "fileSize": actual_size_mb
            }
            
        finally:
            # Cleanup temp files
            for path in [input_path, stl_path, gltf_path]:
                if os.path.exists(path):
                    try:
                        os.unlink(path)
                    except:
                        pass
                    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Conversion failed: {str(e)}")

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "cadLibraries": CAD_AVAILABLE,
        "maxFileSizeMB": MAX_FILE_SIZE_MB
    }

@app.get("/api/limits")
async def get_limits():
    return {
        "maxFileSizeMB": MAX_FILE_SIZE_MB,
        "supportedFormats": ["step", "stp"]
    }
