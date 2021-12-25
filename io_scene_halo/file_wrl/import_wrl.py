import bpy
import bmesh

from . import tatsu
from ..global_functions import mesh_processing

# Author: Conscars <inbox@t3hz0r.com>, 2020-03-05
VERSION_STR = "1.1.0"

# What follows is an EBNF grammar for the subset of VRML 1.0 which tool ouputs.
# It's used to generate a parser which can load the files into syntax tree for
# easier reformatting into OBJ. See the tatsu syntax docs for more info:
# https://tatsu.readthedocs.io/en/stable/syntax.html
WRL_PARSER = tatsu.compile("""
    @@grammar::VRML1
    # This just cleans up some information we don't need from the AST
    @@parseinfo::False

    # WRL files consist of a list of "Separator" nodes, one for each error found
    # by Tool. This grammar already treats whitespace as a token separator, so a
    # reformatted WRL file will still parse.
    start = '#VRML V1.0 ascii' { @+:separator }* $ ;

    # Each separator can the following properties, in this order:
    separator =
        'Separator'
        '{'
            # The coordinates array contains all vertices which are referenced
            # by index later.
            [ 'Coordinate3' '{' 'point' '[' coords:points ']' '}' ]

            # The material binding tells us how material properties are used.
            # correspond to the coordinates above, or faces.
            [ 'MaterialBinding' '{' 'value' mtl_binding:binding_type '}' ]

            # The material has two sub-sections whose lengths are not guaranteed
            # to match. The diffuseColor array contains a number of float
            # triplets (RGB) equal to the number of bound elements. However, in
            # the case of PER_FACE bound materials, the transparency array has
            # a single float rather than one per diffuseColor.
            [
                'Material'
                '{'
                    'diffuseColor' '[' mtl_diffuse_colors:points ']'
                    'transparency[' mtl_transparencies:floats ']'
                '}'
            ]

            # An indexed line set contains 1 or more edges, each defined by a
            # pair of indexes into the coords array.
            [
                'IndexedLineSet'
                '{'
                    'coordIndex' '[' indexed_lines:index_groups ']'
                '}'
            ]

            # Similarly to the indexed lines, the faces are triplets of indexes.
            [
                'IndexedFaceSet'
                '{'
                    'coordIndex' '[' indexed_faces:index_groups ']'
                '}'
            ]
        '}'
        ;

    # If the binding type is PER_VERTEX, then the material properties map to the
    # coordinates array. For PER_FACE, they map to the IndexedFaceSet.
    binding_type = 'PER_VERTEX' | 'PER_FACE' ;

    # Index arrays appear "flat", but actually use -1 as a terminator marking
    # the end of spans of indexes within. There's never actually any negative
    # indexes. Also note that the indexes may sometimes be output in a single
    # line, or when there's many values they can be output over multiple lines
    # in which case they will also gain a trailing comma before the closing "]".
    index_groups = { @+:index_group ',' } [ @+:index_group ] ;
    index_group = { @+:index ',' }+ '-1' ;
    index = /\\d+/ ;

    # Within an array, points are separated by comma (optional trailing comma)
    points = { @+:point ',' } [ @+:point ] ;
    # Points/colours are float triplets separated by whitespace.
    point = x:float y:float z:float ;

    # The only places where a comma-separated list of single floats is seen is
    # the transparency material property.
    floats = { @+:float ',' } [ @+:float ] ;

    # Floats can be negative and always have a 6 digit decimal part
    float = /-?\\d+\\.\\d+/ ;
""")

