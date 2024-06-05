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

import os
import struct

from .process_scene import process_scene
from ..global_functions import global_functions

DECIMAL_POINT = "6"
DECIMAL_1 = '\n%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_2 = '\n%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_3 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
DECIMAL_4 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)

def write_version(file, jms_version, version_bounds, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', jms_version))

    else:
        if write_comments:
            file.write(';### VERSION ###')
            file.write('\n')

        file.write('%s' % (jms_version))

        if write_comments:
            file.write('\n;\t<%s>' % (version_bounds))

        if write_whitespace:
            file.write('\n')

def write_checksum(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', JMS.node_checksum))

    else:
        if write_comments:
            file.write('\n;### CHECKSUM ###')

        file.write('\n%s' % (JMS.node_checksum))

        if write_whitespace:
            file.write('\n')

def write_nodes_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.nodes)))
        for idx, node in enumerate(JMS.nodes):
            transform = JMS.transforms[idx]
            file.write(struct.pack('<%ssx' % (len(node.name)), bytes(node.name, 'utf-8')))
            file.write(struct.pack('<i', node.child))
            file.write(struct.pack('<i', node.sibling))
            file.write(struct.pack('<ffff', *transform.rotation))
            file.write(struct.pack('<fff', *transform.translation))

    else:
        if write_comments:
            file.write('\n;### NODES ###')

        file.write('\n%s' % (len(JMS.nodes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<child node index>')
            file.write('\n;\t<sibling node index>')
            file.write('\n;\t<default rotation <i,j,k,w>>')
            file.write('\n;\t<default translation <x,y,z>>')
            if write_whitespace:
                file.write('\n')

        for idx, node in enumerate(JMS.nodes):
            if write_comments:
                file.write('\n;NODE %s' % idx)

            transform = JMS.transforms[idx]
            file.write('\n%s' % (node.name))
            file.write('\n%s' % (node.child))
            file.write('\n%s' % (node.sibling))
            file.write(DECIMAL_4 % (transform.rotation))
            file.write(DECIMAL_3 % (transform.translation))
            if write_whitespace:
                file.write('\n')

def write_nodes_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.nodes)))
        for idx, node in enumerate(JMS.nodes):
            transform = JMS.transforms[idx]
            file.write(struct.pack('<%ssx' % (len(node.name)), bytes(node.name, 'utf-8')))
            file.write(struct.pack('<i', node.child))
            file.write(struct.pack('<i', node.sibling))
            file.write(struct.pack('<ffff', *transform.rotation))
            file.write(struct.pack('<fff', *transform.translation))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Frames###')

        file.write('\n%s' % (len(JMS.nodes)))
        for idx, node in enumerate(JMS.nodes):
            transform = JMS.transforms[idx]
            file.write('\n%s' % (node.name))
            file.write('\n%s' % (node.child))
            file.write('\n%s' % (node.sibling))
            file.write(DECIMAL_4 % (transform.rotation))
            file.write(DECIMAL_3 % (transform.translation))
            if write_whitespace:
                file.write('\n')

