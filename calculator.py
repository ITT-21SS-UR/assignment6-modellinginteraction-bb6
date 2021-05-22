
from PyQt5 import QtCore, QtGui, QtWidgets, uic
import pandas as pd


# decorator function for logging to stdout
# (not a very pretty implementation, but only thought of them when i was done with the rest)
def decorator(func):
    def inner(*args, **kwargs):
        if len(args) > 2:
            print(args[2] + args[1])
        else:
            print(args[1])
        func(*args, **kwargs)

    return inner


class UI(QtWidgets.QMainWindow):

    # initializes class with some variables and loads ui file
    def __init__(self):
        super(UI, self).__init__()
        self.ui = uic.loadUi("calculator.ui", self)
        self.init_buttons()
        self.operatorslist = ["+", "-", "*", "/"]
        self.numberslist = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
        self.resultup = False

    # initializes all buttons
    def init_buttons(self):
        self.ui.zeroButton.clicked.connect(lambda x: self.on_numbutton('0', "button: "))
        self.ui.oneButton.clicked.connect(lambda x: self.on_numbutton('1', "button: "))
        self.ui.twoButton.clicked.connect(lambda x: self.on_numbutton('2', "button: "))
        self.ui.threeButton.clicked.connect(lambda x: self.on_numbutton('3', "button: "))
        self.ui.fourButton.clicked.connect(lambda x: self.on_numbutton('4', "button: "))
        self.ui.fiveButton.clicked.connect(lambda x: self.on_numbutton('5', "button: "))
        self.ui.sixButton.clicked.connect(lambda x: self.on_numbutton('6', "button: "))
        self.ui.sevenButton.clicked.connect(lambda x: self.on_numbutton('7', "button: "))
        self.ui.eigthButton.clicked.connect(lambda x: self.on_numbutton('8', "button: "))
        self.ui.nineButton.clicked.connect(lambda x: self.on_numbutton('9', "button: "))
        self.ui.plusButton.clicked.connect(lambda x: self.on_mathbutton('+', "button: "))
        self.ui.multButton.clicked.connect(lambda x: self.on_mathbutton('*', "button: "))
        self.ui.minusButton.clicked.connect(lambda x: self.on_mathbutton('-', "button: "))
        self.ui.divButton.clicked.connect(lambda x: self.on_mathbutton('/', "button: "))
        self.ui.equalButton.clicked.connect(lambda x: self.on_equalbutton("button: ="))
        self.ui.cButton.clicked.connect(lambda x: self.on_cbutton("button: c"))
        self.ui.ceButton.clicked.connect(lambda x: self.on_cebutton("button: ce"))

    # adds number to output, deletes result if a result is shown (logmsg only used for decorator function)
    @decorator
    def on_numbutton(self, key, logmsg):

        if self.resultup:
            self.resultup = False
            self.ui.outputlabel.setText(key)
        else:
            if self.ui.outputlabel.text() == "0":
                self.ui.outputlabel.setText("")
            self.ui.outputlabel.setText(self.ui.outputlabel.text() + key)

    # adds operator to output, but only if no other operator was pressed beforehand (logmsg only used for decorator function)
    @decorator
    def on_mathbutton(self, key, logmsg):
        if self.resultup:
            self.resultup = False
        if self.ui.outputlabel.text()[-1] in self.operatorslist:
            print("Can't follow operator with another operator")
        else:
            self.ui.outputlabel.setText(self.ui.outputlabel.text() + key)

    # prints result,  only shows 3 decimal places so the result is still readable (logmsg only used for decorator function)
    @decorator
    def on_equalbutton(self, logmsg):
        if self.ui.outputlabel.text()[-1] in self.operatorslist:
            print("Can't end on an operator you can use ce or backspace to undo the last button press")
        else:
            try:
                result = eval(self.ui.outputlabel.text())
                self.resultup = True
                self.ui.outputlabel.setText("{:.3f}".format(result) if result % 1 else str(result))
            except ZeroDivisionError:
                print("Stop dividing by Zero!")
                self.ui.outputlabel.setText("")

    # deletes the entire output (logmsg only used for decorator function)
    @decorator
    def on_cbutton(self, logmsg):
        if self.resultup:
            self.resultup = False
        self.ui.outputlabel.setText("0")

    # deletes last input, or reverts output to 0 if there is only a single digit or if a result is shown (logmsg only used for decorator function)
    @decorator
    def on_cebutton(self, logmsg):
        if self.resultup:
            self.resultup = False
            self.ui.outputlabel.setText("0")

        if len(self.ui.outputlabel.text()) > 1:
            self.ui.outputlabel.setText(self.ui.outputlabel.text()[:-1])
        else:
            self.ui.outputlabel.setText("0")

    # assigns keypress events to their respective functions
    def keyPressEvent(self, event):
        if event.text() in self.numberslist:
            self.on_numbutton(event.text(), "keystroke: ")
        elif event.text() in self.operatorslist:
            self.on_mathbutton(event.text(), "keystroke: ")
        elif event.key() == QtCore.Qt.Key_Backspace:
            self.on_cebutton("keystroke: backspace")
        elif event.key() == QtCore.Qt.Key_Delete:
            self.on_cbutton("keystroke: delete")
        elif event.key() == QtCore.Qt.Key_Return:
            self.on_equalbutton("keystroke: return")


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ui = UI()
    ui.show()
    sys.exit(app.exec_())
