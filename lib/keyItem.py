from PySide6.QtWidgets import QGraphicsPixmapItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap
import os


class KeyItem(QGraphicsPixmapItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent=parent)

        images_dir = os.path.join(os.path.dirname(__file__), 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setPixmap(pixmap)

        # ----------------------------------- Attrs -------------------------------------------
        self._value = None
        self._position = None
        self._scene = scene

        self.setAcceptHoverEvents(True)
        self.setAcceptDrops(True)
        self.hovered = False
        self.selection_offset = QPointF(0, 0)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):

        if not isinstance(new_value, float | int):
            return

        self._value = new_value
        self.setY(self._scene.target_height * self._value)

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
        self.setX(self._scene.target_width * self._position)

    def hoverEnterEvent(self, event):
        self.hovered = True
        self.setScale(1.1)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        self.setScale(1)
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._scene.grabbed_item = self
            self.selection_offset = self.pos() - event.scenePos()

        super().mousePressEvent(event)
