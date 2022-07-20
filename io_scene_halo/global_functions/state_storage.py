
def store_collection_visibility(layer_collection_list):
    object_visibility_list = list()

    for layer_collection in layer_collection_list:
        object_visibility_list.append({
            'layer_collection': layer_collection,
            'exclude': layer_collection.exclude,
            'hide_render': layer_collection.collection.hide_render,
            'hide_viewport': layer_collection.collection.hide_viewport,
        })

    return object_visibility_list

def restore_collection_visibility(collection_visibility_list):
    for state in collection_visibility_list:
        layer_collection = state['layer_collection']

        layer_collection.exclude = state['exclude']
        layer_collection.collection.hide_render = state['hide_render']
        layer_collection.collection.hide_viewport = state['hide_viewport']

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
