bl_info = {
    'name': 'Blend2Halo2 JMS',
    'author': 'Cyboryxmen, Modified by Fulsy + MosesofEgypt" + General_101',
    'version': (0, 0, 1),
    'blender': (2, 80, 0),
    'location': 'File > Export > Halo 2 Jointed Model Skeleton (.jms)',
    'description': 'Import-Export Halo 2 Jointed Model Skeleton File (.jms)',
    'warning': '',
    'category': 'Import-Export'}

import time
import os
import bpy
import mathutils
import math
import re

from decimal import *

from bpy_extras.io_utils import ExportHelper
from bpy.props import StringProperty, BoolProperty, EnumProperty, FloatProperty, IntProperty, PointerProperty
from bpy.types import Operator, Panel, PropertyGroup

getcontext().prec = 13

#DECLARING ALL GLOBAL FUNCTIONS!
def throw_exception(failmessage, info, opinstance):
    print("Blend2Halo2 JMS Error!")
    print("Error message:%s" % failmessage)
    if failmessage == 0:
        opinstance.report({'ERROR'}, "Please link all nodes to one object!")
        print("please link all nodes to one object!")

    elif failmessage == 1:
        opinstance.report({'ERROR'}, "Frame node is missing.")

    elif failmessage == 2:
        opinstance.report({'ERROR'}, "There were no geometry to be exported. Please link all geometry to a single node!")

    elif failmessage == 3:
        print("You forgot to assign a material to geometry object:" + info)

    elif failmessage == 4:
        print("You linked object {} to more than 1 region".format(obj))

    print("")

def find_region(obj):
    found = None
    for collection in obj.users_collection:
        if found is not None:
            throw_exception(4, obj, opinstance)
        elif re.match("~", collection.name):
            found = collection.name

    return found

def find_last_parent(obj):
    testparent = obj.parent
    while testparent != None:
        obj = testparent
        testparent = obj.parent

    return obj

def find_last_node(obj):
    print(obj)
    if obj.parent.name == 'Armature':
        testparent = bpy.data.objects["Armature"].data.bones[0]
    else:
        testparent = obj.parent
    print(testparent.name[0:6])
    while (not re.match("b_", testparent.name[0:2], re.IGNORECASE) or
           re.match("bone_", testparent.name[0:5], re.IGNORECASE) or
           re.match("bip01_", testparent.name[0:6], re.IGNORECASE) or
           re.match("frame_", testparent.name[0:6], re.IGNORECASE) or           
           re.match("armature", testparent.name, re.IGNORECASE)):
        testparent = testparent.parent
    return testparent 

def find_child(node):
    while child!="found":
        child = node.child

def find_root_node(node, mainframe, nodeslist):
    testframe = find_last_parent(node)
    if testframe not in nodeslist:
        nodeslist.append(testframe)

    if mainframe is None:
        return testframe
    elif testframe != mainframe:
        return None

    return mainframe

def deselect():
    if not bpy.ops.object.select_all.poll():
        bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.primitive_cube_add(align='WORLD', enter_editmode=False, location=(0, 0, 506.061), rotation=(0, 0, 0))
    bpy.ops.object.delete(use_global = False)

def select():
    if not bpy.ops.object.select_all.poll():
        bpy.ops.object.editmode_toggle()
    bpy.ops.object.select_all(action='SELECT')

def select_all_layers():
    x = 0
    y = []
    y.append(bpy.context.view_layer.layer_collection.children)
    x+=1
    return y

def deselect_layers(y):
    x = 0
    for bool in y:
        bpy.context.view_layer.layer_collection.children
        x+=1
class JMSv2_MaterialProps(Panel):
    bl_label = "Region and Permutation"
    bl_idname = "region/permutation_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "material"
    bl_options = {"DEFAULT_CLOSED"}

    object_proprties: BoolProperty(
        name = "Region/Permutation name",
        default = True,
        description = "What is the name for your region and permutation"
        )

    def draw(self, context):
        layout = self.layout      
        layout.use_property_split = True

        box = layout.box()
        box.label(text = "Region/Permutation name") 

        flow = box.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        obj = context.object
        jmsv2_material = obj.active_material.jmsv2
        
        row = box.row()
        row.prop(jmsv2_material, "Region")
        
        row = box.row()
        row.prop(jmsv2_material, "Permutation")        

