import cv2
import numpy as np
import os
import pandas as pd


def html_head():
    # html head
    head = '''<!DOCTYPE html>
<html lang="en">
<head>
   <meta charset="UTF-8">
   <title>Title</title>
   <link rel="stylesheet" href="a.css" type="text/css">
</head>
<body>
<div class="generated_container">\n'''
    return head


def html_tail():
    # html tail
    tail = "</div>\n</body>\n</html>"
    return tail


def generate_html(html, compo, index):
    # html body
    html += '\t<div id=\"' + compo['component'] + str(index) + '\"></div>\n'
    return html


def css_container():
    # container
    container = '''
.generated_container{
    width: 100%; height: 80%;
    margin-top: 40px;
    border: lightslategray solid 2px;
}
'''
    return container


def generate_css(css, compo, index):
    css += '#' + str(compo['component']) + str(index) + '{\n'
    css += '\twidth: ' + str(compo['width']) + 'px; '
    css += 'height: ' + str(compo['height']) + 'px;\n'
    css += '\tmargin-top: ' + str(compo['x_min']) + 'px; '
    css += 'margin-left: ' + str(compo['y_min']) + 'px;\n'

    css += '\tposition: absolute;\n'
    if str(compo['component']) == 'img':
        css += '\tbackground: black;\n'
    elif str(compo['component']) == 'div':
        css += '\tborder: grey solid 1px;\n'

    css += '}\n'
    return css


components = pd.read_csv('output/corners.csv', index_col=0)
file_html = open('webpage/a.html', 'w')
file_css = open('webpage/a.css', 'w')

html = html_head()
css = css_container()
for i in range(len(components)):
    compo = components.iloc[i]
    html = generate_html(html, compo, i)
    css = generate_css(css, compo, i)

html += html_tail()

file_html.write(html)
file_css.write(css)
print(html)
print(css)