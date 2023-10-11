from typing import List

from backend.canvas_body_abc import CanvasBody
from backend.element import Element
from backend.modify_abc import ModifyAbc


class Group(CanvasBody):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.modify = ModifyAbc()
        self.elements: List[Element] = []
