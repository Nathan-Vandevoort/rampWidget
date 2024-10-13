from PySide6.QtWidgets import QGraphicsScene, QWidget
from lib import keyItem as ramp_key
from lib import dummyLogger

class RampScene(QGraphicsScene):

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__()

        self.logger = logger or dummyLogger.DummyLogger()
        self.parent = parent
        self.next_index = 0
        self.keys = {}
        self.target_width = 800
        self.target_height = 400

        self.resizeScene()

        self.logger.debug('RampScene: Initialized')

    def resizeScene(self):
        parent_width = self.parent.width()
        parent_height = self.parent.height()

        if parent_width > self.target_width:
            parent_width = self.target_width

        if parent_height > self.target_height:
            parent_height = self.target_height

        self.setSceneRect(0, 0, parent_width, parent_height)

    def buildDefaultScene(self):
        pass

    def addKey(self, position, value) -> (ramp_key.KeyItem, None):
        new_key = ramp_key.KeyItem(self)
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1

        self.addItem(new_key)

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.removeItem(self.keys[index])
            del self.keys[index]

    def addItem(self, item):
        super().addItem(item)
        self.update()

    def removeItem(self, item):
        super().removeItem(item)
        self.update()

    def setTargetWidth(self, width: int):
        self.target_width = width

    def setTargetHeight(self, height: int):
        self.target_height = height