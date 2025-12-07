"""
CAD file conversion utilities
Authors: Josh Ayokhai & River
"""
import trimesh
import json

try:
    import cadquery as cq
    CAD_AVAILABLE = True
except ImportError:
    CAD_AVAILABLE = False


def convert_step_to_stl(input_path, output_path):
    """Convert STEP file to STL"""
    if not CAD_AVAILABLE:
        raise RuntimeError("CAD libraries not installed")
    
    result = cq.importers.importStep(input_path)
    cq.exporters.export(result, output_path)
    return output_path


def convert_stl_to_gltf(stl_path, gltf_path):
    """Convert STL to glTF format"""
    mesh = trimesh.load(stl_path)
    mesh.export(gltf_path, file_type='gltf')
    
    with open(gltf_path, 'r') as f:
        gltf_json = json.load(f)
    
    return gltf_json


def calculate_dimensions(stl_path):
    """Calculate dimensions from STL mesh"""
    mesh = trimesh.load(stl_path)
    bounds = mesh.bounds
    
    dimensions = {
        'length': float(bounds[1][0] - bounds[0][0]),
        'width': float(bounds[1][1] - bounds[0][1]),
        'height': float(bounds[1][2] - bounds[0][2]),
        'volume': float(mesh.volume) if hasattr(mesh, 'volume') else None,
        'units': 'mm'
    }
    
    return dimensions


def is_cad_available():
    """Check if CAD libraries are available"""
    return CAD_AVAILABLE
