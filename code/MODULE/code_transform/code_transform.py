import cv2
import numpy as np


def html_shape(component):
    height = np.shape(component)[0]
    width = np.shape(component)[1]

    size = "width:" + str(width) + "px; height:" + str(height) + "px;"
    return size


def get_most_value(array):
    array = np.reshape(array, (np.shape(array)[0] * np.shape(array)[1]))
    most = np.bincount(array).argmax()
    return most


def dec2hexstr(dec):
    h = str(hex(dec))[2:]
    if len(h) < 2:
        h = '0' + h
    return h


def html_color(component):
    b = component[:, :, 0]
    g = component[:, :, 1]
    r = component[:, :, 2]
    b_most = get_most_value(r)
    g_most = get_most_value(g)
    r_most = get_most_value(b)

    rgb_html = '#' + dec2hexstr(b_most) + dec2hexstr(g_most) + dec2hexstr(r_most)

    return rgb_html, b_most, g_most, r_most


def color_test(b, g, r):
    b = np.full((20, 20), b)
    g = np.full((20, 20), g)
    r = np.full((20, 20), r)

    rgb = np.zeros((20, 20, 3), dtype=np.uint8)
    rgb[:, :, 0] = b  # b
    rgb[:, :, 1] = g  # g
    rgb[:, :, 2] = r  # r

    print(np.shape(rgb))

    cv2.cvtColor(rgb, cv2.COLOR_BGR2RGB, rgb)

    cv2.imshow('img', rgb)
    cv2.imwrite('result.png', rgb)
    cv2.waitKey(0)


def html_tag(tag):
    return "<" + str(tag) + " "


def html_style(img):
    rgb_html, b, g, r = html_color(img)
    shape_html = html_shape(img)
    style = "style=\"background: " + rgb_html + ";" + shape_html
    return style


def html_assemble(img):
    file = open('result.txt', 'a')

    tag = 'button'
    tag = html_tag(tag)
    style = html_style(img)
    html = tag + style + '>'
    print(html)
    file.write(html)

    return html


img = cv2.imread('83.png')
# color_test(b, g, r)
html_assemble(img)
cv2.imshow('org', img)
cv2.waitKey(0)