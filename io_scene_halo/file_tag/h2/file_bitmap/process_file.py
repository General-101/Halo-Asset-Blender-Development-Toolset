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

from xml.dom import minidom
from ....global_functions import tag_format
from .format import (
        BitmapAsset,
        ImportTypeEnum,
        FormatEnum,
        UsageEnum,
        ImportFlags,
        SpriteBudgetSizeEnum,
        SpriteUsageEnum,
        ForceFormatEnum,
        MoreFlags,
        BitmapTypeEnum,
        BitmapFormatEnum,
        BitmapFlags,
        CacheUsageEnum
        )

XML_OUTPUT = False

def initilize_bitmap(BITMAP):
    BITMAP.sequences = []
    BITMAP.bitmaps = []

def read_bitmap_body(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT):
    BITMAP.bitmap_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    BITMAP.bitmap_body = BITMAP.BitmapBody()
    BITMAP.bitmap_body.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", ImportTypeEnum))
    BITMAP.bitmap_body.format = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "format", FormatEnum))
    BITMAP.bitmap_body.usage = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "usage", UsageEnum))
    BITMAP.bitmap_body.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", ImportFlags))
    BITMAP.bitmap_body.detail_fade_factor = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "detail fade factor"))
    BITMAP.bitmap_body.sharpen_amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "sharpen amount"))
    BITMAP.bitmap_body.bump_height = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bump height"))
    BITMAP.bitmap_body.sprite_budget_size = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sprite budget size", SpriteBudgetSizeEnum))
    BITMAP.bitmap_body.sprite_budget_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sprite budget count"))
    BITMAP.bitmap_body.color_plate_width = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "color plate width"))
    BITMAP.bitmap_body.color_plate_height = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "color plate height"))
    BITMAP.bitmap_body.compressed_color_plate_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "compressed color plate data"))
    BITMAP.bitmap_body.processed_pixel_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(tag_node, "processed pixel data"))
    BITMAP.bitmap_body.blur_filter_size = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "blur filter size"))
    BITMAP.bitmap_body.alpha_bias = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "alpha bias"))
    BITMAP.bitmap_body.mipmap_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "mipmap count"))
    BITMAP.bitmap_body.sprite_usage = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sprite usage", SpriteUsageEnum))
    BITMAP.bitmap_body.sprite_spacing = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "sprite spacing"))
    BITMAP.bitmap_body.force_format = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "force format", ForceFormatEnum))
    BITMAP.bitmap_body.sequences_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sequences"))
    BITMAP.bitmap_body.bitmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bitmaps"))
    if BITMAP.bitmap_body_header.size == 112:
        BITMAP.bitmap_body.color_compression_quality = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "color compression quality"))
        BITMAP.bitmap_body.alpha_compression_quality = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "alpha compression quality"))
        BITMAP.bitmap_body.overlap = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "overlap"))
        BITMAP.bitmap_body.color_subsampling = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(tag_node, "color subsampling"))

def read_sequences(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT):
    if BITMAP.bitmap_body.sequences_tag_block.count > 0:
        sequences_node = tag_format.get_xml_node(XML_OUTPUT, BITMAP.bitmap_body.sequences_tag_block.count, tag_node, "name", "sequences")
        BITMAP.sequence_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for sequence_idx in range(BITMAP.bitmap_body.sequences_tag_block.count):
            sequence_element_node = None
            if XML_OUTPUT:
                sequence_element_node = TAG.xml_doc.createElement('element')
                sequence_element_node.setAttribute('index', str(sequence_idx))
                sequences_node.appendChild(sequence_element_node)

            sequence = BITMAP.Sequence()
            sequence.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(sequence_element_node, "name"))
            sequence.first_bitmap_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(sequence_element_node, "first bitmap index"))
            sequence.bitmap_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(sequence_element_node, "bitmap count"))
            input_stream.read(16) # Padding
            sequence.sprites_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(sequence_element_node, "sprites"))

            BITMAP.sequences.append(sequence)

        for sequence_idx, sequence in enumerate(BITMAP.sequences):
            sequence_element_node = None
            if XML_OUTPUT:
                sequence_element_node = sequences_node.childNodes[sequence_idx]

            sequence.sprites = []
            if sequence.sprites_tag_block.count > 0:
                sprites_node = tag_format.get_xml_node(XML_OUTPUT, sequence.sprites_tag_block.count, sequence_element_node, "name", "sprites")
                sequence.sprites_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for sprite_idx in range(sequence.sprites_tag_block.count):
                    sprite_element_node = None
                    if XML_OUTPUT:
                        sprite_element_node = TAG.xml_doc.createElement('element')
                        sprite_element_node.setAttribute('index', str(sprite_idx))
                        sprites_node.appendChild(sprite_element_node)

                    sprite = BITMAP.Sprite()
                    sprite.bitmap_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(sprite_element_node, "bitmap index"))
                    input_stream.read(6) # Padding
                    sprite.left = TAG.read_float(input_stream, TAG, tag_format.XMLData(sprite_element_node, "left"))
                    sprite.right = TAG.read_float(input_stream, TAG, tag_format.XMLData(sprite_element_node, "right"))
                    sprite.top = TAG.read_float(input_stream, TAG, tag_format.XMLData(sprite_element_node, "top"))
                    sprite.bottom = TAG.read_float(input_stream, TAG, tag_format.XMLData(sprite_element_node, "bottom"))
                    sprite.registration_point = TAG.read_point_2d(input_stream, TAG, tag_format.XMLData(sprite_element_node, "registration point"))

                    sequence.sprites.append(sprite)

