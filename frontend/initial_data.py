from backend.core import Element, Canvas, Group
from backend.transformer import CartesianTransformer

transformer = CartesianTransformer()

# stores elements for commands
temporary_group = Group()
temporary_group.set_transformer(transformer)

# elements for palette
palette_elements = [
    Element(2, 0).set_symbol("&"),
    Element(4, 0).set_symbol("#"),
    Element(6, 0).set_symbol("@"),
    Element(2, 1).set_symbol("%"),
    Element(4, 1).set_symbol("X"),
    Element(6, 1).set_symbol("0")
]

palette = Group()
palette.set_transformer(transformer)
for el in palette_elements:
    palette.add(el)

# predefined figures
z_list = [(30, 10), (31, 10), (32, 10), (33, 10), (34, 10),
          (34, 11),
          (34, 12), (35, 12), (36, 12), (37, 12), (38, 12)]

square_list = [(50, 10), (51, 10), (52, 10), (53, 10), (54, 10),
               (50, 11), (54, 11),
               (50, 12), (54, 12),
               (50, 13), (54, 13),
               (50, 14), (51, 14), (52, 14), (53, 14), (54, 14)]

predefined_square = Group(transformer=transformer)
for xy in square_list:
    element = Element(xy[0], xy[1]).set_transformer(transformer).set_symbol("X")
    predefined_square.add(element)

# Elements preexistent on canvas
element_1 = Element(20, 10).set_symbol("@")
element_2 = Element(22, 10).set_symbol("%")
element_3 = Element(24, 10).set_symbol("X")
canvas = Canvas()
canvas.set_transformer(transformer)
canvas.add(element_1)
canvas.add(element_2)
canvas.add(element_3)
