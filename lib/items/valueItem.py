from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsEllipseItem
from PySide6.QtCore import Qt, QPointF, Slot
from PySide6.QtGui import QPixmap
from lib.items import bezierHandleItem
import os


class ValueItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)
        # -------------------------------- Attrs -----------------------------------
        self.key_item = parent
        self._scale = self.key_item.scale
        self.hovered = False
        self.redrawCurveOnItemChange = True

        # -------------------------------- Setup -----------------------------------
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # ------------------------------- Children ---------------------------------
        self.bezier_handles = []
        self.createBezierHandles()
        self.showBezierHandles()

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        pixmap = QPixmap(os.path.join(images_dir, 'key_dot_01.png'))
        self.setOffset(-256, -256)
        self.setScale(self._scale)
        self.setPixmap(pixmap)

    @property
    def value(self):
        return self.key_item.scene.mapYToValue(self.y())

    @value.setter
    def value(self, new_value):
        self.setY(self.key_item.scene.mapValueToY(new_value))

    @property
    def position(self):
        return self.key_item.scene.mapXToPosition(self.x())

    @position.setter
    def position(self, new_value):
        if new_value > 1:
            new_value = 1
        elif new_value < 0:
            new_value = 0
        self.setX(self.key_item.scene.mapPositionToX(new_value))

    def createBezierHandles(self):
        new_handle = bezierHandleItem.BezierHandleItem(self)
        new_handle.hovered = True
        new_handle.moveBy(-80, 0)
        new_handle.hovered = False # I have to set hovered to make the target Pos set
        self.bezier_handles.append(new_handle)

        new_handle = bezierHandleItem.BezierHandleItem(self)
        new_handle.hovered = True
        new_handle.moveBy(80, 0)
        new_handle.hovered = False
        self.bezier_handles.append(new_handle)

    def confineBezierHandlesToNeighbours(self):
        self.bezier_handles[0].confineToNeighbours()
        self.bezier_handles[1].confineToNeighbours()

    def hideBezierHandles(self):
        self.bezier_handles[0].hide()
        self.bezier_handles[1].hide()

    def showBezierHandles(self):
        self.bezier_handles[0].show()
        self.bezier_handles[1].show()

    def sortBezierHandles(self):
        self.bezier_handles.sort(key=lambda x: x.x())

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:

            if not self.key_item.scene.bound_rect.contains(value) and self.key_item.item_type == 'RAMPKEY':

                if value.x() < self.key_item.scene.bound_rect.left():
                    value.setX(self.key_item.scene.bound_rect.left())

                elif value.x() > self.key_item.scene.bound_rect.right():
                    value.setX(self.key_item.scene.bound_rect.right())

                if value.y() < self.key_item.scene.bound_rect.top():
                    value.setY(self.key_item.scene.bound_rect.top())

                elif value.y() > self.key_item.scene.bound_rect.bottom():
                    value.setY(self.key_item.scene.bound_rect.bottom())

            if self.hovered:
                self.key_item.scene.valueItemXChangedSignal.emit(self.key_item.ramp_index, value.x())

            if self.redrawCurveOnItemChange is True:
                self.key_item.scene.redrawCurveSignal.emit()

        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        #if self.key_item.key_type == 'bezier':
            #self.showBezierHandles()
        self.hovered = True

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        #self.hideBezierHandles()
        self.hovered = False

    def setSelected(self, selected):
        if selected:
            if self.key_item.key_type == 'bezier':
                self.showBezierHandles()

        super().setSelected(selected)
