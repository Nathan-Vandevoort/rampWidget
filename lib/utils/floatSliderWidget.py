from PySide2.QtWidgets import QDoubleSpinBox, QSlider, QWidget
from PySide2.QtCore import Qt
#try:
#    from PySide6.QtWidgets import QDoubleSpinBox, QSlider, QWidget
#    from PySide6.QtCore import Qt
#except ImportError:
#    from PySide2.QtWidgets import QDoubleSpinBox, QSlider, QWidget
#    from PySide2.QtCore import Qt


class FloatSliderWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.value_box = QDoubleSpinBox(parent=self)
        self.slider = QSlider(Qt.Horizontal, parent=self)

