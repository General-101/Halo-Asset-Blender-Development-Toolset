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

import bpy
import bmesh

from bpy.types import (
        PropertyGroup,
        Operator,
        UIList,
        Panel,
        Menu
        )

from bpy.props import StringProperty

def get_custom_attribute(self, attribute_name="Region Assignment"):
    region_attribute = self.attributes.get(attribute_name)
    if region_attribute == None:
        region_attribute = self.attributes.new(name=attribute_name, type="INT", domain="FACE")

    return region_attribute

def get_unique_name(region_list, name):
    formatted_name = name
    region_name_dic = {}
    region_set = set(region_list)
    for region in region_set:
        region_name_dic[region] = region_list.count(region)

    if region_name_dic[name] > 1:
        increment_count = 1
        while not region_name_dic.get(formatted_name) == None:
            formatted_name = "{0}.{1:003}".format(name, increment_count)
            increment_count += 1

    return formatted_name

def update_region_prop(self, context):
    scene = context.scene
    if len(scene.active_region_list) > 1:
        self["name"] = get_unique_name(scene.active_region_list, self.name)

def region_add(self, name="unnamed"):
    scene = bpy.context.scene
    scene.active_region_list.clear()
    for region in self.region_list:
        scene.active_region_list.append(region.name)

    scene.active_region_list.append(name)

    region = self.region_list.add()
    region.name = name
    self.active_region = 0

class RegionItem(PropertyGroup):
    name: StringProperty(
           name="Name",
           description="A name for this item",
           default="unnamed",
           update=update_region_prop
           )

class REGION_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='FACE_MAPS')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Halo_OT_RegionAdd(Operator):
    """Add a new region to the active object"""
    bl_idname = "region_list.region_add"
    bl_label = "Add region"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH":
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object

        ob.region_add()
        ob.data.get_custom_attribute()
        ob.active_region = len(ob.region_list) - 1

        return{'FINISHED'}

class Halo_OT_RegionRemove(Operator):
    """Remove a region from the active object"""
    bl_idname = "region_list.region_remove"
    bl_label = "Remove a region"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(active_object.region_list) > 0:
            valid = True

        return valid

    def execute(self, context):
        ob = context.object
        data = ob.data

        region_list = ob.region_list
        active_region = ob.active_region
        data_region_value = active_region + 1

        modified_indices = list(range(active_region, len(ob.region_list)))
        for idx, index in enumerate(modified_indices):
            modified_indices[idx] += 1

        del modified_indices[0]

        region_attribute = ob.data.get_custom_attribute()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                face_value = face[surface_layer]
                if face_value == data_region_value:
                    face[surface_layer] = -1
                elif face_value in modified_indices:
                    face[surface_layer] += -1

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                face_value = region_attribute.data[face.index].value
                if face_value == data_region_value:
                    region_attribute.data[face.index].value = -1
                elif face_value in modified_indices:
                    region_attribute.data[face.index].value += -1

        region_list.remove(active_region)
        ob.active_region = min(max(0, active_region), len(region_list) - 1)

        return{'FINISHED'}

class Halo_OT_RegionMove(Operator):
    """Move the active region up/down in the list"""
    bl_idname = "region_list.region_move"
    bl_label = "Move region"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(context.active_object.region_list) > 0:
            valid = True

        return valid

    def move_attribute_index(self, context, neighbor, active_region):
        ob = context.object
        data = ob.data

        neighbor += 1
        active_region += 1

        region_attribute = ob.data.get_custom_attribute()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                if face[surface_layer] == neighbor:
                    face[surface_layer] = active_region
                elif face[surface_layer] == active_region:
                    face[surface_layer] = neighbor

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                if region_attribute.data[face.index].value == neighbor:
                    region_attribute.data[face.index].value = active_region
                elif region_attribute.data[face.index].value == active_region:
                    region_attribute.data[face.index].value = neighbor

    def move_index(self, ob):
        active_region = ob.active_region
        list_length = len(ob.region_list) - 1
        new_index = active_region + (-1 if self.direction == 'UP' else 1)

        ob.active_region = max(0, min(new_index, list_length))

    def execute(self, context):
        ob = context.object

        region_list = ob.region_list
        active_region = ob.active_region

        neighbor = active_region + (-1 if self.direction == 'UP' else 1)
        self.move_attribute_index(context, neighbor, active_region)
        region_list.move(neighbor, active_region)
        self.move_index(ob)

        return{'FINISHED'}

