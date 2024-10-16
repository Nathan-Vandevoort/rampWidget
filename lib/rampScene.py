from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem
from PySide6.QtCore import Qt, QPointF, Slot, QRectF
from lib.utils import dummyLogger
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils
from lib.items import valueItem


class RampScene(QGraphicsScene):

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 780, 380)

        # ------------------------- Prep ------------------------------------------
        self.setSceneRect(0, 0, 800, 400)
        self.addItem(QGraphicsRectItem(self.bound_rect))
        self.addItem(rampKey.RampKey(self))