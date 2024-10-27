try:
    from PySide6.QtWidgets import QGraphicsView, QGraphicsItem
    from PySide6.QtCore import Signal, Slot, Qt
    from PySide6.QtGui import QPainter
except ImportError:
    from PySide2.QtWidgets import QGraphicsView, QGraphicsItem
    from PySide2.QtCore import Signal, Slot, Qt
    from PySide2.QtGui import QPainter
import lib.rampScene as ramp_scene
from lib import rampController


class RampView(QGraphicsView):

    focusItemChanged = Signal(QGraphicsItem, QGraphicsItem, Qt.FocusReason)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scene = ramp_scene.RampScene(parent=self)
        self.controller = rampController.RampController(self.scene, parent=self)
        self.scene.debugSignal.connect(self.controller.debugSlot)
        self.scene.focusItemChanged.connect(self.focusItemChangedCarrier)

        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(self.scene)

    @Slot(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    def focusItemChangedCarrier(self, item, old_item, reason):
        self.focusItemChanged.emit(item, old_item, reason)


