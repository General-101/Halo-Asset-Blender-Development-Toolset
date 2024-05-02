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
    SkyAsset,
    SkyFlags,
    LightFlags
    )

XML_OUTPUT = False

def initilize_sky(SKY):
    SKY.cubemap = []
    SKY.atmospheric_fog = []
    SKY.secondary_fog = []
    SKY.sky_fog = []
    SKY.patchy_fog = []
    SKY.lights = []
    SKY.shader_functions = []
    SKY.animations = []

def read_sky_body_v0(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    SKY.sky_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SKY.sky_body = SKY.SkyBody()
    SKY.sky_body.render_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "render model"))
    SKY.sky_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    SKY.sky_body.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SkyFlags))
    SKY.sky_body.render_model_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SKY.sky_body.movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SKY.sky_body.cubemap_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cubemap"))
    SKY.sky_body.indoor_ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "indoor ambient color"))
    input_stream.read(4) # Padding?
    SKY.sky_body.outdoor_ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor ambient color"))
    input_stream.read(4) # Padding?
    SKY.sky_body.fog_spread_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fog spread distance"))
    SKY.sky_body.atmospheric_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "atmospheric fog"))
    SKY.sky_body.secondary_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "secondary fog"))
    SKY.sky_body.sky_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sky fog"))
    SKY.sky_body.patchy_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "patchy fog"))
    SKY.sky_body.amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "amount"))
    SKY.sky_body.threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "threshold"))
    SKY.sky_body.brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "brightness"))
    SKY.sky_body.gamma_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gamma power"))
    SKY.sky_body.lights_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lights"))
    SKY.sky_body.global_sky_rotation = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "global sky rotation"))
    SKY.sky_body.shader_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "shader functions"))
    SKY.sky_body.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "animations"))
    input_stream.read(12) # Padding?

    if SKY.sky_body.render_model.name_length > 0:
        SKY.sky_body.render_model.name = TAG.read_variable_string(input_stream, SKY.sky_body.render_model.name_length, TAG)

    if SKY.sky_body.animation_graph.name_length > 0:
        SKY.sky_body.animation_graph.name = TAG.read_variable_string(input_stream, SKY.sky_body.animation_graph.name_length, TAG)

def read_sky_body_retail(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    SKY.sky_body_header = TAG.TagBlockHeader().read(input_stream, TAG)
    SKY.sky_body = SKY.SkyBody()
    SKY.sky_body.render_model = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "render model"))
    SKY.sky_body.animation_graph = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(tag_node, "animation graph"))
    SKY.sky_body.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(tag_node, "flags", SkyFlags))
    SKY.sky_body.render_model_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SKY.sky_body.movement_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "bounding radius"))
    SKY.sky_body.cubemap_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "cubemap"))
    SKY.sky_body.indoor_ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "indoor ambient color"))
    input_stream.read(4) # Padding?
    SKY.sky_body.outdoor_ambient_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "outdoor ambient color"))
    input_stream.read(4) # Padding?
    SKY.sky_body.fog_spread_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "fog spread distance"))
    SKY.sky_body.atmospheric_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "atmospheric fog"))
    SKY.sky_body.secondary_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "secondary fog"))
    SKY.sky_body.sky_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "sky fog"))
    SKY.sky_body.patchy_fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "patchy fog"))
    SKY.sky_body.amount = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "amount"))
    SKY.sky_body.threshold = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "threshold"))
    SKY.sky_body.brightness = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "brightness"))
    SKY.sky_body.gamma_power = TAG.read_float(input_stream, TAG, tag_format.XMLData(tag_node, "gamma power"))
    SKY.sky_body.lights_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "lights"))
    SKY.sky_body.global_sky_rotation = TAG.read_degree(input_stream, TAG, tag_format.XMLData(tag_node, "global sky rotation"))
    SKY.sky_body.shader_functions_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "shader functions"))
    SKY.sky_body.animations_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(tag_node, "animations"))
    input_stream.read(12) # Padding?
    SKY.sky_body.clear_color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(tag_node, "clear color"))

    if SKY.sky_body.render_model.name_length > 0:
        SKY.sky_body.render_model.name = TAG.read_variable_string(input_stream, SKY.sky_body.render_model.name_length, TAG)

    if SKY.sky_body.animation_graph.name_length > 0:
        SKY.sky_body.animation_graph.name = TAG.read_variable_string(input_stream, SKY.sky_body.animation_graph.name_length, TAG)

