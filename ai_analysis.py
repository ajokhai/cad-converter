"""
AI-powered CAD analysis using OpenRouter
Authors: Josh Ayokhai & River
"""
import httpx
import json
from typing import Dict, Any, List


async def analyze_file_with_ai(
    file_data: Dict[str, Any],
    api_key: str,
    model: str = "anthropic/claude-3.5-sonnet",
    site_url: str = None
) -> Dict[str, Any]:
    """
    Use OpenRouter AI to analyze CAD file and extract structured data
    
    Args:
        file_data: Dictionary with filename, file_type, metadata, dimensions, step_content
        api_key: OpenRouter API key
        model: OpenRouter model identifier
        site_url: Your site URL for OpenRouter attribution
    """
    if not api_key:
        return {"error": "No API key provided"}
    
    prompt = f"""Analyze this CAD file and extract structured BOM data.

File name: {file_data.get('filename', 'unknown')}
File type: {file_data.get('file_type', 'unknown')}

Extracted metadata:
{json.dumps(file_data.get('metadata', {}), indent=2)}

Physical dimensions:
{json.dumps(file_data.get('dimensions', {}), indent=2)}

"""
    
    if file_data.get('step_content'):
        prompt += f"\nSTEP file header content:\n```\n{file_data['step_content'][:3000]}\n```\n"
    
    prompt += """
Please provide a structured JSON response with the following fields:
{
  "part_name": "Best guess for part name",
  "part_number": "Part number if identifiable, or suggest format",
  "description": "Brief description of the part",
  "category": "Part category (e.g., mechanical, electronic, fastener)",
  "material": "Suggested material based on context",
  "quantity": 1,
  "estimated_cost": null,
  "manufacturer": "Manufacturer if identifiable",
  "notes": "Any additional relevant information",
  "confidence": "high/medium/low - how confident you are in this data"
}

Make reasonable inferences based on:
- Filename patterns
- Dimension ranges (e.g., small parts might be fasteners)
- Common CAD naming conventions
- Industry standards

Return ONLY valid JSON, no additional text.
"""
    
    messages = [{"role": "user", "content": prompt}]
    
    try:
        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": site_url,
                    "X-Title": "CAD Converter"
                },
                json={
                    "model": model,
                    "messages": messages
                }
            )
            response.raise_for_status()
            result = response.json()
            
            ai_content = result['choices'][0]['message']['content']
            
            # Parse JSON response
            ai_content = ai_content.strip()
            if ai_content.startswith('```'):
                ai_content = ai_content.split('```')[1]
                if ai_content.startswith('json'):
                    ai_content = ai_content[4:]
            ai_content = ai_content.strip()
            
            structured_data = json.loads(ai_content)
            return structured_data
            
    except json.JSONDecodeError:
        return {
            "error": "AI response was not valid JSON",
            "raw_response": ai_content
        }
    except Exception as e:
        return {"error": f"AI analysis failed: {str(e)}"}


async def generate_bom_from_batch(
    files_data: List[Dict[str, Any]],
    api_key: str,
    model: str = "anthropic/claude-3.5-sonnet",
    site_url: str = None
) -> Dict[str, Any]:
    """
    Use AI to generate a complete BOM from multiple files
    
    Args:
        files_data: List of file data dictionaries
        api_key: OpenRouter API key
        model: OpenRouter model identifier
        site_url: Your site URL for OpenRouter attribution
    """
    if not api_key:
        return {"error": "No API key provided"}
    
    prompt = f"""You are analyzing {len(files_data)} CAD files to generate a Bill of Materials (BOM).

Files analyzed:
"""
    
    for i, file_data in enumerate(files_data, 1):
        prompt += f"\n{i}. {file_data.get('filename', f'File {i}')}\n"
        prompt += f"   Type: {file_data.get('file_type', 'unknown')}\n"
        prompt += f"   Dimensions: {file_data.get('dimensions', {})}\n"
        prompt += f"   Metadata: {file_data.get('metadata', {})}\n"
    
    prompt += """

Generate a complete BOM in JSON format with the following structure:
{
  "bom_name": "Suggested BOM name based on parts",
  "total_parts": number,
  "parts": [
    {
      "line_number": 1,
      "part_number": "PN-XXX",
      "part_name": "Name",
      "description": "Description",
      "quantity": 1,
      "category": "Category",
      "material": "Material",
      "manufacturer": "Manufacturer or TBD",
      "estimated_cost": null,
      "notes": "Notes"
    }
  ],
  "assembly_notes": "Overall notes about the assembly",
  "missing_information": ["List of data that needs manual entry"]
}

Rules:
- Assign sequential line numbers
- Suggest part numbers if not available (format: PN-001, PN-002, etc.)
- Group similar parts (e.g., if multiple identical fasteners, combine with quantity)
- Flag duplicate or similar parts
- Identify common hardware (screws, nuts, washers) by dimensions
- Suggest materials based on typical use cases
- List what information is missing or uncertain

Return ONLY valid JSON.
"""
    
    try:
        async with httpx.AsyncClient(timeout=120.0) as client:
            response = await client.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": site_url,
                    "X-Title": "CAD Converter"
                },
                json={
                    "model": model,
                    "messages": [{"role": "user", "content": prompt}]
                }
            )
            response.raise_for_status()
            result = response.json()
            
            ai_content = result['choices'][0]['message']['content']
            
            # Parse JSON
            ai_content = ai_content.strip()
            if ai_content.startswith('```'):
                ai_content = ai_content.split('```')[1]
                if ai_content.startswith('json'):
                    ai_content = ai_content[4:]
            ai_content = ai_content.strip()
            
            bom_data = json.loads(ai_content)
            return bom_data
            
    except Exception as e:
        return {"error": f"BOM generation failed: {str(e)}"}
