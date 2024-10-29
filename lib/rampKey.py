try:
    from PySide6.QtWidgets import QGraphicsItem
    from PySide6.QtCore import Qt, QPointF, QRectF
except ImportError:
    from PySide2.QtWidgets import QGraphicsItem
    from PySide2.QtCore import Qt, QPointF, QRectF
from lib.items import valueItem, positionItem


class RampKey(QGraphicsItem):

    def __init__(self, scene, ramp_index, parent=None):
        super().__init__(parent=parent)

        # ------------------------------- Attrs --------------------------------
        self.key_type = 'bezier'
        self.item_type = 'RAMPKEY'
        self.scale = .125
        self.scene = scene
        self.broken_tangents = False
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

    def resetBezierHandle(self):
        self.toggleBrokenTangents()
        self.value_item.bezier_handles[0].setPos(QPointF(-200, 0))
        self.value_item.bezier_handles[0].targetPos = QPointF(-200, 0)
        self.value_item.bezier_handles[1].setPos(QPointF(200, 0))
        self.value_item.bezier_handles[1].targetPos = QPointF(200, 0)
        self.toggleBrokenTangents()
        self.value_item.bezier_handle_line.draw()
        self.scene.redrawCurveSignal.emit()

    def keyScenePos(self):
        return self.value_item.scenePos()

    def redrawCurveOnItemChange(self, enable:bool):
        self.value_item.redrawCurveOnItemChange = enable

    def removeKey(self):
        self.value_item.removeHandles()
        self.scene.removeItem(self.value_item)
        self.scene.removeItem(self.position_item)

    def drawBezierHandleLine(self):
        self.value_item.bezier_handle_line.draw()

    def boundingRect(self):
        return QRectF(-2, -2, -1, -1)

    def paint(self, painter, option, widget=None):
        pass

    def toggleBrokenTangents(self):
        if self.broken_tangents is False:
            self.broken_tangents = True
        else:
            self.broken_tangents = False

    def setInterpolation(self, interpolation):
        self.key_type = interpolation

        if interpolation == 'linear':
            self.value_item.hideBezierHandles()
            self.resetBezierHandle()

        if interpolation == 'bezier':
            self.value_item.showBezierHandles()



