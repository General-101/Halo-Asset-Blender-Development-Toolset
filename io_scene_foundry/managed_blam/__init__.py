import os

def create_shader_tag(blender_material):
    # Check if bitmaps exist already, if not, create them
    
    from tag_shader import TagShader
    tag = TagShader()