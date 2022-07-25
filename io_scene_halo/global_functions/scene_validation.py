from ..global_functions.global_functions import ParseError
from ..global_functions import resource_management

def validate_halo_jms_scene(game_version, version, blend_scene, object_list, is_jmi):
    node_count = len(blend_scene.node_list)
    root_nodes = resource_management.filter_root_nodes(blend_scene.node_list, is_jmi)

    if len(object_list) == 0:
        raise ParseError("No objects in scene.")

    elif node_count == 0:
        raise ParseError("No nodes in scene. Add an armature or object mesh named frame.")

    elif not is_jmi and len(root_nodes) > 1:
        raise ParseError("More than one root node. Please remove or rename objects until you only have one root frame object.")

    elif blend_scene.mesh_frame_count > 0 and blend_scene.armature_count > 0:
        raise ParseError("Using both armature and object mesh node setup. Choose one or the other.")

    elif game_version == 'haloce' and version >= 8201:
        raise ParseError("This version is not supported for Halo CE. Choose from 8197-8200 if you wish to export for Halo CE.")

    elif game_version == 'halo2' and version >= 8211:
        raise ParseError("This version is not supported for Halo 2. Choose from 8197-8210 if you wish to export for Halo 2.")

    elif game_version == 'halo3' and version >= 8213:
        raise ParseError("This version is not supported for Halo 3. Choose from 8197-8213 if you wish to export for Halo 3.")

    elif game_version == 'haloce' and len(blend_scene.render_geometry_list + blend_scene.collision_geometry_list + blend_scene.marker_list) == 0:
        raise ParseError("No geometry in scene.")

    elif not game_version == 'haloce' and len(blend_scene.render_geometry_list + blend_scene.collision_geometry_list + blend_scene.marker_list + blend_scene.hinge_list + blend_scene.ragdoll_list + blend_scene.point_to_point_list + blend_scene.sphere_list + blend_scene.box_list + blend_scene.capsule_list + blend_scene.convex_shape_list + blend_scene.xref_instances + blend_scene.car_wheel_list + blend_scene.prismatic_list + blend_scene.bounding_sphere_list + blend_scene.skylight_list) == 0:
        raise ParseError("No geometry in scene.")

    elif game_version == 'haloce' and node_count > 64:
        raise ParseError("This model has more nodes than Halo CE supports. Please limit your node count to 64 nodes")

    elif game_version == 'halo2' and node_count > 255:
        raise ParseError("This model has more nodes than Halo 2 supports. Please limit your node count to 255 nodes")

    elif game_version == 'halo3' and node_count > 255:
        raise ParseError("This model has more nodes than Halo 3 supports. Please limit your node count to 255 nodes")
