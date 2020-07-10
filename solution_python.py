import collections

"""
The logic behind this class is that using Stack to storage the operations except `undo` and `redo`. 
- For example, for `add()` and `subtract()`, push the function name and parameters into the stack after each calling

If encounter `undo()` operation, 
"""


class EventSourcer():
    # Do not change the signature of any functions

    def __init__(self):
        self.value = 0
        self.done_operations = []
        self.undo_operations = collections.deque()

    def add(self, num: int):
        """
        - add num to the value
        new value will be calculated by adding num
        :param num: int
        :return: value
        """
        # update current value
        self.value += num
        # save the operation and its parameter into the stack of done_operations
        self.done_operations.append((self.add, num))
        return self.value

    def subtract(self, num: int):
        """
        - subtract num from the value
        new value will be calculated by subtracting num
        :param num: int
        :return: value
        """
        # update current value
        self.value -= num
        # save the operation and its parameter into the stack of done_operations
        self.done_operations.append((self.subtract, num))
        return self.value

    def undo(self):
        """
        - revert last event
        new value will be calculated by calling last functions (except undo/redo)
        :return: value
        """
        if self.done_operations:  
            # operations that have been done are existed
            # get the previous function and its parameter to revert the operation
            last_function, last_param = self.done_operations.pop()
            self.undo_operations.append((last_function, last_param))
            if last_function == self.add:
                self.value -= last_param
            elif last_function == self.subtract:
                self.value += last_param

        return self.value

    def redo(self):
        """
        - redo next event
        new value will be calculated by repeating last functions (except undo/redo)
        :return: value
        """
        if self.undo_operations:
            # operations that have been done are existed
            # get the previous function and its parameter to repeat the operation
            last_function, last_param = self.undo_operations.popleft()
            self.done_operations.append((last_function, last_param))
            if last_function == self.add:
                self.add(last_param)
            elif last_function == self.subtract:
                self.subtract(last_param)

        return self.value

    def bulk_undo(self, steps: int):
        """
        - undo the given amount of events
        perform undo() for steps times
        :return: value
        """
        while steps != 0:
            self.undo()
            steps -= 1

    def bulk_redo(self, steps: int):
        """
        - redo the given amount of events
        perform redo() for steps times
        :return: value
        """
        while steps != 0:
            self.redo()
            steps -= 1
