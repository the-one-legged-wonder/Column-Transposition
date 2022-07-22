import sys, os, math
import numpy as np
from functools import partial

from PyQt5.QtGui import QFont, QMovie, QIcon
from qt_material import apply_stylesheet
from requests.auth import HTTPBasicAuth

# Import QApplication and the required widgets from PyQt5.QtWidgets
from PyQt5.QtCore import Qt, pyqtSlot, QThreadPool, QSize
from PyQt5.QtWidgets import *


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


class MainWindow(QMainWindow):
    def __init__(self):
        """View initializer."""
        super().__init__()
        self.setWindowTitle("Encode Your Mother")
        self.setFixedSize(960, 540)
        self.setFont(QFont('Roboto', 12))
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        self.thread_manager = QThreadPool()
        self.currentPage = 1
        self.token = None


        self.createPage1()

    def createPage1(self):
        # Page 2
        self.page1 = QWidget()
        self.page1.setObjectName("pg1")
        self.page1Layout = QVBoxLayout()
        self.page1Layout.setContentsMargins(15, 15, 15, 15)
        self.page1Layout.setSpacing(10)

        self.tabs = QTabWidget()

        tab1 = QWidget()
        tab1lay = QVBoxLayout()
        label1 = QLabel("Type message here:")
        tab1lay.addWidget(label1)
        tab1txtbox = QTextEdit("")
        tab1lay.addWidget(tab1txtbox)
        queryContainer1 = QHBoxLayout()
        queryContainer1.addStretch()
        label2 = QLabel("Enter Key:")
        self.key_field1 = QLineEdit("")
        self.key_field1.textChanged.connect(partial(self.runAsync, self.updateKeyFields, self.key_field1.text()))
        queryContainer1.addWidget(label2)
        queryContainer1.addWidget(self.key_field1)
        queryContainer1.addWidget(QLabel("Output:"))
        lineEdit1 = QLineEdit("")
        lineEdit1.setReadOnly(True)
        queryContainer1.addWidget(lineEdit1)
        queryContainer1.addStretch()
        tab1lay.addLayout(queryContainer1)
        tab1.setLayout(tab1lay)

        tab2 = QWidget()
        tab2lay = QVBoxLayout()
        label3 = QLabel("Paste encoded message here:")
        tab2lay.addWidget(label3)
        tab2txtbox = QTextEdit("")
        tab2lay.addWidget(tab2txtbox)
        queryContainer2 = QHBoxLayout()
        queryContainer2.addStretch()
        label3 = QLabel("Enter Key:")
        self.key_field2 = QLineEdit("")
        self.key_field2.textChanged.connect(partial(self.runAsync, self.updateKeyFields, self.key_field2.text()))
        queryContainer2.addWidget(label3)
        queryContainer2.addWidget(self.key_field2)
        queryContainer2.addWidget(QLabel("Output:"))
        lineEdit2 = QLineEdit("")
        lineEdit2.setReadOnly(True)
        queryContainer2.addWidget(lineEdit2)
        queryContainer2.addStretch()
        tab2lay.addLayout(queryContainer2)
        tab2.setLayout(tab2lay)

        self.tabs.addTab(tab1, "Encode")
        self.tabs.addTab(tab2, "Decode")
        self.page1Layout.addWidget(self.tabs)

        # Nav Buttons
        btnLay = QHBoxLayout()
        btnLay.addStretch()

        self.btnCopy = QPushButton("Copy Output")
        self.btnCopy.clicked.connect(partial(self.addToClipboard))
        self.btnCopy.setEnabled(True)

        self.btnNext2 = QPushButton("Go")
        self.btnNext2.setStyleSheet("background-color: green; color: white;")
        self.btnNext2.setFont(QFont('Arial', 12))
        self.btnNext2.clicked.connect(partial(self.runAsync, self.doRequest))
        self.btnNext2.setEnabled(True)
        btnLay.addWidget(self.btnCopy)
        btnLay.addWidget(self.btnNext2)
        btnLay.addStretch()
        self.page1Layout.addLayout(btnLay)

        self.page1.setLayout(self.page1Layout)
        self.stacked_widget.addWidget(self.page1)

    def check_id(self, *args):
        pass
        return

    def doRequest(self, *args):
        self.btnNext2.setIconSize(QSize(32, 32))
        self.btnNext2.setText("  Go")

        print(self.tabs.currentIndex())

        if self.tabs.currentIndex() == 0:
            key = self.tabs.currentWidget().layout().itemAt(2).layout().itemAt(2).widget().text()
            message = self.tabs.currentWidget().layout().itemAt(1).widget().toPlainText()
            print(key, message)
            output = self.encode(key, message)
        else:
            key = self.tabs.currentWidget().layout().itemAt(2).layout().itemAt(2).widget().text()
            message = self.tabs.currentWidget().layout().itemAt(1).widget().toPlainText()
            print(key, message)
            output = self.decode(key, message)

        print(output)
        if output:
            self.tabs.currentWidget().layout().itemAt(2).layout().itemAt(4).widget().setText(output)
        else:
            pass

        self.btnNext2.setText("Go")
        self.btnNext2.setIconSize(QSize(0, 0))

    def addToClipboard(self):
        if self.tabs.currentWidget().layout().itemAt(2).layout().itemAt(4).widget().text() != "":
            clipboard.setText(self.tabs.currentWidget().layout().itemAt(2).layout().itemAt(4).widget().text())
        else:
            WarnAlert("Please select an item").exec_()

    def updateKeyFields(self, *args):
        self.key_field1.setText(args[1])
        self.key_field2.setText(args[1])

    def encode(self, key, message):
        if len(key) > 9:
            ErrorAlert("Encryption key too long (key length < 9 please)").exec_()
            return False
        clean_message = message.replace(" ", "_")  # .lower().replace("_","")

        sort_order = [k for k, v in sorted(
            list({k + 1: v for k, v in enumerate(key)}.items()),
            key=lambda keyval: keyval[1]
        )]

        # create 2d array from clean_message
        pos = 0
        cols = math.ceil(len(clean_message) / len(key))
        rows = len(key)
        arr = np.zeros(shape=(cols, rows), dtype=str)

        for x in range(cols):
            for y in range(rows):
                if pos < len(clean_message):
                    arr[x][y] = clean_message[pos]
                else:
                    arr[x][y] = "_"
                pos += 1

        # sort each row of the array
        for x in range(cols):
            sorttttt = list(
                {k: v for k, v in sorted(list({k + 1: v for k, v in enumerate(arr[x])}.items()),
                                         key=lambda i: sort_order.index(i[0]))}.values())
            arr[x] = sorttttt

        return "".join([x for y in arr for x in y])

    def decode(self, key, message):
        if len(key) > 9:
            ErrorAlert("Encryption key too long (key length < 9 please)").exec_()
            return False

        header = {k: v for k, v in sorted(
            list({k + 1: v for k, v in enumerate(key)}.items()),
            key=lambda keyval: keyval[1]
        )}
        sort_order = [x for x in header]
        wanted_sort_order = [x for x in range(1, len(key) + 1)]

        # create 2d array from message
        pos = 0
        cols = math.ceil(len(message) / len(key))
        rows = len(key)
        arr = np.zeros(shape=(cols, rows), dtype=str)

        for x in range(cols):
            for y in range(rows):
                if pos < len(message):
                    arr[x][y] = message[pos]
                pos += 1

        # sort each row of the array
        for x in range(cols):
            sorttttt = list(
                {k: v for k, v in sorted(list({k + 1: v for k, v in enumerate(arr[x])}.items()),
                                         key=lambda i: sort_order[i[0] - 1])}.values())

            arr[x] = sorttttt

        return "".join([x for y in arr for x in y]).replace("_", " ").strip()

    @pyqtSlot()
    def runAsync(self, fn, *args):
        self.thread_manager.start(partial(fn, *args))


