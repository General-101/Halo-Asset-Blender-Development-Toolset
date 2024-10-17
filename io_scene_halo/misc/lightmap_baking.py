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

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

def bake_clusters(context, game_title, scenario_path, image_multiplier, report, H2V=False):
    bpy.ops.object.select_all(action='DESELECT')
    if game_title == "halo1" and Image:
        input_stream = open(scenario_path, "rb")
        SCNR_ASSET = process_h1_scenario(input_stream, report)
        input_stream.close()

        TAG = tag_format.TagAsset()

        levels_collection = bpy.data.collections.get("BSPs")
        if not levels_collection == None:
            for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                for cluster_collection in bsp_collection.children:
                    cluster_collection.hide_render = True

            for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                bsp_element = SCNR_ASSET.structure_bsps[bsp_idx]
                BSP_ASSET = parse_tag(bsp_element, report, game_title, "retail")
                BITMAP_ASSET = parse_tag(BSP_ASSET.level_body.lightmap_bitmaps_tag_ref, report, game_title, "retail")

                bitmap_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_1_tag_path, "%s.bitmap" %  BSP_ASSET.level_body.lightmap_bitmaps_tag_ref.name)

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
                BITMAP.header.checksum = -1
                BITMAP.header.data_offset = 64
                BITMAP.header.data_length = 0
                BITMAP.header.unk2 = 0
                BITMAP.header.version = 7
                BITMAP.header.destination = 0
                BITMAP.header.plugin_handle = -1
                BITMAP.header.engine_tag = "blam"

                BITMAP.bitmap_body = BITMAP.BitmapBody()
                BITMAP.bitmap_body.format = BITMAP_ASSET.bitmap_body.format
                BITMAP.bitmap_body.usage = H1UsageEnum.light_map.value
                BITMAP.bitmap_body.color_plate_width = 0
                BITMAP.bitmap_body.color_plate_height = 0
                BITMAP.bitmap_body.compressed_color_plate_data = TAG.RawData()
                BITMAP.bitmap_body.compressed_color_plate = bytes()
                BITMAP.bitmap_body.processed_pixel_data = TAG.RawData()
                BITMAP.bitmap_body.processed_pixels = bytes()
                BITMAP.sequences = []
                BITMAP.bitmaps = []

                for cluster_collection in bsp_collection.children:
                    cluster_collection.hide_render = False
                    for cluster_idx, cluster_ob in enumerate(cluster_collection.objects):
                        if not cluster_ob.tag_view.lightmap_index == -1:
                            bitmap_element = BITMAP_ASSET.bitmaps[cluster_idx]
                            width = int(bitmap_element.width * image_multiplier)
                            height = int(bitmap_element.height * image_multiplier)
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

                            cluster_ob.select_set(True)
                            context.view_layer.objects.active = cluster_ob

                            context.scene.render.engine = 'CYCLES'
                            bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT','INDIRECT'}, uv_layer=cluster_ob.data.uv_layers[1].name)
                            cluster_ob.select_set(False)
                            context.view_layer.objects.active = None

                            buf = bytearray([int(p * 255) for p in image.pixels])
                            image = Image.frombytes("RGBA", (width, height), buf, 'raw', "RGBA")

                            bitmap_format = BITMAP.bitmap_body.format
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
                    BITMAP.bitmap_body.processed_pixel_data = TAG.RawData(len(pixel_data))
                    BITMAP.bitmap_body.processed_pixels = pixel_data

                    BITMAP.bitmap_body.sequences_tag_block = TAG.TagBlock(len(BITMAP.sequences))
                    BITMAP.bitmap_body.bitmaps_tag_block = TAG.TagBlock(len(BITMAP.bitmaps))

                    output_stream = open(bitmap_path, 'wb')
                    build_h1_bitmap(output_stream, BITMAP, report)
                    output_stream.close()

    elif game_title == "halo2" and Image:
        levels_collection = bpy.data.collections.get("BSPs")
        if not levels_collection == None:
            for bsp_idx, bsp_collection in enumerate(levels_collection.children):
                for cluster_collection in bsp_collection.children:
                    cluster_collection.hide_render = True

        input_stream = open(scenario_path, "rb")
        SCNR_ASSET = process_h2_scenario(input_stream, report)
        input_stream.close()

        TAG = tag_format.TagAsset()
        for bsp_element in SCNR_ASSET.structure_bsps:
            bsp_name = os.path.basename(bsp_element.structure_bsp.name)
            lightmap_name = "%s_lightmaps" % bsp_name
            lightmap_collection = bpy.data.collections.get(lightmap_name)
            if not lightmap_collection == None:
                BSP_ASSET = parse_tag(bsp_element.structure_bsp, report, game_title, "retail")
                LTMP_ASSET = parse_tag(bsp_element.structure_lightmap, report, game_title, "retail")
                BITMAP_ASSET = parse_tag(LTMP_ASSET.lightmap_groups[0].bitmap_group_tag_ref, report, game_title, "retail")

                bitmap_path = os.path.join(bpy.context.preferences.addons["io_scene_halo"].preferences.halo_2_tag_path, "%s.bitmap" %  LTMP_ASSET.lightmap_groups[0].bitmap_group_tag_ref.name)

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
                BITMAP.header.checksum = -1
                BITMAP.header.data_offset = 64
                BITMAP.header.data_length = 0
                BITMAP.header.unk2 = 0
                BITMAP.header.version = 7
                BITMAP.header.destination = 0
                BITMAP.header.plugin_handle = -1
                BITMAP.header.engine_tag = "BLM!"

                BITMAP.bitmap_body_header = TAG.TagBlockHeader("tbfd", 0, 1, 112)
                BITMAP.bitmap_body = BITMAP.BitmapBody()
                BITMAP.bitmap_body.format = H2FormatEnum.compressed_with_color_key_transparency.value
                BITMAP.bitmap_body.usage = H2UsageEnum.alpha_blend.value
                BITMAP.bitmap_body.color_plate_width = 0
                BITMAP.bitmap_body.color_plate_height = 0
                BITMAP.bitmap_body.compressed_color_plate_data = TAG.RawData()
                BITMAP.bitmap_body.compressed_color_plate = bytes()
                BITMAP.bitmap_body.processed_pixel_data = TAG.RawData()
                BITMAP.bitmap_body.processed_pixels = bytes()
                BITMAP.sequences = []
                BITMAP.bitmaps = []

                lightmap_idx = 0
                lightmap_collection.hide_render = False
                for lightmap_ob in lightmap_collection.objects:
                    if lightmap_ob.tag_view.instance_lightmap_policy_enum == '0':
                        bitmap_element = BITMAP_ASSET.bitmaps[lightmap_idx]
                        width = int(bitmap_element.width * image_multiplier)
                        height = int(bitmap_element.height * image_multiplier)
                        image = bpy.data.images.get("Lightmap_%s" % lightmap_idx)
                        if not image:
                            image = bpy.data.images.new("Lightmap_%s" % lightmap_idx, width, height)
                        else:
                            image.scale(width, height)
                            image.update()

                        lightmap_idx += 1
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

                        lightmap_ob.select_set(True)
                        context.view_layer.objects.active = lightmap_ob

                        context.scene.render.engine = 'CYCLES'
                        bpy.ops.object.bake(type='DIFFUSE', pass_filter={'DIRECT','INDIRECT'}, uv_layer=lightmap_ob.data.uv_layers[1].name)
                        lightmap_ob.select_set(False)
                        context.view_layer.objects.active = None

                        buf = bytearray([int(p * 255) for p in image.pixels])
                        image = Image.frombytes("RGBA", (width, height), buf, 'raw', "RGBA")

                        bitmap_format = BITMAP.bitmap_body.format
                        lightmap_flags = H2BitmapFlags.power_of_two_dimensions.value

                        lightmap_image = image.convert('RGBA')
                        r,g,b,a = lightmap_image.split()
                        lightmap_data = Image.merge("RGBA", (b, g, r, a)).tobytes()
                        lightmap_format = H2BitmapFormatEnum.a8r8g8b8.value

                        pixel_data = pixel_data + lightmap_data

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

                        BITMAP.bitmaps.append(bitmap_class)

                        pixel_offset += len(lightmap_data)

                lightmap_collection.hide_render = True
                BITMAP.bitmap_body.processed_pixel_data = TAG.RawData(len(pixel_data))
                BITMAP.bitmap_body.processed_pixels = pixel_data

                bitmap_count = len(BITMAP.bitmaps)
                BITMAP.sequence_header = TAG.TagBlockHeader("tbfd", 0, 0, 64)
                if H2V:
                    BITMAP.bitmap_header = TAG.TagBlockHeader("tbfd", 1, bitmap_count, 116)
                else:
                    BITMAP.bitmap_header = TAG.TagBlockHeader("tbfd", 2, bitmap_count, 140)

                BITMAP.bitmap_body.sequences_tag_block = TAG.TagBlock()
                BITMAP.bitmap_body.bitmaps_tag_block = TAG.TagBlock(bitmap_count)

                output_stream = open(bitmap_path, 'wb')
                build_h2_bitmap(output_stream, BITMAP, report, H2V)
                output_stream.close()

    return {'FINISHED'}

if __name__ == '__main__':
    bpy.ops.halo_bulk.bake_clusters()