class JMSv2_ObjectProps(Panel):
    bl_label = "JMS Object Properties"
    bl_idname = "jms_object_panel"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    bl_options = {"DEFAULT_CLOSED"}

    object_proprties: BoolProperty(
        name = "Primitive Type",
        default = True,
        description = "How the object is handled on export"
        )

    def draw(self, context):
        layout = self.layout      
        layout.use_property_split = True

        box = layout.box()
        box.label(text = "Primitive Type")        

        flow = box.grid_flow(row_major=True, columns=0, even_columns=True, even_rows=False, align=False)

        obj = context.object
        jmsv2_object = obj.jmsv2   

        row = box.row()
        row.prop(jmsv2_object, "JMSv2_Object_Type")
        
class JMSv2_MaterialPropertiesGroup(PropertyGroup):
    Region : StringProperty(
        name = "Region",
        default = "Default",
        description = "Set region name."
        )

    Permutation : StringProperty(
        name = "Permutation",
        default = "Default",
        description = "Set permutation name."
        )
        
class JMSv2_ObjectPropertiesGroup(PropertyGroup):
    JMSv2_Object_Type : EnumProperty(
        name="Dropdown:",
        description="Apply Data to attribute.",
        items=[ ('SPHERE', "SPHERE", ""),
                ('BOX', "BOX", ""),
                ('CAPSULES', "CAPSULES", ""),
                ('CONVEX SHAPES', "CONVEX SHAPES", ""),
               ]
        )           
        
#MAKING IMPORT-EXPORT OPERATOR!
#This operator is the main flow control setup. It's also responsible for the file browser.
class ExportJMSv2(Operator, ExportHelper):
    """Write a JMS file"""
    bl_idname = "export_jmsv2.export"
    bl_label = "Export JMSv2"

    filename_ext = ".jms"

    filter_glob = StringProperty(
            default="*.jms",
            options={'HIDDEN'},
            )

    def execute(self, context):
        return export_jmsv2(self, self.filepath)
        
classesjmsv2 = (
    JMSv2_MaterialPropertiesGroup,
    JMSv2_MaterialProps,
    JMSv2_ObjectPropertiesGroup,
    JMSv2_ObjectProps,
    ExportJMSv2
)          

#This allows the operator to appear in the import/export menu
def menu_func_export(self, context):
    self.layout.operator(ExportJMSv2.bl_idname, text="Halo 2 Jointed Model Skeleton (.jms)")

def register():
    for clsjmsv2 in classesjmsv2:
        bpy.utils.register_class(clsjmsv2)
    bpy.types.TOPBAR_MT_file_export.append(menu_func_export)
    bpy.types.Material.jmsv2 = PointerProperty(type=JMSv2_MaterialPropertiesGroup, name="JMS Material Properties", description="JMS Material properties")
    bpy.types.Object.jmsv2 = PointerProperty(type=JMSv2_ObjectPropertiesGroup, name="JMS Object Properties", description="JMS Object properties")    

def unregister():
    for clsjmsv2 in classesjmsv2:
        bpy.utils.unregister_class(clsjmsv2)
    bpy.types.TOPBAR_MT_file_export.remove(menu_func_export)
    del bpy.types.Material.jmsv2
    del bpy.types.Object.jmsv2
    
if __name__ == "__main__":
    register()

class JmsVertex:
    node_influence_count = '0'
    node0 = '-1'
    node1 = '-1'
    node2 = '-1'
    node3 = '-1'
    node0_weight = '1.0000000000'
    node1_weight = '1.0000000000'
    node2_weight = '1.0000000000'
    node3_weight = '1.0000000000'
    pos = None
    norm = None
    uv = None

class JmsTriangle:
    v0 = 0
    v1 = 0
    v2 = 0
    region = 0
    material = 0

