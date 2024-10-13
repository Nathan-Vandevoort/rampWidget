from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os


class KeyItem(QGraphicsPixmapItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent=parent)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setPixmap(pixmap)

        # ----------------------------------- Attrs -------------------------------------------
        self._value = None
        self._position = None
        self._scene = scene

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        if not isinstance(new_value, float | int):
            return

        self._value = new_value
        self.setY(self._scene.height() * self._value)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):

        if not isinstance(new_value, float | int):
            return

        if new_value > 1:
            self._position = 1
            return

        if new_value < 0:
            self._position = 0
            return

        self._position = new_value
        self.setX(self._scene.width() * self._position)


