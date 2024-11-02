import numpy as np
import json
import os


class FloatArrayKnob:

    def __init__(self, name: str, length: int):
        self._data = np.empty(length, dtype=float)
        self._name = name
        self._path = os.path.join(os.path.dirname(__file__), 'data', self._name + '.json')

        if os.path.isfile(self._path):
            self.load()

    def value(self, index) -> int:
        """
        Returns the value at a given index
        :param index: int
        :return: int
        """
        return self._data[index]

    def setValue(self, index, value):
        self._data[index] = value

    def width(self) -> int:
        """
        Returns the length of the array
        :return: int
        """
        return self._data.size

    def array(self) -> list:
        """
        Returns a list of knob values
        :return: list
        """
        return self._data.tolist()

    def save(self):
        with open(self._path, 'w') as file:
            json.dump(self.array(), file)
            file.close()

    def load(self):
        with open(self._path, 'r') as file:
            data = json.load(file)
        self._data = np.array(data, dtype=float)


class IntArrayKnob:

    def __init__(self, name: str, length: int):
        self._data = np.full(length, -1, dtype=int)
        self._name = name
        self._path = os.path.join(os.path.dirname(__file__), 'data', self._name + '.json')

        if os.path.isfile(self._path):
            self.load()

    def value(self, index) -> int:
        """
        Returns the value at a given index
        :param index: int
        :return: int
        """
        return self._data[index]

    def setValue(self, index, value):
        self._data[index] = value

    def width(self) -> int:
        """
        Returns the length of the array
        :return: int
        """
        return self._data.size

    def array(self) -> list:
        """
        Returns a list of knob values
        :return: list
        """
        return self._data.tolist()

    def save(self):
        with open(self._path, 'w') as file:
            json.dump(self.array(), file)
            file.close()

    def load(self):
        with open(self._path, 'r') as file:
            data = json.load(file)
        self._data = np.array(data, dtype=int)
