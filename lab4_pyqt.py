import sys
import time
import numpy as np
from voltera_time import voltera_time
from isolines import voltera_isolines

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QHBoxLayout, QLineEdit,\
     QMessageBox, QGridLayout, QDesktopWidget, QLabel, QSizePolicy, QCheckBox
from PyQt5.QtCore import QTimer

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib import rcParams

plt.style.use('ggplot')
rcParams['font.size'] = 13
rcParams['mathtext.fontset'] = 'cm'
rcParams['font.family'] = 'STIXGeneral'
rcParams['text.color'] = 'white'
rcParams['axes.labelcolor'] = 'white'
rcParams['xtick.color'] = 'white'
rcParams['ytick.color'] = 'white'
rcParams['axes.facecolor'] = '#1B2027'
rcParams['figure.facecolor'] = '#1B2027'
rcParams['savefig.facecolor'] = '#1B2027'


# Ініціалізація вікна
class Window(QDialog):
    def __init__(self, parent = None):
        super(Window, self).__init__(parent)        
        self.showMaximized() 

        # Фігура
        self.figure_time = plt.figure()
        self.figure_depend = plt.figure()

        # Ініціалізує параметр canvas
        self.canvas_predator_prey_time = FigureCanvas(self.figure_time)
        self.canvas_predator_prey_depend = FigureCanvas(self.figure_depend)

        self.toolbar_time = NavigationToolbar(self.canvas_predator_prey_time, self)
        self.toolbar_depend = NavigationToolbar(self.canvas_predator_prey_depend, self)

        # Поле вводу та підписи
        self.textBox_A = QLineEdit(self)
        self.textBox_A.setText("1.58")
        self.textBox_B = QLineEdit(self)
        self.textBox_B.setText("1.94")
        self.textBox_C = QLineEdit(self)
        self.textBox_C.setText("1.19")
        self.textBox_D = QLineEdit(self)
        self.textBox_D.setText("0.63")
        self.buttonFormula = QPushButton(self)
        self.buttonFormula.setText("Cистема")
        self.buttonFormula.clicked.connect(self.dif_system_dialog) 
        self.textBox_X = QLineEdit(self)
        self.textBox_X.setText("2.85")
        self.textBox_Y = QLineEdit(self)
        self.textBox_Y.setText("1.85")
        self.textBox_t1 = QLineEdit(self)
        self.textBox_t1.setText("9")
        self.textBox_t2 = QLineEdit(self)
        self.textBox_t2.setText("39")
        self.checkBox = QCheckBox("Ізолінії")
        self.checkBox.setChecked(False)

        # Оновлення з часом
        self.timer = QTimer()
        self.timer.timeout.connect(self.plot)
        self.timer.start(1000)

        # Група текстових полів
        textBoxLayoutInit = QHBoxLayout()
        textBoxLayoutInit.addWidget(QLabel("a = "))
        textBoxLayoutInit.addWidget(self.textBox_A)
        textBoxLayoutInit.addWidget(QLabel("b = "))
        textBoxLayoutInit.addWidget(self.textBox_B)
        textBoxLayoutInit.addWidget(QLabel("c = "))
        textBoxLayoutInit.addWidget(self.textBox_C)
        textBoxLayoutInit.addWidget(QLabel("d = "))
        textBoxLayoutInit.addWidget(self.textBox_D)
        textBoxLayoutInit.addWidget(self.buttonFormula)
        textBoxLayoutInit.addStretch(4)

        textBoxLayoutInitXY = QHBoxLayout()
        textBoxLayoutInitXY.addWidget(QLabel("x0 = "))
        textBoxLayoutInitXY.addWidget(self.textBox_X)
        textBoxLayoutInitXY.addWidget(QLabel("y0 = "))
        textBoxLayoutInitXY.addWidget(self.textBox_Y)
        textBoxLayoutInitXY.addWidget(self.checkBox)
        textBoxLayoutInitXY.addStretch(3)
        textBoxLayoutInitXY.addWidget(QLabel("t = "))
        textBoxLayoutInitXY.addWidget(self.textBox_t1)
        textBoxLayoutInitXY.addWidget(self.textBox_t2)

        # Задаємо слой
        grid = QGridLayout()
        grid.addWidget(self.toolbar_time, 0, 0)
        grid.addWidget(self.toolbar_depend, 0, 1)
        grid.addLayout(textBoxLayoutInit, 1, 0, 1, 1)
        grid.addLayout(textBoxLayoutInitXY, 1, 1, 1, 1)
        grid.addWidget(self.canvas_predator_prey_time, 2, 0)
        grid.addWidget(self.canvas_predator_prey_depend, 2, 1)
        self.setLayout(grid)

    # Побудова
    def plot(self):
        eps = 0.001

        # Отримуємо шлях до файлу
        a_value = self.textBox_A.text()
        b_value = self.textBox_B.text()
        c_value = self.textBox_C.text()
        d_value = self.textBox_D.text()
        x0_value = self.textBox_X.text()
        y0_value = self.textBox_Y.text()
        t1_value = self.textBox_t1.text()
        t2_value = self.textBox_t2.text()

        # Очищає фігуру при перезавантаженні
        self.figure_time.clear()
        self.figure_depend.clear()

        # Сформувати осі
        ax_time = self.figure_time.add_subplot(111)
        ax_depend = self.figure_depend.add_subplot(111)
        try:
            a = float(a_value)
            b = float(b_value)
            c = float(c_value)
            d = float(d_value)
            x0 = float(x0_value)
            y0 = float(y0_value)
            t1 = float(t1_value)
            t2 = float(t2_value)

            ax_depend.set_title("Фазовий портрет системи")
            ax_time.set_title("Динаміка популяцій")

            t_list, x_data, y_data = voltera_time(a, b, c, d, x0, y0, t1, t2, eps = eps)

            ax_time.plot(t_list, x_data, label = 'Здобич', linewidth = 2)
            ax_time.plot(t_list, y_data, label = 'Хижак', linewidth = 2, linestyle = "--")
            ax_time.set(xlabel = r"$t$", ylabel = r"$x$, $y$")

            if self.checkBox.isChecked() == True:
                X2, Y2, Z2 = voltera_isolines(a, b, c, d, x_data, y_data)
                ax_depend.contourf(X2, Y2, Z2, cmap=plt.cm.CMRmap, alpha=0.5)
                ax_depend.contour(X2, Y2, Z2, colors='black', linewidths=2. )
            else:
                ax_depend.plot(x_data, y_data)

            ax_depend.scatter(c / d, a / b, color = "#CD5C5C") 
            ax_depend.annotate(r'Критична точка, ({}, {})'.format(round(c / d, 2), round(a / b, 2)), xy = (c / d, a / b), xytext = (-20,20), 
                textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle = 'round, pad=0.2', fc = 'white', alpha = 0.3),
                arrowprops=dict(arrowstyle = '->', color = 'red', linewidth = 1))
            ax_depend.set(xlabel = r"$x$", ylabel = r"$y$")

            ax_time.legend(loc = 'upper left')
        except:
            pass

        ax_time.grid(True)
        ax_depend.grid(True)
        self.canvas_predator_prey_time.draw()
        self.canvas_predator_prey_depend.draw()

    def dif_system_dialog(self):
        try:
            a = float(self.textBox_A.text())
            b = float(self.textBox_B.text())
            c = float(self.textBox_C.text())
            d = float(self.textBox_D.text())
            x0 = float(self.textBox_X.text())
            y0 = float(self.textBox_Y.text())
            t1 = float(self.textBox_t1.text())

            first_eq = r"$\frac{dx}{dt}$" + r"$ = {}x - {}xy$".format(a, b)
            second_eq = r"$\frac{dy}{dt}$" + r"$ = {}y + {}xy$".format(-c, d)
            first_eq_cauchy = r"$\frac{dx}{dt}$" + r"$ = {}x(t) - {}x(t)y(t)$".format(a, b)
            second_eq_cauchy = r"$\frac{dy}{dt}$" + r"$ = {}y(t) + {}x(t)y(t)$".format(-c, d)
            third_eq_cauchy = r"$y({}) = {}, x({}) = {}$".format(t1, y0, t1, x0)

            formula_figure = plt.figure()
            formula_figure.tight_layout()
            formula_canvas = FigureCanvas(formula_figure)

            ax1 = formula_figure.add_subplot(2, 1, 1)
            ax1.set_title('Система диференціальних рівнянь')
            ax1.text(0, 0.75, s = first_eq, fontsize = 24)
            ax1.text(0, 0.44, s = second_eq, fontsize = 24)
            ax1.text(-0.08, 0.47, s = r"$\{$", fontsize = 50)
            ax1.axis('off')

            ax2 = formula_figure.add_subplot(2, 1, 2)
            ax2.set_title('Задача Коші')
            ax2.text(0, 0.75, s = first_eq_cauchy, fontsize = 24)
            ax2.text(0, 0.44, s = second_eq_cauchy, fontsize = 24)
            ax2.text(0, 0.22, s = third_eq_cauchy, fontsize = 24)
            ax2.text(-0.11, 0.32, s = r"$\{$", fontsize = 70)
            ax2.axis('off')

            formula_canvas.show()
        except:
            msg = QMessageBox()
            msg.setText("Введено не правильні дані.")
            msg.exec()

    # Закриття вікна
    def closeEvent(self, event):
        reply = QMessageBox.question(self, 'Повідомлення', 'Ви впевнені, що хочете вийти?', QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            event.accept()

        else:
            event.ignore()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')

    main = Window()
    main.show()

    sys.exit(app.exec_())
