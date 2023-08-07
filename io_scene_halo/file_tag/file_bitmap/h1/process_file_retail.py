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
from .format_retail import (
        BitmapAsset,
        BitmapTypeEnum,
        FormatEnum,
        UsageEnum,
        BitmapFlags,
        SpriteBudgetSizeEnum,
        SpriteUsageEnum
        )

XML_OUTPUT = True

def process_file_retail(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    BITMAP = BitmapAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    BITMAP.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    BITMAP.bitmap_body = BITMAP.BitmapBody()
    BITMAP.bitmap_body.type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "type", BitmapTypeEnum))
    BITMAP.bitmap_body.format = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "format", FormatEnum))
    BITMAP.bitmap_body.usage = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "usage", UsageEnum))
    BITMAP.bitmap_body.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "flags", BitmapFlags))
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
    input_stream.read(2) # Padding
    BITMAP.bitmap_body.sequences_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sequences"))
    BITMAP.bitmap_body.bitmaps_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "bitmaps"))

    BITMAP.bitmap_body.compressed_color_plate = input_stream.read(BITMAP.bitmap_body.compressed_color_plate_data.size)
    BITMAP.bitmap_body.processed_pixels = input_stream.read(BITMAP.bitmap_body.processed_pixel_data.size)

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
