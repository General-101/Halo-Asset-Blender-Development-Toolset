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

from bpy.props import (
        IntProperty,
        BoolProperty,
        EnumProperty,
        StringProperty,
        PointerProperty,
        CollectionProperty
        )

def get_unique_name(object_name_list, name):
    object_name_values = []
    for object_name in object_name_list:
        object_name_values.append(object_name.name)

    formatted_name = name
    object_name_dic = {}
    object_name_set = set(object_name_values)
    for object_name in object_name_set:
        object_name_dic[object_name] = object_name_values.count(name)

    if object_name_dic[name] > 1:
        increment_count = 1
        while not object_name_dic.get(formatted_name) == None:
            formatted_name = "{0}.{1:003}".format(name, increment_count)
            increment_count += 1

    return formatted_name

def update_region_prop(self, context):
    scene = context.scene
    if len(scene.object_names) > 1:
        self["name"] = get_unique_name(scene.object_names, self.name)

def object_name_add(self, name="unnamed"):
    object_name_element = self.object_names.add()
    object_name_element.name = name
    self.active_object_name = 0

class ObjectNameItem(PropertyGroup):
    name: StringProperty(
           name="Name",
           description="A name for this item",
           update=update_region_prop
           )

class OBJECTNAME_UL_List(UIList):
    def draw_item(self, context, layout, data, item, icon, active_data, active_propname, index):
        if self.layout_type in {'DEFAULT', 'COMPACT'}:
            layout.prop(item, "name", text="", emboss=False, icon='FACE_MAPS')

        elif self.layout_type == 'GRID':
            layout.alignment = 'CENTER'
            layout.label(text="", icon_value=icon)

class Halo_OT_ObjectNameAdd(Operator):
    """Add a new object name to the scene"""
    bl_idname = "object_names.object_name_add"
    bl_label = "Add an object name"

    def execute(self, context):
        scene = context.scene

        scene.object_name_add()
        scene.active_object_name = len(scene.object_names) - 1

        return{'FINISHED'}

class Halo_OT_ObjectNameRemove(Operator):
    """Remove an object name from the scene"""
    bl_idname = "object_names.object_name_remove"
    bl_label = "Remove an object name"

    @classmethod
    def poll(cls, context):
        valid = False
        scene = context.scene
        if scene and len(scene.object_names) > 0:
            valid = True

        return valid

    def execute(self, context):
        scene = context.scene

        object_names = scene.object_names
        active_object_name = scene.active_object_name

        object_names.remove(active_object_name)
        scene.active_object_name = min(max(0, active_object_name), len(object_names) - 1)

        return{'FINISHED'}

class Halo_OT_ObjectNameMove(Operator):
    """Move the active object name up/down in the list"""
    bl_idname = "object_names.object_name_move"
    bl_label = "Move Object Name"

    direction: bpy.props.EnumProperty(items=(('UP', 'Up', ""), ('DOWN', 'Down', ""),))

    @classmethod
    def poll(cls, context):
        valid = False
        scene = context.scene
        if scene and len(scene.object_names) > 0:
            valid = True

        return valid

    def move_index(self, scene):
        list_length = len(scene.object_names) - 1
        new_index = scene.active_object_name + (-1 if self.direction == 'UP' else 1)

        scene.active_object_name = max(0, min(new_index, list_length))

    def execute(self, context):
        scene = context.scene

        object_names = scene.object_names
        active_object_name = scene.active_object_name

        neighbor = active_object_name + (-1 if self.direction == 'UP' else 1)
        object_names.move(neighbor, active_object_name)
        self.move_index(scene)

        return{'FINISHED'}

class Halo_ObjectNamePanel(Panel):
    bl_label = "Halo Object Names"
    bl_idname = "COLLECTIOM_PT_ObjectNames"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "scene"
    bl_options = {'DEFAULT_CLOSED'}
    bl_parent_id = "HALO_PT_ScenarioTag"

    @classmethod
    def poll(cls, context):
        valid = False
        collection = context.collection
        if collection:
            valid = True

        return valid

    def draw(self, context):
        layout = self.layout
        collection = context.collection
        scene = context.scene
        object_name_count = len(scene.object_names)

        row = layout.row()
        row.template_list("OBJECTNAME_UL_List", "Object_Name_List", scene, "object_names", scene, "active_object_name")

        col = row.column(align=True)
        col.operator("object_names.object_name_add", icon='ADD', text="")
        col.operator("object_names.object_name_remove", icon='REMOVE', text="")

        if object_name_count >= 2:
            col.separator()
            col.operator("object_names.object_name_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object_names.object_name_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

        #col.separator()
        #col.menu("REGION_MT_context_menu", icon='DOWNARROW_HLT', text="")
