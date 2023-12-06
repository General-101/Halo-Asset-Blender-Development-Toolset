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
from .format import ItemCollectionAsset
from ....global_functions import tag_format

XML_OUTPUT = False

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    ITEMCOLLECTION = ItemCollectionAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    ITEMCOLLECTION.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    ITEMCOLLECTION.item_collection_body = ITEMCOLLECTION.ItemCollectionBody()
    ITEMCOLLECTION.item_collection_body.item_permutations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "item permutations"))
    ITEMCOLLECTION.item_collection_body.spawn_time = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(tag_node, "spawn time"))
    input_stream.read(78) # Padding?

    ITEMCOLLECTION.item_permutations = []
    item_permutations_node = tag_format.get_xml_node(XML_OUTPUT, ITEMCOLLECTION.item_collection_body.item_permutations_tag_block.count, tag_node, "name", "item permutations")
    for item_permutation_idx in range(ITEMCOLLECTION.item_collection_body.item_permutations_tag_block.count):
        item_permutation_element_node = None
        if XML_OUTPUT:
            item_permutation_element_node = TAG.xml_doc.createElement('element')
            item_permutation_element_node.setAttribute('index', str(item_permutation_idx))
            item_permutations_node.appendChild(item_permutation_element_node)

        item_permutation = ITEMCOLLECTION.ItemPermutation()
        input_stream.read(32) # Padding?
        item_permutation.weight = TAG.read_float(input_stream, TAG, tag_format.XMLData(item_permutation_element_node, "weight"))
        item_permutation.item = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(item_permutation_element_node, "item"))
        input_stream.read(32) # Padding?

        ITEMCOLLECTION.item_permutations.append(item_permutation)

    for item_permutation_idx, item_permutation in enumerate(ITEMCOLLECTION.item_permutations):
        item_permutation_element_node = None
        if XML_OUTPUT:
            item_permutation_element_node = item_permutations_node.childNodes[item_permutation_idx]

        if item_permutation.item.name_length > 0:
            item_permutation.item.name = TAG.read_variable_string(input_stream, item_permutation.item.name_length, TAG)

        if XML_OUTPUT:
            item_node = tag_format.get_xml_node(XML_OUTPUT, 1, item_permutation_element_node, "name", "item")
            item_permutation.item.append_xml_attributes(item_node)
    
    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, ITEMCOLLECTION.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return ITEMCOLLECTION
