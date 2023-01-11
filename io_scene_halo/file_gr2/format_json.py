# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2022 Crisp
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

from .nwo_utils import not_bungie_game, CheckType
from .nwo_format import NWOObject, NWOFrame, NWOLight, NWOMarker, NWOMesh, NWOAnimationEvent, NWOAnimationControl, NWOAnimationCamera, NWOFramePCA, NWOMaterial

class NWOJSON(dict):
    def __init__(self, objects, sidecar_type, model_armature, world_frame, asset_name, bone_list):
        self.objects = objects
        self.sidecar_type = sidecar_type
        self.model_armature = model_armature
        self.world_frame = world_frame
        self.asset_name = asset_name
        self.bone_list = bone_list
        self.string_table = self.build_string_table()
        self.nodes_properties = self.build_nodes_properties()
        self.meshes_properties = self.build_meshes_properties()
        self.material_properties = self.build_material_properties()

        self.json_dict = {}
        self.json_dict.update({'string_table': self.string_table})
        self.json_dict.update({'nodes_properties': self.nodes_properties})
        self.json_dict.update({'meshes_properties': self.meshes_properties})
        self.json_dict.update({'material_properties': self.material_properties})

        del self.objects
        del self.sidecar_type
        del self.model_armature
        del self.world_frame
        del self.asset_name
        del self.bone_list
        del self.string_table
        del self.nodes_properties
        del self.meshes_properties
        del self.material_properties

    # STRING TABLE
    def build_string_table(self):
        global_materials = self.get_global_materials()
        regions = self.get_regions()
        table = {}
        if self.sidecar_type in ('MODEL', 'SCENARIO', 'PREFAB', 'SKY'):
            table.update({'global_materials_names': list(global_materials.keys())})
            table.update({'global_materials_values': list(global_materials.values())})
        if self.sidecar_type in ('MODEL', 'SKY'):
            table.update({'regions_names': list(regions.keys())})
            table.update({'regions_values': list(regions.values())})

        return table
        
    def get_global_materials(self):
        global_materials = {'default': '0'}
        index = 0
        for ob in self.objects:
            name = ob.nwo.Face_Global_Material
            if True and ob.nwo.Face_Global_Material not in global_materials.keys():
                index +=1
                global_materials.update({name: str(index)})

        return global_materials

    def get_regions(self):
        regions = {'default': '0'}
        index = 0
        for ob in self.objects:
            name = ob.nwo.Region_Name
            if True and ob.nwo.Region_Name not in regions.keys():
                index +=1
                regions.update({name: str(index)})

        return regions

    def build_nodes_properties(self):
        node_properties = self.bone_list
        # build frame props
        for ob in self.objects:
            match CheckType.get(ob):
                case '_connected_geometry_object_type_animation_event':
                    props = NWOAnimationEvent(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_animation_control':
                    props = NWOAnimationControl(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_animation_camera':
                    props = NWOAnimationCamera(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_light':
                    props = NWOLight(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_marker':
                    props = NWOMarker(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_frame_pca':
                    props = NWOFramePCA(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})
                case '_connected_geometry_object_type_frame':
                    props = NWOFrame(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                    node_properties.update({ob.name: props.__dict__})


        return node_properties

    def build_meshes_properties(self):
        mesh_properties = {}
        # build mesh props
        for ob in self.objects:
            if CheckType.mesh(ob):
                props = NWOMesh(ob, self.sidecar_type, self.model_armature, self.world_frame, self.asset_name)
                mesh_properties.update({ob.name: props.__dict__})

        return mesh_properties

    def build_material_properties(self):
        # first, get all materials for the selected objects
        materials = []
        for ob in self.objects:
            for slot in ob.material_slots:
                if slot.material is not None and slot.material not in materials:
                    materials.append(slot.material)

        material_properties = {}
        # build material props
        for mat in materials:
            props = NWOMaterial(mat)
            material_properties.update({mat.name: props.__dict__})

        return material_properties