"""Elements for the UI initiation

This file creates:
    - single elements for the palette
    - groups of elements for the 'Insert Shape' function
    - the canvas and temporary group for elements storage
"""

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

palette_group = Group()
palette_group.set_transformer(transformer)
for el in palette_elements:
    palette_group.add(el)

# predefined square
square = [(50, 10), (51, 10), (52, 10), (53, 10), (54, 10),
          (50, 11), (54, 11),
          (50, 12), (54, 12),
          (50, 13), (54, 13),
          (50, 14), (51, 14), (52, 14), (53, 14), (54, 14)]

predefined_square = Group(transformer=transformer)
predefined_square.x = 52
predefined_square.y = 12
for xy in square:
    element = Element(xy[0], xy[1]).set_transformer(transformer).set_symbol("X")
    predefined_square.add(element)

# predefined z-shape
z = [(100, 10), (101, 10), (102, 10), (103, 10), (104, 10),
     (100, 11), (101, 11), (102, 11), (103, 11), (104, 11),

     (104, 13), (105, 13), (106, 13), (107, 13), (108, 13),
     (104, 14), (105, 14), (106, 14), (107, 14), (108, 14)]

predefined_z_shape = Group(transformer=transformer)
predefined_z_shape.x = 104
predefined_z_shape.y = 12
for xy in z:
    element = Element(xy[0], xy[1]).set_transformer(transformer).set_symbol("X")
    predefined_z_shape.add(element)

# predefined smiley
smiley = [(71, 9), (72, 9), (78, 9), (79, 9),
          (71, 10), (72, 10), (78, 10), (79, 10),

          (67, 12), (68, 12), (82, 12),
          (68, 13), (69, 13), (81, 13),
          (70, 14), (71, 14), (72, 14), (73, 14), (74, 14), (75, 14),
          (76, 14), (77, 14), (78, 14), (79, 14), (80, 14)]

predefined_smiley = Group(transformer=transformer)
predefined_smiley.x = 75
predefined_smiley.y = 12
for xy in smiley:
    element = Element(xy[0], xy[1]).set_transformer(transformer).set_symbol("X")
    predefined_smiley.add(element)

# Canvas
canvas_group = Canvas()
canvas_group.set_transformer(transformer)

