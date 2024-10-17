from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import Qt, QPointF
from lib.items import valueItem, positionItem
from lib.utils import utils as ramp_utils


class RampKey(QGraphicsItem):

    def __init__(self, scene, key_id, parent=None):
        super().__init__(parent=parent)

        # ------------------------------- Attrs --------------------------------
        self.key_type = 'bezier'
        self.scene = scene
        self.scale = .15
        self.key_id = key_id
        self.selection_offset = QPointF(0, 0)
        self.hovered = False
        self.selected_item = None

        # ------------------------------ Children -------------------------------
        self.position_item = positionItem.PositionItem(parent=self)
        self.value_item = valueItem.ValueItem(parent=self)

    def __repr__(self):
        return f'({self.key_id}, {self.position}, {self.value})'

    @property
    def value(self):
        return self.value_item.value

    @value.setter
    def value(self, new_value):
        self.value_item.value = new_value

    @property
    def position(self):
        return self.position_item.position

    @position.setter
    def position(self, new_value):
        self.position_item.position = new_value

    def drag(self, pos: QPointF):
        if self.selected_item is None:
            return

        elif self.selected_item == self.value_item:
            self.position = self.scene.mapXToPosition(pos.x() + self.selection_offset.x())
            self.value = self.scene.mapYToValue(pos.y() + self.selection_offset.y())
            return

        elif self.selected_item == self.position_item:
            self.position = self.scene.mapXToPosition(pos.x() + self.selection_offset.x())
            self.value = self.value
            return

    def deselect(self):
        self.selected_item = None

    def hoverEnterEvent(self, event):
        self.hovered = True
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.hovered = False
        super().hoverLeaveEvent(event)

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.hovered is True:
            scene_pos = event.scenePos()

            if self.value_item.contains(self.value_item.mapFromScene(scene_pos)):
                self.selected_item = self.value_item

            elif self.position_item.contains(self.position_item.mapFromScene(scene_pos)):
                self.selected_item = self.position_item

            if self.selected_item is not None:
                self.selection_offset = self.selected_item.scenePos() - event.scenePos()
                self.scene.grabbed_item = self

            super().mousePressEvent(event)

    def pos(self):
        return QPointF(self.position * self.scene.target_width, (1 - self.value) * self.scene.target_height)



    def setInteractable(self, enable):
        pass

