from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem
from PySide6.QtCore import Qt, QPointF, Slot, QRectF, Signal
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils


class RampScene(QGraphicsScene):

    positionItemXChangedSignal = Signal(int, float)
    valueItemXChangedSignal = Signal(int, float)
    redrawCurveSignal = Signal()
    valueChangedSignal = Signal(int, QPointF)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- Signals ------------------------------------
        self.positionItemXChangedSignal.connect(self.positionItemXChangedSlot)
        self.valueItemXChangedSignal.connect(self.valueItemXChangedSlot)
        self.redrawCurveSignal.connect(self.redrawCurveSlot)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 780, 380)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []
        self.setSceneRect(0, 0, 800, 400)
        self.start_key = None
        self.end_key = None

        # ------------------------- Children -------------------------------------
        self.spline_item = splineItem.SplineItem(scene=self)
        self.start_key = self.addKey(-.1, 0)
        self.start_key.forceSetPosition(self.sceneRect().left())
        self.start_key.redrawCurveOnItemChange(False)
        self.start_key.hide()
        self.end_key = self.addKey(1.1, 1)
        self.end_key.forceSetPosition(self.sceneRect().right())
        self.end_key.redrawCurveOnItemChange(False)
        self.end_key.hide()

        # ------------------------- Prep ------------------------------------------
        self.addItem(QGraphicsRectItem(self.bound_rect))
        self.addKey(0, 0)
        self.addKey(1, 1)
        self.addItem(self.spline_item)
        self.redrawCurveSlot()

    @Slot(int, float)
    def positionItemXChangedSlot(self, item, x):
        self.keys[item].value_item.setX(x)
        self.sort_keys()

    @Slot(int, float)
    def valueItemXChangedSlot(self, item, x):
        self.keys[item].position_item.setX(x)
        self.sort_keys()

    @Slot()
    def redrawCurveSlot(self):
        self.alignEndKeys()
        self.spline_item.draw()

    def sort_keys(self):
        if self.start_key and self.end_key:
            reverse_key_dict = {self.keys[key]: key for key in self.keys}
            keys = [self.keys[key] for key in self.keys if self.keys[key] != self.start_key and self.keys[key] != self.end_key]
            keys.sort(key=lambda x: x.position)
            keys.insert(0, self.start_key)
            keys.append(self.end_key)
            self.sorted_keys = [reverse_key_dict[key] for key in keys]

    def alignEndKeys(self):
        if len(self.sorted_keys) > 2:
            self.start_key.value = self.keys[self.sorted_keys[1]].value
            self.end_key.value = self.keys[self.sorted_keys[-2]].value

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
        return_val = ramp_utils.fit_range(position, 0, 1, self.bound_rect.left(), self.bound_rect.right())
        return return_val

    def mapYToValue(self, y):
        return_val = ramp_utils.fit_range(y, self.bound_rect.bottom(), self.bound_rect.top(), 0, 1)
        return return_val

    def mapValueToY(self, value):
        return_val = ramp_utils.fit_range(value, 1, 0, self.bound_rect.top(), self.bound_rect.bottom())
        return return_val

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.scenePos()
            self.addKey(self.mapXToPosition(pos.x()), self.mapYToValue(pos.y()))
            self.redrawCurveSlot()
        super().mouseDoubleClickEvent(event)