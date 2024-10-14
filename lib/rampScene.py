from PySide6.QtWidgets import QGraphicsScene, QWidget
from PySide6.QtCore import Qt
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

        self.grabbed_item = None

        self.resizeScene()

        self.logger.debug('RampScene: Initialized')

    def resizeScene(self):
        parent_width = self.parent.width()
        parent_height = self.parent.height()

        if parent_width > self.target_width:
            parent_width = self.target_width

        if parent_height > self.target_height:
            parent_height = self.target_height

        self.setSceneRect(0, 0, self.target_width, self.target_height)

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
        self.resizeScene()

    def setTargetHeight(self, height: int):
        self.target_height = height
        self.resizeScene()

    def mouseGrabberItem(self):
        return self.grabbed_item

    def mouseMoveEvent(self, event):
        if self.grabbed_item is not None:
            pos = event.scenePos()
            self.grabbed_item.position = (pos.x() + self.grabbed_item.selection_offset.x()) / self.target_width
            self.grabbed_item.value = (pos.y() + self.grabbed_item.selection_offset.y()) / self.target_height

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.grabbed_item = None

        super().mouseReleaseEvent(event)