from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem, QMenu
from PySide6.QtCore import Qt, QPointF, Slot, QRectF, Signal
from PySide6.QtGui import QTransform, QAction
from lib.items import splineItem
from lib import rampKey
from lib.utils import utils as ramp_utils
from lib.items import valueItem, positionItem


class RampScene(QGraphicsScene):

    positionItemXChangedSignal = Signal(int, float)
    valueItemXChangedSignal = Signal(int, float)
    redrawCurveSignal = Signal()
    bezierHandleMovedSignal = Signal(int)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- Scene Settings -----------------------------

        # ------------------------- Signals ------------------------------------
        self.positionItemXChangedSignal.connect(self.positionItemXChangedSlot)
        self.valueItemXChangedSignal.connect(self.valueItemXChangedSlot)
        self.redrawCurveSignal.connect(self.redrawCurveSlot)
        self.bezierHandleMovedSignal.connect(self.bezierHandleMovedSlot)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 780, 380)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []
        self.setSceneRect(0, 0, 800, 400)
        self.start_key = None
        self.end_key = None
        self.prepared = False

        # ------------------------- Children -------------------------------------
        self.spline_item = splineItem.SplineItem(scene=self)
        self.start_key = self.addKey(-.1, 0)
        self.start_key.item_type = 'ENDKEY'
        self.start_key.forceSetPosition(self.sceneRect().left() - 100)
        self.start_key.redrawCurveOnItemChange(False)
        self.start_key.hide()
        self.end_key = self.addKey(1.1, 1)
        self.end_key.item_type = 'ENDKEY'
        self.end_key.forceSetPosition(self.sceneRect().right() + 100)
        self.end_key.redrawCurveOnItemChange(False)
        self.end_key.hide()

        # ------------------------- Prep ------------------------------------------
        self.addItem(QGraphicsRectItem(self.bound_rect))
        self.addKey(0, 0)
        self.addKey(1, 1)
        self.addItem(self.spline_item)
        self.spline_item.setZValue(0)
        self.redrawCurveSlot()
        self.prepared = True

    @Slot(int, float)
    def positionItemXChangedSlot(self, item, x):
        value_item = self.keys[item].value_item
        value_item.setX(x)
        value_item.confineBezierHandlesToNeighbours() # confine bezier handles
        neighbours = self.getNeighbourKeys(item)
        self.keys[neighbours[0]].value_item.confineBezierHandlesToNeighbours()
        self.keys[neighbours[1]].value_item.confineBezierHandlesToNeighbours()
        self.sort_keys()

    @Slot(int, float)
    def valueItemXChangedSlot(self, item, x):
        self.keys[item].position_item.setX(x)
        self.keys[item].value_item.confineBezierHandlesToNeighbours()
        neighbours = self.getNeighbourKeys(item)
        self.keys[neighbours[0]].value_item.confineBezierHandlesToNeighbours()
        self.keys[neighbours[1]].value_item.confineBezierHandlesToNeighbours()
        self.sort_keys()

    @Slot()
    def redrawCurveSlot(self):
        self.alignEndKeys()
        self.spline_item.draw()

    @Slot(int)
    def bezierHandleMovedSlot(self, item):
        key_item = self.keys.get(item)
        if key_item is not None:
            self.keys[item].sortBezierHandles()

    def sort_keys(self):
        reverse_key_dict = {self.keys[key]: key for key in self.keys}
        keys = [self.keys[key] for key in self.keys if self.keys[key] != self.start_key and self.keys[key] != self.end_key]
        keys.sort(key=lambda x: x.position)
        if self.start_key and self.end_key:
            keys.insert(0, self.start_key)
            keys.append(self.end_key)
        self.sorted_keys = [reverse_key_dict[key] for key in keys]

    def alignEndKeys(self):
        if self.prepared:
            self.start_key.value_item.setY(self.keys[self.sorted_keys[1]].leftControlPointPos().y())
            self.end_key.value_item.setY(self.keys[self.sorted_keys[-2]].rightControlPointPos().y())

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        new_key = rampKey.RampKey(self, self.next_index)
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1
        self.addItem(new_key)
        new_key.setZValue(.5)
        self.sort_keys()
        return new_key

    def removeKey(self, index: int):
        if self.keys.get(index) is None:
            return
        else:
            self.keys[index].removeKey()
            self.removeItem(self.keys[index])
            self.keys.pop(index)
            self.sort_keys()
            self.redrawCurveSlot()
            self.update()

    def getNeighbourKeys(self, item):
        try:
            found_key_index = self.sorted_keys.index(item)
            neighbours = (self.sorted_keys[found_key_index - 1], self.sorted_keys[found_key_index + 1])
            return neighbours
        except ValueError:
            return None

    def mapXToPosition(self, x):
        return_val = ramp_utils.fit_range(x, self.bound_rect.left(), self.bound_rect.right(), 0, 1)
        return return_val

    def mapPositionToX(self, position):
        return_val = ramp_utils.fit_range(position, 0, 1, self.bound_rect.left(), self.bound_rect.right())
        return return_val

    def mapYToValue(self, y):
        return_val = ramp_utils.fit_range(y, self.bound_rect.bottom(), self.bound_rect.top(), 0, 1)
        return return_val

    def mapValueToY(self, value):
        return_val = ramp_utils.fit_range(value, 1, 0, self.bound_rect.top(), self.bound_rect.bottom())
        return return_val

    def mouseDoubleClickEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            pos = event.scenePos()
            self.addKey(self.mapXToPosition(pos.x()), self.mapYToValue(pos.y()))
            self.redrawCurveSlot()
        super().mouseDoubleClickEvent(event)

    def contextMenuEvent(self, event):
        menu = None
        pos = event.scenePos()
        item = self.itemAt(pos, QTransform())

        if isinstance(item, valueItem.ValueItem) or isinstance(item, positionItem.PositionItem):
            menu = QMenu()
            reset_bezier_handle_action = QAction('Reset Bezier Handles')
            delete_key_action = QAction('Delete Key')

            ramp_index = item.key_item.ramp_index

            reset_bezier_handle_action.triggered.connect(lambda: self.keys[ramp_index].resetBezierHandles())
            delete_key_action.triggered.connect(lambda: self.removeKey(ramp_index))

            menu.addAction(reset_bezier_handle_action)
            menu.addAction(delete_key_action)

        if menu is not None:
            menu.exec(event.screenPos())

