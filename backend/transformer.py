from abc import ABC, abstractmethod


class TransformerAbc(ABC):

    @abstractmethod
    def transform(self, x, y, delta_x, delta_y):
        pass


class MoveTransformer(TransformerAbc):

    def transform(self, x, y, delta_x, delta_y):
        x += delta_x
        y += delta_y
        print("Transformer is moving things")
        return x, y
