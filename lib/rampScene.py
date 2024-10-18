from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem
from PySide6.QtCore import Qt, QPointF, Slot, QRectF, Signal
from lib.utils import dummyLogger
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils
from lib.items import valueItem


class RampScene(QGraphicsScene):

    valueChangedSignal = Signal(int, float)
    positionChangedSignal = Signal(int, float)
    positionItemXChangedSignal = Signal(int, float)
    valueItemXChangedSignal = Signal(int, float)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- Signals ------------------------------------
        self.valueChangedSignal.connect(self.valueChangedSlot)
        self.positionChangedSignal.connect(self.positionChangedSlot)
        self.positionItemXChangedSignal.connect(self.positionItemXChangedSlot)
        self.valueItemXChangedSignal.connect(self.valueItemXChangedSlot)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 780, 380)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []

        # ------------------------- Prep ------------------------------------------
        self.setSceneRect(0, 0, 800, 400)
        self.addItem(QGraphicsRectItem(self.bound_rect))
        self.addKey(0, 0)
        self.addKey(1, 1)

    @Slot(int, float)
    def valueChangedSlot(self, item, x):
        pass

    @Slot(int, float)
    def positionChangedSlot(self, item, position):
        self.sort_keys()

    @Slot(int, float)
    def positionItemXChangedSlot(self, item, x):
        self.keys[item].value_item.setX(x)

    @Slot(int, float)
    def valueItemXChangedSlot(self, item, x):
        self.keys[item].position_item.setX(x)

    def sort_keys(self):
        #{key_expression(item): value_expression(item) for item in something if condition}
        reverse_key_dict = {self.keys[key]: key for key in self.keys}
        keys = [self.keys[key] for key in self.keys]
        keys.sort(key=lambda x: x.position)
        self.sorted_keys = [reverse_key_dict[key] for key in keys]

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        new_key = rampKey.RampKey(self, self.next_index)
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1

        self.addItem(new_key)
        self.sort_keys()

        return new_key

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.removeItem(self.keys[index])
            del self.keys[index]
            self.sort_keys()

    def mapXToPosition(self, x):
        return_val = ramp_utils.fit_range(x, self.bound_rect.left(), self.bound_rect.right(), 0, 1)
        return return_val

    def mapPositionToX(self, position):
        return_val = ramp_utils.fit_range(position, 0, 1, self.bound_rect.right(), self.bound_rect.left())
        return return_val

    def mapYToValue(self, y):
        return_val = ramp_utils.fit_range(y, self.bound_rect.top(), self.bound_rect.bottom(), 0, 1)
        return return_val

    def mapValueToY(self, value):
        return_val = ramp_utils.fit_range(value, 0, 1, self.bound_rect.top(), self.bound_rect.bottom())
        return return_val