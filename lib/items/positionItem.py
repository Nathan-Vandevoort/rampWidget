from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap
import os


class PositionItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent=parent)

        # -------------------------------- Attrs -----------------------------------
        self.key = parent
        self._position = 0
        self._scale = self.key.scale

        # -------------------------------- Setup -----------------------------------
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)
        #self.setFlags(QGraphicsItem.ItemIsSelectable)

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setScale(self._scale)
        self.setPixmap(pixmap)

    @property
    def position(self):
        return self._position

    @position.setter
    def position(self, new_value):
        self._position = new_value

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if not self.key.scene.bound_rect.contains(value):

                if value.x() < self.key.scene.bound_rect.left():
                    value.setX(self.key.scene.bound_rect.left())

                elif value.x() > self.key.scene.bound_rect.right():
                    value.setX(self.key.scene.bound_rect.right())

                if value.y() < self.key.scene.bound_rect.top():
                    value.setY(self.key.scene.bound_rect.top())

                elif value.y() > self.key.scene.bound_rect.bottom():
                    value.setY(self.key.scene.bound_rect.bottom())

        return super().itemChange(change, value)
