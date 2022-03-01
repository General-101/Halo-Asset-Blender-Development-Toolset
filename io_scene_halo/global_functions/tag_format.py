# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Steven Garcia
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

from mathutils import Vector

def check_file_size(input_stream):
    input_stream.seek(0, os.SEEK_END)
    filesize = input_stream.tell()
    input_stream.seek(0)

    return filesize

def check_group(input_stream):
    valid_group =  ["mode", "mod2", "coll", "phys", "antr", "sbsp", "psbs", "trak"]
    group_match = False

    input_stream.seek(36) # Position of tag group in all tags
    tag_group = input_stream.read(4).decode()
    input_stream.seek(0)
    if tag_group in valid_group:
        group_match = True

    return tag_group, group_match

class TagAsset():
    class TagBlock:
        def __init__(self, count=0, maximum_count=0, address=0, definition=0):
            self.count = count
            self.maximum_count = maximum_count
            self.address = address
            self.definition = definition

    class TagRef:
        def __init__(self, tag_group="", name="", name_length=0, salt=0, index=0):
            self.tag_group = tag_group
            self.name = name
            self.name_length = name_length
            self.salt = salt
            self.index = index

    class RawData:
        def __init__(self, size=0, flags=0, raw_pointer=0, pointer=0, id=0):
            self.size = size
            self.flags = flags
            self.raw_pointer = raw_pointer
            self.pointer = pointer
            self.id = id

    class Plane:
        def __init__(self, translation=Vector(), distance=0.0):
            self.translation = translation
            self.distance = distance

    class Header:
        def __init__(self, unk1=0, flags=0, type=0, name="", tag_group="", checksum=0, data_offset=0, data_length=0, unk2=0, version=0, destination=0, plugin_handle=0, engine_tag=""):
            self.unk1 = unk1
            self.flags = flags
            self.type = type
            self.name = name
            self.tag_group = tag_group
            self.checksum = checksum
            self.data_offset = data_offset
            self.data_length = data_length
            self.unk2 = unk2
            self.version = version
            self.destination = destination
            self.plugin_handle = plugin_handle
            self.engine_tag = engine_tag
