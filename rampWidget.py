from PySide6.QtWidgets import QWidget, QGraphicsView
from PySide6.QtGui import QPainter, QPen, QColor
from PySide6.QtCore import Qt, Signal, Slot
import lib.rampScene as ramp_scene
from lib import dummyLogger
from lib import rampController


class RampWidget(QGraphicsView):

    def __init__(self, parent=None, logger=None):
        super().__init__(parent=parent)

        self.scene = ramp_scene.RampScene(parent=self, logger=logger)
        self.logger = logger or dummyLogger.DummyLogger()
        self.target_width = 800
        self.target_height = 400
        self.controller = rampController.RampController(self.scene)

        self.setRenderHint(QPainter.Antialiasing)
        self.painter = QPainter(self)
        self.painter.setPen(QPen(QColor(79, 106, 25), 10, Qt.SolidLine, Qt.FlatCap, Qt.MiterJoin))

        self.prepare_scene()
        self.setScene(self.scene)
        self.scene.drawSplineSignal.connect(self.drawSpline)
        self.logger.debug('RampWidget: Initialized')

        # ------------------------------------ Sandbox ------------------------------------------


        self.scene.addKey(0, 1)
        self.scene.addKey(1, 0)
        self.scene.addKey(0, 0)
        self.scene.addKey(1, 1)
        self.scene.sort_keys()

    def prepare_scene(self):
        self.scene.setTargetWidth = self.target_width
        self.scene.setTargetHeight = self.target_height

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene.resizeScene()

    @Slot(object)
    def drawSpline(self, spline):
        self.painter.drawPath(spline)