#Beginning of the export function
def export_jmsv2(opinstance, filepath):
    layersSelected = []
    scene = bpy.context.scene

    blenderscale = bpy.context.scene.unit_settings.scale_length
    scale = Decimal(1/blenderscale)
    objectslist = list(bpy.context.scene.objects)

    #Lists of data for JMS file
    version_number = 8200
    node_checksum = 3251

    mainframe = None
    directory = ""

    nodeslist = []
    materialslist = []
    texturedirectory = "<none>"

    markerslist = []
    geometrylist = []
    sphereslist = []
    boxeslist = []
    capsuleslist = []
    convexshapeslist = []
    mesheslist = []
    vertexgroups = []
    convexvertexgroups = []
    regionslist = ["unnamed"]

    vertices = []
    triangles = []
    polymaterials = []
    getcontext().prec = 13

    #THE SORTING OF STUFF!
    #Picks out all markers, nodes, and mesh objects in the scene, and puts them into appropriate lists.
    print("------------Script start------------")

    layersSelected = select_all_layers()

    uses_armature = False
    for obj in objectslist:
        if (obj.name[0:2].lower() == 'b_' or obj.name[0:5].lower() == "bone_" or obj.name[0:6].lower() == "bip01_" or obj.name[0:6].lower() == "frame_" or obj.name.lower() == "armature"):
            #A catch-all solution is employed here for if people want to use a simple object for a frame
            #or if they want to use an armature
            if obj.type == 'ARMATURE':
                nodeslist = list(obj.data.bones)
                uses_armature = True
                
            else:
                nodeslist.append(obj)

        elif re.match("#", obj.name):
            markerslist.append(obj)
            
        elif obj.name[0:1].lower() == '$':
            if obj.jmsv2.JMSv2_Object_Type == 'SPHERE':
                sphereslist.append(obj)
            if obj.jmsv2.JMSv2_Object_Type == 'BOX':
                boxeslist.append(obj)               
            if obj.jmsv2.JMSv2_Object_Type == 'CAPSULES':
                capsuleslist.append(obj)    
            if obj.jmsv2.JMSv2_Object_Type == 'CONVEX SHAPES':
                convexshapeslist.append(obj)                  

        elif obj.type== 'MESH':
            geometrylist.append(obj)

    #Check to see if nodes exist
    print(list(nodeslist))
    if len(nodeslist)==0:
        throw_exception(1, "lol", opinstance)
        return {'CANCELLED'}

    print("geometrylist =", len(geometrylist))

    for node in nodeslist:
        print("checking node:" + node.name + "...")
        node_root = find_root_node(node, mainframe, nodeslist)

        if mainframe is None:
            mainframe = node_root

        if mainframe != node_root:
            mainframe = None
            break

    if mainframe is None:
        throw_exception(0, "lol", opinstance)
        return {'CANCELLED'}

    print("current mainframe:" + mainframe.name)
    del nodeslist[nodeslist.index(mainframe)]
    nodeslist.insert(0, mainframe)
    print("deleting unnnessary items...")
    if mainframe in geometrylist:
        del geometrylist[geometrylist.index(mainframe)]
    elif mainframe in markerslist:
        del markerslist[markerslist.index(mainframe)]
    elif mainframe in sphereslist:
        del sphereslist[sphereslist.index(mainframe)]
    elif mainframe in boxeslist:
        del boxeslist[boxeslist.index(mainframe)]
    elif mainframe in capsuleslist:
        del capsuleslist[capsuleslist.index(mainframe)]
    elif mainframe in convexshapeslist:
        del convexshapeslist[convexshapeslist.index(mainframe)]         

    # Comb through geometry list, remove objects not linked to frame from list
    for obj in geometrylist:
#        print(obj)
        if find_last_parent(obj).name == 'Armature':
            testparent = bpy.data.objects["Armature"].data.bones[0]
        else:
            testparent = find_last_parent(obj)        
        if testparent != mainframe:
            if testparent != 'Armature':
                del geometrylist[geometrylist.index(obj)]

#    print(geometrylist)

#    for obj in markerslist:
#        testparent = find_last_parent(obj)
#        if testparent!=mainframe:
#            del markerslist[markerslist.index(obj)]

    if len(geometrylist) == 0 and len(sphereslist) == 0 and len(boxeslist) == 0 and len(capsuleslist) == 0 and len(convexshapeslist) == 0:
        throw_exception(2, "lol", opinstance)
        return {'CANCELLED'}

    print("gathering materials...")
    for obj in geometrylist:
        if len(obj.material_slots)!=0:
            for slot in obj.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(3, obj.name, opinstance)
            return {'CANCELLED'}
            
    for spheres in sphereslist:
        if len(spheres.material_slots)!=0:
            for slot in spheres.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(3, spheres.name, opinstance)
            return {'CANCELLED'}
            
    for boxes in boxeslist:
        if len(boxes.material_slots)!=0:
            for slot in boxes.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(3, boxes.name, opinstance)
            return {'CANCELLED'}        

    for capsules in capsuleslist:
        if len(capsules.material_slots)!=0:
            for slot in capsules.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(3, capsules.name, opinstance)
            return {'CANCELLED'}  

    for convexshapes in convexshapeslist:
        if len(convexshapes.material_slots)!=0:
            for slot in convexshapes.material_slots:
                if slot.material not in materialslist:
                    materialslist.append(slot.material)
        else:
            throw_exception(3, convexshapes.name, opinstance)
            return {'CANCELLED'}             
            
    print("gathering regions...")
    for collections in bpy.data.collections:
        regionslist.append(collections.name)
    try:
        regionslist[0]
    except:
        bpy.ops.group.create(name="unnamed")
        regionslist.append(bpy.data.groups["unnamed"])

    #THE REAL FUN BEGINS!
    #Prepare mesh object for exporting.
