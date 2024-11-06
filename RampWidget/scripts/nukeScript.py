# I put all my definition code into a multiline string (using """)
the_code = """

"""
# Create a NoOp node on which we'll add the knobs
node = nuke.createNode("NoOp")
# Storage knob as previously
storage = nuke.Int_Knob('storage_knob')
storage.setFlag(nuke.INVISIBLE)
node.addKnob(storage)
# A hidden python script button
button = nuke.PyScript_Knob('class_definitions', '', the_code)
button.setFlag(nuke.INVISIBLE)
node.addKnob(button)
# A PyCustom knob that will execute the button
init_knob = nuke.PyCustom_Knob("initialization", "", "nuke.thisNode()['class_definitions'].execute()")
node.addKnob(init_knob)
# Our real knob that will execute AFTER the init knob
knob = nuke.PyCustom_Knob("todo", "", "MyRamp(nuke.thisNode())")
node.addKnob(knob)

nuke.clearDiskCache()

####################################################################################################################
#  nuke.toNode('GroupNode').node('Grade') get a node within a group

import sys
from PySide2.QtWidgets import QWidget, QGraphicsItem
from PySide2.QtCore import Slot
sys.path.append('Z:/Repos/RampWidget')
from RampWidget import qRampWidget

class BlinkNode:

    def __init__(self, my_node):
        self.node = my_node.node('kernel')
        self.key_order = self.node.knob('RampKernel_key_order')
        self.memory = self.node.knob('RampKernel_memory')
        self.key_positions = self.node.knob('RampKernel_key_positions')
        self.key_values = self.node.knob('RampKernel_key_values')
        self.bezier_handle_positions = self.node.knob('RampKernel_bezier_handle_positions')
        self.bezier_handle_values = self.node.knob('RampKernel_bezier_handle_values')

        self.initializeKnobs()

    def alloc(self, ramp_index):
        pass

    def free(self, ramp_index):
        pass

    def orderChanged(self):
        pass

    def buildRelationArray(self):
        pass

    def initializeKnobs(self):
        memory_list = self.memory.array()
        for i in range(memory_list):
            self.memory.setValue(-1, i)


class MyRamp(qRampWidget.QRampWidget):

    def __init__(self, parent):
        super(MyRamp, self).__init__()
        width = 500
        height = 500

        self.blink_node = BlinkNode(nuke.thisNode())

        self.makeConnections()
        self.setSceneDimensions(width, height)
        self.setScenePadding(0, 13, 0, 26)
        self.start()

    def makeConnections(self):
        self.orderChanged.connect(self.orderChangedSlot)
        self.keyAdded.connect(self.keyAddedSlot)
        self.keyRemoved.connect(self.keyRemovedSlot)
        self.valueChanged.connect(self.valueChangedSlot)

    @Slot(tuple)
    def orderChangedSlot(self, new_order):
        pass

    @Slot(int)
    def keyAddedSlot(self, ramp_key):
        ramp_index = ramp_key.ramp_index
        if self.blink_node.alloc(ramp_index) is False:
            self.blockSignals(True)
            self.removeKey(ramp_index)
            self.blockSignals(False)

    @Slot(QGraphicsItem)
    def keyRemovedSlot(self, ramp_index):
        pass

    @Slot(QGraphicsItem, float, float)
    def valueChangedSlot(self):
        pass

    def makeUI(self):
        return self

    def updateValue(self):
        return


node = nuke.thisNode()
knob = nuke.PyCustom_Knob("todo", "", "MyRamp(nuke.thisNode())")
node.addKnob(knob)