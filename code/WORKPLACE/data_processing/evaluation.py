import json

class_map = ['button', 'input', 'select', 'search', 'list', 'img', 'block', 'text', 'icon']


def read_detect_result(file_name):
    '''
    :return: {list of [[col_min, row_min, col_max, row_max]], list of [class id]
    '''
    file = open(file_name, 'r')
    bboxes = []
    categories = []
    for l in file.readlines():
        labels = l.split()[1:]
        for label in labels:
            label = label.split(',')
            bboxes.append([int(b) for b in label[:-1]])
            categories.append(class_map[int(label[-1])])

    return {file_name.split('_')[0]: {'bboxes':bboxes, 'categories':categories}}


def read_ground_truth():
    def get_img_by_id(img_id):
        for image in images:
            if image['id'] == img_id:
                return image['file_name'].split('/')[-1][:-4]

    def cvt_bbox(bbox):
        '''
        :param bbox: [x,y,width,height]
        :return: [col_min, row_min, col_max, row_max]
        '''
        bbox = [int(b) for b in bbox]
        return [bbox[0], bbox[1], bbox[0] + bbox[2], bbox[1] + bbox[3]]

    data = json.load(open('instances_test.json', 'r'))

    images = data['images']
    annots = data['annotations']

    compos = {}
    for annot in annots:
        img_name = get_img_by_id(annot['image_id'])
        if img_name not in compos:
            compos[img_name] = {'bboxes': [annot['bbox']], 'categories': [annot['category_id']]}
        else:
            compos[img_name]['bboxes'].append(cvt_bbox(annot['bbox']))
            compos[img_name]['categories'].append(annot['category_id'])
    return compos


# print(read_ground_truth())
print(read_detect_result('6_merged.txt'))