def read_cubemaps(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.cubemap_tag_block.count > 0:
        cubemaps_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.cubemap_tag_block.count, tag_node, "name", "cubemap")
        SKY.cubemap_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for cubemap_idx in range(SKY.sky_body.cubemap_tag_block.count):
            cubemap_element_node = None
            if XML_OUTPUT:
                cubemap_element_node = TAG.xml_doc.createElement('element')
                cubemap_element_node.setAttribute('index', str(cubemap_idx))
                cubemaps_node.appendChild(cubemap_element_node)

            cubemap = SKY.Cubemap()
            cubemap.cubemap_reference = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(cubemap_element_node, "cubemap reference"))
            cubemap.power_scale = TAG.read_float(input_stream, TAG, tag_format.XMLData(cubemap_element_node, "power scale"))

            SKY.cubemap.append(cubemap)

        for cubemap_idx, cubemap in enumerate(SKY.cubemap):
            cubemap_element_node = None
            if XML_OUTPUT:
                cubemap_element_node = cubemaps_node.childNodes[cubemap_idx]

            if cubemap.cubemap_reference.name_length > 0:
                cubemap.cubemap_reference.name = TAG.read_variable_string(input_stream, cubemap.cubemap_reference.name_length, TAG)

            if XML_OUTPUT:
                cubemap_reference_node = tag_format.get_xml_node(XML_OUTPUT, 1, cubemap_element_node, "name", "cubemap reference")
                cubemap.cubemap_reference.append_xml_attributes(cubemap_reference_node)

def read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, tag_block_count, tag_block_header, tag_block_name, tag_block):
    if tag_block_count > 0:
        fog_node = tag_format.get_xml_node(XML_OUTPUT, tag_block_count, tag_node, "name", tag_block_name)
        tag_block_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for fog_idx in range(tag_block_count):
            fog_element_node = None
            if XML_OUTPUT:
                fog_element_node = TAG.xml_doc.createElement('element')
                fog_element_node.setAttribute('index', str(fog_idx))
                fog_node.appendChild(fog_element_node)

            fog = SKY.Fog()
            fog.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(fog_element_node, "color"))
            fog.maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "maximum density"))
            fog.start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "start distance"))
            fog.opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "opaque distance"))

            tag_block.append(fog)

def read_sky_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.sky_fog_tag_block.count > 0:
        sky_fog_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.sky_fog_tag_block.count, tag_node, "name", "sky fog")
        SKY.sky_fog_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for sky_fog_idx in range(SKY.sky_body.sky_fog_tag_block.count):
            sky_fog_element_node = None
            if XML_OUTPUT:
                sky_fog_element_node = TAG.xml_doc.createElement('element')
                sky_fog_element_node.setAttribute('index', str(sky_fog_idx))
                sky_fog_node.appendChild(sky_fog_element_node)

            sky_fog = SKY.Fog()
            sky_fog.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(sky_fog_element_node, "color"))
            sky_fog.maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(sky_fog_element_node, "density"))

            SKY.sky_fog.append(sky_fog)

def read_patchy_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.patchy_fog_tag_block.count > 0:
        patchy_fog_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.patchy_fog_tag_block.count, tag_node, "name", "patchy fog")
        SKY.patchy_fog_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for patchy_fog_idx in range(SKY.sky_body.patchy_fog_tag_block.count):
            patchy_fog_element_node = None
            if XML_OUTPUT:
                patchy_fog_element_node = TAG.xml_doc.createElement('element')
                patchy_fog_element_node.setAttribute('index', str(patchy_fog_idx))
                patchy_fog_node.appendChild(patchy_fog_element_node)

            patchy_fog = SKY.PatchyFog()
            patchy_fog.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(patchy_fog_element_node, "color"))
            input_stream.read(12) # Padding?
            patchy_fog.density = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(patchy_fog_element_node, "density"))
            patchy_fog.distance = TAG.read_min_max(input_stream, TAG, tag_format.XMLData(patchy_fog_element_node, "distance"))
            input_stream.read(32) # Padding?
            patchy_fog.patchy_fog = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(patchy_fog_element_node, "patchy fog"))

            SKY.patchy_fog.append(patchy_fog)

        for patchy_fog_idx, patchy_fog in enumerate(SKY.patchy_fog):
            patchy_fog_element_node = None
            if XML_OUTPUT:
                patchy_fog_element_node = patchy_fog_node.childNodes[patchy_fog_idx]

            if patchy_fog.patchy_fog.name_length > 0:
                patchy_fog.patchy_fog.name = TAG.read_variable_string(input_stream, patchy_fog.patchy_fog.name_length, TAG)

            if XML_OUTPUT:
                patchy_fog_reference_node = tag_format.get_xml_node(XML_OUTPUT, 1, patchy_fog_element_node, "name", "patchy fog")
                patchy_fog.patchy_fog.append_xml_attributes(patchy_fog_reference_node)

