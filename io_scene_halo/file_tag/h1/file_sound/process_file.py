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
        SoundAsset,
        SoundFlags,
        ClassEnum,
        SampleRateEnum,
        EncodingEnum,
        CompressionEnum
        )

XML_OUTPUT = False

def initilize_sound(SOUND):
    SOUND.pitch_ranges = []

def read_sound_body(SOUND, TAG, input_stream, tag_node, XML_OUTPUT):
    SOUND.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SoundFlags))
    SOUND.class_type = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "class", ClassEnum))
    SOUND.sample_rate = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "sample rate", SampleRateEnum))
    SOUND.minimum_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "minimum distance"))
    SOUND.maximum_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum distance"))
    SOUND.skip_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "skip fraction"))
    SOUND.random_pitch_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(tag_node, "random pitch bounds"))
    SOUND.inner_cone_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "inner cone angle"))
    SOUND.outer_cone_angle = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "outer cone angle"))
    SOUND.outer_cone_gain = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum distance"))
    SOUND.randomization_gain_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gain modifier"))
    SOUND.maximum_bend_per_second = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "maximum bend per second"))
    SOUND.scale_zero_skip_fraction_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "skip fraction modifier"))
    SOUND.scale_zero_gain_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gain modifier"))
    SOUND.scale_zero_pitch_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "pitch modifier"))
    SOUND.scale_one_skip_fraction_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "skip fraction modifier"))
    SOUND.scale_one_gain_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gain modifier"))
    SOUND.scale_one_pitch_modifier = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "pitch modifier"))
    SOUND.encoding = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "encoding", EncodingEnum))
    SOUND.compression = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "compression", CompressionEnum))
    SOUND.promotion_sound = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "promotion sound"))
    SOUND.promotion_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(tag_node, "promotion count"))
    SOUND.pitch_ranges_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "pitch ranges"))

def read_pitch_ranges(SOUND, TAG, input_stream, tag_node, XML_OUTPUT):
    pitch_ranges_node = tag_format.get_xml_node(XML_OUTPUT, SOUND.pitch_ranges_tag_block.count, tag_node, "name", "pitch ranges")
    for pitch_range_idx in range(SOUND.pitch_ranges_tag_block.count):
        pitch_range_element_node = None
        if XML_OUTPUT:
            pitch_range_element_node = TAG.xml_doc.createElement('element')
            pitch_range_element_node.setAttribute('index', str(pitch_range_idx))
            pitch_ranges_node.appendChild(pitch_range_element_node)

        pitch_range = SOUND.PitchRange()
        pitch_range.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(pitch_range_element_node, "name"))
        pitch_range.natural_pitch = TAG.read_float(input_stream, TAG, tag_format.XMLData(pitch_range_element_node, "natural pitch"))
        pitch_range.bend_bounds = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(pitch_range_element_node, "bend bounds"))
        pitch_range.actual_permutation_count = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(pitch_range_element_node, "actual permutation count"))
        pitch_range.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(pitch_range_element_node, "permutations"))

        SOUND.pitch_ranges.append(pitch_range)

    for pitch_range_idx, pitch_range in enumerate(SOUND.pitch_ranges):
        pitch_range_element_node = None
        if XML_OUTPUT:
            pitch_range_element_node = pitch_ranges_node.childNodes[pitch_range_idx]

        pitch_range.permutations = []
        permutation_node = tag_format.get_xml_node(XML_OUTPUT, pitch_range.permutations_tag_block.count, pitch_range_element_node, "name", "permutations")
        for permutation_idx in range(pitch_range.permutations_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutation_node.appendChild(permutation_element_node)

            permutation = SOUND.Permutation()
            permutation.name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(permutation_element_node, "name"))
            permutation.skip_fraction = TAG.read_float(input_stream, TAG, tag_format.XMLData(permutation_element_node, "skip fraction"))
            permutation.gain = TAG.read_float(input_stream, TAG, tag_format.XMLData(permutation_element_node, "gain"))
            permutation.compression = TAG.read_enum_unsigned_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "compression", CompressionEnum))
            permutation.next_permutation_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(permutation_element_node, "next permutation index"))
            permutation.samples = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "samples"))
            permutation.mouth_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "mouth data"))
            permutation.subtitle_data = TAG.RawData().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "subtitle_data"))

            pitch_range.permutations.append(permutation)

        for permutation_idx, permutation in enumerate(pitch_range.permutations):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = permutation_node.childNodes[permutation_idx]

            permutation.samples.data = input_stream.read(permutation.samples.size)
            permutation.mouth_data.data = input_stream.read(permutation.mouth_data.size)
            permutation.subtitle_data.data = input_stream.read(permutation.subtitle_data.size)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SOUND = SoundAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SOUND.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_sound(SOUND)
    read_sound_body(SOUND, TAG, input_stream, tag_node, XML_OUTPUT)
    if SOUND.promotion_sound.name_length > 0:
        SOUND.promotion_sound.name = TAG.read_variable_string(input_stream, SOUND.promotion_sound.name_length, TAG)

    if XML_OUTPUT:
        promotion_sound_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "promotion sound")
        SOUND.promotion_sound.append_xml_attributes(promotion_sound_node)

    read_pitch_ranges(SOUND, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SOUND.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SOUND
