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

from .format import WRLAsset
from ..global_functions import global_functions

DEBUG_PARSER = False

def process_old_vrml(input_stream):
    WRL = WRLAsset()
    root_nodes = []
    child_nodes = []
    content_nodes = []

    current_root_node = None
    current_child_node = None
    current_content_node = None

    wrl_content = ""
    for line in input_stream:
        element = line.strip()
        if element != '' and not element.startswith("#"):
            wrl_content += element

    previous_line = ""
    bracket_level = -1
    start_index = 0
    for char_idx, char in enumerate(wrl_content):
        if char == "{" or char == "[" :
            if char == "{":
                previous_line = "".join(wrl_content[start_index:char_idx]).replace('\t', '').strip("{[}] ")
                start_index = char_idx
                if bracket_level == -1:
                    current_root_node = WRL.Node()
                    current_root_node.header = previous_line
                    child_nodes = []

                else:
                    current_child_node = WRL.Node()
                    current_child_node.header = previous_line
                    content_nodes = []

                bracket_level += 1

            elif char == "[":
                previous_line = "".join(wrl_content[start_index:char_idx]).replace('\t', '').strip("{[}] ")
                start_index = char_idx
                current_content_node = WRL.Node()
                current_content_node.header = previous_line

        elif char == "}" or char == "]":
            if char == "}":
                previous_line = "".join(wrl_content[start_index:char_idx]).replace('\t', '').strip("{[}] ")
                start_index = char_idx

                if bracket_level >= 1:
                    current_child_node.content = previous_line

                bracket_level += -1
                if bracket_level == 0:
                    current_child_node.child_nodes = content_nodes
                    child_nodes.append(current_child_node)

                elif bracket_level == -1:
                    current_root_node.child_nodes = child_nodes
                    root_nodes.append(current_root_node)

            elif char == "]":
                previous_line = "".join(wrl_content[start_index:char_idx]).replace('\t', '').strip("{[}] ")
                start_index = char_idx
                current_content_node.content = previous_line
                content_nodes.append(current_content_node)

    WRL.nodes = root_nodes

    return WRL

def process_new_vrml(input_stream):
    WRL = WRLAsset()
    WRL.version = 2.0

    root_nodes = []
    child_nodes = []
    content_nodes = []
    value_nodes = []

    current_root_node = None
    current_child_node = None
    current_content_node = None
    current_value_node = None

    previous_line = ""
    store_content = False
    content = []
    bracket_level = -1
    for line in input_stream:
        element = line.strip()
        if element != '' and not element.startswith("#"):
            if element.endswith("FALSE") or element.endswith("TRUE"):
                current_child_node.content = element

            if element == "{" or element == "[" :
                if element == "{":
                    if bracket_level == -1:
                        current_root_node = WRL.Node()
                        current_root_node.header = previous_line
                        child_nodes = []

                    elif bracket_level == 0:
                        current_child_node = WRL.Node()
                        current_child_node.header = previous_line
                        content_nodes = []

                    else:
                        current_content_node = WRL.Node()
                        current_content_node.header = previous_line
                        value_nodes = []

                    bracket_level += 1

                elif element == "[":
                    store_content = True
                    current_value_node = WRL.Node()
                    current_value_node.header = previous_line

            elif element == "}" or element == "]":
                if element == "}":
                    bracket_level += -1
                    if bracket_level == 1:
                        current_content_node.child_nodes = value_nodes
                        content_nodes.append(current_content_node)

                    elif bracket_level == 0:
                        current_child_node.child_nodes = content_nodes
                        child_nodes.append(current_child_node)

                    elif bracket_level == -1:
                        current_root_node.child_nodes = child_nodes
                        root_nodes.append(current_root_node)

                elif element == "]":
                    current_value_node.content = content
                    value_nodes.append(current_value_node)
                    content = []
                    store_content = False

            previous_line = element
            if store_content:
                for set in element.replace(",", "").split():
                    line = set.strip("{[}] ")
                    if not global_functions.string_empty_check(line):
                        content.append(line)

    WRL.nodes = root_nodes

    return WRL

def process_file(input_stream):
    version_header = input_stream.readline().strip()
    print(version_header)
    if version_header == "#VRML V1.0 ascii":
        WRL = process_old_vrml(input_stream)

    elif version_header == "#VRML V2.0 utf8":
        WRL = process_new_vrml(input_stream)

    if DEBUG_PARSER:
        print(" ===== WRL ===== ")
        for root_node_idx, root_node in enumerate(WRL.nodes):
            print(" ===== Root Node %s ===== " % root_node_idx)
            print("Header: ", root_node.header)
            print("Type: ", root_node.content)
            for child_node_idx, child_node in enumerate(root_node.child_nodes):
                print(" ===== Child Node %s ===== " % child_node_idx)
                print("Header: ", child_node.header)
                print("Type: ", child_node.content)
                for content_node_idx, content_node in enumerate(child_node.child_nodes):
                    print(" ===== Content Node %s ===== " % content_node_idx)
                    print("Header: ", content_node.header)
                    print("Type: ", content_node.content)
                    for value_node_idx, value_node in enumerate(content_node.child_nodes):
                        print(" ===== Value Node %s ===== " % value_node_idx)
                        print("Header: ", value_node.header)
                        print("Type: ", value_node.content)
            print(" ")

    return WRL