WRL2_PARSER = tatsu.compile("""
    @@grammar::VRML2
    @@parseinfo::False

    start = '#VRML V2.0 utf8' { @+:shape }* $ ;

    shape =
        'Shape'
        '{'
            'geometry DEF' description:string type:geometry_type
            '{'
                [ 'colorPerVertex' color_per_vert:bool ]
                [
                    'color' 'Color'
                    '{'
                        'color'
                        '['
                            colors:points
                        ']'
                    '}'
                ]
                [
                    'coord' 'Coordinate'
                    '{'
                        'point'
                        '['
                            coords:points
                        ']'
                    '}'
                ]
                [
                    'coordIndex'
                    '['
                        indices:index_groups
                    ']'
                ]
            '}'
        '}'
        ;

    geometry_type = 'IndexedLineSet' | 'IndexedFaceSet' ;

    points = { @+:point ',' } [ @+:point ] ;
    point = x:float y:float z:float ;

    index_groups = { @+:index_group ',' } [ @+:index_group ] ;
    index_group = { @+:index [ ',' ] }+ '-1' ;
    index = /\\d+/ ;

    string = '"' @:/[^"\n]+/ '"' ;
    bool = 'FALSE' | 'TRUE' ;
    float = /-?\\d+\\.\\d+/ ;
""")

class MeshData():
    def __init__(self, face_color_data = [], face_error_data = [], line_color_data = [], line_error_data = [], face_data = [], line_data = [], vert_data = []):
        self.face_color_data = face_color_data
        self.face_error_data = face_error_data
        self.line_color_data = line_color_data
        self.line_error_data = line_error_data
        self.face_data = face_data
        self.line_data = line_data
        self.vert_data = vert_data

def parse_wrl_to_ast(wrl_content):
    '''
    Given a string of the WRL content, returns its abstract syntax tree.
    '''
    return WRL_PARSER.parse(wrl_content)

def parse_wrl2_to_ast(wrl2_content):
    '''
    Given a string of the WRL 2.0 content, returns its abstract syntax tree.
    '''
    return WRL2_PARSER.parse(wrl2_content)

def infer_error_type(binding_type, mtl_diffuse_colors):
    '''
    Infer the type of error based on color used by Tool
    '''
    # thanks to dt192 for this trick!
    color_names = {
        "1.000000,0.000000,0.000000": "red",
        "0.000000,1.000000,0.000000": "green",
        "1.000000,0.500000,0.000000": "orange",
        "0.000000,1.000000,1.000000": "cyan",
        "1.000000,1.000000,0.000000": "yellow",
        "1.000000,0.000000,1.000000": "magenta",
        "0.000000,0.000000,0.000000": "black",
        "0.000000,0.000000,1.000000": "blue",
        # unconfirmed values:
        }

    color_info = " (white)"
    if mtl_diffuse_colors:
        found_colors = set()
        for color in mtl_diffuse_colors:
            color_str = ",".join([color.x, color.y, color.z])
            color_name = color_names.get(color_str, color_str)
            found_colors.add(color_name)

        color_info = " (" + ", ".join(sorted(found_colors)) + ")"

        if binding_type == "PER_FACE":
            ### WARNING found nearly coplanar surfaces (red and green).
            if "red" in found_colors and "green" in found_colors:
                return "nearly coplanar surfaces" + color_info
            ### WARNING found #1 degenerate triangles.
            ### ERROR found z buffered triangles (red).
            if "red" in found_colors:
                return "degenerate or z-buffered triangle" + color_info
            ### WARNING: portal outside the bsp. [see magenta in error geometry]
            if "magenta" in found_colors:
                return "portal outside BSP" + color_info
        elif binding_type == "PER_VERTEX":
            ### ERROR edge #%d is open (red)
            ### ERROR couldn't update edge #%d (red)
            ### ERROR edge #%d is too short (red)
            # edge has more than four triangles (see red in error geometry)
            if "red" in found_colors:
                return "bad edge" + color_info
            ### WARNING unearthed edge (magenta boxed lines)
            ### WARNING found possible T-junction (pink).
            if "magenta" in found_colors:
                return "unearthed edge or T-junction" + color_info
        ### WARNING: a surface clipped to no leaves (see cyan in error geometry)
        if "cyan" in found_colors:
            return "surface clipped to no leaves" + color_info
        ### WARNING: portal doesn't divide any space (it may be coincident with seam sealer?). [see green in error geometry]
        if "green" in found_colors:
            return "portal does not divide space" + color_info
        ### ERROR: portal does not define two closed spaces. (see yellow in error geometry)
        if "yellow" in found_colors:
            return "portal does not define two closed spaces" + color_info
        ### WARNING: found duplicate triangle building connected geometry. YOU SHOULD FIX THIS. (see orange in error geometry)
        ### ERROR couldn't build bsp because of overlapping surfaces (orange)
        if "orange" in found_colors:
            return "duplicate triangle or overlapping surface" + color_info
        #two fog planes intersected in a cluster (see black in error geometry).
        if "black" in found_colors:
            return "two fog planes intersected in a cluster" + color_info
        #degenerate triangle [or triangle with bad uvs] (see blue in error geometry)
        if "blue" in found_colors:
            return "degenerate triangle or UVs" + color_info
    return "unknown" + color_info

