try:
    from PySide6.QtCore import QPointF
except ImportError:
    from PySide2.QtCore import QPointF
import math


def fit_range(value: float, old_min: float, old_max: float, new_min: float, new_max: float):
    return_val = new_min + (value - old_min) * (new_max - new_min) / (old_max - old_min)
    return return_val


def distance(pt1, pt2):
    return math.sqrt((pt1.x() - pt2.x()) ** 2 +
                     (pt1.y() - pt2.y()) ** 2)


def normalize(pt):
    length = math.sqrt(pt.x() ** 2 + pt.y() ** 2)
    if length == 0:
        return QPointF(0, 0)
    return QPointF(pt.x() / length, pt.y() / length)
