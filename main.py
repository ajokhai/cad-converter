"""
CAD Converter API - Main application
Authors: Josh Ayokhai & River
GitHub: https://github.com/ajokhai/cad-converter
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import httpx
import tempfile
import os

from app.models import ConversionRequest, BatchConversionRequest
from app.metadata import extract_step_metadata, get_step_text_content
from app.converter import (
    convert_step_to_stl,
    convert_stl_to_gltf,
    calculate_dimensions,
    is_cad_available
)
from app.ai_analysis import analyze_file_with_ai, generate_bom_from_batch
from app.config import (
    MAX_FILE_SIZE_MB,
    MAX_FILE_SIZE,
    CORS_ORIGINS,
    SUPPORTED_FORMATS,
    SUPPORTED_AI_MODELS,
    SITE_URL,
    PROJECT_AUTHORS,
    GITHUB_USERNAME,
    GITHUB_REPO,
    DOWNLOAD_TIMEOUT,
    AI_TIMEOUT
)

app = FastAPI(
    title="CAD Converter API",
    description=f"Convert CAD files and generate BOMs with AI | Authors: {PROJECT_AUTHORS}",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "cadLibraries": is_cad_available(),
        "maxFileSizeMB": MAX_FILE_SIZE_MB,
        "authors": PROJECT_AUTHORS,
        "repository": f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}"
    }


@app.get("/api/limits")
async def get_limits():
    """Get service limits and capabilities"""
    return {
        "maxFileSizeMB": MAX_FILE_SIZE_MB,
        "supportedFormats": SUPPORTED_FORMATS,
        "supportedAIModels": SUPPORTED_AI_MODELS
    }


@app.post("/api/convert")
async def convert_cad(request: ConversionRequest):
    """Convert single CAD file with optional AI analysis"""
    if not is_cad_available():
        raise HTTPException(500, "CAD libraries not installed")
    
    try:
        # Download file
        async with httpx.AsyncClient() as client:
            head_response = await client.head(request.fileUrl, timeout=10.0)
            content_length = head_response.headers.get('content-length')
            
            if content_length and int(content_length) > MAX_FILE_SIZE:
                file_size_mb = int(content_length) / 1024 / 1024
                raise HTTPException(413, f"File size ({file_size_mb:.1f}MB) exceeds limit")
            
            response = await client.get(request.fileUrl, timeout=DOWNLOAD_TIMEOUT, follow_redirects=True)
            response.raise_for_status()
            file_content = response.content
        
        with tempfile.NamedTemporaryFile(suffix=f".{request.fileType}", delete=False) as tmp_input:
            tmp_input.write(file_content)
            input_path = tmp_input.name
        
        stl_path = input_path.replace(f".{request.fileType}", ".stl")
        gltf_path = input_path.replace(f".{request.fileType}", ".gltf")
        
        try:
            # Extract metadata
            metadata = extract_step_metadata(input_path)
            step_content = get_step_text_content(input_path)
            
            # Convert to 3D
            if request.fileType.lower() in ["step", "stp"]:
                convert_step_to_stl(input_path, stl_path)
            elif request.fileType.lower() == "stl":
                import shutil
                shutil.copy(input_path, stl_path)
            else:
                raise HTTPException(400, f"File type '{request.fileType}' not supported")
            
            # Calculate dimensions and convert to glTF
            dimensions = calculate_dimensions(stl_path)
            gltf_json = convert_stl_to_gltf(stl_path, gltf_path)
            
            response_data = {
                "success": True,
                "gltf": gltf_json,
                "metadata": metadata,
                "dimensions": dimensions,
                "filename": os.path.basename(request.fileUrl)
            }
            
            # AI Analysis if API key provided
            if request.apiKey:
                file_data = {
                    "filename": os.path.basename(request.fileUrl),
                    "file_type": request.fileType,
                    "metadata": metadata,
                    "dimensions": dimensions,
                    "step_content": step_content
                }
                
                ai_analysis = await analyze_file_with_ai(
                    file_data,
                    request.apiKey,
                    request.aiModel,
                    SITE_URL
                )
                response_data["ai_analysis"] = ai_analysis
            
            return response_data
            
        finally:
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


@app.post("/api/batch-convert")
async def batch_convert_cad(request: BatchConversionRequest):
    """Process multiple CAD files and optionally generate BOM"""
    if not is_cad_available():
        raise HTTPException(500, "CAD libraries not installed")
    
    results = []
    files_data = []
    
    for file_req in request.files:
        try:
            # Download file
            async with httpx.AsyncClient() as client:
                response = await client.get(file_req.fileUrl, timeout=DOWNLOAD_TIMEOUT, follow_redirects=True)
                response.raise_for_status()
                file_content = response.content
            
            with tempfile.NamedTemporaryFile(suffix=f".{file_req.fileType}", delete=False) as tmp_input:
                tmp_input.write(file_content)
                input_path = tmp_input.name
            
            stl_path = input_path.replace(f".{file_req.fileType}", ".stl")
            gltf_path = input_path.replace(f".{file_req.fileType}", ".gltf")
            
            try:
                file_result = {
                    "filename": file_req.fileName or os.path.basename(file_req.fileUrl),
                    "file_type": file_req.fileType,
                    "success": True
                }
                
                # Extract metadata
                step_content = None
                if request.extractMetadata:
                    metadata = extract_step_metadata(input_path)
                    step_content = get_step_text_content(input_path)
                    file_result["metadata"] = metadata
                
                # Generate preview
                if request.generatePreview:
                    if file_req.fileType.lower() in ["step", "stp"]:
                        convert_step_to_stl(input_path, stl_path)
                    elif file_req.fileType.lower() == "stl":
                        import shutil
                        shutil.copy(input_path, stl_path)
                    
                    dimensions = calculate_dimensions(stl_path)
                    gltf_json = convert_stl_to_gltf(stl_path, gltf_path)
                    
                    file_result["dimensions"] = dimensions
                    file_result["gltf"] = gltf_json
                
                # Collect for AI analysis
                if request.apiKey:
                    file_data = {
                        "filename": file_result["filename"],
                        "file_type": file_result["file_type"],
                        "metadata": file_result.get("metadata", {}),
                        "dimensions": file_result.get("dimensions", {}),
                        "step_content": step_content
                    }
                    files_data.append(file_data)
                    
                    # Individual AI analysis
                    ai_analysis = await analyze_file_with_ai(
                        file_data,
                        request.apiKey,
                        request.aiModel,
                        SITE_URL
                    )
                    file_result["ai_analysis"] = ai_analysis
                
                results.append(file_result)
                
            finally:
                for path in [input_path, stl_path, gltf_path]:
                    if os.path.exists(path):
                        try:
                            os.unlink(path)
                        except:
                            pass
                            
        except Exception as e:
            results.append({
                "filename": file_req.fileName or os.path.basename(file_req.fileUrl),
                "success": False,
                "error": str(e)
            })
    
    response_data = {
        "success": True,
        "total_files": len(request.files),
        "processed": len([r for r in results if r.get("success")]),
        "failed": len([r for r in results if not r.get("success")]),
        "files": results
    }
    
    # Generate BOM if requested
    if request.generateBOM and request.apiKey and files_data:
        bom = await generate_bom_from_batch(
            files_data,
            request.apiKey,
            request.aiModel,
            SITE_URL
        )
        response_data["bom"] = bom
    
    return response_data


@app.post("/api/metadata")
async def extract_metadata_only(request: ConversionRequest):
    """Extract BOM metadata without 3D conversion (faster)"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(request.fileUrl, timeout=DOWNLOAD_TIMEOUT, follow_redirects=True)
            response.raise_for_status()
            file_content = response.content
        
        with tempfile.NamedTemporaryFile(suffix=f".{request.fileType}", delete=False) as tmp_input:
            tmp_input.write(file_content)
            input_path = tmp_input.name
        
        try:
            metadata = extract_step_metadata(input_path)
            step_content = get_step_text_content(input_path)
            
            response_data = {
                "success": True,
                "metadata": metadata,
                "filename": os.path.basename(request.fileUrl)
            }
            
            # AI Analysis if API key provided
            if request.apiKey:
                file_data = {
                    "filename": os.path.basename(request.fileUrl),
                    "file_type": request.fileType,
                    "metadata": metadata,
                    "step_content": step_content
                }
                
                ai_analysis = await analyze_file_with_ai(
                    file_data,
                    request.apiKey,
                    request.aiModel,
                    SITE_URL
                )
                response_data["ai_analysis"] = ai_analysis
            
            return response_data
            
        finally:
            if os.path.exists(input_path):
                os.unlink(input_path)
                
    except Exception as e:
        raise HTTPException(500, f"Metadata extraction failed: {str(e)}")
