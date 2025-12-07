from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import httpx
import tempfile
import os
import json
import re

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


def extract_step_metadata(file_path):
    """Extract metadata from STEP file for BOM generation"""
    metadata = {
        'part_name': None,
        'part_number': None,
        'author': None,
        'organization': None,
        'description': None,
        'timestamp': None,
        'material': None,
        'custom_properties': {}
    }
    
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(10000)  # Read first 10KB for header info
            
            # Extract FILE_NAME entity
            # FILE_NAME('filename','2024-01-01T12:00:00',('author'),('organization'),'preprocessor','originating_system','authorization');
            file_name_pattern = r"FILE_NAME\s*\(\s*'([^']*)'.*?\('([^']*)'\)\s*,\s*\('([^']*)'\)"
            match = re.search(file_name_pattern, content)
            if match:
                metadata['part_name'] = match.group(1).strip("'")
                metadata['author'] = match.group(2).strip("'")
                metadata['organization'] = match.group(3).strip("'")
            
            # Extract FILE_DESCRIPTION
            desc_pattern = r"FILE_DESCRIPTION\s*\(\s*\('([^']*)'\)"
            desc_match = re.search(desc_pattern, content)
            if desc_match:
                metadata['description'] = desc_match.group(1)
            
            # Look for PRODUCT entities (contains part numbers often)
            product_pattern = r"PRODUCT\s*\(\s*'([^']*)'.*?'([^']*)'"
            product_match = re.search(product_pattern, content)
            if product_match:
                if not metadata['part_number']:
                    metadata['part_number'] = product_match.group(1)
                if not metadata['part_name']:
                    metadata['part_name'] = product_match.group(2)
            
            # Extract timestamp from FILE_NAME if present
            timestamp_pattern = r"'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'"
            timestamp_match = re.search(timestamp_pattern, content)
            if timestamp_match:
                metadata['timestamp'] = timestamp_match.group(1)
    
    except Exception as e:
        print(f"Metadata extraction warning: {e}")
    
    return metadata


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
            # Extract metadata first (before conversion)
            metadata = extract_step_metadata(input_path)
            
            # Import the STEP file (IGES support can be added if needed)
            if request.fileType.lower() in ["step", "stp"]:
                result = cq.importers.importStep(input_path)
            else:
                raise HTTPException(400, f"File type '{request.fileType}' not supported yet")
            
            # Export to STL first (intermediate format)
            cq.exporters.export(result, stl_path)
            
            # Load STL with trimesh
            mesh = trimesh.load(stl_path)
            
            # Calculate volume/dimensions for BOM
            bounds = mesh.bounds
            dimensions = {
                'length': float(bounds[1][0] - bounds[0][0]),
                'width': float(bounds[1][1] - bounds[0][1]),
                'height': float(bounds[1][2] - bounds[0][2]),
                'volume': float(mesh.volume) if hasattr(mesh, 'volume') else None,
                'units': 'mm'  # CadQuery defaults to mm
            }
            
            # Convert to GLTF
            mesh.export(gltf_path, file_type='gltf')
            
            # Read the GLTF file
            with open(gltf_path, 'r') as f:
                gltf_json = json.load(f)
            
            return {
                "success": True,
                "gltf": gltf_json,
                "metadata": metadata,  # BOM data
                "dimensions": dimensions,  # Physical specs
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
                    

@app.post("/api/metadata")
async def extract_metadata_only(request: ConversionRequest):
    """Extract BOM metadata without 3D conversion (faster/cheaper)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                request.fileUrl, 
                timeout=30.0,
                follow_redirects=True
            )
            response.raise_for_status()
            file_content = response.content
        
        with tempfile.NamedTemporaryFile(
            suffix=f".{request.fileType}", 
            delete=False
        ) as tmp_input:
            tmp_input.write(file_content)
            input_path = tmp_input.name
        
        try:
            metadata = extract_step_metadata(input_path)
            
            return {
                "success": True,
                "metadata": metadata,
                "filename": os.path.basename(request.fileUrl)
            }
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
                
    except Exception as e:
        raise HTTPException(500, f"Metadata extraction failed: {str(e)}")


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
