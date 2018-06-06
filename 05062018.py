import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, \
    QPushButton, QLineEdit, QLabel
from PyQt5.QtCore import pyqtSlot
import parser
from numpy import arange
from math import *
import matplotlib.pyplot as plt
import datetime


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self._eq_in = QLineEdit(self)
        self._eq_in.resize(80, 20)
        self._eq_in.move(35, 10)
        self._a_in = XInput(self)
        self._a_in.move(135, 10)
        self._b_in = XInput(self)
        self._b_in.move(181, 10)

        func_label = QLabel(self)
        func_label.setText('y =')
        func_label.move(10, 6)
        func_label.resize(18, 27)
        interval_label1 = XLabel(self)
        interval_label1.setText('[')
        interval_label1.move(128, 6)
        interval_label2 = XLabel(self)
        interval_label2.setText(';')
        interval_label2.move(176, 6)
        interval_label3 = XLabel(self)
        interval_label3.setText(']')
        interval_label3.move(223, 6)

        plot_button = QPushButton('Go!', self)
        plot_button.move(65, 40)
        plot_button.clicked.connect(self.go)

        self._result_label = QLabel(self)
        self._result_label.move(85, 80)

        self.setFixedSize(260, 120)
        self.setWindowTitle('Method of middle rectangles')
        self.setStyleSheet(open('style.css', 'r').read())
        self.show()

    @pyqtSlot()
    def go(self):
        try:
            equation = parser.expr(self.eq_in).compile()
            a = self.a_in
            b = self.b_in
        except (SyntaxError, ValueError):
            self.result_label = "Invalid input!"
            self._eq_in.setText("")
            self._a_in.setText("")
            self._b_in.setText("")
            return
        h = abs((self.a_in - self.b_in) / 100)
        xs = arange(a + h / 2, b, h)
        ys = []
        for x in xs:
            ys.append(eval(equation))
        area = self.method_of_middle_rectangles(ys, h)
        self.result_label = "Area: %.3f" % area
        self.log(area)
        plt.close('all')
        plt.plot(xs, ys, 'b')
        plt.show()

    def log(self, area):
        f = open('MethodOfMiddleRectanglesLog.txt', 'a')
        now = datetime.datetime.now()
        f.write("%s %f %f %s %.3f\n"
                % (now.strftime('%Y-%m-%d %H:%M'), self.a_in, self.b_in, self.eq_in, area))
        f.close()

    @staticmethod
    def method_of_middle_rectangles(ys, h):
        area = 0.0
        for y in ys:
            area += abs(y) * h
        return area

    @property
    def a_in(self):
        return float(self._a_in.text())

    @property
    def b_in(self):
        return float(self._b_in.text())

    @property
    def eq_in(self):
        return self._eq_in.text()

    @property
    def result_label(self):
        return self._result_label.text()

    @result_label.setter
    def result_label(self, value):
        self._result_label.setText(str(value))


class XInput(QLineEdit):
    def __init__(self, window):
        super(XInput, self).__init__(window)
        self.resize(40, 20)

class XLabel(QLabel):
    def __init__(self, window):
        super(XLabel, self).__init__(window)
        self.resize(5, 27)


app = QApplication(sys.argv)
gui = Window()
sys.exit(app.exec_())
