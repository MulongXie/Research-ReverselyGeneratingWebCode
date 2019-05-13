import pandas as pd
import cv2
import numpy as np
import os


def select_color(item):
    color = (0, 0, 0)
    if item == 'div':
        color = (0, 0, 200)
    elif item == 'input':
        color = (255, 0, 0)
    elif item == 'button':
        color = (180, 0, 0)
    elif item == 'h1':
        color = (0, 255, 0)
    elif item == 'h2':
        color = (0, 180, 0)
    elif item == 'p':
        color = (0, 100, 0)
    elif item == 'a':
        color = (200, 100, )
    elif item == 'img':
        color = (0, 100, 255)
    return color


def draw(label, pic):
    count = {}
    for i in range(0, len(label)):
        item = label.iloc[i]

        top_left = (int(item.bx), int(item.by))
        botom_right = (int(item.bx + item.bw), int(item.by + item.bh))
        element = item.element

        color = select_color(item.element)
        if element in count:
            count[element] += 1
        else:
            count[element] = 1

        pic = cv2.rectangle(pic, top_left, botom_right, color, 1)
        cv2.putText(pic, element + str(count[element]), top_left, cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 1, cv2.LINE_AA)


def show(root_path="labeled_image", wait_key=0):
    imgs = []
    for _, _, imgs in os.walk('./labeled_image'):
        pass
    for img in imgs:
        print('./' + root_path + '/' + img)
        i = cv2.imread('./' + root_path + '/' + img)
        cv2.imshow('img', i)
        cv2.waitKey(wait_key)


def label(label, img, output_path, show=False):
    distort = 1
    print(np.shape(img))
    img = cv2.resize(img, (int(np.shape(img)[1] * distort), int(np.shape(img)[0] * distort)))
    draw(label, img)

    if show:
        cv2.imshow('img', img)
        cv2.waitKey(0)

    cv2.imwrite(output_path, img)
    print(output_path)


# used for sorting by area
def takearea(element):
    return element['area']


def wireframe(label, image, number, output_path):
    df = pd.read_csv(label)
    img = cv2.imread(image)

    pic = np.zeros(np.shape(img), np.uint8)
    pic.fill(255)

    layers = []
    for i in range(0, len(df)):
        item = df.iloc[i]
        element = item.element
        if element == 'div':
            continue

        layer = {}
        layer['top_left'] = (int(item.bx), int(item.by))
        layer['bottom_right'] = (int(item.bx + item.bw), int(item.by + item.bh))
        layer['area'] = int(item.bw * item.bh)
        layer['color'] = select_color(element)
        layer['element'] = element
        layers.append(layer)

    # sort in descent order
    layers.sort(key=takearea, reverse=True)

    count = {}  # count for each component category
    for l in layers:
        element = l['element']
        if element in count:
            count[element] += 1
        else:
            count[element] = 1

        pic = cv2.rectangle(pic, l['top_left'], l['bottom_right'], l['color'], -1)
        cv2.putText(pic, element + str(count[element]), l['top_left'], cv2.FONT_HERSHEY_SIMPLEX, 0.5, l['color'], 2,
                    cv2.LINE_AA)

    cv2.imwrite(output_path, pic)
    print(output_path)