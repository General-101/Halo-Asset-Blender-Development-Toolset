# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2025 Steven Garcia
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

try:
    from .. import tag_common
except ImportError:
    import tag_common
    
from .common import initialize_definitions, parse_all_xmls, dump_merged_xml, merge_parent_tag, DUMP_XML

def generate_defs(base_dir, output_dir):
    tag_defs, regolith_map = parse_all_xmls(base_dir)
    merged_cache = {}
    for tag_def in tag_defs:
        merge_parent_tag(tag_def, tag_defs, merged_cache, tag_common.h2_tag_groups, tag_common.h2_tag_extensions)

    for tag_def in merged_cache:
        initialize_definitions(merged_cache[tag_def], regolith_map)

    if DUMP_XML:
        dump_merged_xml(merged_cache, output_dir, tag_common.h2_tag_groups)

    return merged_cache
