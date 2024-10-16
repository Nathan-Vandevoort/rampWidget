from PySide6.QtWidgets import QMainWindow, QApplication, QGraphicsScene, QGraphicsView
import rampWidget
import sys
import logging

logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(800, 400)
        self.ramp_widget = rampWidget.RampWidget(self, logger=logger)
        self.setCentralWidget(self.ramp_widget)

app = QApplication(sys.argv)
main_window = MainWindow()
main_window.show()
sys.exit(app.exec())