def read_lights(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.lights_tag_block.count > 0:
        lights_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.lights_tag_block.count, tag_node, "name", "lights")
        SKY.lights_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for light_idx in range(SKY.sky_body.lights_tag_block.count):
            light_element_node = None
            if XML_OUTPUT:
                light_element_node = TAG.xml_doc.createElement('element')
                light_element_node.setAttribute('index', str(light_idx))
                lights_node.appendChild(light_element_node)

            light = SKY.Light()
            light.direction_vector = TAG.read_vector(input_stream, TAG, tag_format.XMLData(light_element_node, "direction vector"))
            light.direction = TAG.read_degree_2d(input_stream, TAG, tag_format.XMLData(light_element_node, "direction"))
            light.lens_flare = TAG.TagRef().read(input_stream, TAG, tag_format.XMLData(light_element_node, "lens flare"))
            light.fog_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(light_element_node, "fog"))
            light.fog_opposite_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(light_element_node, "fog opposite"))
            light.radiosity_tag_block = TAG.TagBlock().read(input_stream, TAG, tag_format.XMLData(light_element_node, "radiosity"))

            SKY.lights.append(light)

        for light_idx, light in enumerate(SKY.lights):
            light_element_node = None
            if XML_OUTPUT:
                light_element_node = lights_node.childNodes[light_idx]

            if light.lens_flare.name_length > 0:
                light.lens_flare.name = TAG.read_variable_string(input_stream, light.lens_flare.name_length, TAG)

            if XML_OUTPUT:
                lens_flare_reference_node = tag_format.get_xml_node(XML_OUTPUT, 1, light_element_node, "name", "lens flare")
                light.lens_flare.append_xml_attributes(lens_flare_reference_node)

            light.fog = []
            light.fog_opposite = []
            light.radiosity = []
            if light.fog_tag_block.count > 0:
                fog_node = tag_format.get_xml_node(XML_OUTPUT, light.fog_tag_block.count, light_element_node, "name", "fog")
                light.fog_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for fog_idx in range(light.fog_tag_block.count):
                    fog_element_node = None
                    if XML_OUTPUT:
                        fog_element_node = TAG.xml_doc.createElement('element')
                        fog_element_node.setAttribute('index', str(fog_idx))
                        fog_node.appendChild(fog_element_node)

                    light_fog = SKY.LightFog()
                    light_fog.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(fog_element_node, "color"))
                    light_fog.maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "maximum density"))
                    light_fog.start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "start distance"))
                    light_fog.opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "opaque distance"))
                    light_fog.cone = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(fog_element_node, "cone"))
                    light_fog.atmospheric_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "atmospheric fog influence"))
                    light_fog.secondary_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "secondary fog influence"))
                    light_fog.sky_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_element_node, "sky fog influence"))

                    light.fog.append(light_fog)

            if light.fog_opposite_tag_block.count > 0:
                fog_opposite_node = tag_format.get_xml_node(XML_OUTPUT, light.fog_opposite_tag_block.count, light_element_node, "name", "fog opposite")
                light.fog_opposite_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for fog_opposite_idx in range(light.fog_opposite_tag_block.count):
                    fog_opposite_element_node = None
                    if XML_OUTPUT:
                        fog_opposite_element_node = TAG.xml_doc.createElement('element')
                        fog_opposite_element_node.setAttribute('index', str(fog_opposite_idx))
                        fog_opposite_node.appendChild(fog_opposite_element_node)

                    light_fog = SKY.LightFog()
                    light_fog.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "color"))
                    light_fog.maximum_density = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "maximum density"))
                    light_fog.start_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "start distance"))
                    light_fog.opaque_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "opaque distance"))
                    light_fog.cone = TAG.read_min_max_degree(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "cone"))
                    light_fog.atmospheric_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "atmospheric fog influence"))
                    light_fog.secondary_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "secondary fog influence"))
                    light_fog.sky_fog_influence = TAG.read_float(input_stream, TAG, tag_format.XMLData(fog_opposite_element_node, "sky fog influence"))

                    light.fog.append(light_fog)

            if light.radiosity_tag_block.count > 0:
                radiosity_node = tag_format.get_xml_node(XML_OUTPUT, light.radiosity_tag_block.count, light_element_node, "name", "radiosity")
                light.radiosity_header = TAG.TagBlockHeader().read(input_stream, TAG)
                for radiosity_idx in range(light.radiosity_tag_block.count):
                    radiosity_element_node = None
                    if XML_OUTPUT:
                        radiosity_element_node = TAG.xml_doc.createElement('element')
                        radiosity_element_node.setAttribute('index', str(radiosity_idx))
                        radiosity_node.appendChild(radiosity_element_node)

                    radiosity = SKY.Radiosity()
                    radiosity.flags = TAG.read_flag_unsigned_integer(input_stream, TAG, tag_format.XMLData(radiosity_element_node, "flags", LightFlags))
                    radiosity.color = TAG.read_rgb(input_stream, TAG, tag_format.XMLData(radiosity_element_node, "color"))
                    radiosity.power = TAG.read_float(input_stream, TAG, tag_format.XMLData(radiosity_element_node, "power"))
                    radiosity.test_distance = TAG.read_float(input_stream, TAG, tag_format.XMLData(radiosity_element_node, "test distance"))
                    input_stream.read(12) # Padding?
                    radiosity.diameter = TAG.read_degree(input_stream, TAG, tag_format.XMLData(radiosity_element_node, "diameter"))

                    light.radiosity.append(radiosity)

