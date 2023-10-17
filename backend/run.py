from backend.componentabc_element_group import Element, Group
from backend.transformer import *

# -----------------------------------------------
print("LEAF TEST:")

t1 = CartesianTransformer()
t2 = PolarTransformer()

t1.move(3, 4, 2, 2)
t2.scale()


element_1 = Element(3, 4, transformer=t1)
element_1.move(2, 2)
print("After Run", element_1.x, element_1.y)

element_1.set_transformer(transformer=t2)
element_1.move(2, 45)
print("After Run", element_1.x, element_1.y)
element_1.rotate()
element_1.mirror()
element_1.scale()
element_1.fill()

# -----------------------------------------------
print("GROUP TEST:")

elements = [Element(1, 1)] * 10
group = Group(transformer=t1)
for element in elements:
    group.add(element)

group.move(2, 2)
