import os
import bpy
import base64
import numpy as np

from mathutils import Vector
from enum import Flag, Enum, auto
from ...file_tag.tag_interface import tag_interface, tag_common
from ..shader_generation.shader_helper import (connect_inputs, get_linked_node, get_output_material_node)

try:
    from PIL import Image
except ModuleNotFoundError:
    print("PIL not found. Unable to create image node.")
    Image = None

class RasterizerFlags(Flag):
    unfiltered = auto()
    undithered = auto()
    clamped = auto()
    trilinear_filtered = auto()
    alpha_replicate = auto()
    not_mipmapped = auto()
    alpha_test = auto()

class FormatEnum(Enum):
    _16_bit = 0
    _32_bit = auto()
    compressed = auto()

class EncodingEnum(Enum):
    _8bit = 0
    _8bit_intensity = auto()
    _16bit_555 = auto()
    _16bit_565 = auto()
    _16bit_4444 = auto()
    _16bit_8palette_plus_8alpha = auto()
    _16bit_intensity = auto()
    _32bit_888 = auto()
    _32bit_8888 = auto()
    _32bit_compressed = auto()
    _32bit_alpha_compressed = auto()

def decode_bitmap565(width, height, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(width):
        for height_idx in range(height):
            a = pixel_data[pixels_offset + (2 * (height_idx + height * width_idx))]
            b = pixel_data[pixels_offset + (2 * (height_idx + height * width_idx) + 1)]
            if big_endian:
                value = ((a << 8) | b)
            else:
                value = (a | (b << 8))

            red = (((value & 63488) >> 11) << 3)
            green = (((value & 2016) >> 5) << 2)
            blue = ((value & 31) << 3)

            yield (red, green, blue)

def decode_bitmap_8bit_intensity(width, height, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(width):
        for height_idx in range(height):
            value = pixel_data[pixels_offset + (height_idx + height * width_idx)]
            yield (value, value, value)

def decode_bitmap888(width, height, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(width):
        for height_idx in range(height):
            a = pixel_data[pixels_offset + (4 * (width_idx + width * height_idx) + 0)]
            b = pixel_data[pixels_offset + (4 * (width_idx + width * height_idx) + 1)]
            c = pixel_data[pixels_offset + (4 * (width_idx + width * height_idx) + 2)]
            d = pixel_data[pixels_offset + (4 * (width_idx + width * height_idx) + 3)]

            if big_endian:
                color_tuple = (b, c, d)
            else:
                color_tuple = (d, c, b)

            yield color_tuple

def decode_bitmap8888(width, height, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(width):
        for height_idx in range(height):
            a = pixel_data[pixels_offset + (4 * (height_idx + height * width_idx) + 0)]
            b = pixel_data[pixels_offset + (4 * (height_idx + height * width_idx) + 1)]
            c = pixel_data[pixels_offset + (4 * (height_idx + height * width_idx) + 2)]
            d = pixel_data[pixels_offset + (4 * (height_idx + height * width_idx) + 3)]

            if big_endian:
                color_tuple = (b, c, d, a)
            else:
                color_tuple = (a, d, c, b)

            yield color_tuple

def decode_bitmap4444(width, height, pixels_offset, pixel_data, big_endian=True):
    for width_idx in range(width):
        for height_idx in range(height):
            a = (pixel_data[pixels_offset + (2 * (height_idx + height * width_idx) + 0)] & 240)
            b = ((pixel_data[pixels_offset + (2 * (height_idx + height * width_idx) + 0)] & 15) << 4)
            c = (pixel_data[pixels_offset + (2 * (height_idx + height * width_idx) + 1)] & 240)
            d = ((pixel_data[pixels_offset + (2 * (height_idx + height * width_idx) + 1)] & 15) << 4)

            if big_endian:
                color_tuple = (b, c, d, a)
            else:
                color_tuple = (a, d, c, b)

            yield color_tuple

def decode_bitmap(bitmap, pixel_data):
    width = bitmap["width"]
    height = bitmap["height"]
    pixel_offset = bitmap["pixels offset"]
    encoding = EncodingEnum(bitmap["format"]["value"])

    image = None
    if Image:
        if encoding == EncodingEnum._16bit_565:
            image = Image.new('RGB', (width, height), color=0)
            pixels = list(decode_bitmap565(width, height, pixel_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        elif encoding == EncodingEnum._32bit_888:
            image = Image.new('RGB', (width, height), color=0)
            pixels = list(decode_bitmap888(width, height, pixel_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        elif encoding == EncodingEnum._32bit_8888:
            image = Image.new('RGBA', (width, height), color=0)
            pixels = list(decode_bitmap8888(width, height, pixel_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == EncodingEnum._16bit_4444:
            image = Image.new('RGBA', (width, height), color=0)
            pixels = list(decode_bitmap4444(width, height, pixel_offset, pixel_data))
            image.putdata(pixels)

        elif encoding == EncodingEnum._8bit_intensity:
            image = Image.new('RGB', (width, height), color=0)
            pixels = list(decode_bitmap_8bit_intensity(width, height, pixel_offset, pixel_data))
            image.putdata(pixels)
            image.putalpha(255)

        else:
            print("Unsupported format %s" % encoding)

    return image

def generate_image_node(mat, bitm_asset, asset_cache, tag_ref):
    image_node = mat.node_tree.nodes.new("ShaderNodeTexImage")
    bitmap_name = "White"
    image_path = tag_ref.get("path", "")
    image_group = tag_ref.get("group name", None)
    print(asset_cache)
    if bitm_asset and Image:
        texture = asset_cache[image_group][image_path]["blender_assets"].get("blender_asset")
        if texture is None:
            bitmap_name = bitm_asset["Header"]["name"]
            bitm_data = bitm_asset["Data"]
            primary_entry = None
            secondary_entry = None
            fallback_entry = None
            format_entry = None
            for format_element in bitm_data["formats"]:
                format_enum = FormatEnum(format_element["format"]["value"])
                if format_enum == FormatEnum._16_bit:
                    secondary_entry = format_element
                elif format_enum == FormatEnum._32_bit:
                    primary_entry = format_element
                elif format_enum == FormatEnum.compressed:
                    fallback_entry = format_element

            if not primary_entry == None:
                format_entry = primary_entry
            elif not secondary_entry == None:
                format_entry = secondary_entry
            elif not fallback_entry == None:
                format_entry = fallback_entry

            if format_entry is not None:
                pixel_data = base64.b64decode(format_entry["pixels"]["encoded"])
                for bitmap in format_entry["bitmaps"]:
                    pil_image = decode_bitmap(bitmap, pixel_data)
                    if not pil_image == None:
                        pil_image = pil_image.rotate(90, expand=True)
                        x = bitmap["width"]
                        y = bitmap["height"]

                        texture = bpy.data.images.new(bitmap_name, x, y, alpha = True)
                        normalized = 1.0 / 255.0
                        blender_pixels = (np.asarray(pil_image.convert('RGBA'),dtype=np.float32) * normalized).ravel()

                        texture.pixels[:] = blender_pixels
                        texture.pack()

                        asset_cache[image_group][image_path]["blender_assets"]["blender_asset"] = texture

                        break

        image_node.image = texture
            
    else:
        if not Image:
            print("Pillow is not installed. Generating white image.")
        else:
            print("Invalid bitmap. Generating white image.")
        image = bpy.data.images.new(bitmap_name, 2, 2)
        image.generated_color = (1, 1, 1, 1)
        image.pack()

        image_node.image = image

    return image_node

def generate_shader_simple(mat, map, asset_cache, report):
    if bpy.app.version < (5, 0, 0):
        mat.use_nodes = True
    tag_groups = tag_common.h1_20000525_tag_groups
    tag_extension = tag_groups.get(map["texture"]["group name"])
    bitm_asset = tag_interface.get_disk_asset(os.path.join(map["texture"]["path"]), tag_extension)

    output_material_node = get_output_material_node(mat)
    output_material_node.location = Vector((0.0, 0.0))
    bdsf_principled = get_linked_node(output_material_node, "Surface", "BSDF_PRINCIPLED")
    if bdsf_principled is None:
        bdsf_principled = mat.node_tree.nodes.new("ShaderNodeBsdfPrincipled")
        connect_inputs(mat.node_tree, bdsf_principled, "BSDF", output_material_node, "Surface")

    bdsf_principled.location = Vector((-260.0, 0.0))

    base_node = generate_image_node(mat, bitm_asset, asset_cache, map["texture"])
    if base_node is not None:
        base_node.location = Vector((-1600, 500))

        connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")

        if not base_node.image == None:
            base_node.image.alpha_mode = 'CHANNEL_PACKED'

        rasterizer_flags_result = RasterizerFlags(map["rasterizer flags"])
        if RasterizerFlags.alpha_test == rasterizer_flags_result:
            connect_inputs(mat.node_tree, base_node, "Alpha", bdsf_principled, "Alpha")
            mat.blend_method = 'HASHED'
        else:
            mat.blend_method = 'OPAQUE'

        connect_inputs(mat.node_tree, base_node, "Color", bdsf_principled, "Base Color")
