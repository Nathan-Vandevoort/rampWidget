from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPixmap
import os


class BezierHandleItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)

        # ----------------------- Attributes ------------------------
        self._scene = parent.key_item.scene
        self._scale = parent._scale
        self._ramp_index = parent.key_item.ramp_index
        self.parent = parent
        self.hovered = False
        self.targetPos = self.pos()

        # ----------------------- Flags ----------------------------
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # ----------------------- Setup ----------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'bezierHandleItem_02.svg'))
        self.setOffset(-50, -50)
        self.setPixmap(pixmap)
        self.setScale(.5)
        self.hide()

    def confineToNeighbours(self):
        if self._ramp_index <= 1:
            return

        self.setPos(self.targetPos)
        neighbours = self._scene.getNeighbourKeys(self._ramp_index)
        if neighbours:
            left_bound = self._scene.keys[neighbours[0]].value_item.scenePos().x()
            right_bound = self._scene.keys[neighbours[1]].value_item.scenePos().x()
            pos = self.scenePos().x()

            if pos > right_bound:
                self.setX(right_bound)

            elif pos < left_bound:
                self.setX(left_bound)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            if self.parentItem().redrawCurveOnItemChange is True:
                value_scene = self.parent.mapToParent(value)

                if self._scene.prepared:
                    neighbours = self._scene.getNeighbourKeys(self._ramp_index)
                    if neighbours:
                        left_bound = self._scene.keys[neighbours[0]].value_item.scenePos().x()
                        right_bound = self._scene.keys[neighbours[1]].value_item.scenePos().x()
                        if value_scene.x() < left_bound:
                            value_scene.setX(left_bound + 1)
                        elif value_scene.x() > right_bound:
                            value_scene.setX(right_bound - 1)

                value = self.parent.mapFromParent(value_scene)
                if self.hovered:
                    self.targetPos = value
                self._scene.bezierHandleMovedSignal.emit(self._ramp_index)
                self._scene.redrawCurveSignal.emit()

        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        self.hovered = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        super().hoverLeaveEvent(event)
