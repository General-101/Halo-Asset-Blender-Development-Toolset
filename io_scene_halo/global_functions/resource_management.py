
def gather_collection_resources(layer_collection, layer_collection_set, object_set, hidden_geo, nonrender_geo, include_this_collection = False):
    """
        Recursively gathers the relevant collections and objects for export, starting from a root layer collection.
        "include_this_collection" should be false for the root collection, else restoring visibility will cause everything to become visible regardless of stored value.
    """

    # Don't include anything from collection if exclude
    if layer_collection.exclude:
        return

    # Don't include anything from collection if hidden in an undesired way
    if not hidden_geo and layer_collection.collection.hide_viewport:
        return

    if not nonrender_geo and layer_collection.collection.hide_render:
        return

    # Add collection to set of all included collections
    if include_this_collection:
        layer_collection_set.add(layer_collection)

    # Add all of collection's objects when not hidden in an undesired way
    for obj in layer_collection.collection.objects:
        if not hidden_geo and obj.hide_viewport:
            continue

        if not hidden_geo and obj.hide_get():
            continue

        if not nonrender_geo and obj.hide_render:
            continue

        object_set.add(obj)

    # Recursively gather resources for child collections
    for collection in layer_collection.children:
        gather_collection_resources(collection, layer_collection_set, object_set, hidden_geo, nonrender_geo, True)

def filter_root_nodes(node_list, is_jmi = False):
    ''' Takes a set of objects and returns all that are root nodes '''

    root_nodes = set()

    for node in node_list:
        # Is a root node if has no parent
        if node.parent == None:
            root_nodes.add(node)

        # If exporting JMI root nodes will have a parent with a name starting with `!`
        elif is_jmi and node.parent.name[0:1] == '!':
            root_nodes.add(node)

    return root_nodes

def filter_objects_from_root_object(object_set, root_object, include_root: bool = False):
    ''' Takes a set of objects and returns all that descend from the provided root object '''

    filtered_children = list()

    if include_root:
        filtered_children.append(root_object)

    # Get a list of all root object descendants
    all_children = root_object.children_recursive

    for child in all_children:
        # Add child to filtered output only if it exists in the object set
        if child in object_set:
            filtered_children.append(child)

    return filtered_children

def store_collection_visibility(layer_collection_list):
    collection_visibility_list = list()

    for layer_collection in layer_collection_list:
        collection_visibility_list.append({
            'layer_collection': layer_collection,
            'exclude': layer_collection.exclude,
            'hide_viewport': layer_collection.hide_viewport,
            'collection_hide_render': layer_collection.collection.hide_render,
            'collection_hide_viewport': layer_collection.collection.hide_viewport,
        })

    return collection_visibility_list

def restore_collection_visibility(collection_visibility_list):
    for state in collection_visibility_list:
        layer_collection = state['layer_collection']

        layer_collection.exclude = state['exclude']
        layer_collection.hide_viewport = state['hide_viewport']
        layer_collection.collection.hide_render = state['collection_hide_render']
        layer_collection.collection.hide_viewport = state['collection_hide_viewport']

def store_object_visibility(object_list):
    object_visibility_list = list()

    for obj in object_list:
        object_visibility_list.append({
            'object': obj,
            'hide_get': obj.hide_get(),
            'hide_render': obj.hide_render,
            'hide_viewport': obj.hide_viewport,
        })

    return object_visibility_list

def restore_object_visibility(object_visibility_list):
    for state in object_visibility_list:
        obj = state['object']
        obj.hide_set(state['hide_get'])
        obj.hide_render = state['hide_render']
        obj.hide_viewport = state['hide_viewport']

def store_modifier_visibility(object_list):
    modifier_visibility_list = list()

    for obj in object_list:
        for modifier in obj.modifiers:
            modifier_visibility_list.append({
                'modifier': modifier,
                'show_render': modifier.show_render,
                'show_viewport': modifier.show_viewport,
                'show_in_editmode': modifier.show_in_editmode,
            })

    return modifier_visibility_list

def restore_modifier_visibility(modifier_visibility_list):
    for state in modifier_visibility_list:
        modifier = state['modifier']
        modifier.show_render = state['show_render']
        modifier.show_viewport = state['show_viewport']
        modifier.show_in_editmode = state['show_in_editmode']

def unhide_relevant_resources(layer_collection_set, object_set):
    for layer_collection in layer_collection_set:
        layer_collection.exclude = False
        layer_collection.hide_viewport = False
        layer_collection.collection.hide_viewport = False

    for obj in object_set:
        obj.hide_set(False)
        obj.hide_viewport = False
