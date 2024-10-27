try:
    from PySide6.QtWidgets import QWidget, QSlider, QVBoxLayout
    from PySide6.QtCore import Qt
except ImportError:
    from PySide2.QtWidgets import QWidget, QSlider, QVBoxLayout
    from PySide2.QtCore import Qt
import rampView


class RampWidget(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        # ---------------------------------- Widgets ----------------------------
        self.ramp_view = rampView.RampView(self)
        #self.position_slider = QSlider(Qt.Horizontal, parent=self)
        #self.value_slider = QSlider(Qt.Horizontal, parent=self)

        # -------------------------------- Layouts -------------------------------
        self.main_layout = QVBoxLayout()

        # ------------------------------- Set Layouts -----------------------------
        self.main_layout.addWidget(self.ramp_view)
        #self.main_layout.addWidget(self.position_slider)
        #self.main_layout.addWidget(self.value_slider)

        # ------------------------------- Prep -------------------------------------
        self.setLayout(self.main_layout)

