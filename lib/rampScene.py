from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem
from PySide6.QtCore import Qt, QPointF, Slot, QRectF, Signal
from lib.utils import dummyLogger
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils
from lib.items import valueItem


class RampScene(QGraphicsScene):

    valueChangedSignal = Signal(float)
    positionChangedSignal = Signal(float)

    valueItemXChangedSignal = Signal(float)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 780, 380)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []

        # ------------------------- Prep ------------------------------------------
        self.setSceneRect(0, 0, 800, 400)
        self.addItem(QGraphicsRectItem(self.bound_rect))
        self.addItem(rampKey.RampKey(self))

    def addKey(self, position=0, value=0):


    def mapXToPosition(self, x):
        return_val = ramp_utils.fit_range(x, self.bound_rect.left(), self.bound_rect.right(), 0, 1)
        return return_val

    def mapPositionToX(self, position):
        return_val = ramp_utils.fit_range(position, 0, 1, self.bound_rect.left(), self.bound_rect.right())
        return return_val

    def mapYToValue(self, y):
        return_val = ramp_utils.fit_range(y, self.bound_rect.top(), self.bound_rect.bottom(), 0, 1)
        return return_val

    def mapValueToY(self, value):
        return_val = ramp_utils.fit_range(value, 0, 1, self.bound_rect.top(), self.bound_rect.bottom())
        return return_val