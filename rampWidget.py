from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtCore import QEvent, QRectF
import lib.rampScene as ramp_scene


class RampWidget(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.scene = ramp_scene.RampScene(parent=self)

    def resizeEvent(self, event):
        super().resizeEvent(event=event)
        self.scene.resizeScene()
