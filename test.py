from PySide6.QtWidgets import QMainWindow, QApplication
import rampWidget as rw
import sys


class MainWindow(QMainWindow):
    def __init__(self, qapp: QApplication, parent=None):
        super().__init__(parent=parent)

        self.qapp = qapp

        self.setWindowTitle('Ramp Test')

        self.ramp_widget = rw.RampWidget(parent=self)

        self.setCentralWidget(self.ramp_widget)


app = QApplication(sys.argv)
main_window = QMainWindow()
main_window.show()
sys.exit(app.exec())