from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap
import os


class ValueItem(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # -------------------------------- Attrs -----------------------------------
        self.parent = parent
        self._value = 0
        self._scale = 1 or self.parent.scale

        # -------------------------------- Setup -----------------------------------
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setFlags(QGraphicsItem.ItemIsSelectable)

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setScale(self._scale)
        self.setPixmap(pixmap)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        if not isinstance(new_value, float | int):
            return

        elif new_value > 1:
            new_value = 1

        elif new_value < 0:
            new_value = 0

        self._value = new_value

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            print(f'newPos: {value}')