#    print("converting geometry object to mesh...")
    deselect()
    for obj in geometrylist:
        obj.select_set(state = True)
#        bpy.ops.object.duplicate(linked = False)
        mesheslist.append(bpy.context.selected_objects[0])
        deselect()

#    print("applying modifiers...")
#    for mesh in mesheslist:
#        deselect()
#        mesh.select = True
#        bpy.context.scene.objects.active = mesh
#        bpy.ops.object.convert(target='MESH', keep_original = False)

#    print("UV unwrapping wrapped objects...")
#    for mesh in mesheslist:
#        deselect()
#        mesh.select = True
#        bpy.context.scene.objects.active = mesh
#        try:
#            mesh.data.uv_layers.active.data
#        except:
#            bpy.ops.uv.smart_project(angle_limit = 66, island_margin = 0, user_area_weight = 0)

#    print("triangulating faces...")
#    for mesh in mesheslist:
#        deselect()
#        mesh.select = True
#        bpy.context.scene.objects.active = mesh
#        if not bpy.ops.mesh.quads_convert_to_tris.poll():
#            bpy.ops.object.editmode_toggle()
#        bpy.ops.mesh.select_all(action='SELECT')
#        bpy.ops.mesh.quads_convert_to_tris()
#        bpy.ops.object.editmode_toggle()

    print("gathering faces and vertices...")
    print(mesheslist)
    for mesh in mesheslist:
        c = 0 
        vertexgroups.clear()
        for groups in mesh.vertex_groups:
            vertexgroups.append(mesh.vertex_groups[c].name)
            c = c + 1     
        region_name = find_region(mesh)
        if region_name is None:
            region_name = regionslist[0]

        region = regionslist.index(region_name)
        
        if uses_armature == False:
            node_index = nodeslist.index(find_last_node(mesh))             
        else:
            node_index = 0

        matrix = mesh.matrix_world
        deselect()
        mesh.select_set(state = True)

        bpy.context.view_layer.objects.active = mesh

        uv_layer = mesh.data.uv_layers.active.data
        mesh_loops = mesh.data.loops
        mesh_verts = mesh.data.vertices

        #print('vertex groups', list(vertexgroups))
        for face in mesh.data.polygons:
            jms_triangle = JmsTriangle()
            triangles.append(jms_triangle)

            jms_triangle.v0 = len(vertices)
            jms_triangle.v1 = len(vertices) + 1
            jms_triangle.v2 = len(vertices) + 2
            jms_triangle.region = region
            jms_triangle.material = materialslist.index(mesh.data.materials[face.material_index])
            for loop_index in face.loop_indices:
                vert = mesh_verts[mesh_loops[loop_index].vertex_index]
                uv = uv_layer[loop_index].uv

                jms_vertex = JmsVertex()
                vertices.append(jms_vertex)

                pos  = matrix@vert.co
                norm = matrix@(vert.co + vert.normal) - pos

                jms_vertex.pos = pos
                jms_vertex.norm = norm
                jms_vertex.uv = uv
                if len(vert.groups) > 0:
                    #node0
                    value = len(vert.groups)
                    if value > 4:
                        value = 4
                    jms_vertex.node_influence_count = value
                    for n in range(len(vert.groups)):
                        vertex_group = vert.groups[n].group
                        object_vertex_group = vertexgroups[vertex_group]
                        armature_obj = bpy.data.objects["Armature"].data.bones[object_vertex_group]       
                        if n == 0:
                            jms_vertex.node0 = nodeslist.index(armature_obj)      
                            jms_vertex.node0_weight = '%0.10f' % vert.groups[0].weight 
                        if n == 1:
                            jms_vertex.node1 = nodeslist.index(armature_obj)      
                            jms_vertex.node1_weight = '%0.10f' % vert.groups[1].weight        
                        if n == 2:
                            jms_vertex.node2 = nodeslist.index(armature_obj)      
                            jms_vertex.node2_weight = '%0.10f' % vert.groups[2].weight  
                        if n == 3:
                            jms_vertex.node3 = nodeslist.index(armature_obj)      
                            jms_vertex.node3_weight = '%0.10f' % vert.groups[3].weight                               
                else:
                    jms_vertex.node_influence_count = '1'
                    jms_vertex.node0 = '0'
                    jms_vertex.node0_weight = '1.0000000000'

    print("preparation complete!")
    print("Here are the meshes to be exported:")
    for mesh in mesheslist:
        print(mesh.name)

    print("")
    print("cleaning up...")

    # Delete all the meshes since we modified them
    deselect()
    for mesh in mesheslist:
        mesh.select_set(state = True)
    #bpy.ops.object.delete(use_global = False)

    deselect_layers(layersSelected)

    print("\n\n")
    print("beginning JMS data export!")
    print("\n\n")

    #Actual writing to file begins here.
    with open(filepath, 'w', encoding='utf_16') as f:
        #write version
        f.write(
            ';### VERSION ###' +
            '\n8210' +
            '\n;\t<8197-8210>\n'        
            )
        
        #write nodes
        f.write(
        '\n;### NODES ###' +
        '\n%s' % len(nodeslist) +
        '\n;\t<name>' +
        '\n;\t<parent node index>' +
        '\n;\t<default rotation <i,j,k,w>>' +
        '\n;\t<default translation <x,y,z>>\n'   
        )        

        for node in nodeslist:
            print("writing node data:{}...".format(node.name))
            layer = nodeslist[0]
            if node.parent == None:
                layer = nodeslist[0]
            else:
                layer = node.parent
            child0 = -1
            if node.parent == None:
                child0 = -1
            else:
                child0 = nodeslist.index(layer)
            if uses_armature == False:
                matrix = node.matrix_world
                
                pos  = matrix@node.location
                quat = node.rotation_quaternion                
            else:              
                pos  = node.head_local
                quat = node.matrix_local.to_quaternion()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale
            
            f.write('\n;NODE %s' % (nodeslist.index(node)))
            f.write('\n%s' % node.name)
            f.write('\n%s' % (child0))
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f\n' % (pos_x, pos_y, pos_z))
            
        #write materials
        f.write(
            '\n;### MATERIALS ###' +
            '\n%s' % len(materialslist) +
            '\n;\t<name>' +
            '\n;\t<???/LOD/Permutation/Region>\n'   
            )
            
        for material in materialslist:
            Permutation = material.jmsv2.Permutation
            Region = material.jmsv2.Region
            print("writing material:{}...".format(material.name))
            f.write('\n;MATERIAL %s' % (materialslist.index(material)))
            f.write('\n%s' % material.name)
            f.write('\n%s %s\n' % (Permutation, Region))

        #write markers
        f.write(
            '\n;### MARKERS ###' +
            '\n%s' % len(markerslist) +
            '\n;\t<name>' +
            '\n;\t<node index>' +
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'         
            )      

        for marker in markerslist:
            name = marker.name.replace(' ', '')[+1:]
            fixed_name = name.split('.')[0]
            print("writing marker data:{}...".format(name))
            region = 0
            marker_parent = bpy.data.objects[marker.name].parent_bone
            if marker_parent == None:
                node = 0
            else:
                marker_node_index = bpy.data.armatures['Armature'].bones['%s' % marker_parent]
                node = nodeslist.index(marker_node_index)
                
            radius = abs(marker.dimensions[0]/2)
            pos  = marker.matrix_local.to_translation()
            quat = marker.matrix_local.to_quaternion().inverted()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            f.write('\n;MARKER %s' % (markerslist.index(marker)))
            f.write('\n%s' % fixed_name)
            f.write('\n%s' % node)
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f' % (pos_x, pos_y, pos_z))
            f.write('\n')            
            f.write('\n%0.10f' % radius)
            
        #write instance xref paths
        f.write(
            '\n;### INSTANCE XREF PATHS ###' +
            '\n0' +
            '\n;\t<path to .MAX file>' +
            '\n;\t<name>\n'        
            )

        #write instance markers
        f.write(
            '\n;### INSTANCE MARKERS ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<unique identifier>' +
            '\n;\t<path index>' +        
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>\n'    
            )     

        #write vertices               
        f.write(
            '\n;### VERTICES ###' +
            '\n%s' % len(vertices) +
            '\n;\t<position>' +
            '\n;\t<normal>' +
            '\n;\t<node influences count>' +        
            '\n;\t\t<index>' +
            '\n;\t\t<weight>' +
            '\n;\t<texture coordinate count>' +
            '\n;\t\t<texture coordinates <u,v>>\n'        
            )
        
        for jms_vertex in vertices:
            pos  = jms_vertex.pos
            norm = jms_vertex.norm
            uv   = jms_vertex.uv

            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            norm_i = Decimal(norm[0]).quantize(Decimal('1.0000000000'))
            norm_j = Decimal(norm[1]).quantize(Decimal('1.0000000000'))
            norm_k = Decimal(norm[2]).quantize(Decimal('1.0000000000'))

            tex_u = Decimal(uv[0]).quantize(Decimal('1.0000000000'))
            tex_v = Decimal(uv[1]).quantize(Decimal('1.0000000000'))
            
            vert_string =  '\n;VERTEX %s' % (vertices.index(jms_vertex))
            vert_string += '\n%0.10f\t%0.10f\t%0.10f' % (pos_x, pos_y, pos_z)
            vert_string += '\n%0.10f\t%0.10f\t%0.10f' % (norm_i, norm_j, norm_k)
            vert_string += '\n%s' % (jms_vertex.node_influence_count)
            for s in range(int(jms_vertex.node_influence_count)):
                if s == 0:
                    vert_string += '\n%s\n%s' % (jms_vertex.node0, jms_vertex.node0_weight)
                if s == 1:
                    vert_string += '\n%s\n%s' % (jms_vertex.node1, jms_vertex.node1_weight)
                if s == 2:
                    vert_string += '\n%s\n%s' % (jms_vertex.node2, jms_vertex.node2_weight)
                if s == 3:
                    vert_string += '\n%s\n%s' % (jms_vertex.node3, jms_vertex.node3_weight)                    
            vert_string += '\n%s' % (1)
            vert_string += '\n%0.10f\t%0.10f\n' % (tex_u, tex_v)
            f.write(vert_string)
                    
        #write triangles               
        f.write(
            '\n;### TRIANGLES ###' +
            '\n%s' % len(triangles) +
            '\n;\t<material index>' +        
            '\n;\t<vertex indices <v0,v1,v2>>\n'       
            )

        x = 0
        for tri in triangles:
            tri_string = '%s\n%s\t%s\t%s\n' % (
                tri.material, tri.v0, tri.v1, tri.v2)
            f.write('\n;TRIANGLE %s\n' % (triangles.index(tri)) + (tri_string))
            x += 3
            
        #write sphere               
        f.write(
            '\n;### SPHERES ###' +
            '\n%s' % len(sphereslist) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +        
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'      
            ) 
            
        for spheres in sphereslist:
            name = spheres.name.replace(' ', '')[+1:]
            print("writing spheres data:{}...".format(name))
            print('parent type', bpy.data.objects[spheres.name].parent_type)
            print('parent bone', bpy.data.objects[spheres.name].parent_bone)            
            spheres_parent_type = bpy.data.objects[spheres.name].parent_type
            spheres_parent_bone = bpy.data.objects[spheres.name].parent_bone
            sphere_materials = spheres.data.materials
            if spheres_parent_type == "BONE":              
                spheres_node_index = bpy.data.armatures['Armature'].bones['%s' % spheres_parent_bone]
                node = nodeslist.index(spheres_node_index)
            else: 
                node = -1
            if len(sphere_materials) > 0:
                sphere_material_index = materialslist.index(sphere_materials[0])
            else:
                sphere_material_index = -1              
            radius = abs(spheres.dimensions[0]/2)
            pos  = spheres.matrix_local.to_translation()
            quat = spheres.matrix_local.to_quaternion()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            f.write('\n;SPHERE %s' % (sphereslist.index(spheres)))
            f.write('\n%s' % name)
            f.write('\n%s' % node)
            f.write('\n%s' % sphere_material_index)            
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f' % (pos_x, pos_y, pos_z))          
            f.write('\n%0.10f\n' % radius)
            
        #write boxes               
        f.write(
            '\n;### BOXES ###' +
            '\n%s' % len(boxeslist) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +        
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<width (x)>' +
            '\n;\t<length (y)>' +
            '\n;\t<height (z)>\n'        
             )
             
        for boxes in boxeslist:
            name = boxes.name.replace(' ', '')[+1:]
            print("writing boxes data:{}...".format(name))
            print('parent type', bpy.data.objects[boxes.name].parent_type)
            print('parent bone', bpy.data.objects[boxes.name].parent_bone)            
            boxes_parent_type = bpy.data.objects[boxes.name].parent_type
            boxes_parent_bone = bpy.data.objects[boxes.name].parent_bone
            box_materials = boxes.data.materials
            if boxes_parent_type == "BONE":              
                boxes_node_index = bpy.data.armatures['Armature'].bones['%s' % boxes_parent_bone]
                node = nodeslist.index(boxes_node_index)
            else: 
                node = -1
            if len(box_materials) > 0:
                boxes_material_index = materialslist.index(box_materials[0])
            else:
                boxes_material_index = -1              
            dimension_x = abs(boxes.dimensions[0]/2)
            dimension_y = abs(boxes.dimensions[1]/2)           
            dimension_z = abs(boxes.dimensions[2]/2)            
            pos  = boxes.matrix_local.to_translation()
            quat = boxes.matrix_local.to_quaternion()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            f.write('\n;BOXES %s' % (boxeslist.index(boxes)))
            f.write('\n%s' % name)
            f.write('\n%s' % node)
            f.write('\n%s' % boxes_material_index)            
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f' % (pos_x, pos_y, pos_z))          
            f.write('\n%0.10f' % dimension_x)
            f.write('\n%0.10f' % dimension_y)
            f.write('\n%0.10f\n' % dimension_z)            
            
        #write capsules               
        f.write(
            '\n;### CAPSULES ###' +
            '\n%s' % len(capsuleslist) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +        
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<height>' +
            '\n;\t<radius>\n'        
             )  
             
        for capsules in capsuleslist:
            name = capsules.name.replace(' ', '')[+1:]
            print("writing capsules data:{}...".format(name))
            print('parent type', bpy.data.objects[capsules.name].parent_type)
            print('parent bone', bpy.data.objects[capsules.name].parent_bone)            
            capsules_parent_type = bpy.data.objects[capsules.name].parent_type
            capsules_parent_bone = bpy.data.objects[capsules.name].parent_bone
            capsules_materials = capsules.data.materials
            if capsules_parent_type == "BONE":              
                capsules_node_index = bpy.data.armatures['Armature'].bones['%s' % capsules_parent_bone]
                node = nodeslist.index(capsules_node_index)
            else: 
                node = -1
            if len(capsules_materials) > 0:
                capsules_material_index = materialslist.index(capsules_materials[0])
            else:
                capsules_material_index = -1              
            dimension_x = abs(capsules.dimensions[0]/2)         
            dimension_z = abs(capsules.dimensions[2]/2)            
            pos  = capsules.matrix_local.to_translation()
            quat = capsules.matrix_local.to_quaternion()

            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            f.write('\n;CAPSULES %s' % (capsuleslist.index(capsules)))
            f.write('\n%s' % name)
            f.write('\n%s' % node)
            f.write('\n%s' % capsules_material_index)            
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f' % (pos_x, pos_y, pos_z))          
            f.write('\n%0.10f' % dimension_x)
            f.write('\n%0.10f\n' % dimension_z)                  

        #write convex shapes               
        f.write(
            '\n;### CONVEX SHAPES ###' +
            '\n%s' % len(convexshapeslist) +
            '\n;\t<name>' +
            '\n;\t<parent>' +
            '\n;\t<material>' +        
            '\n;\t<rotation <i,j,k,w>>' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<vertex count>' +
            '\n;\t<...vertices>\n'        
             )
             
        for convexshapes in convexshapeslist:
            c = 0 
            for groups in convexshapes.vertex_groups:
                convexvertexgroups.append(convexshapes.vertex_groups[c].name)
                c = c + 1       
            print('convex vertex groups', convexvertexgroups)
            name = convexshapes.name.replace(' ', '')[+1:]
            print("writing convex shapes data:{}...".format(name))
            print('parent type', bpy.data.objects[convexshapes.name].parent_type)
            print('parent bone', bpy.data.objects[convexshapes.name].parent_bone)            
            convexshapes_parent_type = bpy.data.objects[convexshapes.name].parent_type
            convexshapes_parent_bone = bpy.data.objects[convexshapes.name].parent_bone
            convexshapes_materials = convexshapes.data.materials
            if len(convexshapes.data.vertices[0].groups) > 0:
                vertex_group_convex = convexshapes.data.vertices[0].groups[0].group
                convex_object_vertex_group = convexvertexgroups[vertex_group_convex]
                armature_convex_obj = bpy.data.objects["Armature"].data.bones[convex_object_vertex_group]       
                test = nodeslist.index(armature_convex_obj)  
            else:
                test = 0
            node = test
            if len(convexshapes_materials) > 0:
                convexshapes_material_index = materialslist.index(convexshapes_materials[0])
            else:
                convexshapes_material_index = -1  
                
            pos  = convexshapes.matrix_local.to_translation()
            quat = convexshapes.matrix_local.to_quaternion() @ armature_convex_obj.matrix_local.to_quaternion()
            x_test = pos[0] - armature_convex_obj.head_local[0]
            y_test = pos[1] - armature_convex_obj.head_local[1]
            z_test = pos[2] - armature_convex_obj.head_local[2]            
            quat_i = Decimal(quat[1]).quantize(Decimal('1.0000000000'))
            quat_j = Decimal(quat[2]).quantize(Decimal('1.0000000000'))
            quat_k = Decimal(quat[3]).quantize(Decimal('1.0000000000'))
            quat_w = Decimal(quat[0]).quantize(Decimal('1.0000000000'))
            pos_x = Decimal(pos[0]).quantize(Decimal('1.0000000000'))*scale
            pos_y = Decimal(pos[1]).quantize(Decimal('1.0000000000'))*scale
            pos_z = Decimal(pos[2]).quantize(Decimal('1.0000000000'))*scale

            f.write('\n;CONVEX SHAPES %s' % (convexshapeslist.index(convexshapes)))
            f.write('\n%s' % name)
            f.write('\n%s' % node)
            f.write('\n%s' % convexshapes_material_index)            
            f.write('\n%0.10f\t%0.10f\t%0.10f\t%0.10f' % (quat_i, quat_j, quat_k, quat_w))
            f.write('\n%0.10f\t%0.10f\t%0.10f' % (x_test, y_test, z_test))          
            f.write('\n%s' % len(convexshapes.data.vertices))
            for vertex in convexshapes.data.vertices:
                f.write('\n%0.10f\t%0.10f\t%0.10f' % (vertex.co[0], vertex.co[1], vertex.co[2]))   
            f.write('\n')
            convexvertexgroups.clear()

        #write rag dolls              
        f.write(
            '\n;### RAGDOLLS ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<attached index>' +
            '\n;\t<referenced index>' +        
            '\n;\t<attached transform>' +
            '\n;\t<reference transform>' +
            '\n;\t<min twist>' +
            '\n;\t<max twist>' +
            '\n;\t<min cone>' +
            '\n;\t<max cone>' +
            '\n;\t<min plane>' +
            '\n;\t<max plane>\n'               
             )  

        #write hinges              
        f.write(
            '\n;### HINGES ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<body A index>' +
            '\n;\t<body B index>' +        
            '\n;\t<body A transform>' +
            '\n;\t<body B transform>' +
            '\n;\t<is limited>' +
            '\n;\t<friction limit>' +
            '\n;\t<min angle>' +
            '\n;\t<max angle>\n'          
             )   

        #write car wheel              
        f.write(
            '\n;### CAR WHEEL ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<chassis index>' +
            '\n;\t<wheel index>' +        
            '\n;\t<chassis transform>' +
            '\n;\t<wheel transform>' +
            '\n;\t<suspension transform>' +
            '\n;\t<suspension min limit>' +
            '\n;\t<suspension max limit>' +
            '\n;\t<friction limit>' +
            '\n;\t<velocity>' +
            '\n;\t<gain>\n'           
             )   

        #write point to point            
        f.write(
            '\n;### POINT TO POINT ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<body A index>' +
            '\n;\t<body B index>' +        
            '\n;\t<body A transform>' +
            '\n;\t<body B transform>' +
            '\n;\t<constraint type>' +
            '\n;\t<x min limit>' +
            '\n;\t<x max limit>' +
            '\n;\t<y min limit>' +
            '\n;\t<y max limit>' +
            '\n;\t<z min limit>' + 
            '\n;\t<z max limit>' +
            '\n;\t<spring length>\n'            
             )     

        #write prismatic            
        f.write(
            '\n;### PRISMATIC ###' +
            '\n0' +
            '\n;\t<name>' +
            '\n;\t<body A index>' +
            '\n;\t<body B index>' +        
            '\n;\t<body A transform>' +
            '\n;\t<body B transform>' +
            '\n;\t<is limited>' +
            '\n;\t<friction limit>' +
            '\n;\t<min limit>' +
            '\n;\t<max limit>\n'          
             )           

        #write bounding sphere            
        f.write(
            '\n;### BOUNDING SPHERE ###' +
            '\n0' +
            '\n;\t<translation <x,y,z>>' +
            '\n;\t<radius>\n'       
             ) 

    print("\n\n")
    print("Export complete!")
    print("\n\n")

    return {'FINISHED'}

#memo
#   support for bones not yet implemented
#   export regions not yet implemented