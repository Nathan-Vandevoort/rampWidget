from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF, Slot
from PySide6.QtGui import QPixmap
import os


class ValueItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)
        # -------------------------------- Attrs -----------------------------------
        self.position_item = parent
        self.key_item = parent.key_item
        self._value = 0
        self._scale = self.key_item.scale

        # -------------------------------- Setup -----------------------------------
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setPixmap(pixmap)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:

            value.setX(self.x())
            new_y = value.y() * self._scale
            value.setY(new_y)

            if not self.key_item.scene.bound_rect.contains(value):

                if value.y() < self.key_item.scene.bound_rect.top():
                    value.setY(self.key_item.scene.bound_rect.top())

                elif value.y() > self.key_item.scene.bound_rect.bottom():
                    value.setY(self.key_item.scene.bound_rect.bottom())

            new_y = value.y() / self._scale
            value.setY(new_y)

        return super().itemChange(change, value)
