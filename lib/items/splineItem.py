from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainterPath, QPen, QColor
import time

class SplineItem(QGraphicsPathItem):

    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.path = QPainterPath()
        self._scene = scene
        self.setPen(QPen(QColor(0, 0, 0), 5, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        self.setPath(self.path)

    def draw(self):
        self.path.clear()
        for i, key in enumerate(self._scene.sorted_keys):
            item = self._scene.keys[key]
            key_type = item.key_type
            pos = item.keyScenePos()
            if i == 0:
                self.path.moveTo(pos.x(), pos.y())
                continue

            if key_type == 'linear':
                self.path.lineTo(pos)

            elif key_type == 'bezier':
                my_item = self._scene.keys[self._scene.sorted_keys[i - 1]]
                ctl1 = my_item.rightControlPointPos()
                ctl2 = item.leftControlPointPos()
                self.path.cubicTo(ctl1, ctl2, pos)

            elif key_type == 'constant':
                pass

        self.setPath(self.path)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setClipRect(self._scene.bound_rect)
        super().paint(painter, option, widget=widget)
        painter.restore()