def read_bitmaps(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT):
    if BITMAP.bitmap_body.bitmaps_tag_block.count > 0:
        bitmap_node = tag_format.get_xml_node(XML_OUTPUT, BITMAP.bitmap_body.bitmaps_tag_block.count, tag_node, "name", "bitmaps")
        BITMAP.bitmap_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for bitmap_idx in range(BITMAP.bitmap_body.bitmaps_tag_block.count):
            bitmap_element_node = None
            if XML_OUTPUT:
                bitmap_element_node = TAG.xml_doc.createElement('element')
                bitmap_element_node.setAttribute('index', str(bitmap_idx))
                bitmap_node.appendChild(bitmap_element_node)

            bitmap = BITMAP.Bitmap()
            if BITMAP.bitmap_header.version == 1:
                bitmap.signature = TAG.read_variable_string_no_terminator(input_stream, 4, TAG, tag_format.XMLData(bitmap_element_node, "signature"))
                bitmap.width = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "width"))
                bitmap.height = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "height"))
                bitmap.depth = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "depth"))
                bitmap.more_flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "more flags", MoreFlags))
                bitmap.bitmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "type", BitmapTypeEnum))
                bitmap.bitmap_format = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "format", BitmapFormatEnum))
                bitmap.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "flags", BitmapFlags))
                bitmap.registration_point = TAG.read_point_2d_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "registration point"))
                bitmap.mipmap_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "mipmap count"))
                bitmap.low_detail_mipmap_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "low detail mipmap count"))
                bitmap.pixels_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "pixels offset"))
                input_stream.read(88) # Padding
                bitmap.native_mipmap_info_tag_block = TAG.TagBlock()

            elif BITMAP.bitmap_header.version == 2:
                bitmap.signature = TAG.read_variable_string_no_terminator(input_stream, 4, TAG, tag_format.XMLData(bitmap_element_node, "signature"))
                bitmap.width = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "width"))
                bitmap.height = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "height"))
                bitmap.depth = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "depth"))
                bitmap.more_flags = TAG.read_flag_unsigned_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "more flags", MoreFlags))
                bitmap.bitmap_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "type", BitmapTypeEnum))
                bitmap.bitmap_format = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "format", BitmapFormatEnum))
                bitmap.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "flags", BitmapFlags))
                bitmap.registration_point = TAG.read_point_2d_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "registration point"))
                bitmap.mipmap_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "mipmap count"))
                bitmap.lod_adjust = TAG.read_signed_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "lod adjust"))
                bitmap.cache_usage = TAG.read_enum_unsigned_byte(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "cache usage", CacheUsageEnum))
                bitmap.pixels_offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "pixels offset"))
                input_stream.read(4) # Padding
                bitmap.native_mipmap_info_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "native mipmap info"))
                bitmap.native_size = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "native size"))
                bitmap.tile_mode = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(bitmap_element_node, "tile mode"))
                input_stream.read(88) # Padding

            BITMAP.bitmaps.append(bitmap)

        for bitmap_idx, bitmap in enumerate(BITMAP.bitmaps):
            bitmap_element_node = None
            if XML_OUTPUT:
                bitmap_element_node = bitmap_node.childNodes[bitmap_idx]

            if BITMAP.bitmap_header.version == 2:
                BITMAP.nbmi_header = TAG.TagBlockHeader().read(input_stream, TAG)

            bitmap.native_mipmap_info = []
            if bitmap.native_mipmap_info_tag_block.count > 0:
                native_mipmap_info_node = tag_format.get_xml_node(XML_OUTPUT, bitmap.native_mipmap_info_tag_block.count, bitmap_element_node, "name", "native mipmap info")
                bitmap.native_mipmap_info_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for native_mipmap_info_idx in range(bitmap.native_mipmap_info_tag_block.count):
                    native_mipmap_info_element_node = None
                    if XML_OUTPUT:
                        native_mipmap_info_element_node = TAG.xml_doc.createElement('element')
                        native_mipmap_info_element_node.setAttribute('index', str(native_mipmap_info_idx))
                        native_mipmap_info_node.appendChild(native_mipmap_info_element_node)

                    native_mipmap_info = BITMAP.NativeMipMapInfo()
                    native_mipmap_info.offset = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(native_mipmap_info_element_node, "offset"))
                    native_mipmap_info.pitch_row = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(native_mipmap_info_element_node, "pitch row"))
                    native_mipmap_info.pitch_slice = TAG.read_signed_integer(input_stream, TAG, tag_format.XMLData(native_mipmap_info_element_node, "pitch slice"))

                    bitmap.native_mipmap_info.append(native_mipmap_info)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    BITMAP = BitmapAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    BITMAP.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_bitmap(BITMAP)
    read_bitmap_body(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT)
    if BITMAP.bitmap_body.compressed_color_plate_data.size > 0:
        size = input_stream.read(4) # Padding
        color_plate_length = BITMAP.bitmap_body.compressed_color_plate_data.size - 4
        if color_plate_length < 0:
            color_plate_length = 0

        BITMAP.bitmap_body.compressed_color_plate = input_stream.read(color_plate_length)

    BITMAP.bitmap_body.processed_pixels = input_stream.read(BITMAP.bitmap_body.processed_pixel_data.size)
    read_sequences(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT)
    read_bitmaps(BITMAP, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, BITMAP.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return BITMAP
