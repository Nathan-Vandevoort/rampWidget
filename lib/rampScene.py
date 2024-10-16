from PySide6.QtWidgets import QGraphicsScene, QWidget
from PySide6.QtCore import Qt, QPointF, Slot
from lib.utils import dummyLogger
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils


class RampScene(QGraphicsScene):

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- State Attributes ---------------------------
        self.logger = logger or dummyLogger.DummyLogger()
        self.parent = parent
        self.target_width = 800
        self.target_height = 400
        self.padding = QPointF(50, 20)
        self.grabbed_item = None
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []

        # ------------------------- Prep ------------------------------------------
        self.spline = splineItem.SplineItem(scene=self)
        self.addItem(self.spline)

        self.start_key = self.addKey(0, 0)
        self.start_key.position_item.forceSet(-.1)
        self.start_key.setInteractable(False)
        self.start_key.hide()

        self.end_key = self.addKey(1, 0)
        self.end_key.position_item.forceSet(1.1)
        self.end_key.setInteractable(False)
        self.end_key.hide()
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

    def sort_keys(self):
        #{key_expression(item): value_expression(item) for item in something if condition}
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
        self.alignEndKeys()
        self.drawSpline()

        return new_key

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.removeItem(self.keys[index])
            del self.keys[index]
            self.sort_keys()
            self.alignEndKeys()
            self.drawSpline()

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
            self.grabbed_item.drag(pos)
            self.sort_keys()
            self.alignEndKeys()
            self.drawSpline()

        super().mouseMoveEvent(event)

    def alignEndKeys(self):
        # ensure that start and end points move with the moved points
        if len(self.sorted_keys) > 2:
            self.start_key.value = self.keys[self.sorted_keys[1]].value
            self.end_key.value = self.keys[self.sorted_keys[-2]].value

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.grabbed_item is not None:
                self.grabbed_item.deselect()
                self.grabbed_item = None
                self.sort_keys()

        super().mouseReleaseEvent(event)

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.scenePos()

            if self.padding.x() < pos.x() < self.target_width - self.padding.x() \
                    and self.padding.y() < pos.y() < self.target_height - self.padding.y():
                self.addKey(self.mapXToPosition(pos.x()), self.mapYToValue(pos.y()))
                event.accept()

        super().mouseDoubleClickEvent(event)

    def drawSpline(self):
        self.spline.draw()

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