def write_nodes_8205(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.nodes)))
        for idx, node in enumerate(JMS.nodes):
            transform = JMS.transforms[idx]
            file.write(struct.pack('<%ssx' % (len(node.name)), bytes(node.name, 'utf-8')))
            file.write(struct.pack('<i', node.parent))
            file.write(struct.pack('<ffff', *transform.rotation))
            file.write(struct.pack('<fff', *transform.translation))

    else:
        if write_comments:
            file.write('\n;### NODES ###')

        file.write('\n%s' % (len(JMS.nodes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent node index>')
            file.write('\n;\t<default rotation <i,j,k,w>>')
            file.write('\n;\t<default translation <x,y,z>>')
            if write_whitespace:
                file.write('\n')

        for idx, node in enumerate(JMS.nodes):
            if write_comments:
                file.write('\n;NODE %s' % idx)

            transform = JMS.transforms[idx]
            file.write('\n%s' % (node.name))
            file.write('\n%s' % (node.parent))
            file.write(DECIMAL_4 % (transform.rotation))
            file.write(DECIMAL_3 % (transform.translation))
            if write_whitespace:
                file.write('\n')

def write_materials_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.materials)))
        for idx, material in enumerate(JMS.materials):
            file.write(struct.pack('<%ssx' % (len(material.name)), bytes(material.name, 'utf-8')))
            file.write(struct.pack('<%ssx' % (len(material.texture_path)), bytes(material.texture_path, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;### Materials ###')

        file.write('\n%s' % (len(JMS.materials)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<texture path>')
            if write_whitespace:
                file.write('\n')

        for idx, material in enumerate(JMS.materials):
            if write_comments:
                file.write('\n;MATERIAL %s' % idx)

            file.write('\n%s' % (material.name))
            file.write('\n%s' % (material.texture_path))
            if write_whitespace:
                file.write('\n')

def write_materials_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.materials)))
        for idx, material in enumerate(JMS.materials):
            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)

            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)

            if not material.region == '':
                material_definition += ' %s' % (material.region)

            file.write(struct.pack('<%ssx' % (len(material.name)), bytes(material.name, 'utf-8')))
            file.write(struct.pack('<%ssx' % (len(material.texture_path)), bytes(material.texture_path, 'utf-8')))
            file.write(struct.pack('<%ssx' % (len(material_definition)), bytes(material_definition, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Materials###')

        file.write('\n%s' % (len(JMS.materials)))
        for idx, material in enumerate(JMS.materials):
            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)

            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)

            if not material.region == '':
                material_definition += ' %s' % (material.region)

            file.write('\n%s' % (material.name))
            file.write('\n%s' % (material.texture_path))
            file.write('\n%s' % (material_definition))
            if write_whitespace:
                file.write('\n')

def write_materials_8205(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.materials)))
        for idx, material in enumerate(JMS.materials):
            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)

            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)

            if not material.region == '':
                material_definition += ' %s' % (material.region)

            file.write(struct.pack('<%ssx' % (len(material.name)), bytes(material.name, 'utf-8')))
            file.write(struct.pack('<%ssx' % (len(material_definition)), bytes(material_definition, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;### MATERIALS ###')

        file.write('\n%s' % (len(JMS.materials)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<material name>')
            if write_whitespace:
                file.write('\n')

        for idx, material in enumerate(JMS.materials):
            if write_comments:
                file.write('\n;MATERIAL %s' % idx)

            material_definition = '(%s)' % (material.slot)
            if not material.lod == None:
                material_definition += ' %s' % (material.lod)

            if not material.permutation == '':
                material_definition += ' %s' % (material.permutation)

            if not material.region == '':
                material_definition += ' %s' % (material.region)

            file.write('\n%s' % (material.name))
            file.write('\n%s' % (material_definition))
            if write_whitespace:
                file.write('\n')

def write_markers_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write(struct.pack('<%ssx' % (len(marker.name)), bytes(marker.name, 'utf-8')))
            file.write(struct.pack('<i', marker.parent))
            file.write(struct.pack('<ffff', *marker.rotation))
            file.write(struct.pack('<fff', *marker.translation))

    else:
        if write_comments:
            file.write('\n;### MARKERS ###')

        file.write('\n%s' % (len(JMS.markers)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<node index>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            if write_whitespace:
                file.write('\n')

        for idx, marker in enumerate(JMS.markers):
            if write_comments:
                file.write('\n;MARKER %s' % idx)

            file.write('\n%s' % (marker.name))
            file.write('\n%s' % (marker.parent))
            file.write(DECIMAL_4 % (marker.rotation))
            file.write(DECIMAL_3 % (marker.translation))
            if write_whitespace:
                file.write('\n')

def write_markers_8198(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write(struct.pack('<%ssx' % (len(marker.name)), bytes(marker.name, 'utf-8')))
            file.write(struct.pack('<i', marker.region))
            file.write(struct.pack('<i', marker.parent))
            file.write(struct.pack('<ffff', *marker.rotation))
            file.write(struct.pack('<fff', *marker.translation))

    else:
        if write_comments:
            file.write('\n;### MARKERS ###')

        file.write('\n%s' % (len(JMS.markers)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<node index>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            if write_whitespace:
                file.write('\n')

        for idx, marker in enumerate(JMS.markers):
            if write_comments:
                file.write('\n;MARKER %s' % idx)

            file.write('\n%s' % (marker.name))
            file.write('\n%s' % (marker.region))
            file.write('\n%s' % (marker.parent))
            file.write(DECIMAL_4 % (marker.rotation))
            file.write(DECIMAL_3 % (marker.translation))
            if write_whitespace:
                file.write('\n')

def write_markers_8200(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write(struct.pack('<%ssx' % (len(marker.name)), bytes(marker.name, 'utf-8')))
            file.write(struct.pack('<i', marker.region))
            file.write(struct.pack('<i', marker.parent))
            file.write(struct.pack('<ffff', *marker.rotation))
            file.write(struct.pack('<fff', *marker.translation))
            file.write(struct.pack('<f', *marker.radius))

    else:
        if write_comments:
            file.write('\n;### MARKERS ###')

        file.write('\n%s' % (len(JMS.markers)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<node index>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, marker in enumerate(JMS.markers):
            if write_comments:
                file.write('\n;MARKER %s' % idx)

            file.write('\n%s' % (marker.name))
            file.write('\n%s' % (marker.region))
            file.write('\n%s' % (marker.parent))
            file.write(DECIMAL_4 % (marker.rotation))
            file.write(DECIMAL_3 % (marker.translation))
            file.write(DECIMAL_1 % (marker.radius))
            if write_whitespace:
                file.write('\n')

def write_markers_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write(struct.pack('<%ssx' % (len(marker.name)), bytes(marker.name, 'utf-8')))
            file.write(struct.pack('<i', marker.region))
            file.write(struct.pack('<i', marker.parent))
            file.write(struct.pack('<ffff', *marker.rotation))
            file.write(struct.pack('<fff', *marker.translation))
            file.write(struct.pack('<f', *marker.radius))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Markers###')

        file.write('\n%s' % (len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write('\n%s' % (marker.name))
            file.write('\n%s' % (marker.region))
            file.write('\n%s' % (marker.parent))
            file.write(DECIMAL_4 % (marker.rotation))
            file.write(DECIMAL_3 % (marker.translation))
            file.write(DECIMAL_1 % (marker.radius))
            if write_whitespace:
                file.write('\n')

def write_markers_8205(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.markers)))
        for idx, marker in enumerate(JMS.markers):
            file.write(struct.pack('<%ssx' % (len(marker.name)), bytes(marker.name, 'utf-8')))
            file.write(struct.pack('<i', marker.parent))
            file.write(struct.pack('<ffff', *marker.rotation))
            file.write(struct.pack('<fff', *marker.translation))
            file.write(struct.pack('<f', marker.radius))

    else:
        if write_comments:
            file.write('\n;### MARKERS ###')

        file.write('\n%s' % (len(JMS.markers)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<node index>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, marker in enumerate(JMS.markers):
            if write_comments:
                file.write('\n;MARKER %s' % idx)

            file.write('\n%s' % (marker.name))
            file.write('\n%s' % (marker.parent))
            file.write(DECIMAL_4 % (marker.rotation))
            file.write(DECIMAL_3 % (marker.translation))
            file.write(DECIMAL_1 % (marker.radius))
            if write_whitespace:
                file.write('\n')

def write_instance_xref_paths_8201(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_instances)))
        for idx, xref_instance in enumerate(JMS.xref_instances):
            file.write(struct.pack('<%ssx' % (len(xref_instance.path)), bytes(xref_instance.path, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instance xref paths###')

        file.write('\n%s' % (len(JMS.xref_instances)))
        for idx, xref_instance in enumerate(JMS.xref_instances):
            file.write('\n%s' % (xref_instance.path))
            if write_whitespace:
                file.write('\n')

def write_instance_xref_paths_8205(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_instances)))
        for idx, xref_instance in enumerate(JMS.xref_instances):
            file.write(struct.pack('<%ssx' % (len(xref_instance.path)), bytes(xref_instance.path, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;### INSTANCE XREF PATHS ###')

        file.write('\n%s' % (len(JMS.xref_instances)))
        if write_comments:
            file.write('\n;\t<name>')
            if write_whitespace:
                file.write('\n')

        for idx, xref_instance in enumerate(JMS.xref_instances):
            if write_comments:
                file.write('\n;XREF %s' % idx)

            file.write('\n%s' % (xref_instance.path))
            if write_whitespace:
                file.write('\n')

def write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_instances)))
        for idx, xref_instance in enumerate(JMS.xref_instances):
            file.write(struct.pack('<%ssx' % (len(xref_instance.path)), bytes(xref_instance.path, 'utf-8')))
            file.write(struct.pack('<%ssx' % (len(xref_instance.name)), bytes(xref_instance.name, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;### INSTANCE XREF PATHS ###')

        file.write('\n%s' % (len(JMS.xref_instances)))
        if write_comments:
            file.write('\n;\t<name>')
            if write_whitespace:
                file.write('\n')

        for idx, xref_instance in enumerate(JMS.xref_instances):
            if write_comments:
                file.write('\n;XREF %s' % idx)

            file.write('\n%s' % (xref_instance.path))
            file.write('\n%s' % (xref_instance.name))
            if write_whitespace:
                file.write('\n')

def write_instance_markers_8201(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_markers)))
        for idx, xref_marker in enumerate(JMS.xref_markers):
            file.write(struct.pack('<%ssx' % (len(xref_marker.name)), bytes(xref_marker.name, 'utf-8')))
            file.write(struct.pack('<i', xref_marker.index))
            file.write(struct.pack('<ffff', *xref_marker.rotation))
            file.write(struct.pack('<fff', *xref_marker.translation))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instance markers###')

        file.write('\n%s' % (len(JMS.xref_markers)))
        for idx, xref_marker in enumerate(JMS.xref_markers):
            file.write('\n%s' % (xref_marker.name))
            file.write('\n%s' % (xref_marker.index))
            file.write(DECIMAL_4 % (xref_marker.rotation))
            file.write(DECIMAL_3 % (xref_marker.translation))
            if write_whitespace:
                file.write('\n')

def write_instance_markers_8203(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_markers)))
        for idx, xref_marker in enumerate(JMS.xref_markers):
            file.write(struct.pack('<%ssx' % (len(xref_marker.name)), bytes(xref_marker.name, 'utf-8')))
            file.write(struct.pack('<i', xref_marker.unique_identifier))
            file.write(struct.pack('<i', xref_marker.index))
            file.write(struct.pack('<ffff', *xref_marker.rotation))
            file.write(struct.pack('<fff', *xref_marker.translation))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instance markers###')

        file.write('\n%s' % (len(JMS.xref_markers)))
        for idx, xref_marker in enumerate(JMS.xref_markers):
            file.write('\n%s' % (xref_marker.name))
            file.write('\n%s' % (xref_marker.unique_identifier))
            file.write('\n%s' % (xref_marker.index))
            file.write(DECIMAL_4 % (xref_marker.rotation))
            file.write(DECIMAL_3 % (xref_marker.translation))
            if write_whitespace:
                file.write('\n')

def write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace):
    if binary:
        file.write(struct.pack('<i', len(JMS.xref_markers)))
        for idx, xref_marker in enumerate(JMS.xref_markers):
            file.write(struct.pack('<%ssx' % (len(xref_marker.name)), bytes(xref_marker.name, 'utf-8')))
            file.write(struct.pack('<i', xref_marker.unique_identifier))
            file.write(struct.pack('<i', xref_marker.index))
            file.write(struct.pack('<ffff', *xref_marker.rotation))
            file.write(struct.pack('<fff', *xref_marker.translation))

    else:
        if write_comments:
            file.write('\n;### INSTANCE MARKERS ###')

        file.write('\n%s' % (len(JMS.xref_markers)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<unique identifier>')
            file.write('\n;\t<path index>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            if write_whitespace:
                file.write('\n')

        for idx, xref_marker in enumerate(JMS.xref_markers):
            if write_comments:
                file.write('\n;XREF OBJECT %s' % idx)

            file.write('\n%s' % (xref_marker.name))
            file.write('\n%s' % (xref_marker.unique_identifier))
            file.write('\n%s' % (xref_marker.index))
            file.write(DECIMAL_4 % (xref_marker.rotation))
            file.write(DECIMAL_3 % (xref_marker.translation))
            if write_whitespace:
                file.write('\n')

def write_regions_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.regions)))
        for idx, region in enumerate(JMS.regions):
            file.write(struct.pack('<%ssx' % (len(region.name)), bytes(region.name, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;### Regions ###')

        file.write('\n%s' % (len(JMS.regions)))
        if write_comments:
            file.write('\n;\t<name>')
            if write_whitespace:
                file.write('\n')

        for idx, region in enumerate(JMS.regions):
            if write_comments:
                file.write('\n;REGION %s' % idx)

            file.write('\n%s' % (region.name))
            if write_whitespace:
                file.write('\n')

def write_regions_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.regions)))
        for idx, region in enumerate(JMS.regions):
            file.write(struct.pack('<%ssx' % (len(region.name)), bytes(region.name, 'utf-8')))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Regions###')

        file.write('\n%s' % (len(JMS.regions)))
        for idx, region in enumerate(JMS.regions):
            file.write('\n%s' % (region.name))
            if write_whitespace:
                file.write('\n')

def write_vertices_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write(struct.pack('<i', vertex.region))
            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<ff', *vertex.uv_set[0]))

    else:
        if write_comments:
            file.write('\n;### VERTICES ###')

        file.write('\n%s' % (len(JMS.vertices)))
        if write_comments:
            file.write('\n;\t<region index>')
            file.write('\n;\t<node index 0>')
            file.write('\n;\t<position>')
            file.write('\n;\t<normal>')
            file.write('\n;\t<node index 1>')
            file.write('\n;\t<node weight 1>')
            file.write('\n;\t<texture coordinates <u,v>>')
            if write_whitespace:
                file.write('\n')

        for idx, vertex in enumerate(JMS.vertices):
            if write_comments:
                file.write('\n;VERTEX %s' % idx)

            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write('\n%s' % vertex.region)
            file.write('\n%s' % node0_index)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write(DECIMAL_2 % (vertex.uv_set[0][0], vertex.uv_set[0][1]))
            if write_whitespace:
                file.write('\n')

def write_vertices_8198(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<ff', *vertex.uv_set[0]))
            file.write(struct.pack('<i', 0))

    else:
        if write_comments:
            file.write('\n;### VERTICES ###')

        file.write('\n%s' % (len(JMS.vertices)))
        if write_comments:
            file.write('\n;\t<node index 0>')
            file.write('\n;\t<position>')
            file.write('\n;\t<normal>')
            file.write('\n;\t<node index 1>')
            file.write('\n;\t<node weight 1>')
            file.write('\n;\t<texture coordinates <u,v>>')
            file.write('\n;\t<unused flag>')
            if write_whitespace:
                file.write('\n')

        for idx, vertex in enumerate(JMS.vertices):
            if write_comments:
                file.write('\n;VERTEX %s' % idx)

            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write('\n%s' % node0_index)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write(DECIMAL_2 % (vertex.uv_set[0][0], vertex.uv_set[0][1]))
            file.write('\n%s' % 0)
            if write_whitespace:
                file.write('\n')

def write_vertices_8199(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<ff', *vertex.uv_set[0]))
            file.write(struct.pack('<i', 0))

    else:
        if write_comments:
            file.write('\n;### VERTICES ###')

        file.write('\n%s' % (len(JMS.vertices)))
        if write_comments:
            file.write('\n;\t<node index 0>')
            file.write('\n;\t<position>')
            file.write('\n;\t<normal>')
            file.write('\n;\t<node index 1>')
            file.write('\n;\t<node weight 1>')
            file.write('\n;\t<texture coordinates <u,v>>')
            file.write('\n;\t<unused flag>')
            if write_whitespace:
                file.write('\n')

        for idx, vertex in enumerate(JMS.vertices):
            if write_comments:
                file.write('\n;VERTEX %s' % idx)

            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write('\n%s' % node0_index)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write(DECIMAL_2 % (vertex.uv_set[0][0], vertex.uv_set[0][1]))
            file.write('\n%s' % 0)
            if write_whitespace:
                file.write('\n')

def write_vertices_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<ff', *vertex.uv_set[0]))
            file.write(struct.pack('<i', 0))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Vertices###')

        file.write('\n%s' % (len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            file.write('\n%s' % node0_index)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write(DECIMAL_2 % (vertex.uv_set[0][0], vertex.uv_set[0][1]))
            file.write('\n%s' % 0)
            if write_whitespace:
                file.write('\n')

def write_vertices_8202(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            uv_0 = vertex.uv_set[0]
            tex_u_0 = uv_0[0]
            tex_v_0 = uv_0[1]

            uv_1 = None
            tex_u_1 = 0.0
            tex_v_1 = 0.0
            if len(vertex.uv_set) > 1:
                uv_1 = vertex.uv_set[1]
                tex_u_1 = uv_1[0]
                tex_v_1 = uv_1[1]

            uv_2 = None
            tex_u_2 = 0.0
            tex_v_2 = 0.0
            if len(vertex.uv_set) > 2:
                uv_2 = vertex.uv_set[2]
                tex_u_2 = uv_2[0]
                tex_v_2 = uv_2[1]

            uv_3 = None
            tex_u_3 = 0.0
            tex_v_3 = 0.0
            if len(vertex.uv_set) > 3:
                uv_3 = vertex.uv_set[3]
                tex_u_3 = uv_3[0]
                tex_v_3 = uv_3[1]

            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<ff', (tex_u_0, tex_v_0)))
            file.write(struct.pack('<ff', (tex_u_1, tex_v_1)))
            file.write(struct.pack('<ff', (tex_u_2, tex_v_2)))
            file.write(struct.pack('<ff', (tex_u_3, tex_v_3)))
            file.write(struct.pack('<i', 0))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Vertices###')

        file.write('\n%s' % (len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node0_index = node0[0]

            node1_index = node1[0]
            node1_weight = node1[1]

            uv_0 = vertex.uv_set[0]
            tex_u_0 = uv_0[0]
            tex_v_0 = uv_0[1]

            uv_1 = None
            tex_u_1 = 0.0
            tex_v_1 = 0.0
            if len(vertex.uv_set) > 1:
                uv_1 = vertex.uv_set[1]
                tex_u_1 = uv_1[0]
                tex_v_1 = uv_1[1]

            uv_2 = None
            tex_u_2 = 0.0
            tex_v_2 = 0.0
            if len(vertex.uv_set) > 2:
                uv_2 = vertex.uv_set[2]
                tex_u_2 = uv_2[0]
                tex_v_2 = uv_2[1]

            uv_3 = None
            tex_u_3 = 0.0
            tex_v_3 = 0.0
            if len(vertex.uv_set) > 3:
                uv_3 = vertex.uv_set[3]
                tex_u_3 = uv_3[0]
                tex_v_3 = uv_3[1]

            file.write('\n%s' % node0_index)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write(DECIMAL_2 % (tex_u_0, tex_v_0))
            file.write(DECIMAL_2 % (tex_u_1, tex_v_1))
            file.write(DECIMAL_2 % (tex_u_2, tex_v_2))
            file.write(DECIMAL_2 % (tex_u_3, tex_v_3))
            file.write('\n%s' % 0)
            if write_whitespace:
                file.write('\n')

def write_vertices_8204(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node2 = (int(-1), float(0.0))
            if len(vertex.node_set) > 2:
                node2 = vertex.node_set[2]

            node3 = (int(-1), float(0.0))
            if len(vertex.node_set) > 3:
                node3 = vertex.node_set[3]

            node0_index = node0[0]
            node0_weight = node0[1]

            node1_index = node1[0]
            node1_weight = node1[1]

            node2_index = node2[0]
            node2_weight = node2[1]

            node3_index = node3[0]
            node3_weight = node3[1]

            uv_0 = vertex.uv_set[0]
            tex_u_0 = uv_0[0]
            tex_v_0 = uv_0[1]

            uv_1 = None
            tex_u_1 = 0.0
            tex_v_1 = 0.0
            if len(vertex.uv_set) > 1:
                uv_1 = vertex.uv_set[1]
                tex_u_1 = uv_1[0]
                tex_v_1 = uv_1[1]

            uv_2 = None
            tex_u_2 = 0.0
            tex_v_2 = 0.0
            if len(vertex.uv_set) > 2:
                uv_2 = vertex.uv_set[2]
                tex_u_2 = uv_2[0]
                tex_v_2 = uv_2[1]

            uv_3 = None
            tex_u_3 = 0.0
            tex_v_3 = 0.0
            if len(vertex.uv_set) > 3:
                uv_3 = vertex.uv_set[3]
                tex_u_3 = uv_3[0]
                tex_v_3 = uv_3[1]

            file.write(struct.pack('<i', node0_index))
            file.write(struct.pack('<f', node0_weight))
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', node1_index))
            file.write(struct.pack('<f', node1_weight))
            file.write(struct.pack('<i', node2_index))
            file.write(struct.pack('<f', node2_weight))
            file.write(struct.pack('<i', node3_index))
            file.write(struct.pack('<f', node3_weight))
            file.write(struct.pack('<ff', (tex_u_0, tex_v_0)))
            file.write(struct.pack('<ff', (tex_u_1, tex_v_1)))
            file.write(struct.pack('<ff', (tex_u_2, tex_v_2)))
            file.write(struct.pack('<ff', (tex_u_3, tex_v_3)))
            file.write(struct.pack('<i', 0))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Vertices###')

        file.write('\n%s' % (len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            node0 = (int(-1), float(0.0))
            if len(vertex.node_set) > 0:
                node0 = vertex.node_set[0]

            node1 = (int(-1), float(0.0))
            if len(vertex.node_set) > 1:
                node1 = vertex.node_set[1]

            node2 = (int(-1), float(0.0))
            if len(vertex.node_set) > 2:
                node2 = vertex.node_set[2]

            node3 = (int(-1), float(0.0))
            if len(vertex.node_set) > 3:
                node3 = vertex.node_set[3]

            node0_index = node0[0]
            node0_weight = node0[1]

            node1_index = node1[0]
            node1_weight = node1[1]

            node2_index = node2[0]
            node2_weight = node2[1]

            node3_index = node3[0]
            node3_weight = node3[1]

            uv_0 = vertex.uv_set[0]
            tex_u_0 = uv_0[0]
            tex_v_0 = uv_0[1]

            uv_1 = None
            tex_u_1 = 0.0
            tex_v_1 = 0.0
            if len(vertex.uv_set) > 1:
                uv_1 = vertex.uv_set[1]
                tex_u_1 = uv_1[0]
                tex_v_1 = uv_1[1]

            uv_2 = None
            tex_u_2 = 0.0
            tex_v_2 = 0.0
            if len(vertex.uv_set) > 2:
                uv_2 = vertex.uv_set[2]
                tex_u_2 = uv_2[0]
                tex_v_2 = uv_2[1]

            uv_3 = None
            tex_u_3 = 0.0
            tex_v_3 = 0.0
            if len(vertex.uv_set) > 3:
                uv_3 = vertex.uv_set[3]
                tex_u_3 = uv_3[0]
                tex_v_3 = uv_3[1]

            file.write('\n%s' % node0_index)
            file.write(DECIMAL_1 % node0_weight)
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % node1_index)
            file.write(DECIMAL_1 % node1_weight)
            file.write('\n%s' % node2_index)
            file.write(DECIMAL_1 % node2_weight)
            file.write('\n%s' % node3_index)
            file.write(DECIMAL_1 % node3_weight)
            file.write(DECIMAL_2 % (tex_u_0, tex_v_0))
            file.write(DECIMAL_2 % (tex_u_1, tex_v_1))
            file.write(DECIMAL_2 % (tex_u_2, tex_v_2))
            file.write(DECIMAL_2 % (tex_u_3, tex_v_3))
            file.write('\n%s' % 0)
            if write_whitespace:
                file.write('\n')

def write_vertices_8205(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', len(vertex.node_set)))
            for node in vertex.node_set:
                node_index, node_weight = node
                file.write(struct.pack('<i', node_index))
                file.write(struct.pack('<f', node_weight))

            file.write(struct.pack('<i', len(vertex.uv_set)))
            for uv in vertex.uv_set:
                file.write(struct.pack('<ff', *uv))


    else:
        if write_comments:
            file.write('\n;### VERTICES ###')

        file.write('\n%s' % (len(JMS.vertices)))
        if write_comments:
            file.write('\n;\t<position>')
            file.write('\n;\t<normal>')
            file.write('\n;\t<node influences count>')
            file.write('\n;\t\t<node influences <index, weight>>')
            file.write('\n;\t\t<...>')
            file.write('\n;\t<texture coordinate count>')
            file.write('\n;\t\t<texture coordinates <u,v>>')
            file.write('\n;\t\t<...>')
            if write_whitespace:
                file.write('\n')

        for idx, vertex in enumerate(JMS.vertices):
            if write_comments:
                file.write('\n;VERTEX %s' % idx)
            
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % len(vertex.node_set))
            for node in vertex.node_set:
                node_index, node_weight = node
                file.write('\n%s' % (node_index))
                file.write(DECIMAL_1 % (node_weight))

            file.write('\n%s' % len(vertex.uv_set))
            for uv in vertex.uv_set:
                uv_0, uv_1 = uv
                file.write(DECIMAL_2 % (uv_0, uv_1))

            if write_whitespace:
                file.write('\n')

def write_vertices_8211(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.vertices)))
        for idx, vertex in enumerate(JMS.vertices):
            file.write(struct.pack('<fff', *vertex.translation))
            file.write(struct.pack('<fff', *vertex.normal))
            file.write(struct.pack('<i', len(vertex.node_set)))
            for node in vertex.node_set:
                node_index, node_weight = node
                file.write(struct.pack('<i', node_index))
                file.write(struct.pack('<f', node_weight))

            file.write(struct.pack('<i', len(vertex.uv_set)))
            for uv in vertex.uv_set:
                file.write(struct.pack('<ff', *uv))

            file.write(struct.pack('<fff', *vertex.color))

    else:
        if write_comments:
            file.write('\n;### VERTICES ###')

        file.write('\n%s' % (len(JMS.vertices)))
        if write_comments:
            file.write('\n;\t<position>')
            file.write('\n;\t<normal>')
            file.write('\n;\t<node influences count>')
            file.write('\n;\t\t<node influences <index, weight>>')
            file.write('\n;\t\t<...>')
            file.write('\n;\t<texture coordinate count>')
            file.write('\n;\t\t<texture coordinates <u,v>>')
            file.write('\n;\t\t<...>')
            file.write('\n;\t<vertex color <r,g,b>>')
            if write_whitespace:
                file.write('\n')

        for idx, vertex in enumerate(JMS.vertices):
            if write_comments:
                file.write('\n;VERTEX %s' % idx)
            
            file.write(DECIMAL_3 % (vertex.translation[0], vertex.translation[1], vertex.translation[2]))
            file.write(DECIMAL_3 % (vertex.normal[0], vertex.normal[1], vertex.normal[2]))
            file.write('\n%s' % len(vertex.node_set))
            for node in vertex.node_set:
                node_index, node_weight = node
                file.write('\n%s' % (node_index))
                file.write(DECIMAL_1 % (node_weight))

            file.write('\n%s' % len(vertex.uv_set))
            for uv in vertex.uv_set:
                uv_0, uv_1 = uv
                file.write(DECIMAL_2 % (uv_0, uv_1))

            file.write(DECIMAL_3 % vertex.color)
            if write_whitespace:
                file.write('\n')

def write_triangles_8197(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.triangles)))
        for idx, triangle in enumerate(JMS.triangles):
            file.write(struct.pack('<i', triangle.material_index))
            file.write(struct.pack('<iii', triangle.v0, triangle.v1, triangle.v2))

    else:
        if write_comments:
            file.write('\n;### TRIANGLES ###')

        file.write('\n%s' % (len(JMS.triangles)))
        if write_comments:
            file.write('\n;\t<material index>')
            file.write('\n;\t<vertex indices <v0,v1,v2>>')
            if write_whitespace:
                file.write('\n')

        for idx, triangle in enumerate(JMS.triangles):
            if write_comments:
                file.write('\n;TRIANGLE %s' % idx)

            file.write('\n%s' % triangle.material_index)
            file.write('\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2))
            if write_whitespace:
                file.write('\n')

def write_triangles_8198(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.triangles)))
        for idx, triangle in enumerate(JMS.triangles):
            file.write(struct.pack('<i', triangle.region))
            file.write(struct.pack('<i', triangle.material_index))
            file.write(struct.pack('<iii', triangle.v0, triangle.v1, triangle.v2))

    else:
        if write_comments:
            file.write('\n;### TRIANGLES ###')

        file.write('\n%s' % (len(JMS.triangles)))
        if write_comments:
            file.write('\n;\t<region index>')
            file.write('\n;\t<material index>')
            file.write('\n;\t<vertex indices <v0,v1,v2>>')
            if write_whitespace:
                file.write('\n')

        for idx, triangle in enumerate(JMS.triangles):
            if write_comments:
                file.write('\n;TRIANGLE %s' % idx)

            file.write('\n%s' % triangle.region)
            file.write('\n%s' % triangle.material_index)
            file.write('\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2))
            if write_whitespace:
                file.write('\n')

def write_triangles_8201(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.triangles)))
        for idx, triangle in enumerate(JMS.triangles):
            file.write(struct.pack('<i', triangle.region))
            file.write(struct.pack('<i', triangle.material_index))
            file.write(struct.pack('<iii', triangle.v0, triangle.v1, triangle.v2))

    else:
        if write_comments:
            file.write('\n;')
            file.write('\n;###Faces###')

        file.write('\n%s' % (len(JMS.triangles)))
        for idx, triangle in enumerate(JMS.triangles):
            file.write('\n%s' % triangle.region)
            file.write('\n%s' % triangle.material_index)
            file.write('\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2))
            if write_whitespace:
                file.write('\n')

def write_triangles_8205(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.triangles)))
        for idx, triangle in enumerate(JMS.triangles):
            file.write(struct.pack('<i', triangle.material_index))
            file.write(struct.pack('<iii', triangle.v0, triangle.v1, triangle.v2))

    else:
        if write_comments:
            file.write('\n;### TRIANGLES ###')

        file.write('\n%s' % (len(JMS.triangles)))
        if write_comments:
            file.write('\n;\t<material index>')
            file.write('\n;\t<vertex indices <v0,v1,v2>>')
            if write_whitespace:
                file.write('\n')

        for idx, triangle in enumerate(JMS.triangles):
            if write_comments:
                file.write('\n;TRIANGLE %s' % idx)

            file.write('\n%s' % triangle.material_index)
            file.write('\n%s\t%s\t%s' % (triangle.v0, triangle.v1, triangle.v2))
            if write_whitespace:
                file.write('\n')

def write_spheres_8206(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.spheres)))
        for idx, sphere in enumerate(JMS.spheres):
            file.write(struct.pack('<%ssx' % (len(sphere.name)), bytes(sphere.name, 'utf-8')))
            file.write(struct.pack('<i', sphere.parent_index))
            file.write(struct.pack('<ffff', *sphere.rotation))
            file.write(struct.pack('<fff', *sphere.translation))
            file.write(struct.pack('<f', sphere.radius))

    else:
        if write_comments:
            file.write('\n;### SPHERES ###')

        file.write('\n%s' % (len(JMS.spheres)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, sphere in enumerate(JMS.spheres):
            if write_comments:
                file.write('\n;SPHERE %s' % idx)

            file.write('\n%s' % sphere.name)
            file.write('\n%s' % sphere.parent_index)
            file.write(DECIMAL_4 % sphere.rotation)
            file.write(DECIMAL_3 % sphere.translation)
            file.write(DECIMAL_1 % sphere.radius)
            if write_whitespace:
                file.write('\n')

def write_spheres_8207(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.spheres)))
        for idx, sphere in enumerate(JMS.spheres):
            file.write(struct.pack('<%ssx' % (len(sphere.name)), bytes(sphere.name, 'utf-8')))
            file.write(struct.pack('<i', sphere.parent_index))
            file.write(struct.pack('<i', sphere.material_index))
            file.write(struct.pack('<ffff', *sphere.rotation))
            file.write(struct.pack('<fff', *sphere.translation))
            file.write(struct.pack('<f', sphere.radius))

    else:
        if write_comments:
            file.write('\n;### SPHERES ###')

        file.write('\n%s' % (len(JMS.spheres)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<material>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, sphere in enumerate(JMS.spheres):
            if write_comments:
                file.write('\n;SPHERE %s' % idx)

            file.write('\n%s' % sphere.name)
            file.write('\n%s' % sphere.parent_index)
            file.write('\n%s' % sphere.material_index)
            file.write(DECIMAL_4 % sphere.rotation)
            file.write(DECIMAL_3 % sphere.translation)
            file.write(DECIMAL_1 % sphere.radius)
            if write_whitespace:
                file.write('\n')

def write_boxes_8206(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.boxes)))
        for idx, box in enumerate(JMS.boxes):
            file.write(struct.pack('<%ssx' % (len(box.name)), bytes(box.name, 'utf-8')))
            file.write(struct.pack('<i', box.parent_index))
            file.write(struct.pack('<ffff', *box.rotation))
            file.write(struct.pack('<fff', *box.translation))
            file.write(struct.pack('<f', box.width))
            file.write(struct.pack('<f', box.length))
            file.write(struct.pack('<f', box.height))

    else:
        if write_comments:
            file.write('\n;### BOXES ###')

        file.write('\n%s' % (len(JMS.boxes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<width (x)>')
            file.write('\n;\t<length (y)>')
            file.write('\n;\t<height (z)>')
            if write_whitespace:
                file.write('\n')

        for idx, box in enumerate(JMS.boxes):
            if write_comments:
                file.write('\n;BOX %s' % idx)

            file.write('\n%s' % box.name)
            file.write('\n%s' % box.parent_index)
            file.write(DECIMAL_4 % box.rotation)
            file.write(DECIMAL_3 % box.translation)
            file.write(DECIMAL_1 % box.width)
            file.write(DECIMAL_1 % box.length)
            file.write(DECIMAL_1 % box.height)
            if write_whitespace:
                file.write('\n')

def write_boxes_8207(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.boxes)))
        for idx, box in enumerate(JMS.boxes):
            file.write(struct.pack('<%ssx' % (len(box.name)), bytes(box.name, 'utf-8')))
            file.write(struct.pack('<i', box.parent_index))
            file.write(struct.pack('<i', box.material_index))
            file.write(struct.pack('<ffff', *box.rotation))
            file.write(struct.pack('<fff', *box.translation))
            file.write(struct.pack('<f', box.width))
            file.write(struct.pack('<f', box.length))
            file.write(struct.pack('<f', box.height))

    else:
        if write_comments:
            file.write('\n;### BOXES ###')

        file.write('\n%s' % (len(JMS.boxes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<material>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<width (x)>')
            file.write('\n;\t<length (y)>')
            file.write('\n;\t<height (z)>')
            if write_whitespace:
                file.write('\n')

        for idx, box in enumerate(JMS.boxes):
            if write_comments:
                file.write('\n;BOX %s' % idx)

            file.write('\n%s' % box.name)
            file.write('\n%s' % box.parent_index)
            file.write('\n%s' % box.material_index)
            file.write(DECIMAL_4 % box.rotation)
            file.write(DECIMAL_3 % box.translation)
            file.write(DECIMAL_1 % box.width)
            file.write(DECIMAL_1 % box.length)
            file.write(DECIMAL_1 % box.height)
            if write_whitespace:
                file.write('\n')

def write_capsules_8206(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.capsules)))
        for idx, capsule in enumerate(JMS.capsules):
            file.write(struct.pack('<%ssx' % (len(capsule.name)), bytes(capsule.name, 'utf-8')))
            file.write(struct.pack('<i', capsule.parent_index))
            file.write(struct.pack('<ffff', *capsule.rotation))
            file.write(struct.pack('<fff', *capsule.translation))
            file.write(struct.pack('<f', capsule.height))
            file.write(struct.pack('<f', capsule.radius))

    else:
        if write_comments:
            file.write('\n;### CAPSULES ###')

        file.write('\n%s' % (len(JMS.capsules)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<height>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, capsule in enumerate(JMS.capsules):
            if write_comments:
                file.write('\n;CAPSULE %s' % idx)

            file.write('\n%s' % capsule.name)
            file.write('\n%s' % capsule.parent_index)
            file.write(DECIMAL_4 % capsule.rotation)
            file.write(DECIMAL_3 % capsule.translation)
            file.write(DECIMAL_1 % capsule.height)
            file.write(DECIMAL_1 % capsule.radius)
            if write_whitespace:
                file.write('\n')

def write_capsules_8207(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.capsules)))
        for idx, capsule in enumerate(JMS.capsules):
            file.write(struct.pack('<%ssx' % (len(capsule.name)), bytes(capsule.name, 'utf-8')))
            file.write(struct.pack('<i', capsule.parent_index))
            file.write(struct.pack('<i', capsule.material_index))
            file.write(struct.pack('<ffff', *capsule.rotation))
            file.write(struct.pack('<fff', *capsule.translation))
            file.write(struct.pack('<f', capsule.height))
            file.write(struct.pack('<f', capsule.radius))

    else:
        if write_comments:
            file.write('\n;### CAPSULES ###')

        file.write('\n%s' % (len(JMS.capsules)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<material>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<height>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, capsule in enumerate(JMS.capsules):
            if write_comments:
                file.write('\n;CAPSULE %s' % idx)

            file.write('\n%s' % capsule.name)
            file.write('\n%s' % capsule.parent_index)
            file.write('\n%s' % capsule.material_index)
            file.write(DECIMAL_4 % capsule.rotation)
            file.write(DECIMAL_3 % capsule.translation)
            file.write(DECIMAL_1 % capsule.height)
            file.write(DECIMAL_1 % capsule.radius)
            if write_whitespace:
                file.write('\n')

def write_convex_shapes_8206(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.convex_shapes)))
        for idx, convex_shape in enumerate(JMS.convex_shapes):
            file.write(struct.pack('<%ssx' % (len(convex_shape.name)), bytes(convex_shape.name, 'utf-8')))
            file.write(struct.pack('<i', convex_shape.parent_index))
            file.write(struct.pack('<ffff', *convex_shape.rotation))
            file.write(struct.pack('<fff', *convex_shape.translation))
            file.write(struct.pack('<f', convex_shape.height))
            file.write(struct.pack('<i', len(convex_shape.verts)))
            for vertex in convex_shape.verts:
                file.write(struct.pack('<fff', *vertex.translation))

    else:
        if write_comments:
            file.write('\n;### CONVEX SHAPES ###')

        file.write('\n%s' % (len(JMS.convex_shapes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<vertex count>')
            file.write('\n;\t<...vertices>')
            if write_whitespace:
                file.write('\n')

        for idx, convex_shape in enumerate(JMS.convex_shapes):
            if write_comments:
                file.write('\n;CONVEX %s' % idx)

            file.write('\n%s' % convex_shape.name)
            file.write('\n%s' % convex_shape.parent_index)
            file.write(DECIMAL_4 % convex_shape.rotation)
            file.write(DECIMAL_3 % convex_shape.translation)
            file.write('\n%s' % (len(convex_shape.verts)))
            for vertex in convex_shape.verts:
                file.write(DECIMAL_3 % vertex.translation)

            if write_whitespace:
                file.write('\n')

def write_convex_shapes_8207(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.convex_shapes)))
        for idx, convex_shape in enumerate(JMS.convex_shapes):
            file.write(struct.pack('<%ssx' % (len(convex_shape.name)), bytes(convex_shape.name, 'utf-8')))
            file.write(struct.pack('<i', convex_shape.parent_index))
            file.write(struct.pack('<i', convex_shape.material_index))
            file.write(struct.pack('<ffff', *convex_shape.rotation))
            file.write(struct.pack('<fff', *convex_shape.translation))
            file.write(struct.pack('<f', convex_shape.height))
            file.write(struct.pack('<i', len(convex_shape.verts)))
            for vertex in convex_shape.verts:
                file.write(struct.pack('<fff', *vertex.translation))

    else:
        if write_comments:
            file.write('\n;### CONVEX SHAPES ###')

        file.write('\n%s' % (len(JMS.convex_shapes)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<parent>')
            file.write('\n;\t<material>')
            file.write('\n;\t<rotation <i,j,k,w>>')
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<vertex count>')
            file.write('\n;\t<...vertices>')
            if write_whitespace:
                file.write('\n')

        for idx, convex_shape in enumerate(JMS.convex_shapes):
            if write_comments:
                file.write('\n;CONVEX %s' % idx)

            file.write('\n%s' % convex_shape.name)
            file.write('\n%s' % convex_shape.parent_index)
            file.write('\n%s' % convex_shape.material_index)
            file.write(DECIMAL_4 % convex_shape.rotation)
            file.write(DECIMAL_3 % convex_shape.translation)
            file.write('\n%s' % (len(convex_shape.verts)))
            for vertex in convex_shape.verts:
                file.write(DECIMAL_3 % vertex.translation)

            if write_whitespace:
                file.write('\n')

def write_ragdolls_8206(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.ragdolls)))
        for idx, ragdoll in enumerate(JMS.ragdolls):
            file.write(struct.pack('<%ssx' % (len(ragdoll.name)), bytes(ragdoll.name, 'utf-8')))
            file.write(struct.pack('<i', ragdoll.attached_index))
            file.write(struct.pack('<i', ragdoll.referenced_index))
            file.write(struct.pack('<ffff', *ragdoll.attached_rotation))
            file.write(struct.pack('<fff', *ragdoll.attached_translation))
            file.write(struct.pack('<ffff', *ragdoll.referenced_rotation))
            file.write(struct.pack('<fff', *ragdoll.referenced_translation))
            file.write(struct.pack('<f', ragdoll.min_twist))
            file.write(struct.pack('<f', ragdoll.max_twist))
            file.write(struct.pack('<f', ragdoll.min_cone))
            file.write(struct.pack('<f', ragdoll.max_cone))
            file.write(struct.pack('<f', ragdoll.min_plane))
            file.write(struct.pack('<f', ragdoll.max_plane))
    else:
        if write_comments:
            file.write('\n;### RAGDOLLS ###')

        file.write('\n%s' % (len(JMS.ragdolls)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<attached index>')
            file.write('\n;\t<referenced index>')
            file.write('\n;\t<attached transform>')
            file.write('\n;\t<reference transform>')
            file.write('\n;\t<min twist>')
            file.write('\n;\t<max twist>')
            file.write('\n;\t<min cone>')
            file.write('\n;\t<max cone>')
            file.write('\n;\t<min plane>')
            file.write('\n;\t<max plane>')
            if write_whitespace:
                file.write('\n')

        for idx, ragdoll in enumerate(JMS.ragdolls):
            if write_comments:
                file.write('\n;RAGDOLL %s' % idx)

            file.write('\n%s' % ragdoll.name)
            file.write('\n%s' % ragdoll.attached_index)
            file.write('\n%s' % ragdoll.referenced_index)
            file.write(DECIMAL_4 % ragdoll.attached_rotation)
            file.write(DECIMAL_3 % ragdoll.attached_translation)
            file.write(DECIMAL_4 % ragdoll.referenced_rotation)
            file.write(DECIMAL_3 % ragdoll.referenced_translation)
            file.write(DECIMAL_1 % ragdoll.min_twist)
            file.write(DECIMAL_1 % ragdoll.max_twist)
            file.write(DECIMAL_1 % ragdoll.min_cone)
            file.write(DECIMAL_1 % ragdoll.max_cone)
            file.write(DECIMAL_1 % ragdoll.min_plane)
            file.write(DECIMAL_1 % ragdoll.max_plane)
            if write_whitespace:
                file.write('\n')

def write_ragdolls_8213(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.ragdolls)))
        for idx, ragdoll in enumerate(JMS.ragdolls):
            file.write(struct.pack('<%ssx' % (len(ragdoll.name)), bytes(ragdoll.name, 'utf-8')))
            file.write(struct.pack('<i', ragdoll.attached_index))
            file.write(struct.pack('<i', ragdoll.referenced_index))
            file.write(struct.pack('<ffff', *ragdoll.attached_rotation))
            file.write(struct.pack('<fff', *ragdoll.attached_translation))
            file.write(struct.pack('<ffff', *ragdoll.referenced_rotation))
            file.write(struct.pack('<fff', *ragdoll.referenced_translation))
            file.write(struct.pack('<f', ragdoll.min_twist))
            file.write(struct.pack('<f', ragdoll.max_twist))
            file.write(struct.pack('<f', ragdoll.min_cone))
            file.write(struct.pack('<f', ragdoll.max_cone))
            file.write(struct.pack('<f', ragdoll.min_plane))
            file.write(struct.pack('<f', ragdoll.max_plane))
            file.write(struct.pack('<f', ragdoll.friction_limit))
    else:
        if write_comments:
            file.write('\n;### RAGDOLLS ###')

        file.write('\n%s' % (len(JMS.ragdolls)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<attached index>')
            file.write('\n;\t<referenced index>')
            file.write('\n;\t<attached transform>')
            file.write('\n;\t<reference transform>')
            file.write('\n;\t<min twist>')
            file.write('\n;\t<max twist>')
            file.write('\n;\t<min cone>')
            file.write('\n;\t<max cone>')
            file.write('\n;\t<min plane>')
            file.write('\n;\t<max plane>')
            file.write('\n;\t<friction limit>')
            if write_whitespace:
                file.write('\n')

        for idx, ragdoll in enumerate(JMS.ragdolls):
            if write_comments:
                file.write('\n;RAGDOLL %s' % idx)

            file.write('\n%s' % ragdoll.name)
            file.write('\n%s' % ragdoll.attached_index)
            file.write('\n%s' % ragdoll.referenced_index)
            file.write(DECIMAL_4 % ragdoll.attached_rotation)
            file.write(DECIMAL_3 % ragdoll.attached_translation)
            file.write(DECIMAL_4 % ragdoll.referenced_rotation)
            file.write(DECIMAL_3 % ragdoll.referenced_translation)
            file.write(DECIMAL_1 % ragdoll.min_twist)
            file.write(DECIMAL_1 % ragdoll.max_twist)
            file.write(DECIMAL_1 % ragdoll.min_cone)
            file.write(DECIMAL_1 % ragdoll.max_cone)
            file.write(DECIMAL_1 % ragdoll.min_plane)
            file.write(DECIMAL_1 % ragdoll.max_plane)
            file.write(DECIMAL_1 % ragdoll.friction_limit)
            if write_whitespace:
                file.write('\n')

def write_hinges(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.hinges)))
        for idx, hinge in enumerate(JMS.hinges):
            file.write(struct.pack('<%ssx' % (len(hinge.name)), bytes(hinge.name, 'utf-8')))
            file.write(struct.pack('<i', hinge.body_a_index))
            file.write(struct.pack('<i', hinge.body_b_index))
            file.write(struct.pack('<ffff', *hinge.body_a_rotation))
            file.write(struct.pack('<fff', *hinge.body_a_translation))
            file.write(struct.pack('<ffff', *hinge.body_b_rotation))
            file.write(struct.pack('<fff', *hinge.body_b_translation))
            file.write(struct.pack('<i', hinge.is_limited))
            file.write(struct.pack('<f', hinge.friction_limit))
            file.write(struct.pack('<f', hinge.min_angle))
            file.write(struct.pack('<f', hinge.max_angle))
    else:
        if write_comments:
            file.write('\n;### HINGES ###')

        file.write('\n%s' % (len(JMS.hinges)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<body A index>')
            file.write('\n;\t<body B index>')
            file.write('\n;\t<body A transform>')
            file.write('\n;\t<body B transform>')
            file.write('\n;\t<is limited>')
            file.write('\n;\t<friction limit>')
            file.write('\n;\t<min angle>')
            file.write('\n;\t<max angle>')
            if write_whitespace:
                file.write('\n')

        for idx, hinge in enumerate(JMS.hinges):
            if write_comments:
                file.write('\n;HINGE %s' % idx)

            file.write('\n%s' % hinge.name)
            file.write('\n%s' % hinge.body_a_index)
            file.write('\n%s' % hinge.body_b_index)
            file.write(DECIMAL_4 % hinge.body_a_rotation)
            file.write(DECIMAL_3 % hinge.body_a_translation)
            file.write(DECIMAL_4 % hinge.body_b_rotation)
            file.write(DECIMAL_3 % hinge.body_b_translation)
            file.write(DECIMAL_1 % hinge.min_twist)
            file.write('\n%s' % hinge.is_limited)
            file.write(DECIMAL_1 % hinge.friction_limit)
            file.write(DECIMAL_1 % hinge.min_angle)
            file.write(DECIMAL_1 % hinge.max_angle)
            if write_whitespace:
                file.write('\n')

def write_bounding_spheres(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.bounding_spheres)))
        for idx, bounding_sphere in enumerate(JMS.bounding_spheres):
            file.write(struct.pack('<fff', *bounding_sphere.translation))
            file.write(struct.pack('<f', bounding_sphere.radius))

    else:
        if write_comments:
            file.write('\n;### BOUNDING SPHERE ###')

        file.write('\n%s' % (len(JMS.bounding_spheres)))
        if write_comments:
            file.write('\n;\t<translation <x,y,z>>')
            file.write('\n;\t<radius>')
            if write_whitespace:
                file.write('\n')

        for idx, bounding_sphere in enumerate(JMS.bounding_spheres):
            if write_comments:
                file.write('\n;BOUNDING SPHERE %s' % idx)

            file.write(DECIMAL_3 % bounding_sphere.translation)
            file.write(DECIMAL_1 % bounding_sphere.radius)
            if write_whitespace:
                file.write('\n')

def write_car_wheels(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.car_wheels)))
        for idx, car_wheel in enumerate(JMS.car_wheels):
            file.write(struct.pack('<%ssx' % (len(car_wheel.name)), bytes(car_wheel.name, 'utf-8')))
            file.write(struct.pack('<i', car_wheel.chassis_index))
            file.write(struct.pack('<i', car_wheel.wheel_index))
            file.write(struct.pack('<ffff', *car_wheel.chassis_rotation))
            file.write(struct.pack('<fff', *car_wheel.chassis_translation))
            file.write(struct.pack('<ffff', *car_wheel.wheel_rotation))
            file.write(struct.pack('<fff', *car_wheel.wheel_translation))
            file.write(struct.pack('<ffff', *car_wheel.suspension_rotation))
            file.write(struct.pack('<fff', *car_wheel.suspension_translation))
            file.write(struct.pack('<f', car_wheel.suspension_min_limit))
            file.write(struct.pack('<f', car_wheel.suspension_max_limit))
            file.write(struct.pack('<f', car_wheel.friction_limit))
            file.write(struct.pack('<f', car_wheel.velocity))
            file.write(struct.pack('<f', car_wheel.gain))
    else:
        if write_comments:
            file.write('\n;### HINGES ###')

        file.write('\n%s' % (len(JMS.car_wheels)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<chassis index>')
            file.write('\n;\t<wheel index>')
            file.write('\n;\t<chassis transform>')
            file.write('\n;\t<wheel transform>')
            file.write('\n;\t<suspension transform>')
            file.write('\n;\t<suspension min limit>')
            file.write('\n;\t<suspension max limit>')
            file.write('\n;\t<friction limit>')
            file.write('\n;\t<velocity>')
            file.write('\n;\t<gain>')
            if write_whitespace:
                file.write('\n')

        for idx, car_wheel in enumerate(JMS.car_wheels):
            if write_comments:
                file.write('\n;CAR WHEEL %s' % idx)

            file.write('\n%s' % car_wheel.name)
            file.write('\n%s' % car_wheel.chassis_index)
            file.write('\n%s' % car_wheel.wheel_index)
            file.write(DECIMAL_4 % car_wheel.chassis_rotation)
            file.write(DECIMAL_3 % car_wheel.chassis_translation)
            file.write(DECIMAL_4 % car_wheel.wheel_rotation)
            file.write(DECIMAL_3 % car_wheel.wheel_translation)
            file.write(DECIMAL_4 % car_wheel.suspension_rotation)
            file.write(DECIMAL_3 % car_wheel.suspension_translation)
            file.write(DECIMAL_1 % car_wheel.suspension_min_limit)
            file.write(DECIMAL_1 % car_wheel.suspension_max_limit)
            file.write(DECIMAL_1 % car_wheel.friction_limit)
            file.write(DECIMAL_1 % car_wheel.friction_limit)
            file.write(DECIMAL_1 % car_wheel.velocity)
            file.write(DECIMAL_1 % car_wheel.gain)
            if write_whitespace:
                file.write('\n')

def write_point_to_points(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.point_to_points)))
        for idx, point_to_point in enumerate(JMS.point_to_points):
            file.write(struct.pack('<%ssx' % (len(point_to_point.name)), bytes(point_to_point.name, 'utf-8')))
            file.write(struct.pack('<i', point_to_point.body_a_index))
            file.write(struct.pack('<i', point_to_point.body_b_index))
            file.write(struct.pack('<ffff', *point_to_point.body_a_rotation))
            file.write(struct.pack('<fff', *point_to_point.body_a_translation))
            file.write(struct.pack('<ffff', *point_to_point.body_b_rotation))
            file.write(struct.pack('<fff', *point_to_point.body_b_translation))
            file.write(struct.pack('<i', point_to_point.constraint_type))
            file.write(struct.pack('<f', point_to_point.x_min_limit))
            file.write(struct.pack('<f', point_to_point.x_max_limit))
            file.write(struct.pack('<f', point_to_point.y_min_limit))
            file.write(struct.pack('<f', point_to_point.y_max_limit))
            file.write(struct.pack('<f', point_to_point.z_min_limit))
            file.write(struct.pack('<f', point_to_point.z_max_limit))
            file.write(struct.pack('<f', point_to_point.spring_length))
    else:
        if write_comments:
            file.write('\n;### POINT TO POINT ###')

        file.write('\n%s' % (len(JMS.point_to_points)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<body A index>')
            file.write('\n;\t<body B index>')
            file.write('\n;\t<body A transform>')
            file.write('\n;\t<body B transform>')
            file.write('\n;\t<constraint type>')
            file.write('\n;\t<x min limit>')
            file.write('\n;\t<x max limit>')
            file.write('\n;\t<y min limit>')
            file.write('\n;\t<y max limit>')
            file.write('\n;\t<z min limit>')
            file.write('\n;\t<z max limit>')
            file.write('\n;\t<spring length>')
            if write_whitespace:
                file.write('\n')

        for idx, point_to_point in enumerate(JMS.point_to_points):
            if write_comments:
                file.write('\n;POINT_TO_POINT %s' % idx)

            file.write('\n%s' % point_to_point.name)
            file.write('\n%s' % point_to_point.body_a_index)
            file.write('\n%s' % point_to_point.body_b_index)
            file.write(DECIMAL_4 % point_to_point.body_a_rotation)
            file.write(DECIMAL_3 % point_to_point.body_a_translation)
            file.write(DECIMAL_4 % point_to_point.body_b_rotation)
            file.write(DECIMAL_3 % point_to_point.body_b_translation)
            file.write('\n%s' % point_to_point.constraint_type)
            file.write(DECIMAL_1 % point_to_point.x_min_limit)
            file.write(DECIMAL_1 % point_to_point.x_max_limit)
            file.write(DECIMAL_1 % point_to_point.y_min_limit)
            file.write(DECIMAL_1 % point_to_point.y_max_limit)
            file.write(DECIMAL_1 % point_to_point.z_min_limit)
            file.write(DECIMAL_1 % point_to_point.z_max_limit)
            file.write(DECIMAL_1 % point_to_point.spring_length)
            if write_whitespace:
                file.write('\n')

def write_prismatics(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.prismatics)))
        for idx, prismatic in enumerate(JMS.prismatics):
            file.write(struct.pack('<%ssx' % (len(prismatic.name)), bytes(prismatic.name, 'utf-8')))
            file.write(struct.pack('<i', prismatic.body_a_index))
            file.write(struct.pack('<i', prismatic.body_b_index))
            file.write(struct.pack('<ffff', *prismatic.body_a_rotation))
            file.write(struct.pack('<fff', *prismatic.body_a_translation))
            file.write(struct.pack('<ffff', *prismatic.body_b_rotation))
            file.write(struct.pack('<fff', *prismatic.body_b_translation))
            file.write(struct.pack('<i', prismatic.is_limited))
            file.write(struct.pack('<f', prismatic.friction_limit))
            file.write(struct.pack('<f', prismatic.min_limit))
            file.write(struct.pack('<f', prismatic.max_limit))
    else:
        if write_comments:
            file.write('\n;### PRISMATIC ###')

        file.write('\n%s' % (len(JMS.prismatics)))
        if write_comments:
            file.write('\n;\t<name>')
            file.write('\n;\t<body A index>')
            file.write('\n;\t<body B index>')
            file.write('\n;\t<body A transform>')
            file.write('\n;\t<body B transform>')
            file.write('\n;\t<is limited>')
            file.write('\n;\t<friction limit>')
            file.write('\n;\t<min limit>')
            file.write('\n;\t<max limit>')
            if write_whitespace:
                file.write('\n')

        for idx, prismatic in enumerate(JMS.prismatics):
            if write_comments:
                file.write('\n;PRISMATIC %s' % idx)

            file.write('\n%s' % prismatic.name)
            file.write('\n%s' % prismatic.body_a_index)
            file.write('\n%s' % prismatic.body_b_index)
            file.write(DECIMAL_4 % prismatic.body_a_rotation)
            file.write(DECIMAL_3 % prismatic.body_a_translation)
            file.write(DECIMAL_4 % prismatic.body_b_rotation)
            file.write(DECIMAL_3 % prismatic.body_b_translation)
            file.write('\n%s' % prismatic.is_limited)
            file.write(DECIMAL_1 % prismatic.friction_limit)
            file.write(DECIMAL_1 % prismatic.min_limit)
            file.write(DECIMAL_1 % prismatic.max_limit)
            if write_whitespace:
                file.write('\n')

def write_skylights(file, JMS, binary, write_comments=False, write_whitespace=False):
    if binary:
        file.write(struct.pack('<i', len(JMS.skylights)))
        for idx, skylight in enumerate(JMS.skylights):
            file.write(struct.pack('<fff', *skylight.direction))
            file.write(struct.pack('<fff', *skylight.radiant_intensity))
            file.write(struct.pack('<f', skylight.solid_angle))
    else:
        if write_comments:
            file.write('\n;### SKYLIGHT ###')

        file.write('\n%s' % (len(JMS.skylights)))
        if write_comments:
            file.write('\n;\t<direction <x,y,z>>')
            file.write('\n;\t<radiant intensity <x,y,z>>')
            file.write('\n;\t<solid angle>')
            if write_whitespace:
                file.write('\n')

        for idx, skylight in enumerate(JMS.skylights):
            if write_comments:
                file.write('\n;SKYLIGHT %s' % idx)

            file.write(DECIMAL_3 % skylight.direction)
            file.write(DECIMAL_3 % skylight.radiant_intensity)
            file.write(DECIMAL_1 % skylight.solid_angle)
            if write_whitespace:
                file.write('\n')

def update_decimal():
    global DECIMAL_POINT
    global DECIMAL_1
    global DECIMAL_2
    global DECIMAL_3
    global DECIMAL_4

    DECIMAL_POINT = "10"
    DECIMAL_1 = '\n%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_2 = '\n%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_3 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)
    DECIMAL_4 = '\n%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f\t%0.{decimal_point}f'.format(decimal_point=DECIMAL_POINT)

def build_asset(context, blend_scene, filepath, jms_version, game_title, generate_checksum, fix_rotations, use_maya_sorting, folder_structure, folder_type, model_type, is_jmi, permutation_ce, level_of_detail_ce, custom_scale, loop_normals, write_textures, report):
    JMS = process_scene(context, jms_version, game_title, generate_checksum, fix_rotations, use_maya_sorting, model_type, blend_scene, custom_scale, loop_normals, write_textures)

    binary = False

    version_bounds = '8197-8200'
    if game_title == "halo2":
        version_bounds = '8197-8210'
    elif game_title == "halo3":
        version_bounds = '8197-8213'

    filename = global_functions.get_filename(game_title, permutation_ce, level_of_detail_ce, folder_structure, model_type, False, filepath)
    root_directory = global_functions.get_directory(context, game_title, model_type, folder_structure, folder_type, is_jmi, filepath)
    output_path = os.path.join(root_directory, filename)
    if binary:
        file = open(output_path + "B", 'wb')
        file.write(struct.pack('<4s', bytes("IMBF", 'utf-8')))

    else:
        file = open(output_path, 'w', encoding='utf_8')

    if jms_version == 8197:
        write_comments = False
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_checksum(file, JMS, binary, write_comments, write_whitespace)
        write_nodes_8197(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8197(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8197(file, JMS, binary, write_comments, write_whitespace)
        write_regions_8197(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8197(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8197(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8198:
        write_comments = False
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_checksum(file, JMS, binary, write_comments, write_whitespace)
        write_nodes_8197(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8197(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8198(file, JMS, binary, write_comments, write_whitespace)
        write_regions_8197(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8198(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8198(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8199: 
        write_comments = False
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_checksum(file, JMS, binary, write_comments, write_whitespace)
        write_nodes_8197(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8197(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8198(file, JMS, binary, write_comments, write_whitespace)
        write_regions_8197(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8199(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8198(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8200:
        write_comments = False
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_checksum(file, JMS, binary, write_comments, write_whitespace)
        write_nodes_8197(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8197(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8200(file, JMS, binary, write_comments, write_whitespace)
        write_regions_8197(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8199(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8198(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8201:
        write_comments = True
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, False, write_whitespace)
        write_checksum(file, JMS, binary, False, write_whitespace)
        write_nodes_8201(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8201(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instances###')
        write_instance_xref_paths_8201(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Skin data###')
        write_regions_8201(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8201(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8201(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8202:
        write_comments = True
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, False, write_whitespace)
        write_checksum(file, JMS, binary, False, write_whitespace)
        write_nodes_8201(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8201(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instances###')
        write_instance_xref_paths_8201(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Skin data###')
        write_regions_8201(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8202(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8201(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8203:
        write_comments = True
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, False, write_whitespace)
        write_checksum(file, JMS, binary, False, write_whitespace)
        write_nodes_8201(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8201(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instances###')
        write_instance_xref_paths_8201(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8203(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Skin data###')
        write_regions_8201(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8202(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8201(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8204:
        write_comments = True
        write_whitespace = False
        write_version(file, jms_version, version_bounds, binary, False, write_whitespace)
        write_checksum(file, JMS, binary, False, write_whitespace)
        write_nodes_8201(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8201(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8201(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Instances###')
        write_instance_xref_paths_8201(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8203(file, JMS, binary, write_comments, write_whitespace)
        if write_comments:
            file.write('\n;')
            file.write('\n;###Skin data###')
        write_regions_8201(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8204(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8201(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8205:
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8206:
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8206(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8206(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8206(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8206(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8207:
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8208:
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8209:
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
        write_bounding_spheres(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8210:
        update_decimal()
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8205(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
        write_car_wheels(file, JMS, binary, write_comments, write_whitespace)
        write_point_to_points(file, JMS, binary, write_comments, write_whitespace)
        write_prismatics(file, JMS, binary, write_comments, write_whitespace)
        write_bounding_spheres(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8211:
        update_decimal()
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8211(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
        write_car_wheels(file, JMS, binary, write_comments, write_whitespace)
        write_point_to_points(file, JMS, binary, write_comments, write_whitespace)
        write_prismatics(file, JMS, binary, write_comments, write_whitespace)
        write_bounding_spheres(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8212:
        update_decimal()
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8211(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8206(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
        write_car_wheels(file, JMS, binary, write_comments, write_whitespace)
        write_point_to_points(file, JMS, binary, write_comments, write_whitespace)
        write_prismatics(file, JMS, binary, write_comments, write_whitespace)
        write_bounding_spheres(file, JMS, binary, write_comments, write_whitespace)
        write_skylights(file, JMS, binary, write_comments, write_whitespace)
    elif jms_version == 8213:
        update_decimal()
        write_comments = True
        write_whitespace = True
        write_version(file, jms_version, version_bounds, binary, write_comments, write_whitespace)
        write_nodes_8205(file, JMS, binary, write_comments, write_whitespace)
        write_materials_8205(file, JMS, binary, write_comments, write_whitespace)
        write_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_instance_xref_paths_8208(file, JMS, binary, write_comments, write_whitespace)
        write_instance_markers_8205(file, JMS, binary, write_comments, write_whitespace)
        write_vertices_8211(file, JMS, binary, write_comments, write_whitespace)
        write_triangles_8205(file, JMS, binary, write_comments, write_whitespace)
        write_spheres_8207(file, JMS, binary, write_comments, write_whitespace)
        write_boxes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_capsules_8207(file, JMS, binary, write_comments, write_whitespace)
        write_convex_shapes_8207(file, JMS, binary, write_comments, write_whitespace)
        write_ragdolls_8213(file, JMS, binary, write_comments, write_whitespace)
        write_hinges(file, JMS, binary, write_comments, write_whitespace)
        write_car_wheels(file, JMS, binary, write_comments, write_whitespace)
        write_point_to_points(file, JMS, binary, write_comments, write_whitespace)
        write_prismatics(file, JMS, binary, write_comments, write_whitespace)
        write_bounding_spheres(file, JMS, binary, write_comments, write_whitespace)
        write_skylights(file, JMS, binary, write_comments, write_whitespace)
    if not binary:
        file.write('\n')

    report({'INFO'}, "Export completed successfully")
    file.close()
