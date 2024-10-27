try:
    from PySide6.QtWidgets import QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QAbstractSpinBox
    from PySide6.QtCore import Qt, Signal, Slot
except ImportError:
    from PySide2.QtWidgets import QDoubleSpinBox, QSlider, QWidget, QHBoxLayout, QAbstractSpinBox
    from PySide2.QtCore import Qt, Signal, Slot


class FloatSliderWidget(QWidget):

    valueChanged = Signal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # ------------------------------ Attribs ------------------------------------
        self.min = 0
        self.max = 1
        self.value = 0
        self._slider_scale_factor = 100

        # ------------------------------ Child widgets -------------------------------
        self.value_box = QDoubleSpinBox(parent=self)
        self.value_box.setButtonSymbols(QAbstractSpinBox.NoButtons)
        self.slider = QSlider(Qt.Horizontal, parent=self)

        # ------------------------------ Connections --------------------------------
        self.value_box.valueChanged.connect(self.spinBoxValueChangedSlot)
        self.slider.valueChanged.connect(self.sliderValueChangedSlot)

        # ------------------------------ Layout --------------------------------------
        self.layout = QHBoxLayout()
        self.layout.addWidget(self.value_box)
        self.layout.addWidget(self.slider)
        self.setLayout(self.layout)

        # ----------------------------- Prep ------------------------------------------
        self.setRange(0, 1)

    @Slot(float)
    def spinBoxValueChangedSlot(self, new_value):
        value = new_value
        self.value = value
        self.slider.setValue(value * self._slider_scale_factor)
        self.valueChanged.emit(value)

    @Slot(float)
    def sliderValueChangedSlot(self, new_value):
        value = new_value / self._slider_scale_factor
        self.value = value
        self.value_box.setValue(value)
        self.valueChanged.emit(value)

    def setRange(self, min_value: float, max_value: float):
        self.min = min_value
        self.max = max_value

        self.value_box.setRange(min_value, max_value)
        self.slider.setRange(int(min_value), int(max_value) * self._slider_scale_factor)

    def setPrefix(self, prefix: str):
        self.value_box.setPrefix(prefix)

    def setSuffix(self, suffix: str):
        self.value_box.setSuffix(suffix)

    def setValue(self, new_value): # Let the slider update the spin box an internal values
        if new_value > self.max:
            self.value_box.setValue(self.max)
        elif new_value < self.min:
            self.value_box.setValue(self.min)
        else:
            self.value_box.setValue(new_value)



