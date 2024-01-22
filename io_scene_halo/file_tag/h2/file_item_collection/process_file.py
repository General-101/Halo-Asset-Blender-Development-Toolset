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
from .format import CollectionAsset
from ....global_functions import tag_format

XML_OUTPUT = False

def initilize_collection(COLLECTION):
    COLLECTION.permutations = []

def read_collection_body_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT):
    COLLECTION.collection_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    COLLECTION.collection_body = COLLECTION.CollectionBody()
    COLLECTION.collection_body.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "item permutations"))
    COLLECTION.collection_body.spawn_time = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawn time"))
    input_stream.read(78) # Padding?

def read_collection_body_retail(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT):
    COLLECTION.collection_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    COLLECTION.collection_body = COLLECTION.CollectionBody()
    COLLECTION.collection_body.permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "item permutations"))
    COLLECTION.collection_body.spawn_time = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawn time"))
    input_stream.read(2) # Padding?

def read_permutations_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLECTION.collection_body.permutations_tag_block.count > 0:
        COLLECTION.permutations_header = TAG.TagBlockHeader().read(input_stream, TAG)
        permutations_node = tag_format.get_xml_node(XML_OUTPUT, COLLECTION.collection_body.permutations_tag_block.count, tag_node, "name", "item permutations")
        for permutation_idx in range(COLLECTION.collection_body.permutations_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutations_node.appendChild(permutation_element_node)

            permutation = COLLECTION.Permutation()
            input_stream.read(32) # Padding?
            permutation.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(permutation_element_node, "weight"))
            permutation.item = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "item"))
            
            TAG.big_endian = True
            input_stream.read(2) # Padding?
            permutation.variant_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False
            
            input_stream.read(28) # Padding?

            COLLECTION.permutations.append(permutation)

        for permutation_idx, permutation in enumerate(COLLECTION.permutations):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = permutations_node.childNodes[permutation_idx]

            if permutation.item.name_length > 0:
                permutation.item.name = TAG.read_variable_string(input_stream, permutation.item.name_length, TAG)

            if permutation.variant_length > 0:
                permutation.variant = TAG.read_variable_string_no_terminator(input_stream, permutation.variant_length, TAG, tag_format.XMLData(tag_node, "variant"))

            if XML_OUTPUT:
                item_node = tag_format.get_xml_node(XML_OUTPUT, 1, permutation_element_node, "name", "item")
                permutation.item.append_xml_attributes(item_node)

def read_permutations_retail(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT):
    if COLLECTION.collection_body.permutations_tag_block.count > 0:
        COLLECTION.permutations_header = TAG.TagBlockHeader().read(input_stream, TAG)
        permutations_node = tag_format.get_xml_node(XML_OUTPUT, COLLECTION.collection_body.permutations_tag_block.count, tag_node, "name", "item permutations")
        for permutation_idx in range(COLLECTION.collection_body.permutations_tag_block.count):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = TAG.xml_doc.createElement('element')
                permutation_element_node.setAttribute('index', str(permutation_idx))
                permutations_node.appendChild(permutation_element_node)

            permutation = COLLECTION.Permutation()
            permutation.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(permutation_element_node, "weight"))
            permutation.item = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(permutation_element_node, "item"))
            
            TAG.big_endian = True
            input_stream.read(2) # Padding?
            permutation.variant_length = TAG.read_signed_short(input_stream, TAG)
            TAG.big_endian = False

            COLLECTION.permutations.append(permutation)

        for permutation_idx, permutation in enumerate(COLLECTION.permutations):
            permutation_element_node = None
            if XML_OUTPUT:
                permutation_element_node = permutations_node.childNodes[permutation_idx]

            if permutation.item.name_length > 0:
                permutation.item.name = TAG.read_variable_string(input_stream, permutation.item.name_length, TAG)

            if permutation.variant_length > 0:
                permutation.variant = TAG.read_variable_string_no_terminator(input_stream, permutation.variant_length, TAG, tag_format.XMLData(tag_node, "variant"))

            if XML_OUTPUT:
                item_node = tag_format.get_xml_node(XML_OUTPUT, 1, permutation_element_node, "name", "item")
                permutation.item.append_xml_attributes(item_node)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    COLLECTION = CollectionAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    COLLECTION.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    initilize_collection(COLLECTION)
    if COLLECTION.header.engine_tag == "LAMB":
        read_collection_body_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)
        read_permutations_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)
    elif COLLECTION.header.engine_tag == "MLAB":
        read_collection_body_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)
        read_permutations_v0(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)
    elif COLLECTION.header.engine_tag == "BLM!":
        read_collection_body_retail(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)
        read_permutations_retail(COLLECTION, TAG, input_stream, tag_node, XML_OUTPUT)

    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, COLLECTION.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return COLLECTION
