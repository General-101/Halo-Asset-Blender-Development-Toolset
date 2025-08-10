# ##### BEGIN MIT LICENSE BLOCK #####
#
# MIT License
#
# Copyright (c) 2023 Steven Garcia & Jadeon Sheppard
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

def gather_scene_resources(context, layer_collection_list, object_list, hidden_geo, nonrender_geo):
    object_scene_list = list(context.scene.objects)
    for obj in object_scene_list:
        if hidden_geo:
            layer_hidden_from_render = False
            for collection in obj.users_collection:
                layer_collection = context.view_layer.layer_collection.children.get(collection.name)
                if not layer_collection == None:
                    if layer_collection.collection.hide_render:
                        layer_hidden_from_render = True
                    if not layer_collection in layer_collection_list:
                        layer_collection_list.append(layer_collection)

            if nonrender_geo:
                object_list.append(obj)
            else:
                if not obj.hide_render and not layer_hidden_from_render:
                    object_list.append(obj)

        else:
            if obj.visible_get():
                layer_hidden_from_render = False
                for collection in obj.users_collection:
                    layer_collection = context.view_layer.layer_collection.children.get(collection.name)
                    if not layer_collection == None:
                        if layer_collection.collection.hide_render:
                            layer_hidden_from_render = True
                        if not layer_collection in layer_collection_list:
                            if layer_collection.is_visible:
                                layer_collection_list.append(layer_collection)

                if nonrender_geo:
                    object_list.append(obj)
                else:
                    if not obj.hide_render and not layer_hidden_from_render:
                        object_list.append(obj)

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
