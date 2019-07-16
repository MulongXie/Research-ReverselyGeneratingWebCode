import pandas as pd
import code_generator as gen


components = pd.read_csv('output/corners.csv', index_col=0)
file_html = open('webpage/a.html', 'w')
file_css = open('webpage/a.css', 'w')

html = gen.html_head()
css = gen.css_container()
for i in range(len(components)):
    compo = components.iloc[i]
    html = gen.generate_html(html, compo, i)
    css = gen.generate_css(css, compo, i)

html += gen.html_tail()

file_html.write(html)
file_css.write(css)
print(html)
print(css)