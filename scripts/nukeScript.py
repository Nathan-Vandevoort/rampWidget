# I put all my definition code into a multiline string (using """)
the_code = """import sys
sys.path.append('Z:/Repos/RampWidget')
import rampWidget


class MyBox(rampWidget.RampWidget):

    def __init__(self, parent):
        super(MyBox, self).__init__()
        width = 400
        height = 200

        self.ramp_view.controller.setSceneDimensions(width, height)
        self.ramp_view.controller.setScenePadding(0, 20, 0, 40)
        self.ramp_view.controller.initializeRamp()


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
knob = nuke.PyCustom_Knob("todo", "", "MyBox(nuke.thisNode())")
node.addKnob(knob)

nuke.clearDiskCache()