try:
    from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout, QGraphicsItem
    from PySide6.QtCore import Qt, Slot
except ImportError:
    from PySide2.QtWidgets import QWidget, QSlider, QVBoxLayout, QGraphicsItem
    from PySide2.QtCore import Qt, Slot
import rampView
from lib.utils import floatSliderWidget
from lib.items import positionItem


class RampWidget(QWidget):

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

        # ------------------------------- Set Layouts -----------------------------
        self.main_layout.addWidget(self.ramp_view)
        self.main_layout.addWidget(self.position_slider)
        self.main_layout.addWidget(self.value_slider)

        # ------------------------------- Prep -------------------------------------
        self.setLayout(self.main_layout)

    @Slot(QGraphicsItem, QGraphicsItem, Qt.FocusReason)
    def focusItemChangedSlot(self, focus_item, old_focus_item, reason):
        if reason == Qt.FocusReason.MouseFocusReason:
            if isinstance(focus_item, positionItem.PositionItem):
                focus_item = focus_item.key_item.value_item # if you are focused on the position item switch focus to value item
            self.focused_item = focus_item
            self.setSlidersToFocusedItem()

    def setSlidersToFocusedItem(self):
        if self.focused_item is None:
            return

        position = self.focused_item.position
        value = self.focused_item.value

        self.position_slider.setValue(position)
        self.value_slider.setValue(value)
