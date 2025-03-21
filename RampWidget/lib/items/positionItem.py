try:
    from PySide6.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
    from PySide6.QtGui import QPixmap
except ImportError:
    from PySide2.QtWidgets import QGraphicsPixmapItem, QGraphicsItem
    from PySide2.QtGui import QPixmap
import os


class PositionItem(QGraphicsPixmapItem):

    def __init__(self, parent):
        super().__init__(parent=parent)

        # -------------------------------- Attrs -----------------------------------
        self.key_item = parent
        self._scale = self.key_item.scale * 1.5
        self.hovered = False
        self.focused = False

        # -------------------------------- Setup -----------------------------------
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setFlag(QGraphicsItem.ItemIsMovable, True)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges, True)

        # -------------------------------- Display ---------------------------------
        images_dir = os.path.join(os.path.dirname(__file__), os.pardir, 'images')
        self.unselected_pixmap = QPixmap(os.path.join(images_dir, 'positionItem_02.svg'))
        self.selected_pixmap = QPixmap(os.path.join(images_dir, 'positionItem_selected_01.svg'))

        self.setOffset(-50, -25)
        self.setScale(self._scale)
        self.setPixmap(self.unselected_pixmap)
        self.hide()

    def setFocused(self, enable: bool):
        self.focused = enable
        if enable is True:
            self.setPixmap(self.selected_pixmap)
        else:
            self.setPixmap(self.unselected_pixmap)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:

            value.setY(self.key_item.scene.bound_rect.bottom())

            if not self.key_item.scene.bound_rect.contains(value) and self.key_item.item_type == 'RAMPKEY':

                if value.x() < self.key_item.scene.bound_rect.left():
                    value.setX(self.key_item.scene.bound_rect.left())

                elif value.x() > self.key_item.scene.bound_rect.right():
                    value.setX(self.key_item.scene.bound_rect.right())

            if self.hovered:
                self.key_item.scene.positionItemXChangedSignal.emit(self.key_item.ramp_index, value.x())
            self.key_item.scene.redrawCurveSignal.emit()
        return super().itemChange(change, value)

    def hoverEnterEvent(self, event):
        super().hoverEnterEvent(event)
        self.setScale(self._scale * 1.1)
        self.hovered = True

    def hoverLeaveEvent(self, event):
        super().hoverLeaveEvent(event)
        self.setScale(self._scale)
        self.hovered = False
