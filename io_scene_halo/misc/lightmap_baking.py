# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
# ##### END MIT LICENSE BLOCK #####

import os
import bpy
import math
import bmesh
import base64
import shutil

from mathutils import Vector
from enum import Flag, Enum, auto
from ..global_functions import global_functions
from ..global_functions.shader_generation.shader_helper import HALO_2_SHADER_RESOURCES
from ..global_functions.shader_generation.shader_helper import connect_inputs
from ..global_functions.mesh_processing import gather_parameters
from ..file_tag.tag_interface import tag_interface, tag_common
from ..file_tag.tag_interface.tag_definitions import h1, h2

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

LIGHTMAP_TEMP = os.path.join(os.path.expanduser("~"), "Blender Halo Toolset", "Lightmap Temp")

class H1FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()
    high_quality_compression = auto()

class H1UsageEnum(Enum):
    alpha_blend = 0
    default = auto()
    height_map = auto()
    detail_map = auto()
    light_map = auto()
    vector_map = auto()

class H1BitmapFormatEnum(Enum):
    a8 = 0
    y8 = auto()
    ay8 = auto()
    a8y8 = auto()
    unused1 = auto()
    unused2 = auto()
    r5g6b5 = auto()
    unused3 = auto()
    a1r5g5b5 = auto()
    a4r4g4b4 = auto()
    x8r8g8b8 = auto()
    a8r8g8b8 = auto()
    unused4 = auto()
    unused5 = auto()
    dxt1 = auto()
    dxt3 = auto()
    dxt5 = auto()
    p8_bump = auto()
    bc7 = auto()

class H1BitmapFlags(Flag):
    power_of_two_dimensions = auto()
    compressed = auto()
    palettized = auto()
    swizzled = auto()
    linear = auto()
    v16u16 = auto()

class H2FormatEnum(Enum):
    compressed_with_color_key_transparency = 0
    compressed_with_explicit_alpha = auto()
    compressed_with_interpolated_alpha = auto()
    _16bit_color = auto()
    _32bit_color = auto()
    monochrome = auto()

class H2UsageEnum(Enum):
    alpha_blend = 0
    default = auto()
    height_map = auto()
    detail_map = auto()
    light_map = auto()
    vector_map = auto()
    height_map_blue_255 = auto()
    embm = auto()
    height_map_a8l8 = auto()
    height_map_g8b8 = auto()
    height_map_g8b8_with_alpha = auto()

class H2BitmapFormatEnum(Enum):
    a8 = 0
    y8 = auto()
    ay8 = auto()
    a8y8 = auto()
    unused1 = auto()
    unused2 = auto()
    r5g6b5 = auto()
    unused3 = auto()
    a1r5g5b5 = auto()
    a4r4g4b4 = auto()
    x8r8g8b8 = auto()
    a8r8g8b8 = auto()
    unused4 = auto()
    unused5 = auto()
    dxt1 = auto()
    dxt3 = auto()
    dxt5 = auto()
    p8_bump = auto()
    p8 = auto()
    argbfb32 = auto()
    rgbfb32 = auto()
    rgbfb16 = auto()
    v8u8 = auto()
    g8b8 = auto()

class H2BitmapFlags(Flag):
    power_of_two_dimensions = auto()
    compressed = auto()
    palettized = auto()
    swizzled = auto()
    linear = auto()
    v16u16 = auto()
    mipmap_debug_level = auto()
    prefer_stutter = auto()

class GeometryBucketFlags(Flag):
    incident_direction = auto()
    color = auto()

def next_power_of_two(x):
    return 2 ** math.ceil(math.log2(x))

def calculate_uv_bounds_object_mode(obj):
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    uv_layer = bm.loops.layers.uv.active

    if uv_layer is None:
        bm.free()
        raise RuntimeError(f"No active UV layer found on {obj.name}")

    min_u = min_v = float('inf')
    max_u = max_v = float('-inf')

    for face in bm.faces:
        for loop in face.loops:
            uv = loop[uv_layer].uv
            min_u = min(min_u, uv.x)
            min_v = min(min_v, uv.y)
            max_u = max(max_u, uv.x)
            max_v = max(max_v, uv.y)

    bm.free()

    uv_width = max_u - min_u
    uv_height = max_v - min_v
    return uv_width, uv_height

