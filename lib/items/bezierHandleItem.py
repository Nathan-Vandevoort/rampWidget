from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
import os


class BezierHandleItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)

        # ----------------------- Attributes ------------------------
        self._scene = parent.key_item.scene
        self._scale = parent._scale
        self._ramp_index = parent.key_item.ramp_index

        # ----------------------- Flags ----------------------------
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # ----------------------- Setup ----------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setPixmap(pixmap)
        self.setScale(.5)
        self.hide()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if self.parentItem().redrawCurveOnItemChange is True:
                self._scene.bezierHandleMovedSignal.emit(self._ramp_index)
                self._scene.redrawCurveSignal.emit()
        return super().itemChange(change, value)
