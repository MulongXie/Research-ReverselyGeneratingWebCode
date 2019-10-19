from code_generation import DIV

d1 = DIV(1)
d2 = DIV(2)
d3 = DIV(3)
d4 = DIV(4)

d3.insert_body(d4.indent())
print(d3.code)

d2.insert_body(d3.indent())
# print(d2.code)

d1.insert_body(d2.indent())
print(d1.code)