def estimate_object_size_diagonal(obj):
    verts = obj.data.vertices
    if not verts:
        return 0.0

    bbox = [obj.matrix_world @ v.co for v in verts]
    min_corner = bbox[0].copy()
    max_corner = bbox[0].copy()

    for v in bbox[1:]:
        min_corner.x = min(min_corner.x, v.x)
        min_corner.y = min(min_corner.y, v.y)
        min_corner.z = min(min_corner.z, v.z)
        max_corner.x = max(max_corner.x, v.x)
        max_corner.y = max(max_corner.y, v.y)
        max_corner.z = max(max_corner.z, v.z)

    size = max_corner - min_corner
    return size.length 

def estimate_image_size(obj, power_of_two=True, texel_density=None, target_resolution=1024):
    uv_width, uv_height = calculate_uv_bounds_object_mode(obj)

    if texel_density is None:
        diagonal = estimate_object_size_diagonal(obj)
        if diagonal < 1e-6:
            texel_density = 512
        else:
            texel_density = target_resolution / diagonal

    img_w = uv_width * texel_density
    img_h = uv_height * texel_density

    if power_of_two:
        img_w = next_power_of_two(img_w)
        img_h = next_power_of_two(img_h)

    return int(img_w), int(img_h)

def ensure_dummy_camera(scene):
    if not scene.camera:
        cam_data = bpy.data.cameras.new("DummyCamera")
        cam_obj = bpy.data.objects.new("DummyCamera", cam_data)
        cam_obj.color = (1, 1, 1, 0)
        scene.collection.objects.link(cam_obj)
        scene.camera = cam_obj

def set_input_modifiers():
    original_input_values = []
    for mat in bpy.data.materials:
        mat_inputs = []
        power_modifier = 1.0
        processed_lightmap_properties = gather_parameters(mat.name)
        processed_parameters = processed_lightmap_properties[1]

        for parameter in processed_parameters:
            if parameter.startswith(" lp"):
                power_modifier = float(parameter.split(":", 1)[1])
                break

        if mat.use_nodes:
            tree = mat.node_tree
            output_node = None

            for node in tree.nodes:
                if node.type == 'OUTPUT_MATERIAL':
                    output_node = node
                    break

            if output_node:
                surface_input = output_node.inputs.get("Surface")
                if not surface_input is None and surface_input.is_linked:
                    linked_node = surface_input.links[0].from_node
                    for input in linked_node.inputs:
                        if "Emissive Power" in input.name and not power_modifier == 1:
                            mat_inputs.append((input, input.default_value))
                            input.default_value *= power_modifier
                        if "Lightmap Factor" == input.name:
                            mat_inputs.append((input, input.default_value))
                            input.default_value = 0.0
                        if "Bump Map Repeat" == input.name:
                            mat_inputs.append((input, input.default_value))
                            input.default_value = 0.0

        original_input_values.append(mat_inputs)

    return original_input_values

def run_lightmap_postprocessing(image_texture):
    GROUP_NAME = "Lightmapper Postprocessing"
    NODE_IMAGE = "Lightmap Image"
    NODE_GROUP = "Postprocessing Group"
    NODE_VIEWER = "Lightmap Viewer"

    if GROUP_NAME not in bpy.data.node_groups:
        with bpy.data.libraries.load(HALO_2_SHADER_RESOURCES, link=False) as (data_from, data_to):
            if GROUP_NAME in data_from.node_groups:
                data_to.node_groups.append(GROUP_NAME)

    scene = bpy.context.scene
    scene.use_nodes = True
    if bpy.app.version >= (5, 0, 0):
        tree = bpy.data.node_groups.new("lightmap postprocessing", "CompositorNodeTree")
        scene.compositing_node_group = tree
    else:
        tree = scene.node_tree

    for node in tree.nodes:
        node.select = False

    for node in list(tree.nodes):
        tree.nodes.remove(node)

    img_node = tree.nodes.get(NODE_IMAGE)
    if not img_node:
        img_node = tree.nodes.new("CompositorNodeImage")
        img_node.name = NODE_IMAGE
        img_node.location = (-600, 0)

    img_node.image = image_texture

    group_node = tree.nodes.get(NODE_GROUP)
    if not group_node:
        group_node = tree.nodes.new("CompositorNodeGroup")
        group_node.name = NODE_GROUP
        group_node.location = (-300, 0)
        group_node.node_tree = bpy.data.node_groups[GROUP_NAME]

    viewer = tree.nodes.get(NODE_VIEWER)
    if not viewer:
        viewer = tree.nodes.new("CompositorNodeViewer")
        viewer.name = NODE_VIEWER
        viewer.location = (100, -200)

    connect_inputs(tree, img_node, "Image", group_node, "Image")
    connect_inputs(tree, group_node, "Image", viewer, "Image")

    ensure_dummy_camera(bpy.context.scene)
    scene = bpy.context.scene

    original_res_x = scene.render.resolution_x
    original_res_y = scene.render.resolution_y

    scene.render.resolution_x = 1
    scene.render.resolution_y = 1

    bpy.ops.render.render(use_viewport=False)

    scene.render.resolution_x = original_res_x
    scene.render.resolution_y = original_res_y

    return bpy.data.images.get("Viewer Node")

