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
from .format import SkyAsset, LightFlags

XML_OUTPUT = False

def process_file(input_stream, tag_format, report):
    TAG = tag_format.TagAsset()
    SKY = SkyAsset()
    TAG.is_legacy = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SKY.header = TAG.Header().read(input_stream, TAG)

    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    SKY.sky_body = SKY.SkyBody()
    SKY.sky_body.model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "model"))
    SKY.sky_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    input_stream.read(24) # Padding?
    SKY.sky_body.indoor_ambient_radiosity_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "indoor ambient radiosity color"))
    SKY.sky_body.indoor_ambient_radiosity_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "indoor ambient radiosity power"))
    SKY.sky_body.outdoor_ambient_radiosity_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor ambient radiosity color"))
    SKY.sky_body.outdoor_ambient_radiosity_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor ambient radiosity power"))
    SKY.sky_body.outdoor_fog_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor fog color"))
    input_stream.read(8) # Padding?
    SKY.sky_body.outdoor_fog_maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor fog maximum density"))
    SKY.sky_body.outdoor_fog_start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor fog start distance"))
    SKY.sky_body.outdoor_fog_opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor fog opaque distance"))
    SKY.sky_body.indoor_fog_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "indoor fog color"))
    input_stream.read(8) # Padding?
    SKY.sky_body.indoor_fog_maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "indoor fog maximum density"))
    SKY.sky_body.indoor_fog_start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "indoor fog start distance"))
    SKY.sky_body.indoor_fog_opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "indoor fog opaque distance"))
    SKY.sky_body.indoor_fog_screen = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "indoor fog screen"))
    input_stream.read(4) # Padding?
    SKY.sky_body.shader_functions = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "shader functions"))
    SKY.sky_body.animations = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "animations"))
    SKY.sky_body.lights = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lights"))

    if SKY.sky_body.model.name_length > 0:
        SKY.sky_body.model.name = TAG.read_variable_string(input_stream, SKY.sky_body.model.name_length, TAG)

    if SKY.sky_body.animation_graph.name_length > 0:
        SKY.sky_body.animation_graph.name = TAG.read_variable_string(input_stream, SKY.sky_body.animation_graph.name_length, TAG)

    if XML_OUTPUT:
        model_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "model")
        animation_graph_node = tag_format.get_xml_node(XML_OUTPUT, 1, tag_node, "name", "animation graph")
        SKY.sky_body.model.append_xml_attributes(model_node)
        SKY.sky_body.animation_graph.append_xml_attributes(animation_graph_node)

    SKY.shader_functions = []
    shader_functions_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.shader_functions.count, tag_node, "name", "shader functions")
    for shader_function_idx in range(SKY.sky_body.shader_functions.count):
        shader_function_element_node = None
        if XML_OUTPUT:
            shader_function_element_node = TAG.xml_doc.createElement('element')
            shader_function_element_node.setAttribute('index', str(shader_function_idx))
            shader_functions_node.appendChild(shader_function_element_node)

        input_stream.read(4) # Padding?
        global_function_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(shader_function_element_node, "label"))

        SKY.shader_functions.append(global_function_name)

    SKY.animations = []
    animations_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.animations.count, tag_node, "name", "animations")
    for animation_idx in range(SKY.sky_body.animations.count):
        animation_element_node = None
        if XML_OUTPUT:
            animation_element_node = TAG.xml_doc.createElement('element')
            animation_element_node.setAttribute('index', str(animation_idx))
            animations_node.appendChild(animation_element_node)

        animation = SKY.Animation()
        animation.animation_index = TAG.read_unsigned_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "animation index"))
        input_stream.read(2) # Padding?
        animation.period = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_element_node, "period"))
        input_stream.read(28) # Padding?

        SKY.animations.append(animation)

    SKY.lights = []
    lights_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.lights.count, tag_node, "name", "lights")
    for light_idx in range(SKY.sky_body.lights.count):
        light_element_node = None
        if XML_OUTPUT:
            light_element_node = TAG.xml_doc.createElement('element')
            light_element_node.setAttribute('index', str(light_idx))
            lights_node.appendChild(light_element_node)

        light = SKY.Light()
        light.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(light_element_node, "lens flare"))
        light.lens_flare_marker_name = TAG.read_string32(input_stream, TAG, tag_format.XMLData(light_element_node, "lens flare marker name"))
        input_stream.read(30) # Padding?
        light.flags = TAG.read_flag_unsigned_short(input_stream, TAG, tag_format.XMLData(light_element_node, "flags", LightFlags))
        light.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(light_element_node, "color"))
        light.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(light_element_node, "power"))
        light.test_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(light_element_node, "test distance"))
        input_stream.read(4) # Padding?
        light.direction = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(light_element_node, "direction"))
        light.diameter = TAG.read_degree(input_stream, TAG, tag_format.XMLData(light_element_node, "diameter"))

        SKY.lights.append(light)

    for light_idx, light in enumerate(SKY.lights):
        light_element_node = None
        if XML_OUTPUT:
            light_element_node = lights_node.childNodes[light_idx]

        if light.lens_flare.name_length > 0:
            light.lens_flare.name = TAG.read_variable_string(input_stream, light.lens_flare.name_length, TAG)

        if XML_OUTPUT:
            light_node = tag_format.get_xml_node(XML_OUTPUT, 1, light_element_node, "name", "lens flare")
            light.lens_flare.append_xml_attributes(light_node)
    
    current_position = input_stream.tell()
    EOF = input_stream.seek(0, 2)
    if not EOF - current_position == 0: # is something wrong with the parser?
        report({'WARNING'}, "%s elements left after parse end" % (EOF - current_position))

    if XML_OUTPUT:
        xml_str = TAG.xml_doc.toprettyxml(indent ="\t")

        save_path_file = tag_format.get_xml_path(input_stream.name, SKY.header.tag_group, TAG.is_legacy)

        with open(save_path_file, "w") as f:
            f.write(xml_str)

    return SKY
