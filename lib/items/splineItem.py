from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainterPath, QPen, QColor

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
            position = item.position
            value = item.value
            pos = QPointF(self._scene.mapPositionToScene(position), self._scene.mapValueToScene(value))
            if i == 0:
                self.path.moveTo(pos.x(), pos.y())
                continue
            self.path.lineTo(pos.x(), pos.y())
        self.setPath(self.path)

