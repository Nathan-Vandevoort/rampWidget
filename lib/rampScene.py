from PySide6.QtWidgets import QGraphicsScene, QWidget
from lib import keyItem as ramp_key

class RampScene(QGraphicsScene):

    def __init__(self, parent: QWidget = None):
        super().__init__(parent=parent)

        self.parent = parent
        self.keys = []

        self.resizeScene()

    def resizeScene(self):
        self.setSceneRect(0, 0, self.parent.width(), self.parent.height())

    def buildDefaultScene(self):
        pass

    def addKey(self, position, value):

        new_key =

    def removeKey(self, key_index):
        pass
