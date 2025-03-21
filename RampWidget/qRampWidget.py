try:
    from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout, QGraphicsItem
    from PySide6.QtCore import Qt, Slot, QPointF, Signal
except ImportError:
    from PySide2.QtWidgets import QWidget, QSlider, QVBoxLayout, QGraphicsItem
    from PySide2.QtCore import Qt, Slot, QPointF, Signal
from RampWidget import rampView
from RampWidget.lib.utils import floatSliderWidget
from RampWidget.lib.items import positionItem, bezierHandleItem


class QRampWidget(QWidget):

    keyAdded = Signal(QGraphicsItem, str)  # the ramp key which was added
    keyRemoved = Signal(int)  # The index of the key which was removed
    valueChanged = Signal(QGraphicsItem)  # Item
    orderChanged = Signal(tuple)  # a tuple containing the new sorted order
    interpolationChanged = Signal(QGraphicsItem, str)  # the item which changed and the new interpolation

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # ---------------------------------- Attribs ---------------------------
        self.focused_item = None

        # ---------------------------------- Widgets ----------------------------
        self.ramp_view = rampView.RampView(self)
        self.position_slider = floatSliderWidget.FloatSliderWidget(parent=self)
        self.position_slider.setPrefix('Position: ')
        self.value_slider = floatSliderWidget.FloatSliderWidget(parent=self)
        self.value_slider.setPrefix('Value: ')

        # -------------------------------- Layouts -------------------------------
        self.main_layout = QVBoxLayout()

        # ------------------------------- Connections -----------------------------
        self.ramp_view.focusItemChanged.connect(self.focusItemChangedSlot)
        self.ramp_view.itemMoved.connect(self.itemMovedCarrier)
        self.position_slider.valueChanged.connect(self.keySliderValueChangedSlot)
        self.value_slider.valueChanged.connect(self.keySliderValueChangedSlot)
        self.ramp_view.sortChanged.connect(self.orderChangedCarrier)
        self.ramp_view.keyRemoved.connect(self.keyRemovedCarrier)
        self.ramp_view.keyAdded.connect(self.keyAddedCarrier)
        self.ramp_view.interpolationChanged.connect(self.interpolationChangedCarrier)

        # ------------------------------- Set Layouts -----------------------------
        self.main_layout.addWidget(self.ramp_view)
        self.main_layout.addWidget(self.position_slider)
        self.main_layout.addWidget(self.value_slider)

        # ------------------------------- Prep -------------------------------------
        self.setLayout(self.main_layout)

    @Slot(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    def focusItemChangedSlot(self, focus_item, old_focus_item, reason):
        if reason == Qt.FocusReason.MouseFocusReason:
            focused = True
            if focus_item is None:  # dont lose focus when the user is clicking a slider or button
                return

            if isinstance(focus_item, positionItem.PositionItem):
                focus_item = focus_item.key_item.value_item  # if you are focused on the position item switch focus to value item

            if old_focus_item is not None:
                old_focus_item.setFocused(False)

            if self.focused_item is not None:
                self.focused_item.setFocused(False)

            focus_item.setFocused(focused)
            self.focused_item = focus_item
            self.setSlidersToFocusedItem()
        else:
            if old_focus_item is not None:
                old_focus_item.setFocused(False)
            self.focused_item = None

    @Slot(QGraphicsItem, QPointF)
    def itemMovedCarrier(self, item, cords):
        position = cords.x()
        value = cords.y()

        self.valueChanged.emit(item.key_item)

        if item == self.focused_item:
            self.position_slider.setValue(position, ignore_range=True)
            self.value_slider.setValue(value, ignore_range=True)

    @Slot(float)
    def keySliderValueChangedSlot(self):
        if self.focused_item is None:
            return
        self.focused_item.setPosFromUserSpace(self.position_slider.value, self.value_slider.value)

    @Slot(tuple)
    def orderChangedCarrier(self, new_order):
        self.orderChanged.emit(new_order)

    @Slot(QGraphicsItem, str)
    def keyAddedCarrier(self, new_key, status):
        self.keyAdded.emit(new_key, status)

    @Slot(int)
    def keyRemovedCarrier(self, ramp_index):
        self.keyRemoved.emit(ramp_index)

    @Slot(QGraphicsItem, str)
    def interpolationChangedCarrier(self, item, interpolation):
        self.interpolationChanged.emit(item, interpolation)

    def setSlidersToFocusedItem(self):
        if self.focused_item is None:
            return

        position = self.focused_item.position
        value = self.focused_item.value

        self.position_slider.setValue(position, ignore_range=True)
        self.value_slider.setValue(value, ignore_range=True)

    def setSceneDimensions(self, width, height):
        self.ramp_view.controller.setSceneDimensions(width, height)

    def setScenePadding(self, left, top, right, bottom):
        self.ramp_view.controller.setScenePadding(left, top, right, bottom)

    def start(self):
        self.ramp_view.controller.initializeRamp()

    def addKey(self, position, value, ramp_index=None):
        return self.ramp_view.scene.addKey(position, value, ramp_index=ramp_index)

    def removeKey(self, ramp_index):
        self.ramp_view.scene.removeKey(ramp_index)

    def blockSignals(self, b):
        super().blockSignals(b)
        self.ramp_view.scene.blockSignals(b)

    def setNextIndex(self, index):
        self.ramp_view.scene.next_index = index

    def clearKeys(self):
        keys = self.ramp_view.scene.keys.copy()
        for key in keys:
            if key <= 1:  # skip start and end keys
                continue
            self.removeKey(key)
