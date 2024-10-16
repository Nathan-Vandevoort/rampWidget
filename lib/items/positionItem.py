from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap
import os


class PositionItem(QGraphicsPixmapItem):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # -------------------------------- Attrs -----------------------------------
        self.parent = parent
        self._position = 0
        self._scale = self.parent.scale

        # -------------------------------- Setup -----------------------------------
        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.selection_offset = QPointF(0, 0)

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setScale(self._scale)
        self.setPixmap(pixmap)
        self.setY(self.parent.scene.target_height)

    def forceSet(self, new_value):
        self._position = new_value

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):
        if not isinstance(new_value, float | int):
            return

        elif new_value > 1:
            new_value = 1

        elif new_value < 0:
            new_value = 0

        self._position = new_value
        self.setX(self.parent.scene.mapPositionToScene(new_value))

    def hoverEnterEvent(self, event):
        self.setScale(self._scale * 1.1)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setScale(self._scale)
        super().hoverLeaveEvent(event)


