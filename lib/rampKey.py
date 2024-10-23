from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtCore import Qt, QPointF, QRectF
from lib.items import valueItem, positionItem
from lib.utils import utils as ramp_utils


class RampKey(QGraphicsItem):

    def __init__(self, scene, ramp_index, parent=None):
        super().__init__(parent=parent)

        # ------------------------------- Attrs --------------------------------
        self.key_type = 'bezier'
        self.item_type = 'RAMPKEY'
        self.scale = .25
        self.scene = scene
        self.ramp_index = ramp_index

        # ------------------------------ Children -------------------------------
        self.position_item = positionItem.PositionItem(parent=self)
        self.value_item = valueItem.ValueItem(parent=self)

    @property
    def value(self):
        return self.value_item.value

    @value.setter
    def value(self, new_value: float):
        self.value_item.value = new_value

    @property
    def position(self):
        return self.value_item.position

    def forceSetPosition(self, x):
        self.position_item.setX(x)
        self.value_item.setX(x)
        print(self.value_item.x())

    @position.setter
    def position(self, new_value: float):
        self.value_item.position = new_value
        self.position_item.setX(self.scene.mapPositionToX(new_value))

    def rightControlPointPos(self):
        return self.value_item.mapToParent(self.value_item.bezier_handles[1].pos())

    def leftControlPointPos(self):
        return self.value_item.mapToParent(self.value_item.bezier_handles[0].pos())

    def sortBezierHandles(self):
        self.value_item.sortBezierHandles()

    def resetBezierHandles(self):
        self.value_item.bezier_handles[0].setPos(QPointF(-80, 0))
        self.value_item.bezier_handles[0].targetPos = QPointF(-80, 0)
        self.value_item.bezier_handles[1].setPos(QPointF(80, 0))
        self.value_item.bezier_handles[1].targetPos = QPointF(80, 0)
        self.scene.redrawCurveSignal.emit()

    def keyScenePos(self):
        return self.value_item.scenePos()

    def redrawCurveOnItemChange(self, enable:bool):
        self.value_item.redrawCurveOnItemChange = enable

    def removeKey(self):
        self.value_item.removeHandles()
        self.scene.removeItem(self.value_item)
        self.scene.removeItem(self.position_item)

    def boundingRect(self):
        return self.childrenBoundingRect()

    def paint(self, painter, option, widget=None):
        pass



