from PySide6.QtWidgets import QGraphicsScene, QWidget
from PySide6.QtCore import Qt, QPointF, Slot
from lib.utils import dummyLogger
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils
from lib.items import valueItem


class RampScene(QGraphicsScene):

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- State Attributes ---------------------------
        self.logger = logger or dummyLogger.DummyLogger()
        self.parent = parent
        self.target_width = 800
        self.target_height = 400
        self.padding = QPointF(50, 20)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []

        # ------------------------- Prep ------------------------------------------
        new_item = valueItem.ValueItem()
        new_item.setX(400)
        new_item.setY(200)
        print(new_item.pos())
        self.addItem(new_item)

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

    def sort_keys(self):
        reverse_key_dict = {self.keys[key]: key for key in self.keys}
        keys = [self.keys[key] for key in self.keys]
        keys.sort(key=lambda x: x.position)
        self.sorted_keys = [reverse_key_dict[key] for key in keys]

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        new_key = rampKey.RampKey(self, self.next_index)
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1

        self.addItem(new_key)
        self.sort_keys()

        return new_key

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.removeItem(self.keys[index])
            del self.keys[index]
            self.sort_keys()

    def setTargetWidth(self, width: int):
        self.target_width = width
        self.resizeScene()

    def setTargetHeight(self, height: int):
        self.target_height = height
        self.resizeScene()

    def mapPositionToScene(self, position):
        new_x = ramp_utils.fit_range(position, 0, 1, self.padding.x(), self.target_width - self.padding.x())
        return new_x

    def mapValueToScene(self, value):
        new_y = ramp_utils.fit_range(value, 0, 1, self.target_height - self.padding.y(), self.padding.y())
        return new_y

    def mapXToPosition(self, x):
        new_position = ramp_utils.fit_range(x, self.padding.x(), self.target_width - self.padding.x(), 0, 1)
        return new_position

    def mapYToValue(self, y):
        new_value = 1 - ramp_utils.fit_range(y, self.padding.y(), self.target_height - self.padding.y(), 0, 1)
        return new_value
