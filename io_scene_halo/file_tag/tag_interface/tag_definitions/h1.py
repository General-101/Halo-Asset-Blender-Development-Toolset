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

import re
import os
import json
import xml.etree.ElementTree as ET

try:
    from .. import tag_common
except ImportError:
    import tag_common
    
from .common import initialize_definitions, parse_all_xmls, dump_merged_xml, merge_parent_tag, DUMP_XML

def get_pad_size(field_node):
    return int(field_node.attrib.get('length', 0))

def calculate_field_size(field_node):
    tag = field_node.tag
    if tag in tag_common.pad_tags:
        return get_pad_size(field_node)

    return tag_common.field_sizes.get(tag, 0)

def calculate_fieldset_size(fieldset_node):
    total_size = 0
    for child in fieldset_node:
        count = int(child.attrib.get('count', '1'))
        tag = child.tag
        if tag == 'Struct':
            layout = child.find('Layout')
            if layout is not None:
                nested_fieldsets = layout.findall('FieldSet')
                for nested_fs in nested_fieldsets:
                    calculate_fieldset_size(nested_fs)
                    nested_size = int(nested_fs.attrib.get('sizeofValue', '0'))
                    total_size += nested_size * count

            else:
                pass

        else:
            field_size = calculate_field_size(child)
            total_size += field_size * count

    fieldset_node.attrib['sizeofValue'] = str(total_size)

def resolve_inherited_fields(struct_def, root_lookup):
    fields = []
    inherits_value = struct_def.get('inherits')
    if inherits_value:
        inherited_struct = root_lookup.get(inherits_value)
        if not inherited_struct:
            inherited_struct = next((v for k, v in root_lookup.items() if k.lower() == inherits_value.lower()), None)

        if inherited_struct:
            inherited_fields = resolve_inherited_fields(inherited_struct, root_lookup)
            fields.extend(inherited_fields)

        else:
            print(f"Warning: Could not resolve inherited struct '{inherits_value}'")

    fields.extend(struct_def.get('fields', []))

    return fields

def purge_invalid_xml_chars(field_name):
    reserved = ['<', '>', '&', '"', "'"]
    for char in reserved:
        field_name = field_name.replace(char, "")

    problem_chars = "€‚ƒ„…†‡ˆ‰Š‹ŒŽ‘’“”•–—˜™š›œžŸ°"
    for char in problem_chars:
        field_name = field_name.replace(char, "")

    illegal_xml_re = re.compile(
        r'[\x00-\x08\x0B\x0C\x0E-\x1F\uD800-\uDFFF\uFFFE\uFFFF]'
    )
    field_name = illegal_xml_re.sub("", field_name)

    return field_name

def remove_alpha_num(value):
    return "".join(c for c in value if c.isalnum() or c == "_")

def generate_csharp_style_name(field_name, is_struct=False):
    if is_struct:
        split_name = re.sub(r'(?<!^)([A-Z])', r' \1', field_name).split()
    else:
        split_name = re.split(r"[ _-]+", field_name.lower().strip())

    for i in range(len(split_name)):
        entry = remove_alpha_num(split_name[i])

        if entry.lower().startswith("dxt"):
            entry = entry.replace("dxt", "DXT")

        if len(entry) > 0:
            split_name[i] = entry[0].upper() + entry[1:]
        else:
            split_name[i] = ""

    cs_name = purge_invalid_xml_chars("".join(split_name))

    return cs_name

