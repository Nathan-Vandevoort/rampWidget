import rampWidget
from PySide6.QtCore import QObject, Signal, Slot


class RampController(QObject):

    def __init__(self, scene):
        super().__init__()
        self.scene = scene

