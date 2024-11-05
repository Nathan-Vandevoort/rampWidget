try:
    from PySide6.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem, QMenu, QGraphicsItem
    from PySide6.QtCore import Qt, QPointF, Slot, QRectF, Signal
    from PySide6.QtGui import QTransform, QAction
    PYSIDE_VERSION = 6
except ImportError:
    from PySide2.QtWidgets import QGraphicsScene, QWidget, QGraphicsRectItem, QMenu, QAction, QGraphicsItem
    from PySide2.QtCore import Qt, QPointF, Slot, QRectF, Signal
    from PySide2.QtGui import QTransform
    PYSIDE_VERSION = 2
from RampWidget.lib.items import splineItem
from RampWidget.lib import rampKey
from RampWidget.lib.utils import utils as ramp_utils
from RampWidget.lib.items import positionItem, bezierHandleItem, valueItem, bezierHandleLineItem


class RampScene(QGraphicsScene):

    positionItemXChangedSignal = Signal(int, float)
    valueItemXChangedSignal = Signal(int, float)
    redrawCurveSignal = Signal()
    bezierHandleMovedSignal = Signal(int, QGraphicsItem)
    debugSignal = Signal()
    itemMovedSignal = Signal(QGraphicsItem, QPointF)
    keyAddedSignal = Signal(QGraphicsItem)
    keyRemovedSignal = Signal(int)
    sortChangedSignal = Signal(tuple)

    def __init__(self, parent: QWidget = None, logger=None):
        super().__init__(parent=parent)

        # ------------------------- Signals ------------------------------------
        self.positionItemXChangedSignal.connect(self.positionItemXChangedSlot)
        self.valueItemXChangedSignal.connect(self.valueItemXChangedSlot)
        self.redrawCurveSignal.connect(self.redrawCurveSlot)
        self.bezierHandleMovedSignal.connect(self.bezierHandleMovedSlot)

        # ------------------------- State Attributes ---------------------------
        self.bound_rect = QRectF(20, 20, 380, 180)
        self.next_index = 0
        self.keys = {}
        self.sorted_keys = []
        self.setSceneRect(0, 0, 400, 200)
        self.start_key = None
        self.end_key = None
        self.prepared = False

        # --------------------------------- Children ---------------------------
        self.spline_item = None
        self.border_rect = None


    @Slot(int, float)
    def positionItemXChangedSlot(self, item, x):
        value_item = self.keys[item].value_item
        self.blockSignals(True)  # block signals to ensure no infinite recursion between position item and value item updates
        value_item.setX(x)
        self.blockSignals(False)
        value_item.confineBezierHandlesToNeighbours()  # confine bezier handles
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
    def bezierHandleMovedSlot(self, item_index, bezier_item):
        key_item = self.keys.get(item_index)
        if key_item is not None:
            if self.keys[item_index].broken_tangents is False:
                other_bezier_item = [x for x in self.keys[item_index].value_item.bezier_handles if x != bezier_item]

                if len(other_bezier_item) == 0:
                    return

                other_bezier_item = other_bezier_item[0]
                distance = ramp_utils.distance(QPointF(0, 0), other_bezier_item.pos())
                direction = ramp_utils.normalize(key_item.value_item.scenePos() - bezier_item.scenePos())
                self.blockSignals(True)
                other_bezier_item.setPos(distance * direction)
                other_bezier_item.targetPos = distance * direction
                other_bezier_item.itemChange(QGraphicsItem.ItemPositionChange, other_bezier_item.scenePos())
                self.blockSignals(False)


            self.keys[item_index].sortBezierHandles()
            self.keys[item_index].drawBezierHandleLine()

    def initializeRamp(self):
        # ------------------------- Children -------------------------------------
        self.spline_item = splineItem.SplineItem(scene=self)
        self.start_key = self.addKey(-.1, 0)
        self.start_key.item_type = 'ENDKEY'
        self.start_key.setInterpolation('bezier')
        self.start_key.forceSetPosition(self.sceneRect().left() - 100)
        self.start_key.redrawCurveOnItemChange(False)
        self.start_key.hide()
        self.end_key = self.addKey(1.1, 1)
        self.end_key.item_type = 'ENDKEY'
        self.end_key.setInterpolation('bezier')
        self.end_key.forceSetPosition(self.sceneRect().right() + 100)
        self.end_key.redrawCurveOnItemChange(False)
        self.end_key.hide()

        # ------------------------- Prep ------------------------------------------
        self.border_rect = QGraphicsRectItem(self.bound_rect)
        self.addItem(self.border_rect)
        self.addKey(0, 0)
        self.addKey(1, 1)
        self.addItem(self.spline_item)
        self.spline_item.setZValue(0)
        self.redrawCurveSlot()
        self.prepared = True

    def sort_keys(self):
        reverse_key_dict = {self.keys[key]: key for key in self.keys}
        keys = [self.keys[key] for key in self.keys if self.keys[key] != self.start_key and self.keys[key] != self.end_key]
        keys.sort(key=lambda x: x.position)
        if self.start_key and self.end_key:
            keys.insert(0, self.start_key)
            keys.append(self.end_key)
        new_sorted_keys = [reverse_key_dict[key] for key in keys]
        if self.sorted_keys == new_sorted_keys:
            return
        self.sortChangedSignal.emit(tuple(new_sorted_keys))
        self.sorted_keys = [reverse_key_dict[key] for key in keys]

    def alignEndKeys(self):
        if self.prepared:
            self.start_key.value_item.setY(self.keys[self.sorted_keys[1]].leftControlPointPos().y())
            self.end_key.value_item.setY(self.keys[self.sorted_keys[-2]].rightControlPointPos().y())

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        new_key = rampKey.RampKey(self, self.next_index)  # the individual ramp key will emit the key added signal
        new_key.position = position
        new_key.value = value

        if new_key.position is None or new_key.value is None:
            return None

        self.keys[self.next_index] = new_key
        self.next_index += 1
        self.addItem(new_key)
        new_key.setZValue(.5)
        self.sort_keys()
        self.keyAddedSignal.emit(new_key)
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
            self.keyRemovedSignal.emit(index)

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
        if (isinstance(item, valueItem.ValueItem)
                or isinstance(item, positionItem.PositionItem)
                or isinstance(item, bezierHandleLineItem.BezierHandleLineItem)
                or isinstance(item, bezierHandleItem.BezierHandleItem)):
            menu = QMenu()
            reset_bezier_handle_action = QAction('Reset Bezier Handles')
            delete_key_action = QAction('Delete Key')
            toggle_broken_tangents_action = QAction('Unify/Break Tangents')

            # create interpolation options menu
            interpolation_menu = QMenu('Set Interpolation')
            linear_interpolation_action = QAction('Linear')
            bezier_interpolation_action = QAction('Bezier')

            # add actions to interpolation menu
            interpolation_menu.addAction(linear_interpolation_action)
            interpolation_menu.addAction(bezier_interpolation_action)

            ramp_index = item.key_item.ramp_index

            reset_bezier_handle_action.triggered.connect(lambda: self.keys[ramp_index].resetBezierHandle())
            delete_key_action.triggered.connect(lambda: self.removeKey(ramp_index))
            toggle_broken_tangents_action.triggered.connect(self.keys[ramp_index].toggleBrokenTangents)

            linear_interpolation_action.triggered.connect(lambda: self.keys[ramp_index].setInterpolation('linear'))
            bezier_interpolation_action.triggered.connect(lambda: self.keys[ramp_index].setInterpolation('bezier'))

            menu.addAction(reset_bezier_handle_action)
            menu.addAction(delete_key_action)
            menu.addAction(toggle_broken_tangents_action)
            menu.addMenu(interpolation_menu)

        else:
            menu = QMenu()
            debug_action = QAction('debug')
            debug_action.triggered.connect(lambda: self.debugSignal.emit())
            menu.addAction(debug_action)

        if menu is not None:
            if PYSIDE_VERSION == 6:
                menu.exec(event.screenPos())
            else:
                menu.exec_(event.screenPos())