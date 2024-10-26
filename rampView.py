from PySide2.QtWidgets import QGraphicsView
from PySide2.QtGui import QPainter
#try:
#    from PySide6.QtWidgets import QGraphicsView
#    from PySide6.QtGui import QPainter
#except ImportError:
#    from PySide2.QtWidgets import QGraphicsView
#    from PySide2.QtGui import QPainter
import lib.rampScene as ramp_scene
from lib import rampController

#import faulthandler, os
#faulthandler.enable()
#os.environ['QT_DEBUG_PLUGINS'] = '1'

class RampView(QGraphicsView):

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        #self.scene = ramp_scene.RampScene(parent=self)
        #self.controller = rampController.RampController(self.scene, parent=self)
        #self.scene.debugSignal.connect(self.controller.debugSlot)

        #self.setRenderHint(QPainter.Antialiasing)
        #self.setScene(self.scene)
