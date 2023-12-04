from backend.core import Element, Group, Canvas
from frontend.memento import History
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

# -----------------------------------------------
print()
print("CANVAS TEST:")

elements_3 = [Element(1, 1), Element(2, 2), Element(3, 3)]
canvas = Canvas(transformer=transformer)
history = History()

for element in elements_3:
    canvas.add(element)

print()
print("Elements on canvas: ", canvas.elements)

history.save_state(canvas.create_memento())

canvas.remove(canvas.elements[-1])
print()
print("Elements on canvas: ", canvas.elements)
history.save_state(canvas.create_memento())

canvas.remove(canvas.elements[-1])
print()
print("Elements on canvas: ", canvas.elements)
history.save_state(canvas.create_memento())


canvas.remove(canvas.elements[-1])
print()
print("Elements on canvas: ", canvas.elements)

# before pop, save current state, so it is available for redo
history.save_state(canvas.create_memento())

last_state = history.get_state_past()
print()
print("Memento last state", last_state)
print("Last state content", last_state.get_state())

if last_state:
    canvas.restore_from_memento(last_state)
print()
print("RESTORED Elements on canvas: ", canvas.elements)

last_state = history.get_state_past()
print()
print("Memento last state", last_state)
print("Last state content", last_state.get_state())

if last_state:
    canvas.restore_from_memento(last_state)
print()
print("RESTORED Elements on canvas: ", canvas.elements)

next_state = history.get_state_future()
print()
print("Memento next state", next_state)
print("Next state content", next_state.get_state())

if next_state:
    canvas.restore_from_memento(next_state)
print()
print("FORWARDED Elements on canvas: ", canvas.elements)
