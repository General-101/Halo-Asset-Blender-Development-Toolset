
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

        if not nonrender_geo and obj.hide_render:
            continue

        object_set.add(obj)

    # Recursively gather resources for child collections
    for collection in layer_collection.children:
        gather_collection_resources(collection, layer_collection_set, object_set, hidden_geo, nonrender_geo, True)

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

def unhide_relevant_resources(layer_collection_set, object_set):
    for layer_collection in layer_collection_set:
        layer_collection.exclude = False
        layer_collection.hide_viewport = False
        layer_collection.collection.hide_viewport = False

    for obj in object_set:
        obj.hide_set(False)
        obj.hide_viewport = False