def generate_cstyle_name(field_name, is_struct=False):
    if is_struct:
        c_name = re.sub(r'(?<!^)([A-Z])', r'_\1', field_name).lower()
    else:
        c_name = field_name.lower().strip().replace(" ", "_").replace("-", "_")

    c_name = "".join(c for c in c_name if c.isalnum() or c == "_")

    if len(c_name) == 0:
        return None

    if not c_name[0].isalpha():
        c_name = "_" + c_name

    if c_name == "default":
        c_name = "default_value"

    c_keywords = {
        "alignas", "alignof", "and", "and_eq", "asm", "atomic_cancel", "atomic_commit",
        "atomic_noexcept", "auto", "bitand", "bitor", "bool", "break", "case", "catch",
        "char", "char8_t", "char16_t", "char32_t", "class", "co_await", "co_return",
        "co_yield", "compl", "concept", "const", "consteval", "constexpr", "constinit",
        "const_cast", "continue", "decltype", "default", "delete", "do", "double",
        "dynamic_cast", "else", "enum", "explicit", "export", "extern", "false",
        "float", "for", "friend", "goto", "if", "inline", "int", "long", "mutable",
        "namespace", "new", "noexcept", "not", "not_eq", "nullptr", "operator",
        "or", "or_eq", "private", "protected", "public", "register", "reinterpret_cast",
        "requires", "return", "short", "signed", "sizeof", "static", "static_assert",
        "static_cast", "struct", "switch", "synchronized", "template", "this", "thread_local",
        "throw", "true", "try", "typedef", "typeid", "typename", "union", "unsigned",
        "using", "virtual", "void", "volatile", "wchar_t", "while", "xor", "xor_eq"
    }

    if c_name in c_keywords:
        c_name = "_" + c_name

    python_keywords = {
        "False", "None", "True", "and", "as", "assert", "async", "await", "break", "class",
        "continue", "def", "del", "elif", "else", "except", "finally", "for", "from",
        "global", "if", "import", "in", "is", "lambda", "nonlocal", "not", "or", "pass",
        "raise", "return", "try", "while", "with", "yield"
    }

    if c_name in python_keywords:
        c_name = "_" + c_name

    c_name = purge_invalid_xml_chars(c_name)

    return c_name

