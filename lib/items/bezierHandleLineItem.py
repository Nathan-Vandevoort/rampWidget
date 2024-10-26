from PySide6.QtWidgets import QGraphicsPathItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainterPath, QPen, QColor


class BezierHandleLineItem(QGraphicsPathItem):

    def __init__(self, parent):
        super().__init__(parent=parent)
        self.key_item = parent.key_item
        self.value_item = parent
        self.path = QPainterPath()
        self.setPen(QPen(QColor(0, 0, 0), 10, Qt.DotLine, Qt.FlatCap, Qt.MiterJoin))
        self.setPath(self.path)

    def draw(self):
        self.path.clear()
        start_pt = self.value_item.bezier_handles[0]
        end_pt = self.value_item.bezier_handles[1]
        self.path.moveTo(start_pt.x(), start_pt.y())
        self.path.lineTo(0, 0)
        self.path.lineTo(end_pt.x(), end_pt.y())
        self.setPath(self.path)