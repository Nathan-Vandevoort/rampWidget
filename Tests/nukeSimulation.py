from RampWidget.qRampWidget import QRampWidget
import NukeTypes as nkTypes
try:
    from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
    from PySide6.QtCore import Slot, Signal
except ImportError:
    from PySide2.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView, QGraphicsItem
    from PySide2.QtCore import Slot, Signal
import sys


class MyRamp(QRampWidget):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.blink_node = BlinkScriptNode(allocated_memory=8)
        self.keyAdded.connect(self.keyAddedSlot)
        self.keyRemoved.connect(self.keyRemovedSlot)
        self.valueChanged.connect(self.valueChangeSlot)
        self.orderChanged.connect(self.orderChangeSlot)

    @Slot(QGraphicsItem)
    def keyAddedSlot(self, item):
        ramp_index = item.ramp_index
        if self.blink_node.alloc(ramp_index) is False:
            self.blockSignals(True)
            self.removeKey(ramp_index)
            self.blockSignals(False)

    @Slot(int)
    def keyRemovedSlot(self, ramp_index):
        print(ramp_index)
        self.blink_node.free(ramp_index)

    @Slot(QGraphicsItem, float, float)
    def valueChangeSlot(self, item, position, value):
        pass

    @Slot(tuple)
    def orderChangeSlot(self, new_order):
        pass
        #print(f'Order Change: {new_order}')


class BlinkScriptNode:

    def __init__(self, allocated_memory=50):
        """
        will be in memory space
        ie: each element will reference an index in the
        HERES THE PLAN
        The value at the memory index corresponds to the rampKeyIndex
        The index at a memory index corresponds to the actual memory
        """
        self.order = nkTypes.IntArrayKnob('order', allocated_memory)
        self.memory = nkTypes.IntArrayKnob('memory', allocated_memory)
        self.key_positions = nkTypes.FloatArrayKnob('keyPositions', allocated_memory)
        self.key_values = nkTypes.FloatArrayKnob('keyValues', allocated_memory)
        self.bezier_positions = nkTypes.FloatArrayKnob('bezierPositions', allocated_memory * 2)
        self.bezier_values = nkTypes.FloatArrayKnob('bezierValues', allocated_memory * 2)

    def alloc(self, ramp_index):
        memory_list = self.memory.array()
        try:
            available_index = memory_list.index(-1)
        except ValueError:
            return False
        self.memory.setValue(available_index, ramp_index)
        #print(self.memory._data)
        return True

    def free(self, ramp_index):
        memory_list = self.memory.array()
        found_index = memory_list.index(ramp_index)
        self.memory.setValue(found_index, -1)
        #print(self.memory._data)

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.resize(800, 400)
        self.ramp_widget = MyRamp(parent=self)
        self.ramp_widget.start()
        self.setCentralWidget(self.ramp_widget)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec_())