class WarnAlert(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Warning")
        self.setFont(QFont('Roboto', 11))
        self.setObjectName('dialog')
        self.setIcon(QMessageBox.Warning)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)

    def apply(self):
        self.close()


class ErrorAlert(QMessageBox):
    def __init__(self, message):
        super().__init__()
        self.setWindowTitle("Error")
        self.setFont(QFont('Roboto', 11))
        self.setObjectName('dialog')
        self.setIcon(QMessageBox.Critical)
        self.setText(message)
        self.setStandardButtons(QMessageBox.Ok)

    def apply(self):
        self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    clipboard = app.clipboard()
    app.setStyle('Fusion')

    #palette = QPalette()
    #palette.setColor(QPalette.Window, QColor(53, 53, 53))
    #palette.setColor(QPalette.WindowText, Qt.white)
    #palette.setColor(QPalette.Base, QColor(15, 15,15))
    #palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    #palette.setColor(QPalette.ToolTipBase, Qt.white)
    #palette.setColor(QPalette.ToolTipText, Qt.white)
    #palette.setColor(QPalette.Text, Qt.white)
    #palette.setColor(QPalette.Button, QColor(53, 53, 53))
    #palette.setColor(QPalette.ButtonText, Qt.white)
    #palette.setColor(QPalette.BrightText, Qt.red)
    #palette.setColor(QPalette.Highlight, QColor(142, 45, 197).lighter())
    #palette.setColor(QPalette.HighlightedText, Qt.black)
    #app.setPalette(palette)
    apply_stylesheet(app, theme='dark_teal.xml')
    app.setFont(QFont('Roboto', 11))

    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
