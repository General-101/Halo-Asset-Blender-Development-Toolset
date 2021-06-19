import bpy
import bmesh

from . import tatsu

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

def parse_wrl_to_ast(wrl_content):
    '''
    Given a string of the WRL content, returns its abstract syntax tree.
    '''
    return WRL_PARSER.parse(wrl_content)

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

def convert_wrl_to_blend(context, filepath, report):
    '''
    Translates the WRL input stream to an OBJ output stream and imports into Blender.
    '''
    input_stream = open(filepath, "r")

    vert_index = 1 # Vertex indexes start at 1 in OBJ
    face_color_data = []
    face_error_data = []
    line_color_data = []
    line_error_data = []
    face_data = []
    line_data = []
    vert_data = []

    collection = bpy.context.collection

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
                face_data.append((f_v0, f_v1, f_v2))
                face_error_data.append(error_name)

                r = float("{x}".format(**separator.mtl_diffuse_colors[mat_idx]))
                g = float("{y}".format(**separator.mtl_diffuse_colors[mat_idx]))
                b = float("{z}".format(**separator.mtl_diffuse_colors[mat_idx]))
                a = 1.0
                face_color_data.append((r, g, b, a))

        if separator.indexed_lines:
            for mat_idx, indexed_line in enumerate(separator.indexed_lines):
                vert_indices = [int(i) + vert_index for i in indexed_line]
                e_v0 = int("{0}".format(*vert_indices)) - 1
                e_v1 = int("{1}".format(*vert_indices)) - 1
                line_data.append((e_v0, e_v1))
                line_error_data.append(error_name)

                r = float("{x}".format(**separator.mtl_diffuse_colors[mat_idx]))
                g = float("{y}".format(**separator.mtl_diffuse_colors[mat_idx]))
                b = float("{z}".format(**separator.mtl_diffuse_colors[mat_idx]))
                a = 1.0
                line_color_data.append((r, g, b, a))

        for coord in separator.coords:
            # Put a list of all vertices at the start of the output
            x_p = float("{x}".format(**coord))
            y_p = float("{y}".format(**coord))
            z_p = float("{z}".format(**coord))
            vert_data.append((x_p, y_p, z_p))
            vert_index += 1

    coplanar_face_id = 0
    coplanar_mesh = bpy.data.meshes.get("nearly coplanar surfaces (green, red)")
    coplanar_object_mesh = bpy.data.objects.get("nearly coplanar surfaces (green, red)")
    coplanar_bm = bmesh.new()

    degenerate_face_id = 0
    degenerate_mesh = bpy.data.meshes.get("degenerate or z-buffered triangle (red)")
    degenerate_object_mesh = bpy.data.objects.get("degenerate or z-buffered triangle (red)")
    degenerate_bm = bmesh.new()

    portal_outside_face_id = 0
    portal_outside_mesh = bpy.data.meshes.get("portal outside BSP (magenta)")
    portal_outside_object_mesh = bpy.data.objects.get("portal outside BSP (magenta)")
    portal_outside_bm = bmesh.new()

    bad_edge_edge_id = 0
    bad_edge_mesh = bpy.data.meshes.get("bad edge (red)")
    bad_edge_object_mesh = bpy.data.objects.get("bad edge (red)")
    bad_edge_bm = bmesh.new()

    unearthed_edge_id = 0
    unearthed_edge_mesh = bpy.data.meshes.get("unearthed edge or T-junction (magenta)")
    unearthed_edge_object_mesh = bpy.data.objects.get("unearthed edge or T-junction (magenta)")
    unearthed_edge_bm = bmesh.new()

    surface_clipped_face_id = 0
    surface_clipped_mesh = bpy.data.meshes.get("surface clipped to no leaves (cyan)")
    surface_clipped_object_mesh = bpy.data.objects.get("surface clipped to no leaves (cyan)")
    surface_clipped_bm = bmesh.new()

    portal_undivide_face_id = 0
    portal_undivide_mesh = bpy.data.meshes.get("portal does not divide space (green)")
    portal_undivide_object_mesh = bpy.data.objects.get("portal does not divide space (green)")
    portal_undivide_bm = bmesh.new()

    portal_closed_face_id = 0
    portal_closed_mesh = bpy.data.meshes.get("portal does not define two closed spaces (yellow)")
    portal_closed_object_mesh = bpy.data.objects.get("portal does not define two closed spaces (yellow)")
    portal_closed_bm = bmesh.new()

    duplicate_triangle_face_id = 0
    duplicate_triangle_mesh = bpy.data.meshes.get("duplicate triangle or overlapping surface (orange)")
    duplicate_triangle_object_mesh = bpy.data.objects.get("duplicate triangle or overlapping surface (orange)")
    duplicate_triangle_bm = bmesh.new()

    intersecting_fog_face_id = 0
    intersecting_fog_mesh = bpy.data.meshes.get("two fog planes intersected in a cluster (black)")
    intersecting_fog_object_mesh = bpy.data.objects.get("two fog planes intersected in a cluster (black)")
    intersecting_fog_bm = bmesh.new()

    degenerate_uv_face_id = 0
    degenerate_uv_mesh = bpy.data.meshes.get("degenerate triangle or UVs (blue)")
    degenerate_uv_object_mesh = bpy.data.objects.get("degenerate triangle or UVs (blue)")
    degenerate_uv_bm = bmesh.new()

    unknown_face_id = 0
    unknown_mesh = bpy.data.meshes.get("unknown (white)")
    unknown_object_mesh = bpy.data.objects.get("unknown (white)")
    unknown_bm = bmesh.new()

    if bpy.context.view_layer.objects.active:
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

    for face_idx, face in enumerate(face_data):
        face_color = face_color_data[face_idx]
        face_error = face_error_data[face_idx]
        if face_error == "nearly coplanar surfaces (green, red)":
            face_error_name_0 = "nearly coplanar surfaces (green, red)"
            face_error_name_1 = "nearly coplanar surfaces (red)"
            face_error_name_2 = "nearly coplanar surfaces (green)"
            if coplanar_mesh is None:
                coplanar_mesh = bpy.data.meshes.new(face_error_name_0)
            if coplanar_object_mesh is None:
                coplanar_object_mesh = bpy.data.objects.new(face_error_name_0, coplanar_mesh)
                collection.objects.link(coplanar_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = coplanar_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = coplanar_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = coplanar_bm.verts.new((p3[0], p3[1], p3[2]))
            coplanar_bm.faces.new((v1, v2, v3))

            coplanar_bm.faces.ensure_lookup_table()

            mat_red = bpy.data.materials.get(face_error_name_1)
            mat_green = bpy.data.materials.get(face_error_name_2)
            if mat_red is None:
                mat_red = bpy.data.materials.new(name=face_error_name_1)
                mat_red.diffuse_color = (1.0, 0.0, 0.0, 1.0)
                coplanar_object_mesh.data.materials.append(mat_red)
            else:
                if mat_red not in  list(coplanar_object_mesh.data.materials):
                    coplanar_object_mesh.data.materials.append(mat_red)
            if mat_green is None:
                mat_green = bpy.data.materials.new(name=face_error_name_2)
                mat_green.diffuse_color = (0.0, 1.0, 0.0, 1.0)
                coplanar_object_mesh.data.materials.append(mat_green)
            else:
                if mat_green not in  list(coplanar_object_mesh.data.materials):
                    coplanar_object_mesh.data.materials.append(mat_green)

            if face_color == (1.0, 0.0, 0.0, 1.0):
                mat = mat_red
            elif face_color == (0.0, 1.0, 0.0, 1.0):
                mat = mat_green

            coplanar_object_mesh_materials = list(coplanar_object_mesh.data.materials)
            coplanar_bm.faces[coplanar_face_id].material_index = coplanar_object_mesh_materials.index(mat)
            coplanar_face_id += 1

        elif face_error == "degenerate or z-buffered triangle (red)":
            face_error_name_0 = "degenerate or z-buffered triangle (red)"
            if degenerate_mesh is None:
                degenerate_mesh = bpy.data.meshes.new(face_error_name_0)
            if degenerate_object_mesh is None:
                degenerate_object_mesh = bpy.data.objects.new(face_error_name_0, degenerate_mesh)
                collection.objects.link(degenerate_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = degenerate_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = degenerate_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = degenerate_bm.verts.new((p3[0], p3[1], p3[2]))
            degenerate_bm.faces.new((v1, v2, v3))

            degenerate_bm.faces.ensure_lookup_table()

            mat_red = bpy.data.materials.get(face_error_name_0)
            if mat_red is None:
                mat_red = bpy.data.materials.new(name=face_error_name_0)
                mat_red.diffuse_color = (1.0, 0.0, 0.0, 1.0)
                degenerate_object_mesh.data.materials.append(mat_red)
            else:
                if mat_red not in  list(degenerate_object_mesh.data.materials):
                    degenerate_object_mesh.data.materials.append(mat_red)

            if face_color == (1.0, 0.0, 0.0, 1.0):
                mat = mat_red

            degenerate_object_mesh_materials = list(degenerate_object_mesh.data.materials)
            degenerate_bm.faces[degenerate_face_id].material_index = degenerate_object_mesh_materials.index(mat)
            degenerate_face_id += 1

        elif face_error == "portal outside BSP (magenta)":
            face_error_name_0 = "portal outside BSP (magenta)"
            if portal_outside_mesh is None:
                portal_outside_mesh = bpy.data.meshes.new(face_error_name_0)
            if portal_outside_object_mesh is None:
                portal_outside_object_mesh = bpy.data.objects.new(face_error_name_0, portal_outside_mesh)
                collection.objects.link(portal_outside_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = portal_outside_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = portal_outside_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = portal_outside_bm.verts.new((p3[0], p3[1], p3[2]))
            portal_outside_bm.faces.new((v1, v2, v3))

            portal_outside_bm.faces.ensure_lookup_table()

            mat_magenta = bpy.data.materials.get(face_error_name_0)
            if mat_magenta is None:
                mat_magenta = bpy.data.materials.new(name=face_error_name_0)
                mat_magenta.diffuse_color = (1.0, 0.0, 1.0, 1.0)
                portal_outside_object_mesh.data.materials.append(mat_magenta)
            else:
                if mat_magenta not in  list(portal_outside_object_mesh.data.materials):
                    portal_outside_object_mesh.data.materials.append(mat_magenta)

            if face_color == (1.0, 0.0, 1.0, 1.0):
                mat = mat_magenta

            portal_outside_object_mesh_materials = list(portal_outside_object_mesh.data.materials)
            portal_outside_bm.faces[portal_outside_face_id].material_index = portal_outside_object_mesh_materials.index(mat)
            portal_outside_face_id += 1

        elif face_error == "surface clipped to no leaves (cyan)":
            face_error_name_0 = "surface clipped to no leaves (cyan)"
            if surface_clipped_mesh is None:
                surface_clipped_mesh = bpy.data.meshes.new(face_error_name_0)
            if surface_clipped_object_mesh is None:
                surface_clipped_object_mesh = bpy.data.objects.new(face_error_name_0, surface_clipped_mesh)
                collection.objects.link(surface_clipped_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = surface_clipped_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = surface_clipped_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = surface_clipped_bm.verts.new((p3[0], p3[1], p3[2]))
            surface_clipped_bm.faces.new((v1, v2, v3))

            surface_clipped_bm.faces.ensure_lookup_table()

            mat_cyan = bpy.data.materials.get(face_error_name_0)
            if mat_cyan is None:
                mat_cyan = bpy.data.materials.new(name=face_error_name_0)
                mat_cyan.diffuse_color = (0.0, 1.0, 1.0, 1.0)
                surface_clipped_object_mesh.data.materials.append(mat_cyan)
            else:
                if mat_cyan not in  list(surface_clipped_object_mesh.data.materials):
                    surface_clipped_object_mesh.data.materials.append(mat_cyan)

            if face_color == (0.0, 1.0, 1.0, 1.0):
                mat = mat_cyan

            surface_clipped_object_mesh_materials = list(surface_clipped_object_mesh.data.materials)
            surface_clipped_bm.faces[surface_clipped_face_id].material_index = surface_clipped_object_mesh_materials.index(mat)
            surface_clipped_face_id += 1

        elif face_error == "portal does not divide space (green)":
            face_error_name_0 = "portal does not divide space (green)"
            if portal_undivide_mesh is None:
                portal_undivide_mesh = bpy.data.meshes.new(face_error_name_0)
            if portal_undivide_object_mesh is None:
                portal_undivide_object_mesh = bpy.data.objects.new(face_error_name_0, portal_undivide_mesh)
                collection.objects.link(portal_undivide_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = portal_undivide_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = portal_undivide_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = portal_undivide_bm.verts.new((p3[0], p3[1], p3[2]))
            portal_undivide_bm.faces.new((v1, v2, v3))

            portal_undivide_bm.faces.ensure_lookup_table()

            mat_green = bpy.data.materials.get(face_error_name_0)
            if mat_green is None:
                mat_green = bpy.data.materials.new(name=face_error_name_0)
                mat_green.diffuse_color = (0.0, 1.0, 0.0, 1.0)
                portal_undivide_object_mesh.data.materials.append(mat_green)
            else:
                if mat_green not in  list(portal_undivide_object_mesh.data.materials):
                    portal_undivide_object_mesh.data.materials.append(mat_green)

            if face_color == (0.0, 1.0, 0.0, 1.0):
                mat = mat_green

            portal_undivide_object_mesh_materials = list(portal_undivide_object_mesh.data.materials)
            portal_undivide_bm.faces[portal_undivide_face_id].material_index = portal_undivide_object_mesh_materials.index(mat)
            portal_undivide_face_id += 1

        elif face_error == "portal does not define two closed spaces (yellow)":
            face_error_name_0 = "portal does not define two closed spaces (yellow)"
            if portal_closed_mesh is None:
                portal_closed_mesh = bpy.data.meshes.new(face_error_name_0)
            if portal_closed_object_mesh is None:
                portal_closed_object_mesh = bpy.data.objects.new(face_error_name_0, portal_closed_mesh)
                collection.objects.link(portal_closed_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = portal_closed_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = portal_closed_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = portal_closed_bm.verts.new((p3[0], p3[1], p3[2]))
            portal_closed_bm.faces.new((v1, v2, v3))

            portal_closed_bm.faces.ensure_lookup_table()

            mat_yellow = bpy.data.materials.get(face_error_name_0)
            if mat_yellow is None:
                mat_yellow = bpy.data.materials.new(name=face_error_name_0)
                mat_yellow.diffuse_color = (1.0, 1.0, 0.0, 1.0)
                portal_closed_object_mesh.data.materials.append(mat_yellow)
            else:
                if mat_yellow not in  list(portal_closed_object_mesh.data.materials):
                    portal_closed_object_mesh.data.materials.append(mat_yellow)

            if face_color == (1.0, 1.0, 0.0, 1.0):
                mat = mat_yellow

            portal_closed_object_mesh_materials = list(portal_closed_object_mesh.data.materials)
            portal_closed_bm.faces[portal_closed_face_id].material_index = portal_closed_object_mesh_materials.index(mat)
            portal_closed_face_id += 1

        elif face_error == "duplicate triangle or overlapping surface (orange)":
            face_error_name_0 = "duplicate triangle or overlapping surface (orange)"
            if duplicate_triangle_mesh is None:
                duplicate_triangle_mesh = bpy.data.meshes.new(face_error_name_0)
            if duplicate_triangle_object_mesh is None:
                duplicate_triangle_object_mesh = bpy.data.objects.new(face_error_name_0, duplicate_triangle_mesh)
                collection.objects.link(duplicate_triangle_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = duplicate_triangle_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = duplicate_triangle_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = duplicate_triangle_bm.verts.new((p3[0], p3[1], p3[2]))
            duplicate_triangle_bm.faces.new((v1, v2, v3))

            duplicate_triangle_bm.faces.ensure_lookup_table()

            mat_orange = bpy.data.materials.get(face_error_name_0)
            if mat_orange is None:
                mat_orange = bpy.data.materials.new(name=face_error_name_0)
                mat_orange.diffuse_color = (1.0, 0.5, 0.0, 1.0)
                duplicate_triangle_object_mesh.data.materials.append(mat_orange)
            else:
                if mat_orange not in  list(duplicate_triangle_object_mesh.data.materials):
                    duplicate_triangle_object_mesh.data.materials.append(mat_orange)

            if face_color == (1.0, 0.5, 0.0, 1.0):
                mat = mat_orange

            duplicate_triangle_object_mesh_materials = list(duplicate_triangle_object_mesh.data.materials)
            duplicate_triangle_bm.faces[duplicate_triangle_face_id].material_index = duplicate_triangle_object_mesh_materials.index(mat)
            duplicate_triangle_face_id += 1

        elif face_error == "two fog planes intersected in a cluster (black)":
            face_error_name_0 = "two fog planes intersected in a cluster (black)"
            if intersecting_fog_mesh is None:
                intersecting_fog_mesh = bpy.data.meshes.new(face_error_name_0)
            if intersecting_fog_object_mesh is None:
                intersecting_fog_object_mesh = bpy.data.objects.new(face_error_name_0, intersecting_fog_mesh)
                collection.objects.link(intersecting_fog_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = intersecting_fog_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = intersecting_fog_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = intersecting_fog_bm.verts.new((p3[0], p3[1], p3[2]))
            intersecting_fog_bm.faces.new((v1, v2, v3))

            intersecting_fog_bm.faces.ensure_lookup_table()

            mat_black = bpy.data.materials.get(face_error_name_0)
            if mat_black is None:
                mat_black = bpy.data.materials.new(name=face_error_name_0)
                mat_black.diffuse_color = (0.0, 0.0, 0.0, 1.0)
                intersecting_fog_object_mesh.data.materials.append(mat_black)
            else:
                if mat_black not in  list(intersecting_fog_object_mesh.data.materials):
                    intersecting_fog_object_mesh.data.materials.append(mat_black)

            if face_color == (0.0, 0.0, 0.0, 1.0):
                mat = mat_black

            intersecting_fog_object_mesh_materials = list(intersecting_fog_object_mesh.data.materials)
            intersecting_fog_bm.faces[intersecting_fog_face_id].material_index = intersecting_fog_object_mesh_materials.index(mat)
            intersecting_fog_face_id += 1

        elif face_error == "degenerate triangle or UVs (blue)":
            face_error_name_0 = "degenerate triangle or UVs (blue)"
            if degenerate_uv_mesh is None:
                degenerate_uv_mesh = bpy.data.meshes.new(face_error_name_0)
            if degenerate_uv_object_mesh is None:
                degenerate_uv_object_mesh = bpy.data.objects.new(face_error_name_0, degenerate_uv_mesh)
                collection.objects.link(degenerate_uv_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = degenerate_uv_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = degenerate_uv_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = degenerate_uv_bm.verts.new((p3[0], p3[1], p3[2]))
            degenerate_uv_bm.faces.new((v1, v2, v3))

            degenerate_uv_bm.faces.ensure_lookup_table()

            mat_blue = bpy.data.materials.get(face_error_name_0)
            if mat_blue is None:
                mat_blue = bpy.data.materials.new(name=face_error_name_0)
                mat_blue.diffuse_color = (0.0, 0.0, 1.0, 1.0)
                degenerate_uv_object_mesh.data.materials.append(mat_blue)
            else:
                if mat_blue not in  list(degenerate_uv_object_mesh.data.materials):
                    degenerate_uv_object_mesh.data.materials.append(mat_blue)

            if face_color == (0.0, 0.0, 1.0, 1.0):
                mat = mat_blue

            degenerate_uv_object_mesh_materials = list(degenerate_uv_object_mesh.data.materials)
            degenerate_uv_bm.faces[degenerate_uv_face_id].material_index = degenerate_uv_object_mesh_materials.index(mat)
            degenerate_uv_face_id += 1

        elif face_error == "unknown (white)":
            face_error_name_0 = "unknown (white)"
            if unknown_mesh is None:
                unknown_mesh = bpy.data.meshes.new(face_error_name_0)
            if unknown_object_mesh is None:
                unknown_object_mesh = bpy.data.objects.new(face_error_name_0, unknown_mesh)
                collection.objects.link(unknown_object_mesh)

            p1 = vert_data[face[0]]
            p2 = vert_data[face[1]]
            p3 = vert_data[face[2]]
            v1 = unknown_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = unknown_bm.verts.new((p2[0], p2[1], p2[2]))
            v3 = unknown_bm.verts.new((p3[0], p3[1], p3[2]))
            unknown_bm.faces.new((v1, v2, v3))

            unknown_bm.faces.ensure_lookup_table()

            mat_white = bpy.data.materials.get(face_error_name_0)
            if mat_white is None:
                mat_white = bpy.data.materials.new(name=face_error_name_0)
                mat_white.diffuse_color = (0.0, 0.0, 0.0, 1.0)
                unknown_object_mesh.data.materials.append(mat_white)
            else:
                if mat_white not in  list(unknown_object_mesh.data.materials):
                    unknown_object_mesh.data.materials.append(mat_white)

            if face_color == (0.0, 0.0, 0.0, 1.0):
                mat = mat_white

            unknown_object_mesh_materials = list(unknown_object_mesh.data.materials)
            unknown_bm.faces[unknown_face_id].material_index = unknown_object_mesh_materials.index(mat)
            unknown_face_id += 1

    for edge_idx, edge in enumerate(line_data):
        edge_color = line_color_data[edge_idx]
        edge_error = line_error_data[edge_idx]
        if edge_error == "bad edge (red)":
            edge_error_name_0 = "bad edge (red)"
            if bad_edge_mesh is None:
                bad_edge_mesh = bpy.data.meshes.new(edge_error_name_0)
            if bad_edge_object_mesh is None:
                bad_edge_object_mesh = bpy.data.objects.new(edge_error_name_0, bad_edge_mesh)
                collection.objects.link(bad_edge_object_mesh)

            p1 = vert_data[edge[0]]
            p2 = vert_data[edge[1]]
            v1 = bad_edge_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = bad_edge_bm.verts.new((p2[0], p2[1], p2[2]))
            bad_edge_bm.edges.new((v1, v2))

            bad_edge_bm.edges.ensure_lookup_table()

            mat_red = bpy.data.materials.get(edge_error_name_0)
            if mat_red is None:
                mat_red = bpy.data.materials.new(name=edge_error_name_0)
                mat_red.diffuse_color = (1.0, 0.0, 0.0, 1.0)
                bad_edge_object_mesh.data.materials.append(mat_red)
            else:
                if mat_red not in  list(bad_edge_object_mesh.data.materials):
                    bad_edge_object_mesh.data.materials.append(mat_red)

            if edge_color == (1.0, 0.0, 0.0, 1.0):
                mat = mat_red

            bad_edge_edge_id += 1

        if edge_error == "unearthed edge or T-junction (magenta)":
            edge_error_name_0 = "unearthed edge or T-junction (magenta)"
            if unearthed_edge_mesh is None:
                unearthed_edge_mesh = bpy.data.meshes.new(edge_error_name_0)
            if unearthed_edge_object_mesh is None:
                unearthed_edge_object_mesh = bpy.data.objects.new(edge_error_name_0, unearthed_edge_mesh)
                collection.objects.link(unearthed_edge_object_mesh)

            p1 = vert_data[edge[0]]
            p2 = vert_data[edge[1]]
            v1 = unearthed_edge_bm.verts.new((p1[0], p1[1], p1[2]))
            v2 = unearthed_edge_bm.verts.new((p2[0], p2[1], p2[2]))

            unearthed_edge_bm.edges.new((v1, v2))

            unearthed_edge_bm.edges.ensure_lookup_table()

            mat_magenta = bpy.data.materials.get(edge_error_name_0)
            if mat_magenta is None:
                mat_magenta = bpy.data.materials.new(name=edge_error_name_0)
                mat_magenta.diffuse_color = (1.0, 0.0, 1.0, 1.0)
                unearthed_edge_object_mesh.data.materials.append(mat_magenta)
            else:
                if mat_magenta not in  list(unearthed_edge_object_mesh.data.materials):
                    unearthed_edge_object_mesh.data.materials.append(mat_magenta)

            if edge_color == (1.0, 0.0, 1.0, 1.0):
                mat = mat_magenta

            unearthed_edge_id += 1

    if coplanar_object_mesh:
        coplanar_bm.to_mesh(coplanar_mesh)
    coplanar_bm.free()

    if degenerate_object_mesh:
        degenerate_bm.to_mesh(degenerate_mesh)
    degenerate_bm.free()

    if portal_outside_object_mesh:
        portal_outside_bm.to_mesh(portal_outside_mesh)
    portal_outside_bm.free()

    if bad_edge_object_mesh:
        bad_edge_bm.to_mesh(bad_edge_mesh)
    bad_edge_bm.free()

    if unearthed_edge_object_mesh:
        unearthed_edge_bm.to_mesh(unearthed_edge_mesh)
    unearthed_edge_bm.free()

    if surface_clipped_object_mesh:
        surface_clipped_bm.to_mesh(surface_clipped_mesh)
    surface_clipped_bm.free()

    if portal_undivide_object_mesh:
        portal_undivide_bm.to_mesh(portal_undivide_mesh)
    portal_undivide_bm.free()

    if portal_closed_object_mesh:
        portal_closed_bm.to_mesh(portal_closed_mesh)
    portal_closed_bm.free()

    if duplicate_triangle_object_mesh:
        duplicate_triangle_bm.to_mesh(duplicate_triangle_mesh)
    duplicate_triangle_bm.free()

    if intersecting_fog_object_mesh:
        intersecting_fog_bm.to_mesh(intersecting_fog_mesh)
    intersecting_fog_bm.free()

    if degenerate_uv_object_mesh:
        degenerate_uv_bm.to_mesh(degenerate_uv_mesh)
    degenerate_uv_bm.free()

    if unknown_object_mesh:
        unknown_bm.to_mesh(unknown_mesh)
    unknown_bm.free()

    return {'FINISHED'}

if __name__== "__main__":
    bpy.ops.import_scene.wrl()
