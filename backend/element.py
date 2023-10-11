from backend.canvas_body_abc import CanvasBody


class Element(CanvasBody):
    def __init__(self, x: int, y: int):
        super().__init__(x, y)
        self.name = ""
        self.symbol = ""
        self.symbol_color = ""
        self.background_color = ""

    # setters and getters
