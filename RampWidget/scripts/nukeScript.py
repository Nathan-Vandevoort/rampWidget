# I put all my definition code into a multiline string (using """)
the_code = """import sys
from PySide2.QtWidgets import QWidget
sys.path.append('Z:/Repos/RampWidget')
from RampWidget import qRampWidget


class MyRamp(qRampWidget.QRampWidget):

    def __init__(self, parent):
        super(MyRamp, self).__init__()
        width = 500
        height = 500

        self.setSceneDimensions(width, height)
        self.setScenePadding(0, 13, 0, 26)
        self.start()


    def makeUI(self):
        return self

    def updateValue(self):
        return

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