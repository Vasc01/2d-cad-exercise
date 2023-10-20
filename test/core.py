from backend.core import Element
from backend.transformer import CartesianTransformer

transformer = CartesianTransformer()

element_1 = Element(x=3, y=4, transformer=transformer)
element_1.move(2, 2)
print("After move", element_1.x, element_1.y)

element_1.fill(set_name, "el1")