class Halo_OT_RegionAssign(Operator):
    """Assign faces to a region"""
    bl_idname = "region_list.region_assign"
    bl_label = "Region Assign"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face.select:
                face[surface_layer] = active_region

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionRemoveFrom(Operator):
    """Remove faces from a region"""
    bl_idname = "region_list.region_remove_from"
    bl_label = "Region Remove From"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face.select and face[surface_layer] == active_region:
                face[surface_layer] = -1

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionSelect(Operator):
    """Select faces beloging to a region"""
    bl_idname = "region_list.region_select"
    bl_label = "Region Select"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face[surface_layer] == active_region:
                face.select = True

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionDeselect(Operator):
    """Deselect faces beloging to a region"""
    bl_idname = "region_list.region_deselect"
    bl_label = "Region Deselect"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            valid = True

        return valid

    def execute(self, context):
        ob = bpy.context.object
        data = ob.data
        active_region = ob.active_region + 1

        ob.data.get_custom_attribute()

        bm = bmesh.from_edit_mesh(data)

        surface_layer = bm.faces.layers.int.get("Region Assignment")
        for face in bm.faces:
            if face[surface_layer] == active_region:
                face.select = False

        bmesh.update_edit_mesh(data)

        return{'FINISHED'}

class Halo_OT_RegionRemoveUnused(Operator):
    """Removes all unused regions from the active object"""
    bl_idname = "region_list.region_remove_unused"
    bl_label = "Remove unused regions"

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and len(active_object.region_list) > 0:
            valid = True

        return valid

    def execute(self, context):
        ob = context.object
        data = ob.data

        region_list = ob.region_list
        active_region = ob.active_region
        data_region_value = active_region + 1
        region_attribute = ob.data.get_custom_attribute()
        index_set = set()
        unused_indices = set()
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(data)

            surface_layer = bm.faces.layers.int.get("Region Assignment")
            for face in bm.faces:
                if not face[surface_layer] == 0:
                    index_set.add(face[surface_layer] - 1)

            bmesh.update_edit_mesh(data)

        else:
            for face in data.polygons:
                if not region_attribute.data[face.index].value == 0:
                    index_set.add(region_attribute.data[face.index].value - 1)

        for region_idx, region in enumerate(region_list):
            if not region_idx in index_set:
                unused_indices.add(region_idx)

        for region_index in reversed(sorted(unused_indices)):
            modified_indices = list(range(region_index, len(ob.region_list)))
            for idx, index in enumerate(modified_indices):
                modified_indices[idx] += 1

            del modified_indices[0]

            if context.mode == 'EDIT_MESH':
                bm = bmesh.from_edit_mesh(data)

                surface_layer = bm.faces.layers.int.get("Region Assignment")
                for face in bm.faces:
                    face_value = face[surface_layer]
                    if face_value in modified_indices:
                        face[surface_layer] += -1

                bmesh.update_edit_mesh(data)

            else:
                for face in data.polygons:
                    face_value = region_attribute.data[face.index].value
                    if face_value in modified_indices:
                        region_attribute.data[face.index].value += -1

            region_list.remove(region_index)
            ob.active_region = min(max(0, active_region), len(region_list) - 1)

        return{'FINISHED'}

class REGION_MT_context_menu(Menu):
    bl_label = "Region Specials"

    def draw(self, _context):
        layout = self.layout

        layout.operator("region_list.region_remove_unused")

class Halo_RegionsPanel(Panel):
    bl_label = "Halo Regions"
    bl_idname = "OBJECT_PT_halo_regions"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}

    @classmethod
    def poll(cls, context):
        valid = False
        active_object = context.active_object
        if active_object and active_object.type == "MESH":
            valid = True

        return valid

    def draw(self, context):
        layout = self.layout
        ob = context.object
        data = ob.data
        region_count = len(ob.region_list)

        scene = context.scene
        if ob and ob.type == "MESH":
            scene.active_region_list.clear()
            for region in ob.region_list:
                scene.active_region_list.append(region.name)

        row = layout.row()
        row.template_list("REGION_UL_List", "Region_List", ob, "region_list", ob, "active_region")

        col = row.column(align=True)
        col.operator("region_list.region_add", icon='ADD', text="")
        col.operator("region_list.region_remove", icon='REMOVE', text="")

        if region_count >= 2:
            col.separator()
            col.operator("region_list.region_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("region_list.region_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        col.separator()
        col.menu("REGION_MT_context_menu", icon='DOWNARROW_HLT', text="")
        if region_count >= 1:
            if ob.mode == 'EDIT' and ob.type == 'MESH':
                row = layout.row()

                sub = row.row(align=True)
                sub.operator("region_list.region_assign", text="Assign")
                sub.operator("region_list.region_remove_from", text="Remove")

                sub = row.row(align=True)
                sub.operator("region_list.region_select", text="Select")
                sub.operator("region_list.region_deselect", text="Deselect")
