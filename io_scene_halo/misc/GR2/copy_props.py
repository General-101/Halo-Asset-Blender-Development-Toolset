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

from ...file_gr2.nwo_utils import (
    all_prefixes,
)

def CopyProps(report, template, targets):
    # Apply prefixes from template object
    template_name = template.name
    template_prefix = ''
    for prefix in all_prefixes:
        if template_name.startswith(prefix):
            template_prefix = prefix
    for ob in targets:
        if ob != template:
            target_name = ob.name
            for prefix in all_prefixes:
                target_name = target_name.replace(prefix, '')
        
            target_name = template_prefix + target_name
            ob.name = target_name

    # Apply halo properties to target objects
    template_props = template.halo_json
    target_count = 0
    for ob in targets:
        if ob != template:
            target_count += 1
            target_props = ob.halo_json

            target_props.object_type_items_all = template_props.object_type_items_all
            target_props.object_type_items_no_mesh = template_props.object_type_items_no_mesh
            target_props.Object_Type_All = template_props.Object_Type_All
            target_props.Object_Type_No_Mesh = template_props.Object_Type_No_Mesh
            target_props.bsp_name = template_props.bsp_name
            target_props.bsp_shared = template_props.bsp_shared
            target_props.ObjectMesh_Type = template_props.ObjectMesh_Type
            target_props.Mesh_Primitive_Type = template_props.Mesh_Primitive_Type
            target_props.Mesh_Tesselation_Density = template_props.Mesh_Tesselation_Density
            target_props.Mesh_Compression = template_props.Mesh_Compression
            target_props.Face_Type = template_props.Face_Type
            target_props.Face_Mode = template_props.Face_Mode
            target_props.Face_Sides = template_props.Face_Sides
            target_props.Face_Draw_Distance = template_props.Face_Draw_Distance
            target_props.Region_Name = template_props.Region_Name
            target_props.Permutation_Name = template_props.Permutation_Name
            target_props.Face_Global_Material = template_props.Face_Global_Material
            target_props.Sky_Permutation_Index = template_props.Sky_Permutation_Index
            target_props.Conveyor = template_props.Conveyor
            target_props.Ladder = template_props.Ladder
            target_props.Slip_Surface = template_props.Slip_Surface
            target_props.Decal_Offset = template_props.Decal_Offset
            target_props.Group_Transparents_By_Plane = template_props.Group_Transparents_By_Plane
            target_props.No_Shadow = template_props.No_Shadow
            target_props.Precise_Position = template_props.Precise_Position
            target_props.Boundary_Surface_Name = template_props.Boundary_Surface_Name
            target_props.Boundary_Surface_Type = template_props.Boundary_Surface_Type
            target_props.Poop_Lighting_Override = template_props.Poop_Lighting_Override
            target_props.Poop_Pathfinding_Override = template_props.Poop_Pathfinding_Override
            target_props.Poop_Imposter_Policy = template_props.Poop_Imposter_Policy
            target_props.Poop_Imposter_Transition_Distance = template_props.Poop_Imposter_Transition_Distance
            target_props.Poop_Imposter_Transition_Distance_Auto = template_props.Poop_Imposter_Transition_Distance_Auto
            target_props.Poop_Render_Only = template_props.Poop_Render_Only
            target_props.Poop_Chops_Portals = template_props.Poop_Chops_Portals
            target_props.Poop_Does_Not_Block_AOE = template_props.Poop_Does_Not_Block_AOE
            target_props.Poop_Excluded_From_Lightprobe = template_props.Poop_Excluded_From_Lightprobe
            target_props.Poop_Decal_Spacing = template_props.Poop_Decal_Spacing
            target_props.Poop_Precise_Geometry = template_props.Poop_Precise_Geometry
            target_props.Poop_Collision_Type = template_props.Poop_Collision_Type
            target_props.Portal_Type = template_props.Portal_Type
            target_props.Portal_AI_Deafening = template_props.Portal_AI_Deafening
            target_props.Portal_Blocks_Sounds = template_props.Portal_Blocks_Sounds
            target_props.Portal_Is_Door = template_props.Portal_Is_Door
            target_props.Decorator_Name = template_props.Decorator_Name
            target_props.Decorator_LOD = template_props.Decorator_LOD
            target_props.Water_Volume_Depth = template_props.Water_Volume_Depth
            target_props.Water_Volume_Flow_Direction = template_props.Water_Volume_Flow_Direction
            target_props.Water_Volume_Flow_Velocity = template_props.Water_Volume_Flow_Velocity
            target_props.Water_Volume_Fog_Color = template_props.Water_Volume_Fog_Color
            target_props.Water_Volume_Fog_Murkiness = template_props.Water_Volume_Fog_Murkiness
            target_props.Fog_Name = template_props.Fog_Name
            target_props.Fog_Appearance_Tag = template_props.Fog_Appearance_Tag
            target_props.Fog_Volume_Depth = template_props.Fog_Volume_Depth
            target_props.Lightmap_Settings_Enabled = template_props.Lightmap_Settings_Enabled
            target_props.Lightmap_Additive_Transparency = template_props.Lightmap_Additive_Transparency
            target_props.Lightmap_Ignore_Default_Resolution_Scale = template_props.Lightmap_Ignore_Default_Resolution_Scale
            target_props.Lightmap_Resolution_Scale = template_props.Lightmap_Resolution_Scale
            target_props.Lightmap_Type = template_props.Lightmap_Type
            target_props.Lightmap_Transparency_Override = template_props.Lightmap_Transparency_Override
            target_props.Lightmap_Analytical_Bounce_Modifier = template_props.Lightmap_Analytical_Bounce_Modifier
            target_props.Lightmap_General_Bounce_Modifier = template_props.Lightmap_General_Bounce_Modifier
            target_props.Lightmap_Translucency_Tint_Color = template_props.Lightmap_Translucency_Tint_Color
            target_props.Lightmap_Lighting_From_Both_Sides = template_props.Lightmap_Lighting_From_Both_Sides
            target_props.Material_Lighting_Enabled = template_props.Material_Lighting_Enabled
            target_props.Material_Lighting_Attenuation_Cutoff = template_props.Material_Lighting_Attenuation_Cutoff
            target_props.Material_Lighting_Attenuation_Falloff = template_props.Material_Lighting_Attenuation_Falloff
            target_props.Material_Lighting_Emissive_Focus = template_props.Material_Lighting_Emissive_Focus
            target_props.Material_Lighting_Emissive_Color = template_props.Material_Lighting_Emissive_Color
            target_props.Material_Lighting_Emissive_Per_Unit = template_props.Material_Lighting_Emissive_Per_Unit
            target_props.Material_Lighting_Emissive_Power = template_props.Material_Lighting_Emissive_Power
            target_props.Material_Lighting_Emissive_Quality = template_props.Material_Lighting_Emissive_Quality
            target_props.Material_Lighting_Use_Shader_Gel = template_props.Material_Lighting_Use_Shader_Gel
            target_props.Material_Lighting_Bounce_Ratio = template_props.Material_Lighting_Bounce_Ratio
            target_props.ObjectMarker_Type = template_props.ObjectMarker_Type
            target_props.Marker_Region = template_props.Marker_Region
            target_props.Marker_All_Regions = template_props.Marker_All_Regions
            target_props.Marker_Game_Instance_Tag_Name = template_props.Marker_Game_Instance_Tag_Name
            target_props.Marker_Game_Instance_Tag_Variant_Name = template_props.Marker_Game_Instance_Tag_Variant_Name
            target_props.Marker_Velocity = template_props.Marker_Velocity
            target_props.Marker_Pathfinding_Sphere_Vehicle = template_props.Marker_Pathfinding_Sphere_Vehicle
            target_props.Pathfinding_Sphere_Remains_When_Open = template_props.Pathfinding_Sphere_Remains_When_Open
            target_props.Pathfinding_Sphere_With_Sectors = template_props.Pathfinding_Sphere_With_Sectors
            target_props.Physics_Constraint_Parent = template_props.Physics_Constraint_Parent
            target_props.Physics_Constraint_Child = template_props.Physics_Constraint_Child
            target_props.Physics_Constraint_Type = template_props.Physics_Constraint_Type
            target_props.Physics_Constraint_Uses_Limits = template_props.Physics_Constraint_Uses_Limits
            target_props.Hinge_Constraint_Minimum = template_props.Hinge_Constraint_Minimum
            target_props.Hinge_Constraint_Maximum = template_props.Hinge_Constraint_Maximum
            target_props.Cone_Angle = template_props.Cone_Angle
            target_props.Plane_Constraint_Minimum = template_props.Plane_Constraint_Minimum
            target_props.Plane_Constraint_Maximum = template_props.Plane_Constraint_Maximum
            target_props.Twist_Constraint_Start = template_props.Twist_Constraint_Start
            target_props.Twist_Constraint_End = template_props.Twist_Constraint_End
            target_props.light_type_override = template_props.light_type_override
            target_props.Light_Game_Type = template_props.Light_Game_Type
            target_props.Light_Shape = template_props.Light_Shape
            target_props.Light_Near_Attenuation = template_props.Light_Near_Attenuation
            target_props.Light_Far_Attenuation = template_props.Light_Far_Attenuation
            target_props.Light_Near_Attenuation_Start = template_props.Light_Near_Attenuation_Start
            target_props.Light_Near_Attenuation_End = template_props.Light_Near_Attenuation_End
            target_props.Light_Far_Attenuation_Start = template_props.Light_Far_Attenuation_Start
            target_props.Light_Far_Attenuation_End = template_props.Light_Far_Attenuation_End
            target_props.Light_Volume_Distance = template_props.Light_Volume_Distance
            target_props.Light_Volume_Intensity = template_props.Light_Volume_Intensity
            target_props.Light_Fade_Start_Distance = template_props.Light_Fade_Start_Distance
            target_props.Light_Fade_End_Distance = template_props.Light_Fade_End_Distance
            target_props.Light_Ignore_BSP_Visibility = template_props.Light_Ignore_BSP_Visibility
            target_props.Light_Color = template_props.Light_Color
            target_props.Light_Intensity = template_props.Light_Intensity
            target_props.Light_Use_Clipping = template_props.Light_Use_Clipping
            target_props.Light_Clipping_Size_X_Pos = template_props.Light_Clipping_Size_X_Pos
            target_props.Light_Clipping_Size_Y_Pos = template_props.Light_Clipping_Size_Y_Pos
            target_props.Light_Clipping_Size_Z_Pos = template_props.Light_Clipping_Size_Z_Pos
            target_props.Light_Clipping_Size_X_Neg = template_props.Light_Clipping_Size_X_Neg
            target_props.Light_Clipping_Size_Y_Neg = template_props.Light_Clipping_Size_Y_Neg
            target_props.Light_Clipping_Size_Z_Neg = template_props.Light_Clipping_Size_Z_Neg
            target_props.Light_Hotspot_Size = template_props.Light_Hotspot_Size
            target_props.Light_Hotspot_Falloff = template_props.Light_Hotspot_Falloff
            target_props.Light_Falloff_Shape = template_props.Light_Falloff_Shape
            target_props.Light_Aspect = template_props.Light_Aspect
            target_props.Light_Frustum_Width = template_props.Light_Frustum_Width
            target_props.Light_Frustum_Height = template_props.Light_Frustum_Height
            target_props.Light_Bounce_Ratio = template_props.Light_Bounce_Ratio
            target_props.Light_Dynamic_Has_Bounce = template_props.Light_Dynamic_Has_Bounce
            target_props.Light_Screenspace_Has_Specular = template_props.Light_Screenspace_Has_Specular
            target_props.Light_Tag_Override = template_props.Light_Tag_Override
            target_props.Light_Shader_Reference = template_props.Light_Shader_Reference
            target_props.Light_Gel_Reference = template_props.Light_Gel_Reference
            target_props.Light_Lens_Flare_Reference = template_props.Light_Lens_Flare_Reference


    report({'INFO'}, f"Copied properties from {template_name} to {target_count} target objects")
    return {'FINISHED'}
