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
import zlib
import math
import bmesh
import shutil

from pathlib import Path
from mathutils import Vector
from ..global_functions import tag_format
from ..global_functions.parse_tags import parse_tag
from ..file_tag.h1.file_bitmap.build_asset import build_asset as build_h1_bitmap
from ..file_tag.h2.file_bitmap.build_asset import build_asset as build_h2_bitmap
from ..file_tag.h1.file_bitmap.format import (
    BitmapAsset as H1BitmapAsset,
    FormatEnum as H1FormatEnum,
    UsageEnum as H1UsageEnum,
    BitmapFormatEnum as H1BitmapFormatEnum,
    BitmapFlags as H1BitmapFlags
    )
from ..file_tag.h2.file_bitmap.format import (
    BitmapAsset as H2BitmapAsset,
    FormatEnum as H2FormatEnum,
    UsageEnum as H2UsageEnum,
    BitmapFormatEnum as H2BitmapFormatEnum,
    BitmapFlags as H2BitmapFlags
    )
from ..file_tag.h1.file_scenario.process_file import process_file as process_h1_scenario
from ..file_tag.h2.file_scenario.process_file import process_file as process_h2_scenario
from ..file_tag.h2.file_scenario_structure_lightmap.build_asset import build_asset as build_h2_lightmap
from ..file_tag.h2.file_scenario_structure_lightmap.format import GeometryBucketFlags
from ..global_functions import global_functions
from ..global_functions.shader_generation.shader_helper import HALO_2_SHADER_RESOURCES
from ..global_functions.shader_generation.shader_helper import connect_inputs
from ..global_functions.mesh_processing import gather_parameters

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

LIGHTMAP_TEMP = os.path.join(os.path.expanduser("~"), "Blender Halo Toolset", "Lightmap Temp")

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
    tree = scene.node_tree

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

        uv_name = "UVMap_%s" % uv_index
        uv_layers[uv_name].active_render = True
        uv_layers[uv_name].active = True 
        target_name = 'VERTEX_COLORS'
        bake_layer = uv_name
    else:
        uv_layers[lightmap_name].active_render = True
        uv_layers[render_name].active = True 
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

def light_halo_2_mesh(context, lightmap_ob, BITMAP_ASSET, BITMAP, TAG, image_multiplier, lightmap_idx, pixel_offset):
    lightmap_data = None
    bitmap_class = None
    if BITMAP_ASSET:
        bitmap_element = BITMAP_ASSET.bitmaps[lightmap_idx]
        width = int(bitmap_element.width * image_multiplier)
        height = int(bitmap_element.height * image_multiplier)
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

    bitmap_class = BITMAP.Bitmap()
    bitmap_class.signature = "bitm"
    bitmap_class.width = width
    bitmap_class.height = height
    bitmap_class.depth = 1
    bitmap_class.bitmap_format = lightmap_format
    bitmap_class.flags = lightmap_flags
    bitmap_class.pixels_offset = pixel_offset
    bitmap_class.native_mipmap_info_tag_block = TAG.TagBlock()
    bitmap_class.native_mipmap_info_header = TAG.TagBlockHeader("tbfd", 0, 0, 12)
    bitmap_class.native_mipmap_info = []
    bitmap_class.nbmi_header = TAG.TagBlockHeader("nbmi", 0, 1, 24)

    return lightmap_data, bitmap_class

def set_vertex_colors(lightmap_ob, geometry_bucket, section_offset, vertex_count):
        for vertex_index in range(vertex_count):
            R, G, B, A = lightmap_ob.data.attributes.active_color.data[vertex_index].color
            geometry_bucket.raw_vertices[section_offset + vertex_index].primary_lightmap_color_RGBA = (R, G, B, A)

