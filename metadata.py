"""
CAD metadata extraction utilities
Authors: Josh Ayokhai & River
"""
import re


def extract_step_metadata(file_path):
    """Extract metadata from STEP file headers"""
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
            
            # Look for PRODUCT entities
            product_pattern = r"PRODUCT\s*\(\s*'([^']*)'.*?'([^']*)'"
            product_match = re.search(product_pattern, content)
            if product_match:
                if not metadata['part_number']:
                    metadata['part_number'] = product_match.group(1)
                if not metadata['part_name']:
                    metadata['part_name'] = product_match.group(2)
            
            # Extract timestamp
            timestamp_pattern = r"'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})'"
            timestamp_match = re.search(timestamp_pattern, content)
            if timestamp_match:
                metadata['timestamp'] = timestamp_match.group(1)
    
    except Exception as e:
        print(f"Metadata extraction warning: {e}")
    
    return metadata


def get_step_text_content(file_path, max_chars=5000):
    """Get text content from STEP file for AI analysis"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read(max_chars)
            return content
    except Exception as e:
        print(f"Error reading STEP content: {e}")
        return None
