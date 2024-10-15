from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainterPath, QPen, QColor, QPainter

class SplineItem(QGraphicsPathItem):

    def __init__(self, parent=None, scene=None):
        super().__init__(parent=parent)

        self.path = QPainterPath()
        self._scene = scene

        self.setPath(self.path)

    def draw(self):
        self.path.clear()
        for i, key in enumerate(self._scene.sorted_keys):
            pos = self._scene.keys[key].pos()
            if i == 0:
                self.path.moveTo(pos.x(), pos.y())
                continue
            self.path.lineTo(pos.x(), pos.y())
        self.setPath(self.path)