def find_layer_collection(layer_collection, target_collection):
    if layer_collection.collection == target_collection:
        return layer_collection
    for child in layer_collection.children:
        result = find_layer_collection(child, target_collection)
        if result:
            return result
    return None

def run_bake(context, lightmap_ob, generate_vertex_colors=False, render_name="UVMap_Render", lightmap_name="UVMap_Lightmap", uv_index=0):
    uv_layers = lightmap_ob.data.uv_layers
    if generate_vertex_colors:
        color_attribute = lightmap_ob.data.attributes.active_color
        if lightmap_ob.data.attributes.active_color == None:
            color_attribute = lightmap_ob.data.attributes.new(name="Color", type="BYTE_COLOR", domain="POINT")

        uv_layers[render_name].active_render = True
        uv_layers[render_name].active = True 
        target_name = 'VERTEX_COLORS'
        bake_layer = render_name
    else:
        uv_layers[render_name].active_render = True
        uv_layers[lightmap_name].active = True 
        target_name = 'IMAGE_TEXTURES'
        bake_layer = lightmap_name

    lightmap_ob.select_set(True)
    context.view_layer.objects.active = lightmap_ob

    context.scene.render.engine = 'CYCLES'
    bpy.ops.object.bake(
        type='DIFFUSE',
        pass_filter={'DIRECT','INDIRECT'}, 
        margin=16,
        margin_type='EXTEND', 
        use_clear=False,
        use_selected_to_active=False,
        target=target_name,
        uv_layer=bake_layer
    )
    
    lightmap_ob.select_set(False)
    context.view_layer.objects.active = None

def light_halo_2_mesh(context, lightmap_ob, bitm_asset, bitm_dict, image_multiplier, lightmap_idx, pixel_offset):
    lightmap_data = None
    bitmap_class = None
    if bitm_asset:
        bitmap_element = bitm_asset["Data"]["bitmaps"][lightmap_idx]
        width = int(bitmap_element["width"] * image_multiplier)
        height = int(bitmap_element["height"] * image_multiplier)
    else:
        width, height = estimate_image_size(lightmap_ob, True, 128)

    image = bpy.data.images.get("Lightmap_%s" % lightmap_idx)
    if not image:
        image = bpy.data.images.new("Lightmap_%s" % lightmap_idx, width, height)
    else:
        image.scale(width, height)
        image.update()

    for material_slot in lightmap_ob.material_slots:
        material_slot.material.use_nodes = True
        material_nodes = material_slot.material.node_tree.nodes
        image_node = material_nodes.get("Lightmap Texture")
        if image_node == None:
            image_node = material_nodes.new("ShaderNodeTexImage")
            image_node.name = "Lightmap Texture"
            image_node.location = Vector((-260.0, 280.0))

        image_node.image = image

        for node in material_nodes:
            node.select = False

        image_node.select = True
        material_nodes.active = image_node

    run_bake(context, lightmap_ob)

    image = run_lightmap_postprocessing(image)

    output_path = os.path.join(LIGHTMAP_TEMP, "Lightmap_%s.png" % lightmap_idx)
    image.filepath_raw = str(output_path)
    image.file_format = 'PNG'
    image.save_render(filepath=image.filepath_raw)

    with open(output_path, 'rb') as f:
        pil_image = Image.open(f).convert("RGBA")

    pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
    r, g, b, a = pil_image.split()
    lightmap_data = Image.merge("RGBA", (b, g, r, a)).tobytes()

    lightmap_flags = H2BitmapFlags.power_of_two_dimensions.value
    lightmap_format = H2BitmapFormatEnum.a8r8g8b8.value

    bitmap_class = {}
    bitmap_class["signature"] = "bitm"
    bitmap_class["width"] = width
    bitmap_class["height"] = height
    bitmap_class["depth"] = 1
    bitmap_class["format"] = {"type": "ShortEnum", "value": lightmap_format, "value name": ""}
    bitmap_class["flags"] = lightmap_flags 
    bitmap_class["pixels offset"] = pixel_offset

    return lightmap_data, bitmap_class

