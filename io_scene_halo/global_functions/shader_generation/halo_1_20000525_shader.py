from mathutils import Vector
from ..shader_generation.shader_helper import (
    place_node,
    connect_inputs, 
    get_linked_node, 
    set_image_scale, 
    get_shader_node,
    generate_image_node, 
    convert_to_blender_color,
    get_output_material_node, 
    HALO_1_SHADER_RESOURCES
    )

def generate_shader_simple(bitm_assset, mat, map, RasterizerFlags, EncodingEnum, report):
    mat.use_nodes = True

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = bitmap_processing.generate_legacy_image_node(mat, "", base_bitmap, map.texture.name, False, EncodingEnum)
    base_node.location = Vector((-1600, 500))

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

    if not base_node.image == None:
        base_node.image.alpha_mode = 'CHANNEL_PACKED'

    if base_bitmap:
        rasterizer_flags_result = RasterizerFlags(map.rasterizer_flags)
        if RasterizerFlags.alpha_test == rasterizer_flags_result:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.blend_method = 'HASHED'
        else:
            mat.blend_method = 'OPAQUE'

    connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")