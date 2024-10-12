from PySide6.QtWidgets import QWidget, QGraphicsView
import lib.rampScene as ramp_scene
from lib import dummyLogger


class RampWidget(QGraphicsView):

    def __init__(self, parent=None, logger=None):
        super().__init__(parent=parent)

        self.scene = ramp_scene.RampScene(parent=self, logger=logger)
        self.logger = logger or dummyLogger.DummyLogger()
        self.target_width = 800
        self.target_height = 400

        self.setScene(self.scene)
        self.logger.debug('RampWidget: Initialized')

        # ------------------------------------ Sandbox ------------------------------------------
        self.scene.addKey(.5, .5)

    def prepare_scene(self):
        self.scene.setTargetWidth = self.target_width
        self.scene.setTargetHeight = self.target_height

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.scene.resizeScene()