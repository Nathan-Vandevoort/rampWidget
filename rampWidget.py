from PySide6.QtWidgets import QGraphicsView
from PySide6.QtGui import QPainter
import lib.rampScene as ramp_scene
from lib import rampController


class RampWidget(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scene = ramp_scene.RampScene(parent=self)
        self.controller = rampController.RampController(self.scene, parent=self)

        self.target_width = 800
        self.target_height = 400

        self.setRenderHint(QPainter.Antialiasing)
        self.setScene(self.scene)

        # ------------------------------------ Sandbox ------------------------------------------