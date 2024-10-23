from lib import rampScene
from lib import rampKey
from PySide6.QtCore import QObject, Signal, Slot


class RampController(QObject):

    def __init__(self, scene: rampScene, parent=None):
        super().__init__(parent=parent)
        self.scene = scene

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        return self.scene.addKey(position, value)

    def removeKey(self, index: int):
        self.scene.removeKey(index)

    def resetBezierHandles(self, index: int):
        if self.scene.keys.get(index) is None:
            return
        else:
            key_item = self.scene.key
            key_item.resetBezierHandles()
