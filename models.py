"""
Request and response models
Authors: Josh Ayokhai & River
"""
from pydantic import BaseModel
from typing import List, Optional


class FileToProcess(BaseModel):
    fileUrl: str
    fileType: str  # "step", "stp", "stl"
    fileName: Optional[str] = None


class ConversionRequest(BaseModel):
    fileUrl: str
    fileType: str
    aiModel: Optional[str] = "anthropic/claude-3.5-sonnet"
    apiKey: Optional[str] = None


class BatchConversionRequest(BaseModel):
    files: List[FileToProcess]
    aiModel: Optional[str] = "anthropic/claude-3.5-sonnet"
    apiKey: Optional[str] = None
    extractMetadata: bool = True
    generatePreview: bool = True
    generateBOM: bool = False
