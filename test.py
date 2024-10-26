from PySide2.QtWidgets import QMainWindow, QApplication
#try:
#    from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
#except ImportError:
#    from PySide2.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
#import rampWidget
import sys


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        #self.resize(800, 400)
        #self.ramp_widget = rampWidget.RampWidget(self)
        #self.setCentralWidget(self.ramp_widget)


app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())






