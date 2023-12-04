from backend.core import Element, Group
from backend.transformer import CartesianTransformer
from frontend.command import MoveCommand

transformer = CartesianTransformer()


class DummyPresenter:
    @staticmethod
    def update(x, y):
        print(f"Presenter says: {x}, {y}")


presenter = DummyPresenter()


# -----------------------------------------------
print("ELEMENT TEST:")

element_1 = Element(x=9, y=9, transformer=transformer)

move_command = MoveCommand(element_1, 1, 1)
move_command.attach(presenter)
move_command.execute()

print("After move taken from Element", element_1.x, element_1.y)
print()
# -----------------------------------------------
print("GROUP TEST:")

element_2 = Element(x=5, y=5, transformer=transformer)
element_3 = Element(x=15, y=15, transformer=transformer)

elements = [element_2, element_3]
group = Group(transformer=transformer)
for element in elements:
    group.add(element)

move_command_2 = MoveCommand(group, 1, 1)
move_command_2.attach(presenter)
move_command_2.execute()

print("After move taken from Group", group.x, group.y)
print("After move", element_2.x, element_2.y)
print("After move", element_3.x, element_3.y)
