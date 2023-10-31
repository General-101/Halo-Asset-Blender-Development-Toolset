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

from enum import Flag, auto
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
        FloatProperty,
        StringProperty,
        PointerProperty,
        FloatVectorProperty,
        CollectionProperty
        )

class Halo_SurfaceFlags(Panel):
    """Set settings for surface to be used in the Halo maze generator"""
    bl_label = "Halo Surface Flags"
    bl_idname = "OBJECT_PT_halo_surface_flags"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"
    bl_options = {'DEFAULT_CLOSED'}
    ebm = dict()

    @classmethod
    def poll(cls, context):
        active_object = context.active_object
        if active_object and active_object.type == "MESH" and context.mode == 'EDIT_MESH':
            me = context.edit_object.data

            cls.ebm.setdefault(me.name, bmesh.from_edit_mesh(me))
            return True

        cls.ebm.clear()
        return False

    def draw(self, context):
        layout = self.layout
        me = context.edit_object.data

        row = layout.row()
        row.label(text="Valid Surface:")
        row.prop(me, "halo_valid_surface", text='')
        row = layout.row()
        row.label(text="Valid Character Flags:")
        row.prop(me, "halo_valid_characters", text='')

        box = layout.split()
        col = box.column(align=True)
        row = col.row()

        row = col.row()
        row.label(text='Marine:')
        row.prop(me, "halo_marine", text='')
        row = col.row()
        row.label(text='Elite:')
        row.prop(me, "halo_elite", text='')
        row = col.row()
        row.label(text='Grunt:')
        row.prop(me, "halo_grunt", text='')
        row = col.row()
        row.label(text='Hunter:')
        row.prop(me, "halo_hunter", text='')
        row = col.row()
        row.label(text='Jackal:')
        row.prop(me, "halo_jackal", text='')
        row = col.row()
        row.label(text='Floodcarrier:')
        row.prop(me, "halo_floodcarrier", text='')
        col = box.column()
        row = col.row()
        row.label(text='Floodcombat Elite:')
        row.prop(me, "halo_floodcombat_elite", text='')
        row = col.row()
        row.label(text='Floodcombat Human:')
        row.prop(me, "halo_floodcombat_human", text='')
        row = col.row()
        row.label(text='Flood Infection:')
        row.prop(me, "halo_flood_infection", text='')
        row = col.row()
        row.label(text='Sentinel:')
        row.prop(me, "halo_sentinel", text='')
        row = col.row()
        row.label(text='Drinol:')
        row.prop(me, "halo_drinol", text='')
        row = col.row()
        row.label(text='Slug Man:')
        row.prop(me, "halo_slug_man", text='')

def set_surface_usage(self, value):
    hvs = self.attributes.get("Halo Valid Surface")
    if hvs is None:
        self.attributes.new(name="Halo Valid Surface", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Surface")

    af = bm.faces.active
    if af and surface_layer:
        af[surface_layer] = value
        bmesh.update_edit_mesh(self)

def get_surface_usage(self):
    hvs = self.attributes.get("Halo Valid Surface")
    if hvs is None:
        self.attributes.new(name="Halo Valid Surface", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Surface")

    af = bm.faces.active
    if af and surface_layer:
        is_valid = af[surface_layer]

    return is_valid

def set_character_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        af[surface_layer] = value
        bmesh.update_edit_mesh(self)

def get_character_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        is_valid = af[surface_layer]

    return is_valid

class CharacterFlags(Flag):
    marine = auto()
    elite = auto()
    grunt = auto()
    hunter = auto()
    jackal = auto()
    floodcarrier = auto()
    floodcombat_elite = auto()
    floodcombat_human = auto()
    flood_infection = auto()
    sentinel = auto()
    drinol = auto()
    slug_man = auto()

def set_marine_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.marine.value
        else:
            af[surface_layer] -= CharacterFlags.marine.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_marine_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.marine in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_elite_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.elite.value
        else:
            af[surface_layer] -= CharacterFlags.elite.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_elite_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.elite in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_grunt_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.grunt.value
        else:
            af[surface_layer] -= CharacterFlags.grunt.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_grunt_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.grunt in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_hunter_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.hunter.value
        else:
            af[surface_layer] -= CharacterFlags.hunter.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_hunter_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.hunter in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_jackal_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.jackal.value
        else:
            af[surface_layer] -= CharacterFlags.jackal.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_jackal_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.jackal in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcarrier_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcarrier.value
        else:
            af[surface_layer] -= CharacterFlags.floodcarrier.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcarrier_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcarrier in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcombat_elite_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcombat_elite.value
        else:
            af[surface_layer] -= CharacterFlags.floodcombat_elite.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcombat_elite_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcombat_elite in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_floodcombat_human_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.floodcombat_human.value
        else:
            af[surface_layer] -= CharacterFlags.floodcombat_human.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_floodcombat_human_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.floodcombat_human in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_flood_infection_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.flood_infection.value
        else:
            af[surface_layer] -= CharacterFlags.flood_infection.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_flood_infection_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.flood_infection in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_sentinel_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.sentinel.value
        else:
            af[surface_layer] -= CharacterFlags.sentinel.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_sentinel_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.sentinel in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_drinol_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.drinol.value
        else:
            af[surface_layer] -= CharacterFlags.drinol.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_drinol_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.drinol in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid

def set_slug_man_usage(self, value):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if value:
            af[surface_layer] += CharacterFlags.slug_man.value
        else:
            af[surface_layer] -= CharacterFlags.slug_man.value
            if af[surface_layer] < 0:
                af[surface_layer] = 0

        bmesh.update_edit_mesh(self)

def get_slug_man_usage(self):
    hvc = self.attributes.get("Halo Valid Characters")
    if hvc is None:
        self.attributes.new(name="Halo Valid Characters", domain='FACE', type='INT')

    is_valid = False
    bm = Halo_SurfaceFlags.ebm.setdefault(self.name, bmesh.from_edit_mesh(self))

    surface_layer = bm.faces.layers.int.get("Halo Valid Characters")

    af = bm.faces.active
    if af and surface_layer:
        if CharacterFlags.slug_man in CharacterFlags(af[surface_layer]):
            is_valid = True

    return is_valid
