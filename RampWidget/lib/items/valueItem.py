try:
    from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsEllipseItem
    from PySide6.QtCore import QPointF
    from PySide6.QtGui import QPixmap
except ImportError:
    from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem, QGraphicsEllipseItem
    from PySide2.QtCore import QPointF
    from PySide2.QtGui import QPixmap
from RampWidget.lib.items import bezierHandleItem, bezierHandleLineItem
import os


class ValueItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent)
        # -------------------------------- Attrs -----------------------------------
        self.key_item = parent
        self._parent_scale = self.key_item.scale
        self._scale = .5
        self.item_type = 'value'
        self.hovered = False
        self.focused = False
        self.redrawCurveOnItemChange = True

        # -------------------------------- Setup -----------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        self.unselected_pixmap = QPixmap(os.path.join(images_dir, 'valueItem_02.svg'))
        self.selected_pixmap = QPixmap(os.path.join(images_dir, 'valueItem_selected_01.svg'))

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # ------------------------------- Children ---------------------------------
        self.bezier_handle_line = bezierHandleLineItem.BezierHandleLineItem(parent=self)
        self.bezier_handles = []
        self.createBezierHandles()
        self.showBezierHandles()
        self.bezier_handle_line.draw()

        # -------------------------------- Display ---------------------------------
        self.setOffset(-128, -128)
        self.setScale(self._scale * self._parent_scale)
        self.setPixmap(self.unselected_pixmap)

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
        new_handle.moveBy(-160, 0)
        new_handle.hovered = False  # I have to set hovered to make the target Pos set
        self.bezier_handles.append(new_handle)

        new_handle = bezierHandleItem.BezierHandleItem(self)
        new_handle.hovered = True
        new_handle.moveBy(160, 0)
        new_handle.hovered = False
        self.bezier_handles.append(new_handle)

    def setFocused(self, enable: bool):
        self.focused = enable
        if enable is True:
            self.key_item.position_item.setFocused(True)
            self.setPixmap(self.selected_pixmap)
        else:
            self.key_item.position_item.setFocused(False)
            self.setPixmap(self.unselected_pixmap)

    def confineBezierHandlesToNeighbours(self):
        self.bezier_handles[0].confineToNeighbours()
        self.bezier_handles[1].confineToNeighbours()

    def hideBezierHandles(self):
        self.bezier_handles[0].hide()
        self.bezier_handles[1].hide()
        self.bezier_handle_line.hide()

    def showBezierHandles(self):
        self.bezier_handles[0].show()
        self.bezier_handles[1].show()
        self.bezier_handle_line.show()

    def sortBezierHandles(self):
        self.bezier_handles.sort(key=lambda x: x.x())

    def removeHandles(self):
        self.key_item.scene.removeItem(self.bezier_handle_line)
        handle = self.bezier_handles.pop()
        self.key_item.scene.removeItem(handle)
        handle = self.bezier_handles.pop()
        self.key_item.scene.removeItem(handle)

    def setPosFromUserSpace(self, position, value):
        x = self.key_item.scene.mapPositionToX(position)
        y = self.key_item.scene.mapValueToY(value)
        self.setPos(x, y)
        self.itemChange(QGraphicsItem.ItemPositionChange, QPointF(x, y))

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

            if self.hovered is True or self.focused is True:
                self.key_item.scene.valueItemXChangedSignal.emit(self.key_item.ramp_index, value.x())

            if self.redrawCurveOnItemChange is True:
                self.key_item.scene.redrawCurveSignal.emit()

            self.key_item.scene.itemMovedSignal.emit(self, QPointF(self.key_item.scene.mapXToPosition(value.x()), self.key_item.scene.mapYToValue(value.y())))

        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.hovered = True

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.hovered = False

    def setSelected(self, selected):
        if selected:
            if self.key_item.key_type == 'bezier':
                self.showBezierHandles()

        super().setSelected(selected)
