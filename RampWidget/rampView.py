try:
    from PySide6.QtWidgets import QGraphicsView, QGraphicsItem
    from PySide6.QtCore import Signal, Slot, Qt, QPointF
    from PySide6.QtGui import QPainter
except ImportError:
    from PySide2.QtWidgets import QGraphicsView, QGraphicsItem
    from PySide2.QtCore import Signal, Slot, Qt, QPointF
    from PySide2.QtGui import QPainter
import RampWidget.lib.rampScene as ramp_scene
from RampWidget.lib import rampController


class RampView(QGraphicsView):

    focusItemChanged = Signal(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    itemMoved = Signal(QGraphicsItem, QPointF)
    keyAdded = Signal(QGraphicsItem, str)
    keyRemoved = Signal(int)
    sortChanged = Signal(tuple)
    interpolationChanged = Signal(QGraphicsItem, str)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scene = ramp_scene.RampScene(parent=self)
        self.controller = rampController.RampController(self.scene, parent=self)
        self.scene.debugSignal.connect(self.controller.debugSlot)
        self.scene.keyAddedSignal.connect(self._keyAddedCarrier)
        self.scene.keyRemovedSignal.connect(self._keyRemovedCarrier)
        self.scene.focusItemChanged.connect(self._focusItemChangedCarrier)
        self.scene.itemMovedSignal.connect(self._itemMovedCarrier)
        self.scene.sortChangedSignal.connect(self._sortChangedCarrier)
        self.scene.interpolationChanged.connect(self._interpolationChangedCarrier)

        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(self.scene)

    @Slot(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    def _focusItemChangedCarrier(self, item, old_item, reason):
        self.focusItemChanged.emit(item, old_item, reason)

    @Slot(QGraphicsItem, QPointF)
    def _itemMovedCarrier(self, item, new_cords):
        self.itemMoved.emit(item, new_cords)

    @Slot(QGraphicsItem, str)
    def _keyAddedCarrier(self, item, status):
        self.keyAdded.emit(item, status)

    @Slot(int)
    def _keyRemovedCarrier(self, index):
        self.keyRemoved.emit(index)

    @Slot(tuple)
    def _sortChangedCarrier(self, new_sort):
        self.sortChanged.emit(new_sort)

    @Slot(QGraphicsItem, str)
    def _interpolationChangedCarrier(self, item, interpolation):
        self.interpolationChanged.emit(item, interpolation)