def bake_clusters(context, game_title, scenario_path, image_multiplier, report, H2V=False):
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
        SCNR_ASSET = None
        try:
            with open(scenario_path, 'rb') as input_stream:
                SCNR_ASSET = process_h1_scenario(input_stream, report)

        except Exception as e:
            report({'WARNING'}, f"Failed to process {scenario_path}: {e}")

        if SCNR_ASSET:
            TAG = tag_format.TagAsset()
            levels_collection = bpy.data.collections.get("BSPs")
            if not levels_collection == None:
                for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                    for cluster_collection in bsp_collection.children:
                        cluster_collection.hide_render = True

                for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                    bsp_element = SCNR_ASSET.structure_bsps[bsp_idx]
                    BSP_ASSET = parse_tag(bsp_element, report, game_title, "retail")
                    if BSP_ASSET:
                        BITMAP_ASSET = parse_tag(BSP_ASSET.lightmap_bitmaps_tag_ref, report, game_title, "retail")
                        bitmap_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path, "%s.bitmap" %  BSP_ASSET.lightmap_bitmaps_tag_ref.name)

                        pixel_data = bytes()
                        pixel_offset = 0

                        BITMAP = H1BitmapAsset()
                        TAG.is_legacy = False

                        BITMAP.header = TAG.Header()
                        BITMAP.header.unk1 = 0
                        BITMAP.header.flags = 0
                        BITMAP.header.type = 0
                        BITMAP.header.name = ""
                        BITMAP.header.tag_group = "bitm"
                        BITMAP.header.checksum = global_functions.get_data_checksum()
                        BITMAP.header.data_offset = 64
                        BITMAP.header.data_length = 0
                        BITMAP.header.unk2 = 0
                        BITMAP.header.version = 7
                        BITMAP.header.destination = 0
                        BITMAP.header.plugin_handle = -1
                        BITMAP.header.engine_tag = "blam"

                        bitmap_format = H1FormatEnum._32bit_color.value
                        if BITMAP_ASSET:
                            bitmap_format = BITMAP_ASSET.bitmap_format

                        BITMAP.bitmap_format = bitmap_format
                        BITMAP.usage = H1UsageEnum.light_map.value
                        BITMAP.color_plate_width = 0
                        BITMAP.color_plate_height = 0
                        BITMAP.compressed_color_plate_data = TAG.RawData()
                        BITMAP.compressed_color_plate = bytes()
                        BITMAP.processed_pixel_data = TAG.RawData()
                        BITMAP.processed_pixels = bytes()
                        BITMAP.sequences = []
                        BITMAP.bitmaps = []

                        for cluster_collection in bsp_collection.children:
                            cluster_collection.hide_render = False
                            for cluster_idx, cluster_ob in enumerate(cluster_collection.objects):
                                if not cluster_ob.tag_mesh.lightmap_index == -1:
                                    if BITMAP_ASSET:
                                        bitmap_element = BITMAP_ASSET.bitmaps[cluster_idx]
                                        width = int(bitmap_element.width * image_multiplier)
                                        height = int(bitmap_element.height * image_multiplier)
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

                                    buf = bytearray([int(p * 255) for p in image.pixels])
                                    image = Image.frombytes("RGBA", (width, height), buf, 'raw', "RGBA")

                                    bitmap_format = BITMAP.bitmap_format
                                    lightmap_flags = H1BitmapFlags.power_of_two_dimensions.value
                                    if bitmap_format == H1FormatEnum._16bit_color.value:
                                        lightmap_data = image.convert('BGR;16').tobytes()
                                        lightmap_format = H1BitmapFormatEnum.r5g6b5.value
                                    elif bitmap_format == H1FormatEnum._32bit_color.value:
                                        lightmap_image = image.convert('RGBA')
                                        r,g,b,a = lightmap_image.split()
                                        lightmap_data = Image.merge("RGBA", (b, g, r, a)).tobytes()
                                        lightmap_format = H1BitmapFormatEnum.x8r8g8b8.value

                                    pixel_data = pixel_data + lightmap_data

                                    sequence = BITMAP.Sequence()
                                    sequence.first_bitmap_index = cluster_idx
                                    sequence.bitmap_count = 1
                                    sequence.sprites_tag_block = TAG.TagBlock()
                                    sequence.sprites = []

                                    BITMAP.sequences.append(sequence)

                                    bitmap_class = BITMAP.Bitmap()
                                    bitmap_class.signature = "bitm"
                                    bitmap_class.width = width
                                    bitmap_class.height = height
                                    bitmap_class.depth = 1
                                    bitmap_class.bitmap_format = lightmap_format
                                    bitmap_class.flags = lightmap_flags
                                    bitmap_class.registration_point = (int(width / 2), int(height / 2))
                                    bitmap_class.pixels_offset = pixel_offset

                                    BITMAP.bitmaps.append(bitmap_class)

                                    pixel_offset += len(lightmap_data)

                            cluster_collection.hide_render = True
                            BITMAP.processed_pixel_data = TAG.RawData(len(pixel_data))
                            BITMAP.processed_pixels = pixel_data

                            BITMAP.sequences_tag_block = TAG.TagBlock(len(BITMAP.sequences))
                            BITMAP.bitmaps_tag_block = TAG.TagBlock(len(BITMAP.bitmaps))

                            with open(bitmap_path, 'wb') as output_stream:
                                build_h1_bitmap(output_stream, BITMAP, report)

    elif game_title == "halo2" and Image:
        levels_collection = bpy.data.collections.get("BSPs")
        if not levels_collection == None:
            for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                for cluster_collection in bsp_collection.children:
                    cluster_collection.hide_render = True

        SCNR_ASSET = None
        try:
            with open(scenario_path, 'rb') as input_stream:
                SCNR_ASSET = process_h2_scenario(input_stream, report)

        except Exception as e:
            report({'WARNING'}, f"Failed to process {scenario_path}: {e}")

        if SCNR_ASSET:
            original_input_values = set_input_modifiers()

            TAG = tag_format.TagAsset()

            unique_id_list = []
            for scenery in SCNR_ASSET.scenery:
                unique_id_list.append(scenery.unique_id)
                
            scenery_collection = bpy.data.collections.get("Scenery")
            for bsp_element in SCNR_ASSET.structure_bsps:
                bsp_name = os.path.basename(bsp_element.structure_bsp.name)
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
                    SBSP_ASSET = parse_tag(bsp_element.structure_bsp, report, game_title, "retail")
                    LTMP_ASSET = parse_tag(bsp_element.structure_lightmap, report, game_title, "retail")
                    if LTMP_ASSET:
                        first_lightmap_group_entry = None
                        for lightmap_group in LTMP_ASSET.lightmap_groups:
                            first_lightmap_group_entry = lightmap_group
                            break

                        BITMAP_ASSET = parse_tag(first_lightmap_group_entry.bitmap_group_tag_ref, report, game_title, "retail")
                        halo2_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
                        bitmap_path = os.path.join(halo2_tag_path, "%s.bitmap" %  first_lightmap_group_entry.bitmap_group_tag_ref.name)

                        pixel_data = bytes()
                        pixel_offset = 0

                        BITMAP = H2BitmapAsset()
                        TAG.is_legacy = False
                        TAG.big_endian = False

                        BITMAP.header = TAG.Header()
                        BITMAP.header.unk1 = 0
                        BITMAP.header.flags = 0
                        BITMAP.header.type = 0
                        BITMAP.header.name = ""
                        BITMAP.header.tag_group = "bitm"
                        BITMAP.header.checksum = global_functions.get_data_checksum()
                        BITMAP.header.data_offset = 64
                        BITMAP.header.data_length = 0
                        BITMAP.header.unk2 = 0
                        BITMAP.header.version = 7
                        BITMAP.header.destination = 0
                        BITMAP.header.plugin_handle = -1
                        BITMAP.header.engine_tag = "BLM!"

                        BITMAP.body_header = TAG.TagBlockHeader("tbfd", 0, 1, 112)
                        BITMAP.bitmap_format = H2FormatEnum.compressed_with_color_key_transparency.value
                        BITMAP.usage = H2UsageEnum.alpha_blend.value
                        BITMAP.color_plate_width = 0
                        BITMAP.color_plate_height = 0
                        BITMAP.compressed_color_plate_data = TAG.RawData()
                        BITMAP.compressed_color_plate = bytes()
                        BITMAP.processed_pixel_data = TAG.RawData()
                        BITMAP.processed_pixels = bytes()
                        BITMAP.sequences = []
                        BITMAP.bitmaps = []

                        lightmap_idx = 0
                        lightmap_collection.hide_render = False
                        if lightmap_instances_collection:
                            lightmap_instances_collection.hide_render = False

                        for lightmap_ob_idx, lightmap_ob in enumerate(lightmap_collection.objects):
                            if lightmap_ob.tag_mesh.instance_lightmap_policy_enum == '0':
                                cluster_lightmap_data, cluster_bitmap_class = light_halo_2_mesh(context, lightmap_ob, BITMAP_ASSET, BITMAP, TAG, image_multiplier, lightmap_idx, pixel_offset)
                                BITMAP.bitmaps.append(cluster_bitmap_class)
                                lightmap_idx += 1
                                pixel_data += cluster_lightmap_data
                                pixel_offset += len(cluster_lightmap_data)
                            else:
                                run_bake(context, lightmap_ob, True)

                        if lightmap_instances_collection:
                            for lightmap_instance_ob_idx, lightmap_instance_ob in enumerate(lightmap_instances_collection.objects):
                                instance_geo = SBSP_ASSET.instanced_geometry_instances[lightmap_instance_ob_idx]
                                instance_definition = SBSP_ASSET.instanced_geometry_definition[instance_geo.instance_definition]
                                if lightmap_instance_ob.tag_mesh.instance_lightmap_policy_enum == '0' and instance_definition.shadow_casting_triangle_count > 0:
                                    instance_lightmap_data, instance_bitmap_class = light_halo_2_mesh(context, lightmap_instance_ob, BITMAP_ASSET, BITMAP, TAG, image_multiplier, lightmap_idx, pixel_offset)
                                    BITMAP.bitmaps.append(instance_bitmap_class)
                                    lightmap_idx += 1
                                    pixel_data += instance_lightmap_data
                                    pixel_offset += len(instance_lightmap_data)
                                else:
                                    run_bake(context, lightmap_instance_ob, True)

                        lightmap_collection.hide_render = True
                        if lightmap_instances_collection:
                            lightmap_instances_collection.hide_render = True
                            
                        BITMAP.processed_pixel_data = TAG.RawData(len(pixel_data))
                        BITMAP.processed_pixels = pixel_data

                        bitmap_count = len(BITMAP.bitmaps)
                        BITMAP.sequence_header = TAG.TagBlockHeader("tbfd", 0, 0, 64)
                        if H2V:
                            BITMAP.bitmap_header = TAG.TagBlockHeader("tbfd", 1, bitmap_count, 116)
                        else:
                            BITMAP.bitmap_header = TAG.TagBlockHeader("tbfd", 2, bitmap_count, 140)

                        BITMAP.sequences_tag_block = TAG.TagBlock()
                        BITMAP.bitmaps_tag_block = TAG.TagBlock(bitmap_count)

                        with open(bitmap_path, 'wb') as output_stream:
                            build_h2_bitmap(output_stream, BITMAP, report, H2V)

                        if lightmap_instances_collection:
                            for instance_idx, instance_bucket_ref in enumerate(first_lightmap_group_entry.instance_bucket_refs):
                                lightmap_instance_ob = lightmap_instances_collection.objects[instance_idx]
                                vertex_count = len(lightmap_instance_ob.data.vertices)
                                bucket_index = instance_bucket_ref.bucket_index
                                geometry_bucket = first_lightmap_group_entry.geometry_buckets[bucket_index]
                                if GeometryBucketFlags.color in GeometryBucketFlags(geometry_bucket.flags):
                                    for section_offset in instance_bucket_ref.section_offsets:
                                        set_vertex_colors(lightmap_instance_ob, geometry_bucket, section_offset, vertex_count)

                        if not scenery_collection == None:
                            scenery_id_list = []
                            for scenery_idx, scenery_object_info in enumerate(first_lightmap_group_entry.scenery_object_info):
                                scenery_id_list.append(scenery_object_info.unique_id)

                            for scenery_idx, scenery_object_bucket_ref in enumerate(first_lightmap_group_entry.scenery_object_bucket_refs):
                                scenery_id = scenery_id_list[scenery_idx]
                                scenery_ob = scenery_collection.objects[unique_id_list.index(scenery_id)]
                                vertex_count = len(scenery_ob.data.vertices)
                                bucket_index = scenery_object_bucket_ref.bucket_index
                                geometry_bucket = first_lightmap_group_entry.geometry_buckets[bucket_index]
                                run_bake(context, scenery_ob, True)
                                if GeometryBucketFlags.color in GeometryBucketFlags(geometry_bucket.flags):
                                    for section_offset in scenery_object_bucket_ref.section_offsets:
                                        set_vertex_colors(scenery_ob, geometry_bucket, section_offset, vertex_count)

                        halo2_tag_path = bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path
                        lightmap_path = os.path.join(halo2_tag_path, "%s.scenario_structure_lightmap" % bsp_element.structure_lightmap.name)
                        with open(lightmap_path, 'wb') as output_stream:
                            build_h2_lightmap(output_stream, LTMP_ASSET, report)

            for material_inputs in original_input_values:
                for original_input in material_inputs:
                    node_input, value = original_input
                    node_input.default_value = value

    context.scene.tag_scenario.global_lightmap_multiplier = 1
    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.bake_clusters()
