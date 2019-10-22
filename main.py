import sys
from PyQt5.QtWidgets import (QWidget, QPushButton, QLineEdit,
QInputDialog, QApplication, QMessageBox)
import subprocess
from ui import Ui_Form

class Example(Ui_Form):
    def __init__(self, form):
        super().__init__()
        self.setupUi(form)
        self.connect_slots()

    def connect_slots(self):
        self.pushButton.clicked.connect(self.buttonClicked)

    def buttonClicked(self):
        mes = QMessageBox()
        ar = ['python3', self.lineEdit.text()+'.py']
        ar.extend(self.lineEdit_2.text().split(' '))
        re = subprocess.run(ar)
        mes.setText(str(re))
        mes.exec_()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = QWidget()
    ui = Example(window)
    window.show()
    # ex = Example()
    sys.exit(app.exec_())
