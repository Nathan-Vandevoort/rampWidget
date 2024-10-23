from lib import rampScene
from lib import rampKey
from PySide6.QtCore import QObject, Signal, Slot, QRectF


class RampController(QObject):

    def __init__(self, scene: rampScene, parent=None):
        super().__init__(parent=parent)
        self.scene = scene

    def addKey(self, position, value) -> (rampKey.RampKey, None):
        return self.scene.addKey(position, value)

    def removeKey(self, index: int):
        self.scene.removeKey(index)

    def resetBezierHandle(self, index: int):
        if self.scene.keys.get(index) is None:
            return
        else:
            key_item = self.scene.key
            key_item.resetBezierHandle()

    def setSceneRect(self, bound_rect: QRectF):
        if not isinstance(bound_rect, QRectF):
            raise ValueError('Must be a QRectF')

        self.scene.setSceneRect(bound_rect)
        self.scene.bound_rect = bound_rect

    def getCurvePoints(self):
        """
        Gets the curve points from the scene and returns them as a list of curve segments.
        All values are returned in scene space.
        :return: returns a list of tuples where each tuple corresponds to a curve segment.
        The tuples are formatted as such:
        (Start Position, End Position, Ctrl Pt 1, Ctrl Pt 2)
        All positions are turned as QPointF
        """

        bezier_segments = []
        for i in range(len(self.scene.sorted_keys) - 1):

            key = self.scene.sorted_keys[i]
            next_key = self.scene.sorted_keys[i + 1]

            start_pos = self.scene.keys[key].keyScenePos()
            end_pos = self.scene.keys[next_key].keyScenePos()
            ctl1 = self.scene.keys[key].rightControlPointPos()
            ctl2 = self.scene.keys[next_key].leftControlPointPos()

            bezier_segments.append((start_pos, end_pos, ctl1, ctl2))

        return bezier_segments

    @Slot()
    def debugSlot(self):
        print(self.getCurvePoints())
