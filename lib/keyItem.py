from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os


class KeyItem(QGraphicsPixmapItem):

    def __init__(self, parent=None, position = .5, value = 0):
        super().__init__(parent=parent)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        pixmap = QPixmap(fileName=os.path.join(images_dir, 'key.png'))
        self.setPixmap(pixmap)

        # ----------------------------------- Attrs -------------------------------------------

        self.value = value
        self.position = position

    @property
    def value(self):
        return self.value

    @value.setter
    def value(self, new_value):

        if not isinstance(new_value, float | int):
            return

        self.value = new_value

    @property
    def position(self):
        return self.position

    @position.setter
    def position(self, new_value):

        if not isinstance(new_value, float | int):
            return

        if new_value > 1:
            self.value = 1
            return

        if new_value < 0:
            self.value = 0
            return

        self.position = new_value