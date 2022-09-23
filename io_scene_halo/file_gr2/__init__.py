# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Generalkidd & Crisp
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

bl_info = {
    "name": "Halo GR2 Export",
    "author": "Generalkidd, Crisp",
    "version": (1.0),
    "blender": (3, 3, 0),
    "location": "File > Export",
    "category": "Export",
    "description": "Halo Granny File and Sidecar exporter",
}
from mimetypes import init
import bpy
from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty
from bpy.types import Operator, Panel
from bpy_extras.io_utils import ExportHelper, orientation_helper

import os
t = os.getcwd()
t += "\\scripts\\addons\\io_scene_fbx"
print(t)
import sys
sys.modules[bpy.types.IMPORT_SCENE_OT_fbx.__module__].__file__
from subprocess import run
import sys
sys.path.insert(0,t)
from io_scene_fbx import export_fbx_bin, __init__
print("HERE!!!")

@orientation_helper(axis_forward='Y', axis_up='Z')

class Export_Halo_GR2(Operator, ExportHelper):
    """Writes a Halo Reach GR2 File using your Halo Editing Kit"""
    bl_idname = "export_halo.gr2"
    bl_label = "Export"

    filename_ext = ".gr2"
    filter_glob: StringProperty(
        default="*.gr2",
        options={'HIDDEN'},
        maxlen=255,
    )

    game_version:EnumProperty(
        name="Game Version",
        description="The game to export this asset for",
        items=[ ('REACH', "Halo Reach", "Export an asset intended for Halo Reach"),
            ]
        )

    export_gr2: BoolProperty(
            name="Export To GR2",
            description="Uses the exported FBX and JSON files to generate a GR2 File",
            default=True,
            )
    keep_fbx: BoolProperty(
            name="FBX",
            description="Keep the source FBX file after GR2 conversion",
            default=False,
            )
    keep_json: BoolProperty(
            name="JSON",
            description="Keep the source JSON file after GR2 conversion",
            default=False,
            )
    export_sidecar: BoolProperty(
            name="Export Sidecar",
            description="",
            default=True,
            )
    sidecar_type: EnumProperty(
            name='Asset Type',
            description='',
            default='MODEL',
            items=[ ('MODEL', "Model", ""),
                ('SCENARIO', "Scenario", ""),
                ('DECORATOR', "Decorator", ""),
                ('PARTICLE MODEL', "Particle Model", ""),
               ]
        )
    
    def UpdateSelected(self, context):
        if self.export_method == 'SELECTED':
            self.use_selection = True
        else:
            self.use_selection = False
    
    export_method: EnumProperty(
            name="Export Method",
            description="",
            update=UpdateSelected,
            items=[('BATCH', "Batch", ""), ('SELECTED', "Selected", "")]
            )
    export_animations: BoolProperty(
            name='Animations',
            description='',
            default=True,
        )
    export_render: BoolProperty(
            name='Render Models',
            description='',
            default=True,
        )
    export_collision: BoolProperty(
            name='Collision Models',
            description='',
            default=True,
        )
    export_physics: BoolProperty(
            name='Physics Models',
            description='',
            default=True,
        )
    export_markers: BoolProperty(
            name='Markers',
            description='',
            default=True,
        )
    export_structure: BoolProperty(
            name='Structure',
            description='',
            default=True,
        )
    export_structure_design: BoolProperty(
            name='Structure Design',
            description='',
            default=True,
        )
    output_biped: BoolProperty(
            name='Biped',
            description='',
            default=False,
    )
    output_crate: BoolProperty(
            name='Crate',
            description='',
            default=False,
    )
    output_creature: BoolProperty(
            name='Creature',
            description='',
            default=False,
    )
    output_device_control: BoolProperty(
            name='Device Control',
            description='',
            default=False,
    )
    output_device_machine: BoolProperty(
            name='Device Machine',
            description='',
            default=False,
    )
    output_device_terminal: BoolProperty(
            name='Device Terminal',
            description='',
            default=False,
    )
    output_effect_scenery: BoolProperty(
            name='Effect Scenery',
            description='',
            default=False,
    )
    output_equipment: BoolProperty(
            name='Equipment',
            description='',
            default=False,
    )
    output_giant: BoolProperty(
            name='Giant',
            description='',
            default=False,
    )
    output_scenery: BoolProperty(
            name='Scenery',
            description='',
            default=False,
    )
    output_vehicle: BoolProperty(
            name='Vehicle',
            description='',
            default=False,
    )
    output_weapon: BoolProperty(
            name='Weapon',
            description='',
            default=False,
    )
    import_to_game: BoolProperty(
            name='Import to Game',
            description='',
            default=False,
    )
    import_check: BoolProperty(
            name='Check',
            description='Run the import process but produce no output files',
            default=False,
    )
    import_force: BoolProperty(
            name='Force',
            description="Force all files to import even if they haven't changed",
            default=False,
    )
    import_verbose: BoolProperty(
            name='Verbose',
            description="Write additional import progress information to the console",
            default=False,
    )
    import_draft: BoolProperty(
            name='Draft',
            description="Skip generating PRT data. Faster speed, lower quality",
            default=False,
    )
    import_seam_debug: BoolProperty(
            name='Seam Debug',
            description="Write extra seam debugging information to the console",
            default=False,
    )
    import_skip_instances: BoolProperty(
            name='Skip Instances',
            description="Skip importing all instanced geometry",
            default=False,
    )
    import_decompose_instances: BoolProperty(
            name='Decompose Instances',
            description="Run convex decomposition for instanced geometry physics (very slow)",
            default=False,
    )
    import_surpress_errors: BoolProperty(
            name='Surpress Errors',
            description="Do not write errors to vrml files",
            default=False,
    )

    asset_path: StringProperty(
            name="Asset Folder Path",
            description="",
            )
    apply_unit_scale: BoolProperty(
            name="Apply Unit",
            description="",
            default=True,
            )
    apply_scale_options: EnumProperty(
            default='FBX_SCALE_UNITS',
            items=[('FBX_SCALE_UNITS', "FBX Units Scale",""),]
            )
    use_selection: BoolProperty(
            name="selection",
            description="",
            default=False,
            )

    def UpdateVisible(self, context):
        if self.export_hidden == True:
            self.use_visible = False
        else:
            self.use_visible = True

    export_hidden: BoolProperty(
            name="Hidden",
            update=UpdateVisible,
            description="Export visible objects only",
            default=True,
    )
    use_visible: BoolProperty(
            name="",
            description="",
            default=False,
            )

    def execute(self, context):

        keywords = self.as_keywords()

        from . import export_gr2, export_sidecar_xml, import_sidecar
        export_fbx_bin.save(self, context, **keywords)
        export_gr2.save(self, context, self.report, **keywords)
        export_sidecar_xml.save(self, context, self.report, **keywords)
        return import_sidecar.save(self, context, self.report, **keywords)

    def draw(self, context):
        scene = context.scene
        layout = self.layout
        layout.use_property_split = True
        box = layout.box()
        # SETTINGS #
        box.label(text="Settings")
        
        col = box.column()
        col.prop(self, "game_version", text='Game Version')
        col.prop(self, "export_method", text='Export Method')
        col.prop(self, "sidecar_type", text='Asset Type')

        sub = box.column(heading="Keep")
        sub.prop(self, "keep_fbx")
        sub.prop(self, "keep_json")
        # EXPORT CATEGORIES #
        box = layout.box()
        box.label(text="Export Categories")
        sub = box.column(heading="Export")
        sub.prop(self, "export_hidden")
        if self.sidecar_type == 'MODEL':
            sub.prop(self, "export_animations")
            sub.prop(self, "export_render")
            sub.prop(self, "export_collision")
            sub.prop(self, "export_physics")
            sub.prop(self, "export_markers")
        elif self.sidecar_type == 'SCENARIO':
            sub.prop(self, "export_structure")
            sub.prop(self, "export_structure_design")
        else:
            sub.prop(self, "export_render")

        # SIDECAR SETTINGS #
        box = layout.box()
        box.label(text="Sidecar Settings")
        col = box.column()
        col.prop(self, "export_sidecar")
        if self.sidecar_type == 'MODEL' and self.export_sidecar:
            sub = box.column(heading="Output Tags")
            if self.sidecar_type == 'MODEL':
                sub.prop(self, "output_biped")
                sub.prop(self, "output_crate")
                sub.prop(self, "output_creature")
                sub.prop(self, "output_device_control")
                sub.prop(self, "output_device_machine")
                sub.prop(self, "output_device_terminal")
                sub.prop(self, "output_effect_scenery")
                sub.prop(self, "output_equipment")
                sub.prop(self, "output_giant")
                sub.prop(self, "output_scenery")
                sub.prop(self, "output_vehicle")
                sub.prop(self, "output_weapon")
        # IMPORT SETTINGS #
        box = layout.box()
        box.label(text="Import Settings")
        col = box.column()
        col.prop(self, "import_to_game")
        if self.import_to_game:
            sub = box.column(heading="Import Flags")
            sub.prop(self, "import_check")
            sub.prop(self, "import_force")
            sub.prop(self, "import_verbose")
            sub.prop(self, "import_surpress_errors")
            if self.sidecar_type == 'SCENARIO':
                sub.prop(self, "import_seam_debug")
                sub.prop(self, "import_skip_instances")
                sub.prop(self, "import_decompose_instances")
            else:
                sub.prop(self, "import_draft")
                
def menu_func_export(self, context):
    self.layout.operator(Export_Halo_GR2.bl_idname, text="Halo Granny File (.gr2)")

classes = (
    Export_Halo_GR2,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)

def unregister():
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)

    for cls in classes:
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
