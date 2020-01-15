import cv2
import json


def extract(obj, layer):
    return {'layer':layer, 'class':obj['class'], 'bound':obj['bounds'], 'rel-bounds':obj['rel-bounds']}


def iter_kids(obj, layer):
    objects.append(extract(obj, layer))
    if 'children' in obj and len(obj['children']) > 0:
        children = obj['children']
        for child in children:
            iter_kids(child, layer + 1)


jfile = json.load(open('1.json'))
act = jfile['activity']
root = act['root']
objects = []

iter_kids(root, 0)

objs_json = json.dumps(objects)
output = open('objects.json', 'w')
output.write(objs_json)
