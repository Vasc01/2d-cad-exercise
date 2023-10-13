from backend.componentabc_element_group import Leaf, Composite
from backend.editorabc_editor import Editor

editor = Editor()
element = Leaf(editor)
element.move(2, 2)

print("After Run", element.x, element.y)

elements = [Leaf(editor), Leaf(editor)]
group = Composite(editor)
for element in elements:
    group.add(element)
group.move(2, 2)