def generate_defs_from_jsons(base_dir, output_dir):
    all_data = []
    for filename in os.listdir(base_dir):
        if filename.endswith('.json'):
            with open(os.path.join(base_dir, filename), 'r', encoding='utf-8') as f:
                try:
                    data = json.load(f)
                    if isinstance(data, list):
                        all_data.extend(data)

                except Exception as e:
                    print(f"Error in {filename}: {e}")

    root_lookup = {item['name']: item for item in all_data if isinstance(item, dict) and 'name' in item}
    generated_xmls = {}

    for group_entry in [item for item in all_data if item.get('type') == 'group']:
        name = group_entry['name']
        struct_name = group_entry['struct']
        version = str(group_entry.get('version', 0))
        fourcc = next((k for k, v in tag_common.h1_tag_groups.items() if v == name), "unknown")

        root = ET.Element('TagGroup', group=fourcc, name=name, version=version)
        layout = ET.SubElement(root, 'Layout', regolithID="%s:%s" % ("block", name), internalName="%s_block" % name, name=name)
        fieldset = ET.SubElement(layout, 'FieldSet', version="0", sizeofValue="0", sizeofSource=f"sizeof(struct {name}_group)", isLatest="true")

        struct_def = root_lookup.get(struct_name)
        if not struct_def:
            print(f"Missing struct definition for {struct_name}")
            continue

        def add_fields(fields, parent):
            for field in fields:
                if isinstance(field, str):
                    continue

                field_type = purge_invalid_xml_chars(field.get('type'))
                field_name = purge_invalid_xml_chars(field.get('name') or field.get('heading') or field_type)
                c_style_name = generate_cstyle_name(field_name)
                p_style_name = generate_csharp_style_name(field_name)

                count = field.get('count', 1)
                if field_type == 'editor_section':
                    for _ in range(count):
                        node = ET.SubElement(parent, 'Explanation', name=field_name)
                        if "cache_only" in field:
                            node.set("cacheOnly", str(field["cache_only"]).lower())

                        if "endian_override" in field:
                            node.set("endianOverride", field["endian_override"])

                        desc = field.get('body')
                        if desc is not None:
                            node.set('description', purge_invalid_xml_chars(desc))

                    continue

                if field_type == 'pad':
                    for _ in range(count):
                        node = ET.SubElement(parent, 'Pad', name=field_name)
                        if "cache_only" in field:
                            node.set("cacheOnly", str(field["cache_only"]).lower())

                        if "endian_override" in field:
                            node.set("endianOverride", field["endian_override"])

                        if 'size' in field:
                            node.set('length', str(field['size']))

                        desc = field.get('comment')
                        if desc is not None:
                            node.set('description', purge_invalid_xml_chars(desc))

                    continue

                if field_type == 'Reflexive':
                    for _ in range(count):
                        node = ET.SubElement(parent, 'Block')
                        node.set("CStyleName", c_style_name)
                        node.set("pascalStyleName", p_style_name)
                        node.set("name", field_name)
                        if "cache_only" in field:
                            node.set("cacheOnly", str(field["cache_only"]).lower())

                        if "endian_override" in field:
                            node.set("endianOverride", field["endian_override"])

                        if 'limit' in field:
                            node.set('maxElementCount', str(field['limit']))

                        desc = field.get('comment')
                        if desc is not None:
                            node.set('description', purge_invalid_xml_chars(desc))

                        ref_struct_name = field.get('struct')
                        ref_struct = root_lookup.get(ref_struct_name)
                        if ref_struct:
                            inner_layout = ET.SubElement(node, 'Layout')
                            inner_layout.set("regolithID", "block:%s" % field_name)
                            inner_layout.set("internalName", "%s_block" % field_name)
                            inner_layout.set("name", "%s_block" % field_name)
                            inner_fieldset = ET.SubElement(inner_layout, 'FieldSet', version="0", sizeofValue="0", isLatest="true")
                            ref_fields = resolve_inherited_fields(ref_struct, root_lookup)
                            add_fields(ref_fields, inner_fieldset)
                            calculate_fieldset_size(inner_fieldset)

                    continue

                if field_type == 'TagReference':
                    for _ in range(count):
                        node = ET.SubElement(parent, 'TagReference')
                        node.set("CStyleName", c_style_name)
                        node.set("pascalStyleName", p_style_name)
                        node.set("name", field_name)
                        if "cache_only" in field:
                            node.set("cacheOnly", str(field["cache_only"]).lower())

                        if "endian_override" in field:
                            node.set("endianOverride", field["endian_override"])

                        desc = field.get('comment')
                        if desc is not None:
                            node.set('description', purge_invalid_xml_chars(desc))

                        groups = field.get('groups', [])
                        if len(groups) == 1:
                            tag = ET.SubElement(node, 'tag')
                            tag.text = groups[0]

                        elif len(groups) == 0:
                            ET.SubElement(node, 'tag')

                    continue

                if field.get("bounds", False):
                    for _ in range(count):
                        if field_type == "float":
                            key = "RealBounds"
                            xml_tag = tag_common.invader_key_conversion.get(key)
                            if not xml_tag:
                                print(f"Missing conversion for type: {key}")
                                continue

                            node = ET.SubElement(parent, xml_tag)
                            node.set("CStyleName", c_style_name)
                            node.set("pascalStyleName", p_style_name)
                            node.set("name", field_name)
                            if "cache_only" in field:
                                node.set("cacheOnly", str(field["cache_only"]).lower())

                            if "endian_override" in field:
                                node.set("endianOverride", field["endian_override"])

                            desc = field.get('comment')
                            if desc is not None:
                                node.set('description', purge_invalid_xml_chars(desc))

                        elif field_type == "Angle":
                            key = "AngleBounds"
                            xml_tag = tag_common.invader_key_conversion.get(key)
                            if not xml_tag:
                                print(f"Missing conversion for type: {key}")
                                continue

                            node = ET.SubElement(parent, xml_tag)
                            node.set("CStyleName", c_style_name)
                            node.set("pascalStyleName", p_style_name)
                            node.set("name", field_name)
                            if "cache_only" in field:
                                node.set("cacheOnly", str(field["cache_only"]).lower())

                            if "endian_override" in field:
                                node.set("endianOverride", field["endian_override"])

                            desc = field.get('comment')
                            if desc is not None:
                                node.set('description', purge_invalid_xml_chars(desc))

                        elif field_type == "int16":
                            key = "ShortBounds"
                            xml_tag = tag_common.invader_key_conversion.get(key)
                            if not xml_tag:
                                print(f"Missing conversion for type: {key}")
                                continue

                            node = ET.SubElement(parent, xml_tag)
                            node.set("CStyleName", c_style_name)
                            node.set("pascalStyleName", p_style_name)
                            node.set("name", field_name)
                            if "cache_only" in field:
                                node.set("cacheOnly", str(field["cache_only"]).lower())

                            if "endian_override" in field:
                                node.set("endianOverride", field["endian_override"])

                            desc = field.get('comment')
                            if desc is not None:
                                node.set('description', purge_invalid_xml_chars(desc))

                        elif field_type in ("ColorRGBFloat", "ColorARGBFloat"):
                            key = field_type
                            xml_tag = tag_common.invader_key_conversion.get(key)
                            if not xml_tag:
                                print(f"Missing conversion for type: {key}")
                                continue

                            for suffix in [" lower bound", " upper bound"]:
                                node = ET.SubElement(parent, xml_tag)
                                node.set("CStyleName", c_style_name)
                                node.set("pascalStyleName", p_style_name)
                                node.set("name", field_name + suffix)
                                if "cache_only" in field:
                                    node.set("cacheOnly", str(field["cache_only"]).lower())

                                if "endian_override" in field:
                                    node.set("endianOverride", field["endian_override"])

                                desc = field.get('comment')
                                if desc is not None:
                                    node.set('description', purge_invalid_xml_chars(desc))

                    continue

                ref_struct = root_lookup.get(field_type)
                if ref_struct:
                    struct_type = ref_struct.get('type')
                    struct_name = purge_invalid_xml_chars(ref_struct.get('name') or ref_struct.get('heading') or struct_type)
                    struct_r_name = re.sub(r'(?<!^)([A-Z])', r' \1', struct_name).lower()
                    struct_c_style_name = generate_cstyle_name(struct_name, True)
                    struct_p_style_name = generate_csharp_style_name(struct_name, True)

                    key = f"bitfield{ref_struct.get('width')}" if struct_type == 'bitfield' else struct_type
                    xml_tag = tag_common.invader_key_conversion.get(key)
                    if not xml_tag:
                        print(f"Missing conversion for type: {key}")
                        continue

                    for _ in range(count):
                        struct_node = ET.SubElement(parent, xml_tag)
                        struct_node.set("CStyleName", c_style_name)
                        struct_node.set("pascalStyleName", p_style_name)
                        struct_node.set("name", field_name)
                        if "cache_only" in field:
                            struct_node.set("cacheOnly", str(field["cache_only"]).lower())

                        if "endian_override" in field:
                            struct_node.set("endianOverride", field["endian_override"])

                        desc = field.get('comment')
                        if desc is not None:
                            struct_node.set('description', purge_invalid_xml_chars(desc))

                        if xml_tag == 'Struct':
                            inner_layout = ET.SubElement(struct_node, 'Layout')
                            inner_layout.set("regolithID", "structure:%s" % struct_c_style_name)
                            inner_layout.set("internalName", struct_c_style_name + "_struct")
                            inner_layout.set("backingBlockInternalName", struct_c_style_name + "_struct_block")
                            inner_layout.set("name", struct_r_name)
                            inner_fieldset = ET.SubElement(inner_layout, 'FieldSet', version="0", sizeofValue="0", isLatest="true")
                            ref_fields = resolve_inherited_fields(ref_struct, root_lookup)
                            add_fields(ref_fields, inner_fieldset)
                            calculate_fieldset_size(inner_fieldset)

                        if struct_type == "bitfield" or struct_type == "enum":
                            options = ET.SubElement(struct_node, "Options")
                            options.set("regolithID", "enum:%s" % c_style_name)
                            options.set("CStyleName", c_style_name)
                            options.set("pascalStyleName", p_style_name)
                            if struct_type == "bitfield":
                                field_items = ref_struct.get("fields", [])
                                for entry in field_items:
                                    entry_name = entry
                                    desc = None
                                    if isinstance(entry, dict):
                                        entry_name = entry.get("name")
                                        desc = entry.get('comment')
                                        if not entry_name:
                                            entry_name = "bit"

                                    entry_name = purge_invalid_xml_chars(entry_name)
                                    bit_c_style_name = generate_cstyle_name(entry_name) + "_bit"
                                    bit_p_style_name = generate_csharp_style_name(entry_name) + "Bit"

                                    bit_layout = ET.SubElement(options,"Bit")
                                    bit_layout.set("name", entry_name)
                                    bit_layout.set("CStyleName", bit_c_style_name)
                                    bit_layout.set("pascalStyleName", bit_p_style_name)
                                    if desc is not None:
                                        bit_layout.set('description', purge_invalid_xml_chars(desc))

                            if struct_type == "enum":
                                field_items = ref_struct.get("options", [])
                                for entry in field_items:
                                    entry_name = entry
                                    desc = None
                                    if isinstance(entry, dict):
                                        entry_name = entry.get("name")
                                        desc = entry.get('comment')
                                        if not entry_name:
                                            entry_name = "enum"

                                    entry_name = purge_invalid_xml_chars(entry_name)
                                    enum_c_style_name = generate_cstyle_name(entry_name)
                                    enum_p_style_name = generate_csharp_style_name(entry_name)

                                    enum_layout = ET.SubElement(options,"Enum")
                                    enum_layout.set("name", entry_name)
                                    enum_layout.set("CStyleName", enum_c_style_name)
                                    enum_layout.set("pascalStyleName", enum_p_style_name)
                                    if desc is not None:
                                        enum_layout.set('description', purge_invalid_xml_chars(desc))

                    continue

                key = f"bitfield{field.get('width')}" if field_type == 'bitfield' else field_type
                xml_tag = tag_common.invader_key_conversion.get(key)
                if not xml_tag:
                    print(f"Missing conversion for type: {key}")
                    continue

                for _ in range(count):
                    node = ET.SubElement(parent, xml_tag, CStyleName=c_style_name, pascalStyleName=p_style_name, name=field_name)
                    if "cache_only" in field:
                        node.set("cacheOnly", str(field["cache_only"]).lower())

                    if "endian_override" in field:
                        node.set("endianOverride", field["endian_override"])

                    if field_type in {"uint8", "uint16", "uint32"}:
                        node.set("unsigned", "true")

                    desc = field.get('comment')
                    if desc is not None:
                        node.set('description', purge_invalid_xml_chars(desc))

        resolved_fields = resolve_inherited_fields(struct_def, root_lookup)
        add_fields(resolved_fields, fieldset)
        calculate_fieldset_size(fieldset)

        generated_xmls[fourcc] = root

    regolith_map = {}
    for elem in generated_xmls.values():
        for subelem in elem.iter():
            reg_id = subelem.attrib.get("regolithID")
            if reg_id:
                regolith_map[reg_id] = subelem

    merged_cache = {}
    for group in generated_xmls:
        merge_parent_tag(group, generated_xmls, merged_cache, tag_common.h1_tag_groups, tag_common.h1_tag_extensions)

    for tag_def in merged_cache:
        initialize_definitions(merged_cache[tag_def], regolith_map)

    if DUMP_XML:
        dump_merged_xml(merged_cache, output_dir, tag_common.h1_tag_groups)

    return merged_cache

def generate_defs(base_dir, output_dir):
    tag_defs, regolith_map = parse_all_xmls(base_dir)
    merged_cache = {}
    for tag_def in tag_defs:
        merge_parent_tag(tag_def, tag_defs, merged_cache, tag_common.h1_tag_groups, tag_common.h1_tag_extensions)

    for tag_def in merged_cache:
        initialize_definitions(merged_cache[tag_def], regolith_map)

    if DUMP_XML:
        dump_merged_xml(merged_cache, output_dir, tag_common.h1_tag_groups)

    return merged_cache
