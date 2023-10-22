from backend.core import Element, Group
from backend.transformer import CartesianTransformer

transformer = CartesianTransformer()

# -----------------------------------------------
print("ELEMENT TEST:")

element_1 = Element(x=9, y=9, transformer=transformer)
element_1.move(1, 1)
print("After move", element_1.x, element_1.y)

element_1.rotate(90)
print("After rotate", element_1.x, element_1.y)

element_1.mirror("y")
print("After mirror", element_1.x, element_1.y)

element_1.scale(2, 2)
print("After scale", element_1.x, element_1.y)

element_1.fill("name", "name_1")
element_1.fill("symbol", "@")
element_1.fill("symbol color", "blue")
element_1.fill("background", "grey")

print(element_1.name, element_1.symbol, element_1.symbol_color, element_1.background_color)

element_2 = Element(x=1, y=1, transformer=transformer)\
    .set_name("name_2")\
    .set_symbol("#")\
    .set_symbol_color("purple")\
    .set_background_color("black")

print(element_2.name, element_2.symbol, element_2.symbol_color, element_2.background_color)

# -----------------------------------------------
print("GROUP TEST:")

elements = [element_1, element_2]
group = Group(transformer=transformer)
for element in elements:
    group.add(element)

print(group.elements)

group.move(1, 1)
print("After move", element_1.x, element_1.y)
print("After move", element_2.x, element_2.y)

group.rotate(90)
print("After rotate", element_1.x, element_1.y)
print("After rotate", element_2.x, element_2.y)

group.mirror("y")
print("After mirror", element_1.x, element_1.y)
print("After mirror", element_2.x, element_2.y)

group.scale(2, 2)
print("After scale", element_1.x, element_1.y)
print("After scale", element_2.x, element_2.y)

group.fill("name", "renamed1/2")
print(element_1.name)
print(element_2.name)

elements2 = [element_2, Element(5, 5)]
group_2 = Group(transformer=transformer)
for element in elements2:
    group_2.add(element)

split_result = group.split(group_2)
for elements in split_result:
    print(*elements)