def read_shader_functions(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.shader_functions_tag_block.count > 0:
        shader_functions_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.shader_functions_tag_block.count, tag_node, "name", "shader functions")
        SKY.shader_functions_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for shader_function_idx in range(SKY.sky_body.shader_functions_tag_block.count):
            shader_function_element_node = None
            if XML_OUTPUT:
                shader_function_element_node = TAG.xml_doc.createElement('element')
                shader_function_element_node.setAttribute('index', str(shader_function_idx))
                shader_functions_node.appendChild(shader_function_element_node)

            input_stream.read(4) # Padding?
            shader_function = TAG.read_string32(input_stream, TAG, tag_format.XMLData(shader_function_element_node, "name"))

            SKY.shader_functions.append(shader_function)

def read_animations(SKY, TAG, input_stream, tag_node, XML_OUTPUT):
    if SKY.sky_body.animations_tag_block.count > 0:
        animations_node = tag_format.get_xml_node(XML_OUTPUT, SKY.sky_body.animations_tag_block.count, tag_node, "name", "animations")
        SKY.animations_header = TAG.TagBlockHeader().read(input_stream, TAG)
        for animation_idx in range(SKY.sky_body.animations_tag_block.count):
            animation_element_node = None
            if XML_OUTPUT:
                animation_element_node = TAG.xml_doc.createElement('element')
                animation_element_node.setAttribute('index', str(animation_idx))
                animations_node.appendChild(animation_element_node)

            animation = SKY.Animation()
            animation.animation_index = TAG.read_signed_short(input_stream, TAG, tag_format.XMLData(animation_element_node, "animation index"))
            input_stream.read(2) # Padding?
            animation.period = TAG.read_float(input_stream, TAG, tag_format.XMLData(animation_element_node, "power scale"))
            input_stream.read(28) # Padding?

            SKY.animations.append(animation)

def process_file(input_stream, report):
    TAG = tag_format.TagAsset()
    SKY = SkyAsset()
    TAG.is_legacy = False
    TAG.big_endian = False

    if XML_OUTPUT:
        TAG.xml_doc = minidom.Document()

    SKY.header = TAG.Header().read(input_stream, TAG)
    tag_node = None
    if XML_OUTPUT:
        tag_node = TAG.xml_doc.childNodes[0]

    if SKY.header.engine_tag == "LAMB":
        initilize_sky(SKY)
        read_sky_body_v0(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_cubemaps(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.atmospheric_fog_tag_block.count, SKY.atmospheric_fog_header, "atmospheric fog", SKY.atmospheric_fog)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.secondary_fog_tag_block.count, SKY.secondary_fog_header, "secondary fog", SKY.secondary_fog)
        read_sky_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_patchy_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_lights(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_shader_functions(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_animations(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SKY.header.engine_tag == "MLAB":
        initilize_sky(SKY)
        read_sky_body_v0(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_cubemaps(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.atmospheric_fog_tag_block.count, SKY.atmospheric_fog_header, "atmospheric fog", SKY.atmospheric_fog)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.secondary_fog_tag_block.count, SKY.secondary_fog_header, "secondary fog", SKY.secondary_fog)
        read_sky_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_patchy_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_lights(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_shader_functions(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_animations(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
    elif SKY.header.engine_tag == "BLM!":
        initilize_sky(SKY)
        read_sky_body_retail(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_cubemaps(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.atmospheric_fog_tag_block.count, SKY.atmospheric_fog_header, "atmospheric fog", SKY.atmospheric_fog)
        read_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT, SKY.sky_body.secondary_fog_tag_block.count, SKY.secondary_fog_header, "secondary fog", SKY.secondary_fog)
        read_sky_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_patchy_fog(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_lights(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_shader_functions(SKY, TAG, input_stream, tag_node, XML_OUTPUT)
        read_animations(SKY, TAG, input_stream, tag_node, XML_OUTPUT)

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
