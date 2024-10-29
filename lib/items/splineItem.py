try:
    from PySide6.QtWidgets import QGraphicsPathItem
    from PySide6.QtCore import Qt
    from PySide6.QtGui import QPainterPath, QPen, QColor
except ImportError:
    from PySide2.QtWidgets import QGraphicsPathItem
    from PySide2.QtCore import Qt
    from PySide2.QtGui import QPainterPath, QPen, QColor


class SplineItem(QGraphicsPathItem):

    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.path = QPainterPath()
        self._scene = scene
        self.setPen(QPen(QColor(40, 40, 40), 3, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))
        self.setPath(self.path)

    def draw(self):
        self.path.clear()
        for i, key in enumerate(self._scene.sorted_keys):
            item = self._scene.keys[key]
            my_item = self._scene.keys[self._scene.sorted_keys[i - 1]]
            pos = item.keyScenePos()
            if i == 0:
                self.path.moveTo(pos.x(), pos.y())
                continue

            if my_item.key_type == 'linear':
                self.path.lineTo(pos)

            elif my_item.key_type == 'bezier':
                ctl1 = my_item.rightControlPointPos()
                ctl2 = item.leftControlPointPos()
                self.path.cubicTo(ctl1, ctl2, pos)

            elif my_item.key_type == 'constant':
                pass

        self.setPath(self.path)

    def paint(self, painter, option, widget=None):
        painter.save()
        painter.setClipRect(self._scene.bound_rect)
        super().paint(painter, option, widget=widget)
        painter.restore()