def set_object_properties(context, object):
    mesh_processing.deselect_objects(context)
    mesh_processing.select_object(context, object)

    object.show_name = True
    bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

    mesh_processing.deselect_objects(context)

def get_material_name(diffuse, error_type):
    mat_name = error_type
    if error_type == "nearly coplanar surfaces (green, red)":
        if diffuse == (1.0, 0.0, 0.0, 1.0):
            mat_name = "nearly coplanar surfaces (red)"
        elif diffuse == (0.0, 1.0, 0.0, 1.0):
            mat_name = "nearly coplanar surfaces (green)"

    return mat_name

def generate_mesh_face(face_error_name, bm_mesh, bm_object, bm_error, vert_data, face, bm_face_id, face_color):
    p1 = vert_data[face[0]]
    p2 = vert_data[face[1]]
    p3 = vert_data[face[2]]
    v1 = bm_error.verts.new((p1[0], p1[1], p1[2]))
    v2 = bm_error.verts.new((p2[0], p2[1], p2[2]))
    v3 = bm_error.verts.new((p3[0], p3[1], p3[2]))
    bm_error.faces.new((v1, v2, v3))

    bm_error.faces.ensure_lookup_table()

    mat_name = get_material_name(face_color, face_error_name)
    error_mat = bpy.data.materials.get(mat_name)
    if error_mat is None:
        error_mat = bpy.data.materials.new(name=mat_name)
        error_mat.diffuse_color = face_color
        bm_object.data.materials.append(error_mat)
    else:
        if error_mat not in list(bm_object.data.materials):
            bm_object.data.materials.append(error_mat)

    bm_object_mesh_materials = list(bm_object.data.materials)
    bm_error.faces[bm_face_id].material_index = bm_object_mesh_materials.index(error_mat)

def generate_mesh_edge(face_error_name, bm_mesh, bm_object, bm_error, vert_data, edge, edge_color):
    p1 = vert_data[edge[0]]
    p2 = vert_data[edge[1]]
    v1 = bm_error.verts.new((p1[0], p1[1], p1[2]))
    v2 = bm_error.verts.new((p2[0], p2[1], p2[2]))
    bm_error.edges.new((v1, v2))

    bm_error.edges.ensure_lookup_table()

    mat_name = get_material_name(edge_color, face_error_name)
    error_mat = bpy.data.materials.get(mat_name)
    if error_mat is None:
        error_mat = bpy.data.materials.new(name=mat_name)
        error_mat.diffuse_color = edge_color
        bm_object.data.materials.append(error_mat)
    else:
        if error_mat not in  list(bm_object.data.materials):
            bm_object.data.materials.append(error_mat)

