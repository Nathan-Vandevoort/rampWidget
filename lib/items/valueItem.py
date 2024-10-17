from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF, Slot
from PySide6.QtGui import QPixmap
import os




class ValueItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)
        # -------------------------------- Attrs -----------------------------------
        self.key_item = parent
        self._value = 0
        self._scale = self.key_item.scale

        # -------------------------------- Setup -----------------------------------
        self.setFlags(QGraphicsItem.ItemIsSelectable)
        self.setFlags(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

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
        self._value = new_value

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:


            if not self.scene().bound_rect.contains(value):

                if value.x() < self.scene().bound_rect.left():
                    value.setX(self.scene().bound_rect.left())

                elif value.x() > self.scene().bound_rect.right():
                    value.setX(self.scene().bound_rect.right())

                if value.y() < self.scene().bound_rect.top():
                    value.setY(self.scene().bound_rect.top())

                elif value.y() > self.scene().bound_rect.bottom():
                    value.setY(self.scene().bound_rect.bottom())

        return super().itemChange(change, value)

    def setY(self, y):
        super().setY(y)
        self.value = self.scene().mapYToValue(y)

    def setX(self, x):
        super().setX(x)
        self.scene().valueItemXChangedSignal.emit(x)
