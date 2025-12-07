"""
Configuration settings
Authors: Josh Ayokhai & River
"""
import os

# =============================================================================
# Service Configuration
# =============================================================================

# File size limits
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE_MB", "100"))
MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

# CORS settings
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*").split(",")

# Port
PORT = int(os.getenv("PORT", "8080"))

# =============================================================================
# File Format Configuration
# =============================================================================

# Supported formats (can be overridden via env var)
_supported_formats_env = os.getenv("SUPPORTED_FORMATS", "")
if _supported_formats_env:
    SUPPORTED_FORMATS = [fmt.strip() for fmt in _supported_formats_env.split(",")]
else:
    SUPPORTED_FORMATS = ["step", "stp", "stl"]

# =============================================================================
# AI Configuration
# =============================================================================

# Supported AI models
SUPPORTED_AI_MODELS = [
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-opus",
    "openai/gpt-4-turbo",
    "openai/gpt-4o",
    "google/gemini-pro-1.5"
]

# Default AI model
DEFAULT_AI_MODEL = os.getenv("DEFAULT_AI_MODEL", "anthropic/claude-3.5-sonnet")

# OpenRouter API key (optional - users can provide their own in requests)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")

# =============================================================================
# GitHub & Attribution
# =============================================================================

# GitHub information
GITHUB_USERNAME = os.getenv("GITHUB_USERNAME", "ajokhai")
GITHUB_REPO = os.getenv("GITHUB_REPO", "cad-converter")

# Site URL for OpenRouter attribution
SITE_URL = os.getenv("SITE_URL", f"https://github.com/{GITHUB_USERNAME}/{GITHUB_REPO}")

# Project authors
PROJECT_AUTHORS = os.getenv("PROJECT_AUTHORS", "Josh Ayokhai, River")

# =============================================================================
# Advanced Settings
# =============================================================================

# Debug mode
DEBUG = os.getenv("DEBUG", "false").lower() == "true"

# Timeouts (in seconds)
DOWNLOAD_TIMEOUT = int(os.getenv("DOWNLOAD_TIMEOUT", "120"))
AI_TIMEOUT = int(os.getenv("AI_TIMEOUT", "120"))