def convert_wrl2_to_blend(input_stream):
    '''
    Translates the WRL input stream to an OBJ output stream and imports into Blender.
    '''
    vert_index = 1 # Vertex indexes start at 1 in OBJ
    mesh_data = MeshData()

    for separator in parse_wrl2_to_ast(input_stream.read()):
        error_name = infer_error_type(separator.mtl_binding, separator.colors)
        # For lines and faces, convert the separator-relative indexes into
        # global OBJ-relative ones, which we add to arrays to print later:
        if separator.type == "IndexedFaceSet":
            for mat_idx, indexed_face in enumerate(separator.indices):
                vert_indices = [int(i) + vert_index for i in indexed_face]
                f_v0 = int("{0}".format(*vert_indices)) - 1
                f_v1 = int("{1}".format(*vert_indices)) - 1
                f_v2 = int("{2}".format(*vert_indices)) - 1
                mesh_data.face_data.append((f_v0, f_v1, f_v2))
                mesh_data.face_error_data.append(error_name)

                r = float("{x}".format(**separator.colors[mat_idx]))
                g = float("{y}".format(**separator.colors[mat_idx]))
                b = float("{z}".format(**separator.colors[mat_idx]))
                a = 1.0
                mesh_data.face_color_data.append((r, g, b, a))

        if separator.type == "IndexedLineSet":
            for mat_idx, indexed_line in enumerate(separator.indices):
                vert_indices = [int(i) + vert_index for i in indexed_line]
                e_v0 = int("{0}".format(*vert_indices)) - 1
                e_v1 = int("{1}".format(*vert_indices)) - 1
                mesh_data.line_data.append((e_v0, e_v1))
                mesh_data.line_error_data.append(error_name)

                r = float("{x}".format(**separator.colors[mat_idx]))
                g = float("{y}".format(**separator.colors[mat_idx]))
                b = float("{z}".format(**separator.colors[mat_idx]))
                a = 1.0
                mesh_data.line_color_data.append((r, g, b, a))

        for coord in separator.coords:
            # Put a list of all vertices at the start of the output
            x_p = float("{x}".format(**coord))
            y_p = float("{y}".format(**coord))
            z_p = float("{z}".format(**coord))
            mesh_data.vert_data.append((x_p, y_p, z_p))
            vert_index += 1

    return mesh_data

def convert_wrl_to_blend(input_stream):
    '''
    Translates the WRL input stream to an OBJ output stream and imports into Blender.
    '''
    vert_index = 1 # Vertex indexes start at 1 in OBJ
    mesh_data = MeshData()

    for separator in parse_wrl_to_ast(input_stream.read()):
        error_name = infer_error_type(separator.mtl_binding, separator.mtl_diffuse_colors)
        # For lines and faces, convert the separator-relative indexes into
        # global OBJ-relative ones, which we add to arrays to print later:
        if separator.indexed_faces:
            for mat_idx, indexed_face in enumerate(separator.indexed_faces):
                vert_indices = [int(i) + vert_index for i in indexed_face]
                f_v0 = int("{0}".format(*vert_indices)) - 1
                f_v1 = int("{1}".format(*vert_indices)) - 1
                f_v2 = int("{2}".format(*vert_indices)) - 1
                mesh_data.face_data.append((f_v0, f_v1, f_v2))
                mesh_data.face_error_data.append(error_name)

                r = float("{x}".format(**separator.mtl_diffuse_colors[mat_idx]))
                g = float("{y}".format(**separator.mtl_diffuse_colors[mat_idx]))
                b = float("{z}".format(**separator.mtl_diffuse_colors[mat_idx]))
                a = 1.0
                mesh_data.face_color_data.append((r, g, b, a))

        if separator.indexed_lines:
            for mat_idx, indexed_line in enumerate(separator.indexed_lines):
                vert_indices = [int(i) + vert_index for i in indexed_line]
                e_v0 = int("{0}".format(*vert_indices)) - 1
                e_v1 = int("{1}".format(*vert_indices)) - 1
                mesh_data.line_data.append((e_v0, e_v1))
                mesh_data.line_error_data.append(error_name)

                r = float("{x}".format(**separator.mtl_diffuse_colors[mat_idx]))
                g = float("{y}".format(**separator.mtl_diffuse_colors[mat_idx]))
                b = float("{z}".format(**separator.mtl_diffuse_colors[mat_idx]))
                a = 1.0
                mesh_data.line_color_data.append((r, g, b, a))

        for coord in separator.coords:
            # Put a list of all vertices at the start of the output
            x_p = float("{x}".format(**coord))
            y_p = float("{y}".format(**coord))
            z_p = float("{z}".format(**coord))
            mesh_data.vert_data.append((x_p, y_p, z_p))
            vert_index += 1

    return mesh_data

