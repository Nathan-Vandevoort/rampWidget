from PySide6.QtWidgets import QGraphicsScene, QWidget
from PySide6.QtCore import Qt, Signal
from lib import keyItem as ramp_key
from lib import dummyLogger
from lib import splineItem

class RampScene(QGraphicsScene):

    drawSplineSignal = Signal(object)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- State Attributes ---------------------------
        self.logger = logger or dummyLogger.DummyLogger()
        self.parent = parent
        self.target_width = 800
        self.target_height = 400
        self.grabbed_item = None
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []

        # ------------------------- Prep ------------------------------------------
        self.spline = splineItem.SplineItem(scene=self)
        self.addItem(self.spline)

        self.start_key = self.addKey(0, 0)
        self.start_key.setInteractable(False)
        self.start_key.hide()

        self.end_key = self.addKey(1, 0)
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

    def addKey(self, position, value) -> (ramp_key.KeyItem, None):
        new_key = ramp_key.KeyItem(self, self.next_index)
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1

        self.addItem(new_key)
        self.sort_keys()
        self.drawSpline()

        return new_key

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.removeItem(self.keys[index])
            del self.keys[index]
            self.sort_keys()
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
            self.grabbed_item.position = (pos.x() + self.grabbed_item.selection_offset.x()) / self.target_width
            self.grabbed_item.value = 1 - ((pos.y() + self.grabbed_item.selection_offset.y()) / self.target_height)
            self.sort_keys()

            # ensure that start and end points move in value with selected key IF it is the start or end key
            self.start_key.value = self.keys[self.sorted_keys[1]].value
            self.end_key.value = self.keys[self.sorted_keys[-2]].value

            self.drawSpline()

        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if self.grabbed_item is not None:
                self.grabbed_item = None
                self.sort_keys()
                self.drawSpline()

        super().mouseReleaseEvent(event)

    def drawSpline(self):
        self.spline.draw()
        self.drawSplineSignal.emit(self.spline.path)
