from RampWidget.qRampWidget import QRampWidget
import NukeTypes as nkTypes


class MyRamp:

    def __init__(self):
        self.data = {}
        self.counter = 1
        self.blink_node = BlinkScriptNode()

    def addKey(self):
        new_key = Key(self.counter, 'potato')
        self.data[self.counter] = new_key
        self.blink_node.alloc(ramp_key=new_key)
        self.counter += 1

    def removeKey(self, index):
        del self.data[index]


class Key:

    def __init__(self, index, value):
        self.index = index
        self.value = value


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
        #self.key_positions = nkTypes.FloatArrayKnob('keyPositions', allocated_memory)
        #self.key_values = nkTypes.FloatArrayKnob('keyValues', allocated_memory)
        #self.bezier_positions = nkTypes.FloatArrayKnob('bezierPositions', allocated_memory * 2)
        #self.bezier_values = nkTypes.FloatArrayKnob('bezierValues', allocated_memory * 2)

    def alloc(self, ramp_key: Key):
        index = ramp_key.index
        value = ramp_key.value

        memory_list = self.memory.array()
        try:
            available_index = memory_list.index(-1)
        except ValueError:
            print('list is full')
            return False

        self.memory.setValue(available_index, index)
