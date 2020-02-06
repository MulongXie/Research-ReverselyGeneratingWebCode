import cv2

class_map = ['button', 'input', 'select', 'search', 'list', 'img', 'block', 'text', 'icon']
COLOR = {'block': (0, 255, 0), 'img': (0, 0, 255), 'icon': (255, 166, 166), 'input': (255, 166, 0),
                      'text': (77, 77, 255), 'search': (255, 0, 166), 'list': (166, 0, 255), 'select': (166, 166, 166),
                      'button': (0, 166, 255)}


def draw_bounding_box_class(org, corners, classes, color_map=COLOR, line=2,
                            draw_text=False, show=False, write_path=None):
    """
    Draw bounding box of components with their classes on the original image
    :param org: original image
    :param corners: [(top_left, bottom_right)]
                    -> top_left: (column_min, row_min)
                    -> bottom_right: (column_max, row_max)
    :param color_map: colors mapping to different components
    :param line: line thickness
    :param compo_class: classes matching the corners of components
    :param show: show or not
    :return: labeled image
    """
    board = org.copy()
    for i in range(len(corners)):
        print(corners[i])
        if not draw_text and classes[i] == 'text':
            continue
        board = cv2.rectangle(board, (corners[i][0], corners[i][1]), (corners[i][2], corners[i][3]), color_map[classes[i]], line)
        board = cv2.putText(board, classes[i], (corners[i][0]+5, corners[i][1]+20),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.8, color_map[classes[i]], 2)
    if show:
        cv2.imshow('a', board)
        cv2.waitKey(0)
    if write_path is not None:
        cv2.imwrite(write_path, board)
    return board


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


def resize_label(bboxes, d_height, gt_height):
    bias = 10
    bboxes_new = []
    scale = gt_height/d_height
    for bbox in bboxes:
        bbox = [int(b * scale) + bias for b in bbox]
        bboxes_new.append(bbox)
    return bboxes_new


img = cv2.imread('6.jpg')
det = read_detect_result('6_merged.txt')['6']
det['bboxes'] = resize_label(det['bboxes'], 600, img.shape[0])
draw_bounding_box_class(img, det['bboxes'], det['categories'], show=True)
