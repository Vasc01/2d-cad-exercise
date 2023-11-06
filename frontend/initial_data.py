from backend.core import Element, Canvas, Group
from backend.transformer import CartesianTransformer

transformer = CartesianTransformer()

# Elements preexistent on canvas
element_1 = Element(20, 10).set_symbol("@")
element_2 = Element(22, 10).set_symbol("%")
element_3 = Element(24, 10).set_symbol("X")
canvas = Canvas()
canvas.set_transformer(transformer)
canvas.add(element_1)
canvas.add(element_2)
canvas.add(element_3)

# stores elements for commands
temporary_group = Group()
temporary_group.set_transformer(transformer)

# elements for palette
element_A = Element(0, 0).set_symbol("&")
element_B = Element(0, 1).set_symbol("#")
palette = Group()
palette.set_transformer(transformer)
palette.add(element_A)
palette.add(element_B)
