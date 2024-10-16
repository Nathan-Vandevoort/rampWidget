from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import Qt, QPointF, QRectF
from lib.items import valueItem, positionItem
from lib.utils import utils as ramp_utils


class RampKey(QGraphicsItem):

    def __init__(self, scene, parent=None):
        super().__init__(parent=parent)

        # ------------------------------- Attrs --------------------------------
        self.key_type = 'bezier'
        self.item_type = 'RAMPKEY'
        self.scale = .25
        self.scene = scene

        # ------------------------------ Children -------------------------------
        self.position_item = positionItem.PositionItem(parent=self)
        self.value_item = valueItem.ValueItem(parent=self.position_item)

    @property
    def value(self):
        return self.value_item.value

    @value.setter
    def value(self, new_value: float):
        self.value_item.value = new_value

    @property
    def position(self):
        return self.position_item.position

    @position.setter
    def position(self, new_value: float):
        self.position_item.position = new_value

    def boundingRect(self):
        return self.childrenBoundingRect()

    def paint(self, painter, option, widget=None):
        pass



