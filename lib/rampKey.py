from PySide6.QtWidgets import QGraphicsItemGroup
from PySide6.QtCore import Qt, QPointF
from lib.items import valueItem, positionItem
from lib.utils import utils as ramp_utils


class RampKey(QGraphicsItemGroup):

    def __init__(self, scene, key_id, parent=None):
        super().__init__(parent=parent)

        # ------------------------------- Attrs --------------------------------
        self.key_type = 'bezier'
        self.scene = scene
        self.scale = .15
        self.key_id = key_id

        # ------------------------------ Children -------------------------------
        self.position_item = positionItem.PositionItem(parent=self)
        self.value_item = valueItem.ValueItem(parent=self)

        self.addToGroup(self.position_item)
        self.addToGroup(self.value_item)

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
