import sys

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication

from gui import MainWindow


def main():
    app = QApplication(sys.argv)

    File = QtCore.QFile("stylesheet.qss")
    if not File.open( QtCore.QFile.ReadOnly):
        return
    qss = QtCore.QTextStream(File)
    app.setStyleSheet(qss.readAll())#setup stylesheet

    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()