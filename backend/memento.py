"""Implementation of undo/redo functionality.

This module uses the memento design pattern to create snapshot of the canvas and save them
if changes need to be reverted or reimplemented.
"""


class CanvasMemento:
    """Saves all elements on the canvas.

    Attributes:
        content (List[Element]): List of all elements on the canvas.
    """

    def __init__(self, content):
        self.content = content[:]

    def get_state(self):
        return self.content


class History:
    """Stores all saved states of the canvas

    The states can be cycled from past to future and vice versa. One of the states is allways current.

    Attributes:
        states_past (List[CanvasMemento]): List of memento objects.
        state_current (List[CanvasMemento]): List with only one object.
        states_future (List[CanvasMemento]): List of memento objects.
    """
    def __init__(self):
        self.states_past = []
        self.state_current = []
        self.states_future = []

    def save_state(self, memento):
        """Save and manage states

        The state of the canvas is saved as current and the previous state is moved to past states.
        By saving the current states the future states are cleared.

        Args:
            memento (CanvasMemento): The newest state of the canvas.
        """
        if self.state_current:
            self.states_past.append(self.state_current.pop())
        self.state_current.append(memento)
        self.states_future.clear()

    def get_state_past(self):
        """Undo

        Takes state from the past, current state becomes future state and in its place comes the past state.

        Returns:
            popped (CanvasMemento): Past state of the canvas.
            None
        """
        if self.states_past:
            popped = self.states_past.pop()

            self.states_future.append(self.state_current.pop())

            self.state_current.append(popped)
            return popped

        return None

    def get_state_future(self):
        """Redo

        Takes state from the future, current state becomes past state and in its place comes the future state.

        Returns:
            popped (CanvasMemento): Future state of the canvas.
            None
        """
        if self.states_future:
            popped = self.states_future.pop()

            self.states_past.append(self.state_current.pop())

            self.state_current.append(popped)
            return popped

        return None
