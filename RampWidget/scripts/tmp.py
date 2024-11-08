import sys
from PySide2.QtWidgets import QWidget, QGraphicsItem
from PySide2.QtCore import Slot
sys.path.append('Z:/Repos/RampWidget')
from RampWidget import qRampWidget


class BlinkNode:

    def __init__(self, my_node):
        self.loading = False
        self.node = my_node.node('kernel')
        self.key_order = self.node.knob('RampKernel_key_order')
        self.memory = self.node.knob('RampKernel_memory')
        self.key_types = self.node.knob('RampKernel_key_types')
        self.key_positions = self.node.knob('RampKernel_key_positions')
        self.key_values = self.node.knob('RampKernel_key_values')
        self.bezier_handle_positions = self.node.knob('RampKernel_bezier_handle_positions')
        self.bezier_handle_values = self.node.knob('RampKernel_bezier_handle_values')
        self.key_index = self.node.knob('RampKernel_key_index')

    def alloc(self, ramp_index):
        if self.loading is True:
            return
        memory_list = self.memory.array()
        self.key_index.setValue(ramp_index)
        try:
            found_index = memory_list.index(-1)
        except ValueError:
            return False
        self.memory.setValue(ramp_index, found_index)
        return True

    def free(self, ramp_index):
        if self.loading is True:
            return
        memory_list = self.memory.array()
        found_index = memory_list.index(ramp_index)
        self.memory.setValue(-1, found_index)

    def orderChanged(self, new_order):
        if self.loading is True:
            return
        order_list = self.key_order.array()
        memory_list = self.memory.array()
        for i in range(len(order_list)):
            if i < len(new_order):
                self.key_order.setValue(memory_list.index(new_order[i]), i)
            elif order_list[i] == -1:  # early return if memory is already clear
                return
            else:
                self.key_order.setValue(-1, i)

    def initializeKnobs(self):
        memory_list = self.memory.array()
        for i in range(len(memory_list)):
            self.memory.setValue(-1, i)

    def updateItem(self, item):
        if self.loading is True:
            return
        ramp_index = item.ramp_index
        position = item.position
        value = item.value
        bezier_left = item.leftHandle
        bezier_right = item.rightHandle
        memory_index = self.memory.array().index(int(ramp_index))

        self.key_positions.setValue(position, memory_index)
        self.key_values.setValue(value, memory_index)
        self.bezier_handle_positions.setValue(bezier_left[0], memory_index * 2)
        self.bezier_handle_positions.setValue(bezier_right[0], memory_index * 2 + 1)
        self.bezier_handle_values.setValue(bezier_left[1], memory_index * 2)
        self.bezier_handle_values.setValue(bezier_right[1], memory_index * 2 + 1)

    def updateInterpolation(self, item, interpolation):
        if self.loading is True:
            return
        if interpolation == 'bezier':
            value = 0
        elif interpolation == 'linear':
            value = 1
        else:
            value = 1
        ramp_index = item.ramp_index
        found_index = self.memory.array().index(ramp_index)
        self.key_types.setValue(value, found_index)


class MyRamp(qRampWidget.QRampWidget):

    def __init__(self, parent):
        super(MyRamp, self).__init__()
        width = 500
        height = 500

        self.delete_next = False
        self.blink_node = BlinkNode(nuke.thisNode())
        self.makeConnections()
        self.setSceneDimensions(width, height)
        self.setScenePadding(0, 13, 0, 26)
        next_index = int(self.blink_node.key_index.getValue())
        if next_index == 0:
            self.blink_node.initializeKnobs()
            self.start()
        else:
            self.blink_node.loading = True
            self.start()
            self.load()
            self.setNextIndex(next_index + 1)

    def load(self):
        key_order = self.blink_node.key_order.array()
        memory = self.blink_node.memory.array()
        key_types = self.blink_node.key_types.array()
        key_positions = self.blink_node.key_positions.array()
        key_values = self.blink_node.key_values.array()
        bezier_handle_positions = self.blink_node.bezier_handle_positions.array()
        bezier_handle_values = self.blink_node.bezier_handle_values.array()

        self.clearKeys()

        for index in key_order:

            index = int(index)

            if index <= 1:
                continue

            if index == -1:
                self.blink_node.loading = False
                return

            ramp_index = int(memory[index])
            position = key_positions[index]
            value = key_values[index]
            print(f'key: {index}, position: {position}, value: {value}')
            key_type = int(key_types[index])
            bezier01_position = bezier_handle_positions[index * 2]
            bezier01_value = bezier_handle_values[index * 2]
            bezier02_position = bezier_handle_positions[index * 2 + 1]
            bezier02_value = bezier_handle_values[index * 2 + 1]

            if key_type == 0:
                interpolation = 'bezier'
            elif key_type == 1:
                interpolation = 'linear'
            else:
                interpolation = 'linear'

            new_key = self.addKey(position, value, ramp_index=ramp_index)
            new_key.setInterpolation(interpolation)
            new_key.setBezierValues(bezier01_position, bezier01_value, bezier02_position, bezier02_value)

        self.blink_node.loading = False


    def makeConnections(self):
        self.orderChanged.connect(self.orderChangedSlot)
        self.keyAdded.connect(self.keyAddedSlot)
        self.keyRemoved.connect(self.keyRemovedSlot)
        self.valueChanged.connect(self.valueChangedSlot)
        self.interpolationChanged.connect(self.interpolationChangedSlot)

    @Slot(tuple)
    def orderChangedSlot(self, new_order):
        self.blink_node.orderChanged(new_order)

    @Slot(int, str)
    def keyAddedSlot(self, ramp_key, status):
        ramp_index = ramp_key.ramp_index
        if status == 'start':
            if self.blink_node.alloc(ramp_index) is False:
                self.delete_next = True
            else:
                self.delete_next = False
        elif status == 'done':
            self.valueChangedSlot(ramp_key)
            if self.delete_next is True:
                self.removeKey(ramp_index)
                self.delete_next = False

    @Slot(QGraphicsItem)
    def keyRemovedSlot(self, ramp_index):
        self.blink_node.free(ramp_index)

    @Slot(QGraphicsItem)
    def valueChangedSlot(self, item):
        if item.initialized is False:
            return
        self.blink_node.updateItem(item)

    @Slot(QGraphicsItem, str)
    def interpolationChangedSlot(self, item, interpolation):
        self.blink_node.updateInterpolation(item, interpolation)

    def makeUI(self):
        return self

    def updateValue(self):
        return