def set_vertex_colors(lightmap_ob, geometry_bucket, section_offset, vertex_count):
        for vertex_index in range(vertex_count):
            R, G, B, A = lightmap_ob.data.attributes.active_color.data[vertex_index].color
            geometry_bucket["raw vertices"][section_offset["section offset"] + vertex_index]["primary lightmap color"] = {"R": R, "G": G, "B": B}

def bake_clusters(context, game_title, scenario_path, image_multiplier, report, H2V=False):
    asset_cache = {}

    os.makedirs(LIGHTMAP_TEMP, exist_ok=True)

    for filename in os.listdir(LIGHTMAP_TEMP):
        file_path = os.path.join(LIGHTMAP_TEMP, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print("Failed to delete %s: %s" % (LIGHTMAP_TEMP, e))

    bpy.ops.object.select_all(action='DESELECT')
    if game_title == "halo1" and Image:
        output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h1_merged_output")
        tag_groups = tag_common.h1_tag_groups
        tag_extensions = tag_common.h1_tag_extensions
        engine_tag = tag_interface.EngineTag.H1Latest.value
        merged_defs = h1.generate_defs(tag_common.h1_defs_directory, output_dir)
        tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path

        if not global_functions.string_empty_check(tags_directory):
            result = scenario_path.split(tags_directory, 1)
            if len(result) > 1:
                local_path, tag_extension = result[1].rsplit(".", 1)
                tag_group = tag_extensions.get(tag_extension)
                tag_ref = {"group name": tag_group, "path": local_path}

                tag_interface.generate_tag_dictionary(game_title, tag_ref, tags_directory, tag_groups, engine_tag, merged_defs, asset_cache)
                scnr_asset = tag_interface.get_disk_asset(local_path, tag_extension)
                if scnr_asset:
                    scnr_data = scnr_asset["Data"]
                    levels_collection = bpy.data.collections.get("BSPs")
                    if not levels_collection == None:
                        for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                            for cluster_collection in bsp_collection.children:
                                cluster_collection.hide_render = True

                        for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                            bsp_element = scnr_data["structure bsps"][bsp_idx]
                            bsp_ref = bsp_element["structure bsp"]
                            sbsp_asset = tag_interface.get_disk_asset(bsp_ref["path"], tag_groups.get(bsp_ref["group name"]))
                            if sbsp_asset:
                                sbsp_data = sbsp_asset["Data"]
                                bitm_ref = sbsp_data["lightmaps bitmap"]
                                bitm_asset = tag_interface.get_disk_asset(bitm_ref["path"], tag_groups.get(bitm_ref["group name"]))
                                bitmap_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path, "%s.bitmap" %  bitm_ref["path"])

                                pixel_data = bytes()
                                pixel_offset = 0

                                bitmap_format = H1FormatEnum._32bit_color.value
                                if bitm_asset:
                                    bitmap_format = bitm_asset["Data"]["encoding format"]["value"]

                                bitm_dict = {"Data": {}}
                                bitm_dict["Data"]["encoding format"] = {"type": "ShortEnum", "value": bitmap_format, "value name": ""}
                                bitm_dict["Data"]["usage"] = {"type": "ShortEnum", "value": H1UsageEnum.light_map.value, "value name": ""}
                                bitm_dict["Data"]["color plate width"] = 0
                                bitm_dict["Data"]["color plate height"] = 0
                                bitm_dict["Data"]["compressed color plate data"] = {"length": 0, "encoded": ""}
                                bitm_dict["Data"]["processed pixel data"] = {"length": 0, "encoded": ""}
                                bitm_dict["Data"]["sequences"] = []
                                bitm_dict["Data"]["bitmaps"] = []

                                for cluster_collection in bsp_collection.children:
                                    cluster_collection.hide_render = False
                                    for cluster_idx, cluster_ob in enumerate(cluster_collection.objects):
                                        if not cluster_ob.tag_mesh.lightmap_index == -1:
                                            if bitm_asset:
                                                bitmap_element = bitm_asset["Data"]["bitmaps"][cluster_idx]
                                                width = int(bitmap_element["width"] * image_multiplier)
                                                height = int(bitmap_element["height"] * image_multiplier)
                                            else:
                                                width, height = estimate_image_size(cluster_ob, True, 128)
                                            
                                            image = bpy.data.images.get("Lightmap_%s" % cluster_idx)
                                            if not image:
                                                image = bpy.data.images.new("Lightmap_%s" % cluster_idx, width, height)
                                            else:
                                                image.scale(width, height)
                                                image.update()

                                            for material_slot in cluster_ob.material_slots:
                                                material_slot.material.use_nodes = True
                                                material_nodes = material_slot.material.node_tree.nodes
                                                image_node = material_nodes.get("Lightmap Texture")
                                                if image_node == None:
                                                    image_node = material_nodes.new("ShaderNodeTexImage")
                                                    image_node.name = "Lightmap Texture"
                                                    image_node.location = Vector((-260.0, 280.0))

                                                image_node.image = image

                                                for node in material_nodes:
                                                    node.select = False

                                                image_node.select = True
                                                material_nodes.active = image_node

                                            run_bake(context, cluster_ob)

                                            image = run_lightmap_postprocessing(image)

                                            output_path = os.path.join(LIGHTMAP_TEMP, "Lightmap_%s.png" % cluster_idx)
                                            image.filepath_raw = str(output_path)
                                            image.file_format = 'PNG'
                                            image.save_render(filepath=image.filepath_raw)

                                            with open(output_path, 'rb') as f:
                                                pil_image = Image.open(f).convert("RGBA")

                                            pil_image = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
                                            r, g, b, a = pil_image.split()
                                            lightmap_data = Image.merge("RGBA", (b, g, r, a)).tobytes()

                                            lightmap_flags = H1BitmapFlags.power_of_two_dimensions.value
                                            lightmap_format = H1BitmapFormatEnum.x8r8g8b8.value

                                            pixel_data = pixel_data + lightmap_data

                                            sequence = {}
                                            sequence["first bitmap index"] = cluster_idx
                                            sequence["bitmap count"] = 1
                                            sequence["sprites"] = []

                                            bitm_dict["Data"]["sequences"].append(sequence)

                                            bitmap_class = {}
                                            bitmap_class["signature"] = "bitm"
                                            bitmap_class["width"] = width
                                            bitmap_class["height"] = height
                                            bitmap_class["depth"] = 1
                                            bitmap_class["format"] = {"type": "ShortEnum", "value": lightmap_format, "value name": ""}
                                            bitmap_class["flags"] = lightmap_flags
                                            bitmap_class["registration point"] = [int(width / 2), int(height / 2)]
                                            bitmap_class["pixel data offset"] = pixel_offset

                                            bitm_dict["Data"]["bitmaps"].append(bitmap_class)

                                            pixel_offset += len(lightmap_data)

                                    cluster_collection.hide_render = True

                                    encoded_pixel_data = base64.b64encode(pixel_data).decode('utf-8')
                                    bitm_dict["Data"]["processed pixel data"] = {"length": len(pixel_data), "encoded": encoded_pixel_data}

                                tag_interface.write_file(merged_defs, bitm_dict, tag_interface.obfuscation_buffer_prepare(), bitmap_path, engine_tag=engine_tag)
            else:
                report({'ERROR'}, "Invalid input provided. Check your tag directory settings and make sure the file exists in your tag directory.")
        else:
            report({'ERROR'}, "Invalid tag directory path provided. Check your tag directory settings.")

    elif game_title == "halo2" and Image:
        output_dir = os.path.join(os.path.dirname(tag_common.h1_defs_directory), "h2_merged_output")
        tag_groups = tag_common.h2_tag_groups
        tag_extensions = tag_common.h2_tag_extensions
        engine_tag = tag_interface.EngineTag.H2Latest.value
        merged_defs = h2.generate_defs(tag_common.h2_defs_directory, output_dir)
        tags_directory = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path

        if not global_functions.string_empty_check(tags_directory):
            result = scenario_path.split(tags_directory, 1)
            if len(result) > 1:
                local_path, tag_extension = result[1].rsplit(".", 1)
                tag_group = tag_extensions.get(tag_extension)
                tag_ref = {"group name": tag_group, "path": local_path}

                tag_interface.generate_tag_dictionary(game_title, tag_ref, tags_directory, tag_groups, engine_tag, merged_defs, asset_cache)
                scnr_asset = tag_interface.get_disk_asset(local_path, tag_extension)

                levels_collection = bpy.data.collections.get("BSPs")
                if not levels_collection == None:
                    for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                        for cluster_collection in bsp_collection.children:
                            cluster_collection.hide_render = True

                if scnr_asset:
                    scnr_data = scnr_asset["Data"]
                    original_input_values = set_input_modifiers()

                    unique_id_list = []
                    for scenery in scnr_data["scenery"]:
                        unique_id_list.append(scenery["unique id"])
                        
                    scenery_collection = bpy.data.collections.get("Scenery")
                    for bsp_element in scnr_data["structure bsps"]:
                        sbsp_ref = bsp_element["structure bsp"]
                        ltmp_ref = bsp_element["structure lightmap"]

                        bsp_name = os.path.basename(sbsp_ref["path"])
                        lightmap_name = "%s_lightmaps" % bsp_name
                        lightmap_instances_name = "%s_lightmap_instances" % bsp_name
                        lightmap_collection = bpy.data.collections.get(lightmap_name)
                        lightmap_instances_collection = bpy.data.collections.get(lightmap_instances_name)

                        bake_collection = False
                        if lightmap_collection:
                            bake_collection = find_layer_collection(bpy.context.view_layer.layer_collection, lightmap_collection).is_visible
                            if lightmap_instances_collection:
                                bake_collection = find_layer_collection(bpy.context.view_layer.layer_collection, lightmap_instances_collection).is_visible

                        if bake_collection:
                            sbsp_asset = tag_interface.get_disk_asset(sbsp_ref["path"], tag_groups.get(sbsp_ref["group name"]))
                            ltmp_asset = tag_interface.get_disk_asset(ltmp_ref["path"], tag_groups.get(ltmp_ref["group name"]))
                            if sbsp_asset and ltmp_asset:
                                sbsp_data = sbsp_asset["Data"]
                                ltmp_data = ltmp_asset["Data"]

                                initial_lightmap = None
                                for lightmap_group in ltmp_data["lightmap groups"]:
                                    initial_lightmap = lightmap_group
                                    break

                                if initial_lightmap:
                                    bitm_ref = initial_lightmap["bitmap group"]
                                    bitm_asset = tag_interface.get_disk_asset(bitm_ref["path"], tag_groups.get(bitm_ref["group name"]))
                                    
                                    halo2_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
                                    bitmap_path = os.path.join(halo2_tag_path, "%s.bitmap" %  bitm_ref["path"])

                                    pixel_data = bytes()
                                    pixel_offset = 0

                                    bitm_dict = {"Data": {}}
                                    bitm_dict["Data"]["format"] = {"type": "ShortEnum", "value": H2FormatEnum.compressed_with_color_key_transparency.value, "value name": ""}
                                    bitm_dict["Data"]["usage"] = {"type": "ShortEnum", "value": H2UsageEnum.alpha_blend.value, "value name": ""}
                                    bitm_dict["Data"]["color plate width"] = 0
                                    bitm_dict["Data"]["color plate height"] = 0
                                    bitm_dict["Data"]["compressed color plate data"] = {"length": 0, "encoded": ""}
                                    bitm_dict["Data"]["processed pixel data"] = {"length": 0, "encoded": ""}
                                    bitm_dict["Data"]["sequences"] = []
                                    bitm_dict["Data"]["bitmaps"] = []

                                    lightmap_idx = 0
                                    lightmap_collection.hide_render = False
                                    if lightmap_instances_collection:
                                        lightmap_instances_collection.hide_render = False

                                    for lightmap_ob_idx, lightmap_ob in enumerate(lightmap_collection.objects):
                                        if lightmap_ob.tag_mesh.instance_lightmap_policy_enum == '0':
                                            cluster_lightmap_data, cluster_bitmap_class = light_halo_2_mesh(context, lightmap_ob, bitm_asset, bitm_dict, image_multiplier, lightmap_idx, pixel_offset)
                                            bitm_dict["Data"]["bitmaps"].append(cluster_bitmap_class)
                                            lightmap_idx += 1
                                            pixel_data += cluster_lightmap_data
                                            pixel_offset += len(cluster_lightmap_data)
                                        else:
                                            run_bake(context, lightmap_ob, True)

                                    if lightmap_instances_collection:
                                        for lightmap_instance_ob_idx, lightmap_instance_ob in enumerate(lightmap_instances_collection.objects):
                                            instance_geo = sbsp_data["instanced geometry instances"][lightmap_instance_ob_idx]
                                            instance_definition = sbsp_data["instanced geometries definitions"][instance_geo["instance definition"]]
                                            if lightmap_instance_ob.tag_mesh.instance_lightmap_policy_enum == '0' and instance_definition["shadow-casting triangle count"] > 0:
                                                instance_lightmap_data, instance_bitmap_class = light_halo_2_mesh(context, lightmap_instance_ob, bitm_asset, bitm_dict, image_multiplier, lightmap_idx, pixel_offset)
                                                bitm_dict["Data"]["bitmaps"].append(instance_bitmap_class)
                                                lightmap_idx += 1
                                                pixel_data += instance_lightmap_data
                                                pixel_offset += len(instance_lightmap_data)
                                            else:
                                                run_bake(context, lightmap_instance_ob, True)

                                    lightmap_collection.hide_render = True
                                    if lightmap_instances_collection:
                                        lightmap_instances_collection.hide_render = True
                                        
                                    encoded_pixel_data = base64.b64encode(pixel_data).decode('utf-8')
                                    bitm_dict["Data"]["processed pixel data"] = {"length": len(pixel_data), "encoded": encoded_pixel_data}

                                    tag_interface.write_file(merged_defs, bitm_dict, tag_interface.obfuscation_buffer_prepare(), bitmap_path, engine_tag=engine_tag)

                                    if lightmap_instances_collection:
                                        for instance_idx, instance_bucket_ref in enumerate(initial_lightmap["instance bucket refs"]):
                                            lightmap_instance_ob = lightmap_instances_collection.objects[instance_idx]
                                            vertex_count = len(lightmap_instance_ob.data.vertices)
                                            bucket_index = instance_bucket_ref["bucket index"]
                                            geometry_bucket = initial_lightmap["geometry buckets"][bucket_index]
                                            if GeometryBucketFlags.color in GeometryBucketFlags(geometry_bucket["flags"]):
                                                for section_offset in instance_bucket_ref["section offsets"]:
                                                    set_vertex_colors(lightmap_instance_ob, geometry_bucket, section_offset, vertex_count)

                                    if not scenery_collection == None:
                                        scenery_id_list = []
                                        for scenery_idx, scenery_object_info in enumerate(initial_lightmap["scenery object info"]):
                                            scenery_id_list.append(scenery_object_info["unique ID"])

                                        for scenery_idx, scenery_object_bucket_ref in enumerate(initial_lightmap["scenery object bucket refs"]):
                                            scenery_id = scenery_id_list[scenery_idx]
                                            scenery_ob = scenery_collection.objects[unique_id_list.index(scenery_id)]
                                            vertex_count = len(scenery_ob.data.vertices)
                                            bucket_index = scenery_object_bucket_ref["bucket index"]
                                            geometry_bucket = initial_lightmap["geometry buckets"][bucket_index]
                                            run_bake(context, scenery_ob, True)
                                            if GeometryBucketFlags.color in GeometryBucketFlags(geometry_bucket["flags"]):
                                                for section_offset in scenery_object_bucket_ref["section offsets"]:
                                                    set_vertex_colors(scenery_ob, geometry_bucket, section_offset, vertex_count)

                                    halo2_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
                                    lightmap_path = os.path.join(halo2_tag_path, "%s.scenario_structure_lightmap" % ltmp_ref["path"])
                                    tag_interface.write_file(merged_defs, ltmp_asset, tag_interface.obfuscation_buffer_prepare(), lightmap_path, engine_tag=engine_tag)

                    for material_inputs in original_input_values:
                        for original_input in material_inputs:
                            node_input, value = original_input
                            node_input.default_value = value
            else:
                report({'ERROR'}, "Invalid input provided. Check your tag directory settings and make sure the file exists in your tag directory.")
        else:
            report({'ERROR'}, "Invalid tag directory path provided. Check your tag directory settings.")

    context.scene.tag_scenario.global_lightmap_multiplier = 1
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.bake_clusters()