def generate_wrl(context, filepath, report):
    input_stream = open(filepath, "r")
    if "2.0" in input_stream.readline():
        input_stream.seek(0)
        mesh_data = convert_wrl2_to_blend(input_stream)
    else:
        input_stream.seek(0)
        mesh_data = convert_wrl_to_blend(input_stream)

    coplanar_face_id = 0
    coplanar_face_error_name = "nearly coplanar surfaces (green, red)"
    coplanar_mesh = None
    coplanar_object_mesh = None
    coplanar_bm = bmesh.new()

    degenerate_face_id = 0
    degenerate_face_error_name = "degenerate or z-buffered triangle (red)"
    degenerate_mesh = None
    degenerate_object_mesh = None
    degenerate_bm = bmesh.new()

    portal_outside_face_id = 0
    portal_outside_face_error_name = "portal outside BSP (magenta)"
    portal_outside_mesh = None
    portal_outside_object_mesh = None
    portal_outside_bm = bmesh.new()

    surface_clipped_face_id = 0
    surface_clipped_face_error_name = "surface clipped to no leaves (cyan)"
    surface_clipped_mesh = None
    surface_clipped_object_mesh = None
    surface_clipped_bm = bmesh.new()

    portal_undivide_face_id = 0
    portal_undivide_face_error_name = "portal does not divide space (green)"
    portal_undivide_mesh = None
    portal_undivide_object_mesh = None
    portal_undivide_bm = bmesh.new()

    portal_closed_face_id = 0
    portal_closed_face_error_name = "portal does not define two closed spaces (yellow)"
    portal_closed_mesh = None
    portal_closed_object_mesh = None
    portal_closed_bm = bmesh.new()

    duplicate_triangle_face_id = 0
    duplicate_triangle_face_error_name = "duplicate triangle or overlapping surface (orange)"
    duplicate_triangle_mesh = None
    duplicate_triangle_object_mesh = None
    duplicate_triangle_bm = bmesh.new()

    intersecting_fog_face_id = 0
    intersecting_fog_face_error_name = "two fog planes intersected in a cluster (black)"
    intersecting_fog_mesh = None
    intersecting_fog_object_mesh = None
    intersecting_fog_bm = bmesh.new()

    degenerate_uv_face_id = 0
    degenerate_uv_face_error_name = "degenerate triangle or UVs (blue)"
    degenerate_uv_mesh = None
    degenerate_uv_object_mesh = None
    degenerate_uv_bm = bmesh.new()

    bad_edge_error_name = "bad edge (red)"
    bad_edge_mesh = None
    bad_edge_object_mesh = None
    bad_edge_bm = bmesh.new()

    unearthed_edge_error_name = "unearthed edge or T-junction (magenta)"
    unearthed_edge_mesh = None
    unearthed_edge_object_mesh = None
    unearthed_edge_bm = bmesh.new()

    unknown_face_id = 0
    unknown_error_name = "unknown (white)"
    unknown_mesh = None
    unknown_object_mesh = None
    unknown_bm = bmesh.new()

    mesh_processing.deselect_objects(context)

    for face_idx, face in enumerate(mesh_data.face_data):
        face_color = mesh_data.face_color_data[face_idx]
        face_error = mesh_data.face_error_data[face_idx]
        if face_error == coplanar_face_error_name:
            coplanar_mesh = bpy.data.meshes.get(coplanar_face_error_name)
            coplanar_object_mesh = bpy.data.objects.get(coplanar_face_error_name)
            if coplanar_mesh is None:
                coplanar_mesh = bpy.data.meshes.new(coplanar_face_error_name)
            if coplanar_object_mesh is None:
                coplanar_object_mesh = bpy.data.objects.new(coplanar_face_error_name, coplanar_mesh)
                context.collection.objects.link(coplanar_object_mesh)

            generate_mesh_face(coplanar_face_error_name, coplanar_mesh, coplanar_object_mesh, coplanar_bm, mesh_data.vert_data, face, coplanar_face_id, face_color)
            coplanar_face_id += 1

        elif face_error == degenerate_face_error_name:
            degenerate_mesh = bpy.data.meshes.get(degenerate_face_error_name)
            degenerate_object_mesh = bpy.data.objects.get(degenerate_face_error_name)
            if degenerate_mesh is None:
                degenerate_mesh = bpy.data.meshes.new(degenerate_face_error_name)
            if degenerate_object_mesh is None:
                degenerate_object_mesh = bpy.data.objects.new(degenerate_face_error_name, degenerate_mesh)
                context.collection.objects.link(degenerate_object_mesh)

            generate_mesh_face(degenerate_face_error_name, degenerate_mesh, degenerate_object_mesh, degenerate_bm, mesh_data.vert_data, face, degenerate_face_id, face_color)
            degenerate_face_id += 1

        elif face_error == portal_outside_face_error_name:
            portal_outside_mesh = bpy.data.meshes.get(portal_outside_face_error_name)
            portal_outside_object_mesh = bpy.data.objects.get(portal_outside_face_error_name)
            if portal_outside_mesh is None:
                portal_outside_mesh = bpy.data.meshes.new(portal_outside_face_error_name)
            if portal_outside_object_mesh is None:
                portal_outside_object_mesh = bpy.data.objects.new(portal_outside_face_error_name, portal_outside_mesh)
                context.collection.objects.link(portal_outside_object_mesh)

            generate_mesh_face(portal_outside_face_error_name, portal_outside_mesh, portal_outside_object_mesh, portal_outside_bm, mesh_data.vert_data, face, portal_outside_face_id, face_color)
            portal_outside_face_id += 1

        elif face_error == surface_clipped_face_error_name:
            surface_clipped_mesh = bpy.data.meshes.get(surface_clipped_face_error_name)
            surface_clipped_object_mesh = bpy.data.objects.get(surface_clipped_face_error_name)
            if surface_clipped_mesh is None:
                surface_clipped_mesh = bpy.data.meshes.new(surface_clipped_face_error_name)
            if surface_clipped_object_mesh is None:
                surface_clipped_object_mesh = bpy.data.objects.new(surface_clipped_face_error_name, surface_clipped_mesh)
                context.collection.objects.link(surface_clipped_object_mesh)

            generate_mesh_face(surface_clipped_face_error_name, surface_clipped_mesh, surface_clipped_object_mesh, surface_clipped_bm, mesh_data.vert_data, face, surface_clipped_face_id, face_color)
            surface_clipped_face_id += 1

        elif face_error == portal_undivide_face_error_name:
            portal_undivide_mesh = bpy.data.meshes.get(portal_undivide_face_error_name)
            portal_undivide_object_mesh = bpy.data.objects.get(portal_undivide_face_error_name)
            if portal_undivide_mesh is None:
                portal_undivide_mesh = bpy.data.meshes.new(portal_undivide_face_error_name)
            if portal_undivide_object_mesh is None:
                portal_undivide_object_mesh = bpy.data.objects.new(portal_undivide_face_error_name, portal_undivide_mesh)
                context.collection.objects.link(portal_undivide_object_mesh)

            generate_mesh_face(portal_undivide_face_error_name, portal_undivide_mesh, portal_undivide_object_mesh, portal_undivide_bm, mesh_data.vert_data, face, portal_undivide_face_id, face_color)
            portal_undivide_face_id += 1

        elif face_error == portal_closed_face_error_name:
            portal_closed_mesh = bpy.data.meshes.get(portal_closed_face_error_name)
            portal_closed_object_mesh = bpy.data.objects.get(portal_closed_face_error_name)
            if portal_closed_mesh is None:
                portal_closed_mesh = bpy.data.meshes.new(portal_closed_face_error_name)
            if portal_closed_object_mesh is None:
                portal_closed_object_mesh = bpy.data.objects.new(portal_closed_face_error_name, portal_closed_mesh)
                context.collection.objects.link(portal_closed_object_mesh)

            generate_mesh_face(portal_closed_face_error_name, portal_closed_mesh, portal_closed_object_mesh, portal_closed_bm, mesh_data.vert_data, face, portal_closed_face_id, face_color)
            portal_closed_face_id += 1

        elif face_error == duplicate_triangle_face_error_name:
            duplicate_triangle_mesh = bpy.data.meshes.get(duplicate_triangle_face_error_name)
            duplicate_triangle_object_mesh = bpy.data.objects.get(duplicate_triangle_face_error_name)
            if duplicate_triangle_mesh is None:
                duplicate_triangle_mesh = bpy.data.meshes.new(duplicate_triangle_face_error_name)
            if duplicate_triangle_object_mesh is None:
                duplicate_triangle_object_mesh = bpy.data.objects.new(duplicate_triangle_face_error_name, duplicate_triangle_mesh)
                context.collection.objects.link(duplicate_triangle_object_mesh)

            generate_mesh_face(duplicate_triangle_face_error_name, duplicate_triangle_mesh, duplicate_triangle_object_mesh, duplicate_triangle_bm, mesh_data.vert_data, face, duplicate_triangle_face_id, face_color)
            duplicate_triangle_face_id += 1

        elif face_error == intersecting_fog_face_error_name:
            intersecting_fog_mesh = bpy.data.meshes.get(intersecting_fog_face_error_name)
            intersecting_fog_object_mesh = bpy.data.objects.get(intersecting_fog_face_error_name)
            if intersecting_fog_mesh is None:
                intersecting_fog_mesh = bpy.data.meshes.new(intersecting_fog_face_error_name)
            if intersecting_fog_object_mesh is None:
                intersecting_fog_object_mesh = bpy.data.objects.new(intersecting_fog_face_error_name, intersecting_fog_mesh)
                context.collection.objects.link(intersecting_fog_object_mesh)

            generate_mesh_face(intersecting_fog_face_error_name, intersecting_fog_mesh, intersecting_fog_object_mesh, intersecting_fog_bm, mesh_data.vert_data, face, intersecting_fog_face_id, face_color)
            intersecting_fog_face_id += 1

        elif face_error == degenerate_uv_face_error_name:
            degenerate_uv_mesh = bpy.data.meshes.get(degenerate_uv_face_error_name)
            degenerate_uv_object_mesh = bpy.data.objects.get(degenerate_uv_face_error_name)
            if degenerate_uv_mesh is None:
                degenerate_uv_mesh = bpy.data.meshes.new(degenerate_uv_face_error_name)
            if degenerate_uv_object_mesh is None:
                degenerate_uv_object_mesh = bpy.data.objects.new(degenerate_uv_face_error_name, degenerate_uv_mesh)
                context.collection.objects.link(degenerate_uv_object_mesh)

            generate_mesh_face(degenerate_uv_face_error_name, degenerate_uv_mesh, degenerate_uv_object_mesh, degenerate_uv_bm, mesh_data.vert_data, face, degenerate_uv_face_id, face_color)
            degenerate_uv_face_id += 1

        else:
            unknown_mesh = bpy.data.meshes.get(unknown_error_name)
            unknown_object_mesh = bpy.data.objects.get(unknown_error_name)
            if unknown_mesh is None:
                unknown_mesh = bpy.data.meshes.new(unknown_error_name)
            if unknown_object_mesh is None:
                unknown_object_mesh = bpy.data.objects.new(unknown_error_name, unknown_mesh)
                context.collection.objects.link(unknown_object_mesh)

            generate_mesh_face(unknown_error_name, unknown_mesh, unknown_object_mesh, unknown_bm, mesh_data.vert_data, face, unknown_face_id, face_color)
            unknown_face_id += 1

    for edge_idx, edge in enumerate(mesh_data.line_data):
        edge_color = mesh_data.line_color_data[edge_idx]
        edge_error = mesh_data.line_error_data[edge_idx]
        if edge_error == bad_edge_error_name:
            bad_edge_mesh = bpy.data.meshes.get(bad_edge_error_name)
            bad_edge_object_mesh = bpy.data.objects.get(bad_edge_error_name)
            if bad_edge_mesh is None:
                bad_edge_mesh = bpy.data.meshes.new(bad_edge_error_name)
            if bad_edge_object_mesh is None:
                bad_edge_object_mesh = bpy.data.objects.new(bad_edge_error_name, bad_edge_mesh)
                context.collection.objects.link(bad_edge_object_mesh)

            generate_mesh_edge(bad_edge_error_name, bad_edge_mesh, bad_edge_object_mesh, bad_edge_bm, mesh_data.vert_data, edge, edge_color)

        elif edge_error == unearthed_edge_error_name:
            unearthed_edge_mesh = bpy.data.meshes.get(unearthed_edge_error_name)
            unearthed_edge_object_mesh = bpy.data.objects.get(unearthed_edge_error_name)
            if unearthed_edge_mesh is None:
                unearthed_edge_mesh = bpy.data.meshes.new(unearthed_edge_error_name)
            if unearthed_edge_object_mesh is None:
                unearthed_edge_object_mesh = bpy.data.objects.new(unearthed_edge_error_name, unearthed_edge_mesh)
                context.collection.objects.link(unearthed_edge_object_mesh)

            generate_mesh_edge(unearthed_edge_error_name, unearthed_edge_mesh, unearthed_edge_object_mesh, unearthed_edge_bm, mesh_data.vert_data, edge, edge_color)

        else:
            unknown_mesh = bpy.data.meshes.get(unknown_error_name)
            unknown_object_mesh = bpy.data.objects.get(unknown_error_name)
            if unknown_mesh is None:
                unknown_mesh = bpy.data.meshes.new(unknown_error_name)
            if unknown_object_mesh is None:
                unknown_object_mesh = bpy.data.objects.new(unknown_error_name, unknown_mesh)
                context.collection.objects.link(unknown_object_mesh)

            generate_mesh_edge(unknown_error_name, unknown_mesh, unknown_object_mesh, unknown_bm, mesh_data.vert_data, edge, edge_color)

    if coplanar_object_mesh:
        coplanar_bm.to_mesh(coplanar_mesh)
        set_object_properties(context, coplanar_object_mesh)

    coplanar_bm.free()

    if degenerate_object_mesh:
        degenerate_bm.to_mesh(degenerate_mesh)
        set_object_properties(context, degenerate_object_mesh)

    degenerate_bm.free()

    if portal_outside_object_mesh:
        portal_outside_bm.to_mesh(portal_outside_mesh)
        set_object_properties(context, portal_outside_object_mesh)

    portal_outside_bm.free()

    if bad_edge_object_mesh:
        bad_edge_bm.to_mesh(bad_edge_mesh)
        set_object_properties(context, bad_edge_object_mesh)

    bad_edge_bm.free()

    if unearthed_edge_object_mesh:
        unearthed_edge_bm.to_mesh(unearthed_edge_mesh)
        set_object_properties(context, unearthed_edge_object_mesh)

    unearthed_edge_bm.free()

    if surface_clipped_object_mesh:
        surface_clipped_bm.to_mesh(surface_clipped_mesh)
        set_object_properties(context, surface_clipped_object_mesh)

    surface_clipped_bm.free()

    if portal_undivide_object_mesh:
        portal_undivide_bm.to_mesh(portal_undivide_mesh)
        set_object_properties(context, portal_undivide_object_mesh)

    portal_undivide_bm.free()

    if portal_closed_object_mesh:
        portal_closed_bm.to_mesh(portal_closed_mesh)
        set_object_properties(context, portal_closed_object_mesh)

    portal_closed_bm.free()

    if duplicate_triangle_object_mesh:
        duplicate_triangle_bm.to_mesh(duplicate_triangle_mesh)
        set_object_properties(context, duplicate_triangle_object_mesh)

    duplicate_triangle_bm.free()

    if intersecting_fog_object_mesh:
        intersecting_fog_bm.to_mesh(intersecting_fog_mesh)
        set_object_properties(context, intersecting_fog_object_mesh)

    intersecting_fog_bm.free()

    if degenerate_uv_object_mesh:
        degenerate_uv_bm.to_mesh(degenerate_uv_mesh)
        set_object_properties(context, degenerate_uv_object_mesh)

    degenerate_uv_bm.free()

    if unknown_object_mesh:
        unknown_bm.to_mesh(unknown_mesh)
        set_object_properties(context, unknown_object_mesh)

    unknown_bm.free()

    return {'FINISHED'}

if __name__== "__main__":
    bpy.ops.import_scene.wrl()
