

class InputOutput:
    def __init__(self, data_type, initial):
        self.data_type = data_type
        self._value = initial

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        # TODO verify this is the correct type of data
        self._value = value


class InputOutputGroup:
    def __init__(self, IOs):
        """
        IOs should be a dictionary of InputOutputs with the key being a name
        """
        # verify initial is correct type
        self.IOs = IOs

    def __call__(self, name):
        return self.IOs[name]

    def get(self):
        return self.IOs

    def set(self, IO):
        self.IOs = IO

    def __getattr__(self, name):
        return self.IOs[name]