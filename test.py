# -*- coding: utf-8 -*-
'''
           _____                    _____
          /\    \                  /\    \                 ______
         /::\    \                /::\    \               |::|   |
        /::::\    \              /::::\    \              |::|   |
       /::::::\    \            /::::::\    \             |::|   |
      /:::/\:::\    \          /:::/\:::\    \            |::|   |
     /:::/__\:::\    \        /:::/__\:::\    \           |::|   |
    /::::\   \:::\    \      /::::\   \:::\    \          |::|   |
   /::::::\   \:::\    \    /::::::\   \:::\    \         |::|   |
  /:::/\:::\   \:::\____\  /:::/\:::\   \:::\    \  ______|::|___|___ ____
 /:::/  \:::\   \:::|    |/:::/__\:::\   \:::\____\|:::::::::::::::::|    |
 \::/   |::::\  /:::|____|\:::\   \:::\   \::/    /|:::::::::::::::::|____|
  \/____|:::::\/:::/    /  \:::\   \:::\   \/____/  ~~~~~~|::|~~~|~~~
        |:::::::::/    /    \:::\   \:::\    \            |::|   |
        |::|\::::/    /      \:::\   \:::\____\           |::|   |
        |::| \::/____/        \:::\   \::/    /           |::|   |
        |::|  ~|               \:::\   \/____/            |::|   |
        |::|   |                \:::\    \                |::|   |
        \::|   |                 \:::\____\               |::|   |
         \:|   |                  \::/    /               |::|___|
          \|___|                   \/____/                 ~~

'''
#---------------------------------------------------------------------------------------#
#                               CREATED BY MAX H. FUNG, 2018
#                                  FOR AEROJET ROCKETDYNE
#---------------------------------------------------------------------------------------#
# cd /d C:\engapps\Anaconda2\
# activate rex
# python U:\MaxFung\Source_Code\REX_Dev\rex.py
# pyi-makespec --onedir --windowed U:\MaxFung\Source_Code\REX_Dev\rex.py
# https://stackoverflow.com/questions/50135676/pyinstaller-and-seaborn
# pyinstaller --onedir --windowed --icon=U:\MaxFung\Source_Code\REX_Dev\icon.ico U:\MaxFung\Source_Code\REX_Dev\rex.py
#---------------------------------------------------------------------------------------#

'''
| _  _  _  _|_ _
|||||_)(_)| |__)
    |
'''

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import glob, os, sys, random
import visa
import matplotlib
# matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from numpy import linspace
#import matplotlib
# matplotlib.use('Qt5Agg')
#import matplotlib.pyplot as plt

QApplication.setStyle(QStyleFactory.create("Fusion"))
style = 'background: rgb(43, 71, 79);color: rgb(140, 195, 212); font-family:bahnschrift;font-size: 20px;'
funte = "bahnschrift"
blue = "#27c9d9"

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

logo = resource_path('logo.png')
# fnt = resource_path("fonts\\bahnschrift.ttf")
fnt = resource_path("fonts/bahnschrift.ttf")
users = resource_path('users.txt')
# results = resource_path('results\\')
results = resource_path('results/')

gurney = resource_path('gurney.png')
# trans_data = resource_path('trans_data\\')
trans_data = resource_path('trans_data/')



'''

|\/| _ . _   |  |. _  _| _
|  |(_||| )  |/\||| )(_|(_)\)/

'''

class MainWindow(QWidget):

    def __init__(self, parent = None):
        super(MainWindow, self).__init__(parent)
        self.width, self.height = 1230, 692
        self.title = 'REX'
        self.setStyleSheet(style)
        self.setFixedSize(1230, 692)
        self.Console = Console(self)
        self.Settings = Settings(self)
        self.int_validator = QIntValidator(0,50000,self)
#       From settings, get the GPIB and ASRL names, addresses, and cmds.
        self.initUI()

    def initUI(self):

        self.label_logo = QLabel()
        pixmap = QPixmap(logo)
        pixmap = pixmap.scaledToHeight(120)
        self.label_logo.setPixmap(pixmap)
        self.label_logo.setStyleSheet("padding-left:30px;")

        self.label_slogan = QLabel("Calibration <b>Assistant</b>")
        self.label_slogan.setStyleSheet("QLabel {font-family:Bahnschrift SemiLight;font-size:25px;font-weight:lighter;color:#63a5b8;text-align:left;}")

        link_sheet = ''' QPushButton{font-family:Bahnschrift SemiLight;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px; padding-right:10px;}
                              QPushButton:hover{color: #2eecff;}'''
        link_tb_sheet = ''' QToolButton{font-family:Bahnschrift SemiLight;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px; padding-right:10px;}
                              QToolButton:hover{color: #2eecff;}'''

        self.link_calibrate = QPushButton("CALIBRATE")
        self.link_calibrate.setStyleSheet(link_sheet)
        self.link_calibrate.setFixedWidth(110)

        self.link_library = QPushButton("LIBRARY")
        self.link_library.setStyleSheet(link_sheet)
        self.link_library.setFixedWidth(110)

        self.link_settings = QToolButton(self)
        self.link_settings.setText("SETTINGS")
        self.link_settings.setStyleSheet(link_tb_sheet)
        self.link_settings.setFixedWidth(110)
        self.link_settings.setPopupMode(QToolButton.InstantPopup)
        self.link_settings_menu = QMenu(self.link_settings)
        self.link_settings.setMenu(self.link_settings_menu)
        self.link_settings_action = QWidgetAction(self.link_settings)
        self.link_settings_action.setDefaultWidget(self.Settings)
        self.link_settings.menu().addAction(self.link_settings_action)

        self.toolbar_frame = QFrame()
        self.toolbar_frame.setFixedSize(500,110)

        self.toolbar_layout = QHBoxLayout(self.toolbar_frame)
        self.toolbar_layout.addWidget(self.link_calibrate, Qt.AlignRight)
        self.toolbar_layout.addWidget(self.link_library, Qt.AlignRight)
        self.toolbar_layout.addWidget(self.link_settings, Qt.AlignRight)

        self.header_frame = QFrame()
        self.header_frame.setStyleSheet("background: rgb(43, 71, 79);")
        self.header_frame.setFixedSize(self.width,120)

        self.header_layout = QHBoxLayout(self.header_frame)
        self.header_layout.addStretch()
        self.header_layout.addWidget(self.label_logo, 1, Qt.AlignTop)
        self.header_layout.addWidget(self.label_slogan, 8, Qt.AlignLeft)
        self.header_layout.addWidget(self.toolbar_frame, Qt.AlignRight)

        self.body_frame = QFrame()
        self.body_frame.setFixedSize(self.width,self.height - 120)
        self.body_frame.setStyleSheet("background-color:rgb(28, 48, 54);padding: 0px 0px 0px 0px;")

        self.body_layout = QHBoxLayout(self.body_frame)
        self.body_layout.addWidget(self.Console,1,Qt.AlignLeft)
        self.body_layout.setContentsMargins(0,0,0,0)

        self.top_layout = QVBoxLayout(self)
        self.top_layout.addWidget(self.header_frame, 1, Qt.AlignTop)
        self.top_layout.addWidget(self.body_frame,1,Qt.AlignTop)
        self.top_layout.setContentsMargins(0, 0, 0, 0)

        self.PlotCanvas = PlotCanvas(self, width=6.5, height=5)
        self.PlotCanvas.move(360-50,96)
        self.PlotCanvas.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;")

        self.plot_label_title = QLabel("",self)
        self.plot_label_title.setFixedWidth(300)
        self.plot_label_title.move(410,170)
        self.plot_label_title.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;")

        self.plot_label_legend_1 = QLabel("",self)
        self.plot_label_legend_1.setFixedWidth(300)
        self.plot_label_legend_1.move(410,195)
        self.plot_label_legend_1.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'aquamarine';font-size:12px;")

        self.plot_label_legend_2 = QLabel("",self)
        self.plot_label_legend_2.setFixedWidth(300)
        self.plot_label_legend_2.move(410,215)
        self.plot_label_legend_2.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'MediumTurquoise';font-size:12px;")

        self.Console.show()
        self.Console.activateWindow()
        self.Console.raise_()

        self.Console.button_next.clicked.connect(self.console_next)
        self.Console.button_back.clicked.connect(self.console_back)

        self.show()

        self.label_pressure = QLabel("Specify actual pressure",self)
        self.label_pressure.setFixedWidth(300)
        self.label_pressure.setStyleSheet("font-size:20px;background-color:transparent;padding: 0px 0px 0px 0px;")
        self.label_pressure.move(33,393)
        self.lineEdit_pressure = QLineEdit(self)
        self.lineEdit_pressure.move(30,430)
        self.lineEdit_pressure.setFixedSize(298,90)
        self.lineEdit_pressure.setStyleSheet("QLineEdit{background-color:transparent;border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; font-size:85px;} QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}")
        self.lineEdit_pressure.setPlaceholderText("0")
        self.lineEdit_pressure.setMaxLength(5)
        self.lineEdit_pressure.textChanged.connect(self.gui_move_psi_label)
        self.lineEdit_pressure.setValidator(self.int_validator)
        self.label_psi = QLabel("PSI",self)
        self.label_psi.setFixedSize(300,100)
        self.label_psi.setStyleSheet("font-size:41px;background-color:transparent;padding: 0px 0px 0px 0px;")
        self.label_psi.move(30+45+15,443)

    def console_next(self):
        print 'Console -> NEXT -> MainWindow'
        # z is the % mV / Pressure. It demonstrates +-0.5% Full Scale Error
        y=[2.4254,8.5509,14.6393,20.7161,26.789,32.835,32.834,26.7674,20.6804,14.5967,8.5129,2.4026]
        z=[0,0.127556574,0.433207613,0.100742637,0.055462793,-0.078206777,-0.081492641,-0.015511857,-0.016562688,-0.00677017,-0.6002693763,-0.074917687]

        if self.Console.step_no == 2:
            self.int_validator.setRange(0,int(self.Console.setup_full_scale)+int(self.Console.setup_full_scale)*0.05)
            self.plot_label_title.setText(self.Console.setup_property_number)
            self.plot_label_legend_1.setText("PSI, mV")
            self.plot_label_legend_2.setText("±0.5% FS ERR")

            self._X = []
            self._Y = []
            self._Z = []

            print self._X, self._Y, self._Z

            self.PlotCanvas.updateData(x=self._X, y=self._Y, z=self._Z, span=int(self.Console.setup_full_scale))

        if self.Console.step_no == 6:
            self.label_pressure.show()
            self.label_psi.show()
            self.lineEdit_pressure.show()
            self.lineEdit_pressure.setFocus()

        if 19 > self.Console.step_no > 6:

            _pressure = self.lineEdit_pressure.text()

            self.lineEdit_pressure.clear()

            if 18 > self.Console.step_no:
                self.lineEdit_pressure.setPlaceholderText(self.Console.text_console_pressure[self.Console.step_scale_index])
                self.gui_move_psi_label(self.Console.text_console_pressure[self.Console.step_scale_index])
                self.lineEdit_pressure.setFocus()

            if self.Console.step_scale_index >= 1:

                if _pressure != '':
                    self._X.append(int(_pressure))
                else:
                    self._X.append(int(self.Console.text_console_pressure[self.Console.step_scale_index-1]))

                self._Y.append(y[self.Console.step_scale_index-1])
                self._Z.append(z[self.Console.step_scale_index-1])

                if z[self.Console.step_scale_index-1] > 0.5:
                    self.plot_label_legend_2.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'OrangeRed';font-size:12px;")
                elif z[self.Console.step_scale_index-1] < -0.5:
                    self.plot_label_legend_2.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'OrangeRed';font-size:12px;")

                self.PlotCanvas.updateData(x = self._X, y = self._Y, z=self._Z, span=int(self.Console.setup_full_scale))

                print self._X, self._Y, self._Z

        if self.Console.step_no == 18:
            self.lineEdit_pressure.clear()
            self.label_pressure.hide()
            self.label_psi.hide()
            self.lineEdit_pressure.hide()


    def console_back(self):
        print 'Console -> BACK -> MainWindow'
        y=[2.4254,8.5509,14.6393,20.7161,26.789,32.835,32.834,26.7674,20.6804,14.5967,8.5129,2.4026]
        z=[-0.8,0.127556574,0.133207613,0.100742637,0.055462793,-0.078206777,-0.081492641,-0.015511857,-0.016562688,-0.00677017,0.002693763,-0.074917687]

        if self.Console.step_no == 1:
            self.plot_label_title.setText("")
            self.plot_label_legend_1.setText("")
            self.plot_label_legend_2.setText("")
            self.PlotCanvas.updateData(ticks=False, x=self._X, y=self._Y, z=self._Z, span=int(self.Console.setup_full_scale))

        if self.Console.step_no == 5:

            self.lineEdit_pressure.clear()

            self.label_pressure.hide()
            self.label_psi.hide()
            self.lineEdit_pressure.hide()

        if self.Console.step_no == 6:

            self.lineEdit_pressure.clear()
            self.lineEdit_pressure.setFocus()
            self.lineEdit_pressure.setPlaceholderText("0")
            self.gui_move_psi_label(self.Console.text_console_pressure[self.Console.step_scale_index])

            self._X = []
            self._Y = []
            self._Z = []

            print self._X, self._Y, self._Z

            self.plot_label_legend_2.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'MediumTurquoise';font-size:12px;")

            self.PlotCanvas.updateData(x=self._X, y=self._Y, z=self._Z, span=int(self.Console.setup_full_scale))

        if 19 > self.Console.step_no > 6:

            self.lineEdit_pressure.clear()
            self.lineEdit_pressure.setPlaceholderText(self.Console.text_console_pressure[self.Console.step_scale_index])
            self.gui_move_psi_label(self.Console.text_console_pressure[self.Console.step_scale_index])
            self.lineEdit_pressure.setFocus()
            self.gui_move_psi_label(self.Console.text_console_pressure[self.Console.step_scale_index])

            if self.Console.step_scale_index >= 1:

                del self._X[-1]
                del self._Y[-1]
                del self._Z[-1]

                if max(self._Z) < 0.5 and min(self._Z) > -0.5:
                    self.plot_label_legend_2.setStyleSheet("background-color:transparent;padding: 0px 0px 0px 0px;color:'MediumTurquoise';font-size:12px;")

                self.PlotCanvas.updateData(x = self._X, y = self._Y, z=self._Z, span=int(self.Console.setup_full_scale))

                print self._X, self._Y, self._Z

        if self.Console.step_no == 17:
            self.label_pressure.show()
            self.label_psi.show()
            self.lineEdit_pressure.show()


    def gui_move_psi_label(self,placeholder='null'):
        self.lineEdit_pressure.setStyleSheet("QLineEdit{background-color:transparent;border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; font-size:85px;} QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}")
        if placeholder == 'null':
            _str = self.lineEdit_pressure.text()
        else:
            _str = placeholder
        if len(_str) >= 1:
            _shift = 45 * len(_str)
            _deshift = 18 * _str.count("1")
            self.label_psi.move(30+15+_shift-_deshift,443)
        elif len(_str) == 0:
            self.label_psi.move(30+15+45,443)



#    Calculates percent full scale error
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       rc = as-found R-Cal value in psi.
#       fs = full scale rating of TI.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.


#        m = m/1000
#        mc = mc/1000
#        ma = ma/1000
#        pfserr = 100 * (float(self.Console.setup_current_rcal) * (_y[n]-_y[0])/(self.reading_rcal-self.reading_atm) - p[n]) / float(self.Console.setup_full_scale)


#    def rcal(self, p, m, mc, ma):
##       Calculates the R-Cal
##       p = array of pressure measurements.
##       m = array of transducer readings in mV.
##       mc = R-Cal millivolt reading.
##       ma = Atmospheric reference millivolt reading.
#        p, m = np.asarray(p), np.asarray(m)
#        s1, s2 = 0, 0
#        for n in range(1, len(p) - 1):
#            s1, s2 = s1 + (p[n] - p[0]) * (m[n] - m[0]), s2 + (m[n] - m[0])**2
#
#        return (mc - ma) * s1 / s2

def best_fit_rcal(X, Y):
    # X is PSI, Y is mV
    # https://nbviewer.jupyter.org/gist/anonymous/eb643d8ea14eb58aa6f853aa67e3d4f5
    # Least Square Method - https://www.varsitytutors.com/hotmath/hotmath_help/topics/line-of-best-fit

    xbar = sum(X)/len(X)
    ybar = sum(Y)/len(Y)
    n = len(X) # or len(Y)

    numer = sum(xi*yi for xi,yi in zip(X, Y)) - n * xbar * ybar
    denum = sum(xi**2 for xi in X) - n * xbar**2

    numer_least_squares = sum((xi-xbar)*(yi-ybar) for xi,yi in zip(X, Y))
    denum_least_squares = sum((xi-xbar)**2 for xi in X)

    b = numer / denum
    a = ybar - b * xbar

    b_least_squares = numer_least_squares / denum_least_squares
    a_least_squares = ybar - b_least_squares * xbar

    print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))
    print('best fit line least squares format 2:\ny = {:.2f} + {:.2f}x'.format(a_least_squares, b_least_squares))

    return a, b



'''
  __
 (_   _ _|_ _|_ o ._   _   _
 __) (/_ |_  |_ | | | (_| _>
                       _|
'''

class Settings(QWidget):
    def __init__(self, parent = MainWindow):
        super(Settings, self).__init__(parent)
        self.width, self.height = 350, 400
        self.title = 'REX'
        self.setStyleSheet("QWidget {background: rgb(59, 98, 110);} QLineEdit { border: none }")
        self.setFixedSize(self.width,self.height)
        self.spinbox_1_index, self.spinbox_2_index, self.visaGPIBAddress, self.visaGPIB_cmd, self.visaASRLAddress, self.visaASRL_cmd, self.visaGPIBAddress_custom, self.visaASRLAddress_custom = self.visaFind()
        self.initUI()

    def initUI(self):

        link_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                              QPushButton:hover{color: #2eecff;}'''
        link_sheet_refresh = ''' QPushButton{font-family:Bahnschrift;font-size:30px;border: 0px;color:rgb(113, 188, 209);padding: 35px 0px 0px 0px;}
                                QPushButton:hover{color: #2eecff;}'''

        self.label_title = QLabel("Settings")
        self.label_title.setStyleSheet("font-size:26px;")

        self.label_sub_multiMeter = QLabel("Multimeter GPIB")
        self.label_sub_multiMeter.setStyleSheet("font-size:16px;")

        self.label_sub_gauge= QLabel("Gauge ASRL")
        self.label_sub_gauge.setStyleSheet("font-size:16px;")



        self.button_back_1 = QPushButton("◀")
        self.button_back_1.setStyleSheet(link_sheet)
        self.button_back_1.clicked.connect(self.spinbox_1_back)
        self.lineEdit_multiMeter = QLineEdit()
        self.lineEdit_multiMeter.setAlignment(Qt.AlignCenter)
        self.lineEdit_multiMeter.setEnabled(False)
        self.button_forward_1 = QPushButton("▶")
        self.button_forward_1.setStyleSheet(link_sheet)
        self.button_forward_1.clicked.connect(self.spinbox_1_forward)

        self.button_back_2 = QPushButton("◀")
        self.button_back_2.setStyleSheet(link_sheet)
        self.button_back_2.clicked.connect(self.spinbox_2_back)
        self.lineEdit_gauge = QLineEdit()
        self.lineEdit_gauge.setAlignment(Qt.AlignCenter)
        self.lineEdit_gauge.setEnabled(False)
        self.button_forward_2 = QPushButton("▶")
        self.button_forward_2.setStyleSheet(link_sheet)
        self.button_forward_2.clicked.connect(self.spinbox_2_forward)


        self.spinbox_layout_1 = QHBoxLayout()
        self.spinbox_layout_1.addWidget(self.button_back_1, 1)
        self.spinbox_layout_1.addWidget(self.lineEdit_multiMeter, 4)
        self.spinbox_layout_1.addWidget(self.button_forward_1, 1)
        self.spinbox_1_option = ['HP 3478A 1', 'HP 3478A 2', 'AUTO', 'NONE']
        self.spinbox_1_address = ['GPIB0::1::INSTR', 'GPIB0::2::INSTR',self.visaGPIBAddress_custom, '']
        self.spinbox_1_cmd = ['*IDN?','*IDN?','*IDN?']
        self.lineEdit_multiMeter.setText(self.spinbox_1_option[self.spinbox_1_index])

        self.spinbox_layout_2 = QHBoxLayout()
        self.spinbox_layout_2.addWidget(self.button_back_2, 1)
        self.spinbox_layout_2.addWidget(self.lineEdit_gauge, 4)
        self.spinbox_layout_2.addWidget(self.button_forward_2, 1)
        self.spinbox_2_option = ['MENSOR 2500 A', 'MENSOR 2500 B', 'AUTO', 'NONE']
        self.spinbox_2_address = ['GPIB0::1::INSTR', 'GPIB0::2::INSTR',self.visaASRLAddress_custom,'']
        self.spinbox_2_cmd = ['A?','B?','A?','']
        self.lineEdit_gauge.setText(self.spinbox_2_option[self.spinbox_2_index])

        self.button_refresh = QPushButton('⟳')
        self.button_refresh.setStyleSheet(link_sheet_refresh)
        self.button_refresh.clicked.connect(self.refresh)

        self.main_frame = QFrame(self)
        self.main_frame.setFixedSize(self.width,self.height)
        self.main_frame.setContentsMargins(20,20, 20, 20)

        self.form_layout = QVBoxLayout(self.main_frame)
        self.form_layout.addWidget(self.label_title, 1)
        self.form_layout.addWidget(self.label_sub_multiMeter, 1)
        self.form_layout.addLayout(self.spinbox_layout_1)
        self.form_layout.addWidget(self.label_sub_gauge, 1)
        self.form_layout.addLayout(self.spinbox_layout_2)
        self.form_layout.addWidget(self.button_refresh, Qt.AlignBottom)

        self.main_layout = QVBoxLayout(self)
        self.main_layout.addWidget(self.main_frame, 1, Qt.AlignTop)
        self.main_layout.setContentsMargins(0, 0, 0, 0)

    def spinbox_1_forward(self):
        if self.spinbox_1_index >= 2:
            self.spinbox_1_index = 0
        else:
            self.spinbox_1_index += 1
        self.lineEdit_multiMeter.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.visaGPIBAddress = self.spinbox_1_address[self.spinbox_1_index]
        self.visaGPIB_cmd = self.spinbox_1_cmd[self.spinbox_1_index]

    def spinbox_1_back(self):
        if self.spinbox_1_index == 0:
            self.spinbox_1_index = 2
        else:
            self.spinbox_1_index -= 1
        self.lineEdit_multiMeter.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.visaGPIBAddress = self.spinbox_1_address[self.spinbox_1_index]
        self.visaGPIB_cmd = self.spinbox_1_cmd[self.spinbox_1_index]

    def spinbox_2_forward(self):
        if self.spinbox_2_index == 3:
            self.spinbox_2_index = 0
        else:
            self.spinbox_2_index += 1
        self.lineEdit_gauge.setText(self.spinbox_2_option[self.spinbox_2_index])
        self.visaASRLAddress = self.spinbox_2_address[self.spinbox_2_index]
        self.visaASRL_cmd = self.spinbox_2_cmd[self.spinbox_2_index]

    def spinbox_2_back(self):
        if self.spinbox_2_index == 0:
            self.spinbox_2_index = 3
        else:
            self.spinbox_2_index -= 1
        self.lineEdit_gauge.setText(self.spinbox_2_option[self.spinbox_2_index])
        self.visaASRLAddress = self.spinbox_2_address[self.spinbox_2_index]
        self.visaASRL_cmd = self.spinbox_2_cmd[self.spinbox_2_index]

    def queryBoolean(self, cmd):
        try:
            self.session.write(cmd)
            read = self.session.read()
            return True
        except:
            return False

    def queryFloat(self, cmd, address):
        try:
            self.session.write(cmd)
            read = self.session.read()
            return read
        except:
            self.setup_self_rm(address)

    def setup_self_rm(self, address):
        self._rm = visa.ResourceManager()
        try:
            self.session = self._rm.open_resources(address)
        except visa.VisaIOError as e:
            print(e.args)
            print(_rm.last_status)
            print(_rm.visalib.last_status)
            if _rm.last_status == visa.constants.StatusCode.error_resource_busy:
                print("The port is busy!")
            self.close_self_rm()

    def close_self_rm(self,address):
        self.session.close()
        self._rm.close()

    def visaFind(self):
        # Function opens the PyVISA Resource Manager, lists the resources, then
        # determines the Index/Preset Name, VISA Address, and associated Cmd.

        rm = visa.ResourceManager()
        print '__init__'
        available = rm.list_resources()
        preferred = False
        visaGPIBAddress_custom = ()
        visaASRLAddress_custom = ()
        if len(available) > 0:
            for address in available:
                self.session = rm.open_resource(address)
                if address == 'GPIB0::1::INSTR':
                # Checks preset Multimeter location
                    read = self.queryBoolean('*IDN?')
                    if read == True:
                        spinbox_1_index = 0
                        visaGPIBAddress = address
                        preferred = True
                        visaGPIB_cmd = '*IDN?'
                elif address == 'GPIB0::2::INSTR':
                    # If Preferred Device is down, use backup
                    read = self.queryBoolean('*IDN?')
                    if read == True and preferred == False:
                        spinbox_1_index = 1
                        visaGPIBAddress = address
                        visaGPIB_cmd = '*IDN?'
                elif address == 'ASRL3::INSTR':
                # Checks preset Serial location
                    read = self.queryBoolean('A?')
                    if read == True:
                        spinbox_2_index = 0
                        visaASRLAddress = address
                        visaASRL_cmd = 'A?'
                elif address == 'ASRL4::INSTR':
                # Checks 2nd preset Serial location
                    read = self.queryBoolean('A?')
                    if read == True:
                        spinbox_2_index = 0
                        visaASRLAddress = address
                        visaASRL_cmd = 'A?'
                else:
                # Attempts to determine AUTO addresses, using preset cmds
                    read = self.queryBoolean('*IDN?')
                    if read == True:
                        spinbox_1_index = 2
                        visaGPIBAddress_custom.append(address)
                    else:
                        spinbox_1_index = 3
                        visaGPIBAddress=''
                        visaGPIB_cmd=''
                    read = self.queryBoolean('A?')
                    if read == True:
                        spinbox_2_index = 2
                        visaASRLAddress_custom.append(address)
                    else:
                        spinbox_2_index = 3
                        visaASRLAddress = ''
                        visaASRL_cmd = ''
                self.session.close()
        else:
            spinbox_1_index = 3
            visaGPIBAddress = ''
            visaGPIB_cmd = ''
            spinbox_2_index = 3
            visaASRLAddress = ''
            visaASRL_cmd = ''
        rm.close()
        return spinbox_1_index, spinbox_2_index, visaGPIBAddress, visaGPIB_cmd, visaASRLAddress, visaASRL_cmd, visaGPIBAddress_custom, visaASRLAddress_custom

    def refresh(self):
        self.spinbox_1_index, self.spinbox_2_index, self.visaGPIBAddress, self.visaGPIB_cmd, self.visaASRLAddress, self.visaASRL_cmd, self.visaGPIBAddress_custom, self.visaASRLAddress_custom = self.visaFind()
        self.lineEdit_multiMeter.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.lineEdit_gauge.setText(self.spinbox_2_option[self.spinbox_2_index])


'''

 /\ |_  _    |_
/--\|_)(_)|_||_

'''

class About(QWidget):

    def gurney(self, e):
        self.gurn += 1
        if (self.gurn % 2) == 0:
            pxmp = QPixmap(logo)
            self.maicon.setPixmap(pxmp)
        else:
            pxmp = QPixmap(gurney)
            self.maicon.setPixmap(pxmp)

    def __init__(self, parent = MainWindow):
        super(QWidget, self).__init__(parent)
        ver = "1.1.19"

#   Fonts

        lFont = QFont(funte)
        lFont.setPointSize(14)

#   Main Icon
        self.gurn = 0
        self.maicon = QLabel()
        self.maicon.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.pxmp = QPixmap(logo)
        self.maicon.setPixmap(self.pxmp)
        self.maicon.mousePressEvent = self.gurney

#   Version
        ver1 = QLabel("Version " + ver)
        ver1.setFont(QFont(funte, 11))
        ver1.setStyleSheet('color: white')
        ver1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

#   Created By

        auth2 = QLabel("Created by Max Fung in 2018")
        auth2.setFont(QFont(funte, 13))
        auth2.setStyleSheet('color: white')
        auth2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

#   License
        lic = QLabel('\nThis software is dedicated to Rex Gurney, whos legacy as an engineer in Aerojet Rocketdyne\'s Metrology Department has pioneered the techniques and procedures utilized in this program.\n\nREX was originally intended to be a complete replacement for the HP-85A Computer that Rex used to code his original calibration programs. Due to time constraints, only his pressure transducer calibration exists here.\n')
        lic.setWordWrap(True)
        lic.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        lic.setFont(lFont)
        lic.setStyleSheet('color: white')

#   Horizontal Layouts
        ver = QVBoxLayout()
        ver.addWidget(self.maicon)
        ver.addWidget(ver1)

#    Main Layout
        layout = QVBoxLayout()
        layout.addLayout(ver)
        layout.addWidget(auth2)
        layout.addWidget(lic)

#   Window Settings
        self.setStyleSheet(style)
        self.setContentsMargins(30,30,30,30)
        self.setFixedSize(680, 900)
        self.setWindowTitle('About')
        self.setLayout(layout)


'''
  _
 /   _  ._   _  _  |  _
 \_ (_) | | _> (_) | (/_

'''

#   Validator Modification necessary for Property Number input:

class CapsValidator(QValidator):
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos

class Console(QWidget):

    def __init__(self, parent = MainWindow):
        super(Console, self).__init__(parent)
        self.width, self.height = 360, 572
        self.no_of_steps = '18'
        self.step_no = 1
        self.ui_style_sheet = "QWidget {background-color: rgb(30, 53, 61);} QLabel {color: rgb(114, 160, 173);} QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; } QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}"
        self.setStyleSheet(self.ui_style_sheet)
        self.userList = self.getUsers(users)
        self.userList.sort()
        self.userList = [x[:-9] for x in self.userList]
        self.userList.insert(0, 'SELECT TECHNICIAN')
        self.userList_upper_case = [x.upper() for x in self.userList]
        self.spinbox_1_index = 0
        self.caps_validator = CapsValidator(self)
        self.int_validator = QIntValidator(0,99999,self)
        self.int_validator.bottom = 0
        self.pn_data_check = False
        self.properties_list = self.getProperties()
        self.initUI()
        self.finish_form = False

        self.text_title = [
                'Connect Devices','Excitation Voltage','R-Cal Voltage','Atmospheric Voltage','Upscale Calibration',
                'Upscale Calibration','Upscale Calibration','Upscale Calibration','Upscale Calibration',
                'Upscale Calibration','Downscale Calibration','Downscale Calibration','Downscale Calibration',
                'Downscale Calibration','Downscale Calibration','Downscale Calibration','Calibration Finished'
        ]
        self.text_console_instructions = [
                'Attach the pressure source to the transducer and the standard, in parallel, with the source vented to atmospheric conditions. Ensure that all the necessary data transfer cables are connected.',
                'Connect the power supply to the multimeter and set the excitation voltage to within ±0.05 V of the recommended voltage.',
                'Activate the R-Cal to display the millivoltage reading.',
                'Deactivate the R-Cal to display the atmospheric reference millivolt reading.',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'Set pressure to',
                'The calibration is finished.'

        ]


    def initUI(self):

        button_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                              QPushButton:hover{color: #2eecff;}'''
        last_calibrated_sheet = "QLabel { font-size:12px;color:rgb(69, 119, 133) };"
        comboBox_sheet = ''' QComboBox{font-family:Bahnschrift;font-size:14px;border: 0px;color:rgb(113, 188, 209);background-color:transparent;selection-background-color:transparent;padding: 0px 0px 0px 0px;}'''
        link_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                         QPushButton:hover{color: #2eecff;}'''
        line_edit_sheet_disabled = " QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent transparent transparent; } QLineEdit:focus {border-color: transparent transparent transparent transparent;}"


        self.label_property_number = QLabel("Property Number")
        self.label_property_number.setStyleSheet("font-size:16px;padding-top:30px;")

        self.lineEdit_property_number = QLineEdit()
        self.lineEdit_property_number.setMaxLength(12)
        self.lineEdit_property_number.setValidator(self.caps_validator)

        property_number_completer = QCompleter()
        property_number_model = QStringListModel()
        property_number_model.setStringList(self.properties_list)
        property_number_model_popup = property_number_completer.popup()
        property_number_model_popup.setStyleSheet(style)
        property_number_completer.setModel(property_number_model)

        self.lineEdit_property_number.setCompleter(property_number_completer)
        self.lineEdit_property_number.textChanged.connect(self.check_property_number)

        self.label_technician = QLabel("Technician")
        self.label_technician.setStyleSheet("font-size:16px;")
        self.label_technician.setAlignment(Qt.AlignLeft)

        self.button_back_1 = QPushButton("◀")
        self.button_back_1.setStyleSheet(link_sheet)
        self.button_back_1.clicked.connect(self.spinbox_1_back)
        self.lineEdit_technician = QLineEdit()
        self.lineEdit_technician.setAlignment(Qt.AlignCenter)
        self.lineEdit_technician.setEnabled(False)
        self.lineEdit_technician.setStyleSheet("QLineEdit { border: none; font-size:14px; }")
        self.button_forward_1 = QPushButton("▶")
        self.button_forward_1.setStyleSheet(link_sheet)
        self.button_forward_1.clicked.connect(self.spinbox_1_forward)

        self.spinbox_frame_1 = QFrame()
        self.spinbox_layout_1 = QHBoxLayout(self.spinbox_frame_1)
        self.spinbox_layout_1.addWidget(self.button_back_1, 1)
        self.spinbox_layout_1.addWidget(self.lineEdit_technician, 4)
        self.spinbox_layout_1.addWidget(self.button_forward_1, 1)
        self.spinbox_1_option = self.userList_upper_case
        self.lineEdit_technician.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.lineEdit_technician.textChanged.connect(self.reset_style_sheet_tech)

        label_full_scale = QLabel("Full Scale")
        label_full_scale.setStyleSheet("font-size:16px;")
        label_full_scale.setAlignment(Qt.AlignLeft|Qt.AlignBottom)
        self.lineEdit_full_scale = QLineEdit()
        self.lineEdit_full_scale.setMaxLength(5)
        self.lineEdit_full_scale.setValidator(self.int_validator)
        self.lineEdit_full_scale.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.lineEdit_full_scale.textChanged.connect(self.reset_style_sheet_full_scale)


        label_psi_type = QLabel("PSI Type")
        label_psi_type.setStyleSheet("font-size:16px;")
        label_psi_type.setAlignment(Qt.AlignLeft|Qt.AlignBottom)
        self.comboBox_psi_type = QComboBox()
        self.comboBox_psi_type.addItem("")
        self.comboBox_psi_type.addItem("PSIG")
        self.comboBox_psi_type.addItem("PSID")
        self.comboBox_psi_type.addItem("PSIA")
        self.comboBox_psi_type.model().item(0).setEnabled(False)
        self.comboBox_psi_type.setFixedWidth((self.width-80)/3)
        self.comboBox_psi_type.currentIndexChanged.connect(self.input_barometer)
        self.comboBox_psi_type.setStyleSheet("text-align:center;")
        self.comboBox_psi_type.activated.connect(self.reset_style_sheet_psi_type)

        self.label_barometer = QLabel("Atmospheric PSI")
        self.label_barometer.setStyleSheet("font-size:16px;color:transparent;")
        self.label_barometer.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.lineEdit_barometer = QLineEdit()
        self.lineEdit_barometer.setFixedWidth((self.width-80)/2)
        self.lineEdit_barometer.setEnabled(False)
        self.lineEdit_barometer.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.lineEdit_barometer.setStyleSheet(line_edit_sheet_disabled)
        self.lineEdit_barometer.setValidator(self.int_validator)
        self.lineEdit_barometer.textChanged.connect(self.reset_style_sheet_barometer)

        self.label_current_rcal = QLabel("R-Cal")
        self.label_current_rcal.setStyleSheet("font-size:16px;")
        self.label_current_rcal.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.lineEdit_current_rcal = QLineEdit()
        self.lineEdit_current_rcal.setAlignment(Qt.AlignLeft|Qt.AlignTop)
        self.lineEdit_current_rcal.textChanged.connect(self.reset_style_sheet_current_rcal)
        self.lineEdit_current_rcal.setValidator(self.int_validator)

        self.layout_grid_1 = QGridLayout()
        self.layout_grid_1.addWidget(label_full_scale,0,0,Qt.AlignBottom)
        self.layout_grid_1.addWidget(self.label_current_rcal,0,1,Qt.AlignBottom)
        self.layout_grid_1.addWidget(self.lineEdit_full_scale,1,0,Qt.AlignTop)
        self.layout_grid_1.addWidget(self.lineEdit_current_rcal,1,1,Qt.AlignTop)
        self.layout_grid_1.setHorizontalSpacing(20)

        self.layout_grid_2 = QGridLayout()
        self.layout_grid_2.addWidget(label_psi_type,2,0,Qt.AlignLeft | Qt.AlignBottom)
        self.layout_grid_2.addWidget(self.label_barometer,2,1,Qt.AlignLeft | Qt.AlignBottom)
        self.layout_grid_2.addWidget(self.comboBox_psi_type,3,0,Qt.AlignLeft | Qt.AlignTop)
        self.layout_grid_2.addWidget(self.lineEdit_barometer,3,1,Qt.AlignLeft | Qt.AlignTop)
        self.layout_grid_2.setHorizontalSpacing(20)

        self.top_frame = QFrame(self)
        self.top_frame.setContentsMargins(20,25,20,40)
        self.top_frame.setFixedSize(self.width, self.height)

        self.label_steps = QLabel("STEP "+str(self.step_no)+"/"+self.no_of_steps+"       ", self)
        self.label_steps.setStyleSheet("font-size:14px;color:rgb(69, 119, 133);")
        self.label_steps.move(30,30)

        self.label_title = QLabel("Calibrate                                                               ", self)
        self.label_title.setStyleSheet("font-size:26px;color: rgb(140, 195, 212)")
        self.label_title.move(30,60)

        self.button_next = QPushButton("NEXT ▶", self)
        self.button_next.setFixedWidth(100)
        self.button_next.setAutoDefault(True)
        self.button_next.setStyleSheet(button_sheet)
        self.button_next.clicked.connect(self.next_event)
        self.button_next.move(self.width-115,self.height-70)

        self.button_back = QPushButton("", self)
        self.button_back.setFixedWidth(100)
        self.button_back.setStyleSheet(button_sheet)
        self.button_back.clicked.connect(self.back_event)
        self.button_back.move(15,self.height-70)
        self.button_back.setEnabled(False)

        self.form = QVBoxLayout(self.top_frame)
        self.form.addStretch(3)
        self.form.addWidget(self.label_technician,-1, Qt.AlignBottom)
        self.form.addWidget(self.spinbox_frame_1,-1, Qt.AlignTop)
        self.form.addWidget(self.label_property_number,-1, Qt.AlignBottom)
        self.form.addWidget(self.lineEdit_property_number,-1, Qt.AlignTop)
        self.form.addStretch(1)
        self.form.addLayout(self.layout_grid_1,1)
        self.form.addStretch(1)
        self.form.addLayout(self.layout_grid_2,1)
        self.form.addStretch(2)
        self.form.setSpacing(2)

        self.setFixedSize(self.width,self.height)

    def getUsers(self, txt):
        arr = []
        with open(txt, 'r') as data:
            for line in data:
                arr.append(line.strip())
        data.close()
        return arr

    def getProperties(self, search_type='f',property_number=None):
        # Retrieves Property Numbers from folder directories if given 'f' and .dat files if given 'dat'
        if search_type == 'f':
            properties= os.listdir(results)
            _list = []
            for _property in properties: # loop through all the files and folders
                if os.path.isdir(os.path.join(os.path.abspath(results), _property)): # check whether the current object is a folder or not
                    _list.append(_property)
            _list.sort()
            return _list
        elif search_type == 'dat':
            if len(self.lineEdit_property_number.text()) >= 7:
                if self.lineEdit_property_number.text() in self.properties_list:
                    print 'Load .dat file from folder with property number', self.lineEdit_property_number.text()

    def spinbox_1_forward(self):
        if self.spinbox_1_index >= len(self.spinbox_1_option)-1:
            self.spinbox_1_index = 1
        else:
            self.spinbox_1_index += 1
        self.lineEdit_technician.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.technician = self.userList[self.spinbox_1_index]

    def spinbox_1_back(self):
        if self.spinbox_1_index <= 1:
            self.spinbox_1_index = len(self.spinbox_1_option)-1
        else:
            self.spinbox_1_index -= 1
        self.lineEdit_technician.setText(self.spinbox_1_option[self.spinbox_1_index])
        self.technician = self.userList[self.spinbox_1_index]

    def check_property_number(self, i):
        last_calibrated_sheet = "QLabel { font-size:12px;color:rgb(69, 119, 133) };"
        self.lineEdit_property_number.setStyleSheet("QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; } QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}")
        if self.pn_data_check == False:
            try:
                dat = self.getProperties('dat',i)
                last_calibrated = dat[0]
                full_scale = dat[3]
                current_rcal = dat[4]
                psi_type = dat[5]

                self.pn_data_check = True
                self.lineEdit_full_scale.setText(str(full_scale))
                self.lineEdit_full_scale.setReadOnly(True)
                self.lineEdit_current_rcal.setText(str(round(float(current_rcal),3)))

                _index = self.comboBox_psi_type.findText(str(psi_type), Qt.MatchFixedString)

                if index2 >= 0:
                    self.comboBox_psi_type.setCurrentIndex(_index)
            except:
                pass

        elif self.pn_data_check == True:
            self.pn_data_check = False
            self.lineEdit_full_scale.setReadOnly(False)

    def input_barometer(self, i):
        # Toggles the atmospheric PSI input.
        line_edit_sheet = " QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; } QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}"
        line_edit_sheet_disabled = " QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent transparent transparent; } QLineEdit:focus {border-color: transparent transparent transparent transparent;}"
        if i == 3:
            self.label_barometer.setStyleSheet("font-size:16px;")
            self.lineEdit_barometer.clear()
            self.lineEdit_barometer.setEnabled(True)
            self.lineEdit_barometer.setStyleSheet(line_edit_sheet)
        else:
            self.label_barometer.setStyleSheet("font-size:16px;color:transparent;")
            self.lineEdit_barometer.clear()
            self.lineEdit_barometer.setEnabled(False)
            self.lineEdit_barometer.setStyleSheet(line_edit_sheet_disabled)

    def next_event(self):
        button_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;} QPushButton:hover{color: #2eecff;}'''

        # Will check if all fields have proper data. Once validated, will set up the test.
        if self.finish_form == False:
            line_edit_sheet_error = "QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent #874646 transparent; } QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}"
            combo_box_sheet_error  = "QComboBox { background-color: #3b1d1d;}"
            self.msg = "     " + 'All required values must be present.'
            valid_count = 0

            if self.spinbox_1_index != 0:
                valid_count += 1
            else:
                self.lineEdit_technician.setStyleSheet("QLineEdit { border: none; font-size:14px;color: rgb(207, 97, 83);  }")

            if len(self.lineEdit_property_number.text()) >= 7:
                valid_count += 1
            else:
                self.lineEdit_property_number.setStyleSheet(line_edit_sheet_error)

            if len(self.lineEdit_full_scale.text()) > 0:
                if float(self.lineEdit_full_scale.text()) > 0:
                    valid_count += 1
                else:
                    self.lineEdit_full_scale.setStyleSheet(line_edit_sheet_error)
            else:
                self.lineEdit_full_scale.setStyleSheet(line_edit_sheet_error)

            if self.comboBox_psi_type.currentIndex() != 0:
                valid_count += 1
                if self.lineEdit_barometer.isEnabled():
                    #BARO
                    if len(self.lineEdit_barometer.text()) > 0:
                        valid_count += 1
                    else:
                        self.lineEdit_barometer.setStyleSheet(line_edit_sheet_error)
                else: valid_count += 1
            else:
                self.comboBox_psi_type.setStyleSheet(combo_box_sheet_error)

            if len(self.lineEdit_current_rcal.text()) > 0:
                if float(self.lineEdit_current_rcal.text()) > 0:
                    if float(self.lineEdit_current_rcal.text()) < float(self.lineEdit_full_scale.text()):
                        valid_count += 1
                    else:
                        self.lineEdit_current_rcal.setStyleSheet(line_edit_sheet_error)
                else:
                    self.lineEdit_current_rcal.setStyleSheet(line_edit_sheet_error)
            else:
               self.lineEdit_current_rcal.setStyleSheet(line_edit_sheet_error)

            if valid_count == 6:
                self.finish_form = True

                # Save Setup
                self.setup_technician = self.spinbox_1_option[self.spinbox_1_index]
                self.setup_property_number = self.lineEdit_property_number.text()
                self.setup_full_scale = self.lineEdit_full_scale.text()
                self.setup_psi_type = self.comboBox_psi_type.currentText()
                self.setup_psi_type_index = self.comboBox_psi_type.currentIndex()
                self.setup_current_rcal = self.lineEdit_current_rcal.text()

                if self.lineEdit_barometer.isEnabled():
                    self.setup_barometer = self.lineEdit_barometer.text()

                console_pressure_dp = float(self.setup_full_scale)/5
                pressure = 0
                self.text_console_pressure = []

                for i in range(0,6):
                    self.text_console_pressure.append(str(int(pressure)))
                    pressure += console_pressure_dp
                pressure -= console_pressure_dp
                for i in range(0,6):
                    self.text_console_pressure.append(str(int(pressure)))
                    pressure -= console_pressure_dp

                if self.setup_psi_type_index == 3:
                    self.text_console_pressure_baro = self.text_console_pressure
                    self.text_console_pressure = []
                    for value in self.text_console_pressure_baro:
                        self.text_console_pressure.append(str(int(value)+int(self.setup_barometer)))

                for i in range(len(self.top_frame.children())):
                    self.top_frame.children()[i].deleteLater()

                self.step_no += 1
                self.step_console_index = self.step_no - 2
                self.step_scale_index = self.step_no - 6
                self.label_steps.setText("STEP "+str(self.step_no)+"/"+self.no_of_steps)
                self.label_title.setText(self.text_title[self.step_console_index])
                self.button_back.setText("◀ SETUP")
                self.button_back.setEnabled(True)

                self.consoleScene_1 = QGraphicsScene()
                self.consoleView = QGraphicsView()
                self.consoleView.setFixedSize(self.width,self.height)
                self.consoleView.setSceneRect(0,0,self.width-10,self.height-10)
                self.consoleView.fitInView(0,0,self.width,self.height,Qt.KeepAspectRatio)
                self.consoleView.setStyleSheet('Background-color:transparent;')

                self.console_instructions = QGraphicsTextItem()
                self.console_font = QFont()
                self.console_font.setFamily("Bahnschrift")
                self.console_font.setPointSize(16)
                self.console_instructions.setDefaultTextColor(QColor(140, 195, 212))
                self.console_instructions.setFont(self.console_font)
                self.console_instructions.setTextWidth(self.width-52)
                self.console_instructions.setPos(23,120)

                self.console_pressure = QGraphicsTextItem()
                self.console_font_p = QFont()
                self.console_font_p.setFamily("Bahnschrift")
                self.console_font_p.setPointSize(60)
                self.console_font_p.setWeight(700)
                self.console_pressure.setDefaultTextColor(QColor(140, 195, 212))
                self.console_pressure.setFont(self.console_font_p)
                self.console_pressure.setTextWidth(self.width-52)
                self.console_pressure.setPos(23,150)

                # IF PSIG
                self.console_instructions.setHtml(self.text_console_instructions[self.step_console_index])
                #   ELIF PSIA
                #   ELSE PSID
                self.consoleScene_1.addItem(self.console_instructions)
                self.consoleScene_1.addItem(self.console_pressure)


                self.consoleView.setScene(self.consoleScene_1)

                self.form.addWidget(self.consoleView)

            else:
                self.finish_form = False
        else:
            self.step_no += 1
            self.step_console_index = self.step_no - 2
            self.step_scale_index = self.step_no - 6
            self.label_steps.setText("STEP "+str(self.step_no)+"/"+self.no_of_steps)

            if self.step_no < 19:
                self.label_title.setText(self.text_title[self.step_console_index])
                self.console_instructions.setHtml(self.text_console_instructions[self.step_console_index])

            if 12 > self.step_scale_index >= 0:
                self.console_pressure.setHtml(self.text_console_pressure[self.step_scale_index]+" <span style='font-size:45px;font-weight:200'>PSI</span>")
            else:
                self.console_pressure.setHtml("")

            if self.step_no == 3:
                self.button_back.setText("◀ BACK")
                self.button_next.setText("RECORD ✓")

            if self.step_no == 4:
                self.button_back.setText("◀ UNDO")

            if self.step_no == 18:
                self.button_next.setText("FINISH ▶")



    def back_event(self):
        if self.step_no > 1:
            self.step_no -= 1
            self.label_steps.setText("STEP "+str(self.step_no)+"/"+self.no_of_steps)
            self.step_console_index = self.step_no - 2
            self.step_scale_index = self.step_no - 6

            if self.step_scale_index >= 0:
                self.console_pressure.setHtml(self.text_console_pressure[self.step_scale_index]+" <span style='font-size:40px;font-weight:200'>PSI</span>")

            if self.step_scale_index < 0:
                self.console_pressure.setHtml("")

            self.label_title.setText(self.text_title[self.step_console_index])
            self.console_instructions.setHtml(self.text_console_instructions[self.step_console_index])

            if self.step_no == 2:
                self.button_back.setText("◀ SETUP")
                self.button_next.setText("NEXT ▶")

            if self.step_no == 3:
                self.button_back.setText("◀ BACK")

            if self.step_no == 4:
                self.button_back.setText("◀ UNDO")

            if self.step_no == 17:
                self.button_next.setText("RECORD ✓")

        if self.step_no == 1:
            for i in range(len(self.top_frame.children())):
                    self.top_frame.children()[i].deleteLater()
            self.button_back.setText("")
            self.button_back.setEnabled(False)
            self.userList = self.getUsers(users)
            self.userList.sort()
            self.userList = [x[:-9] for x in self.userList]
            self.userList.insert(0, 'SELECT TECHNICIAN')
            self.userList_upper_case = [x.upper() for x in self.userList]
            self.pn_data_check = False
            self.properties_list = self.getProperties()
            self.finish_form = False
            button_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                              QPushButton:hover{color: #2eecff;}'''
            last_calibrated_sheet = "QLabel { font-size:12px;color:rgb(69, 119, 133) };"
            comboBox_sheet = ''' QComboBox{font-family:Bahnschrift;font-size:14px;border: 0px;color:rgb(113, 188, 209);background-color:transparent;selection-background-color:transparent;padding: 0px 0px 0px 0px;}'''
            link_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                             QPushButton:hover{color: #2eecff;}'''
            line_edit_sheet_disabled = " QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent transparent transparent; } QLineEdit:focus {border-color: transparent transparent transparent transparent;}"
            self.label_property_number = QLabel("Property Number")
            self.label_property_number.setStyleSheet("font-size:16px;padding-top:30px;")
            self.lineEdit_property_number = QLineEdit()
            self.lineEdit_property_number.setMaxLength(12)
            self.lineEdit_property_number.setValidator(self.caps_validator)
            self.lineEdit_property_number.setText(self.setup_property_number)
            property_number_completer = QCompleter()
            property_number_model = QStringListModel()
            property_number_model.setStringList(self.properties_list)
            property_number_model_popup = property_number_completer.popup()
            property_number_model_popup.setStyleSheet(style)
            property_number_completer.setModel(property_number_model)
            self.lineEdit_property_number.setCompleter(property_number_completer)
            self.lineEdit_property_number.textChanged.connect(self.check_property_number)
            self.label_technician = QLabel("Technician")
            self.label_technician.setStyleSheet("font-size:16px;")
            self.label_technician.setAlignment(Qt.AlignLeft)
            self.button_back_1 = QPushButton("◀")
            self.button_back_1.setStyleSheet(link_sheet)
            self.button_back_1.clicked.connect(self.spinbox_1_back)
            self.lineEdit_technician = QLineEdit()
            self.lineEdit_technician.setAlignment(Qt.AlignCenter)
            self.lineEdit_technician.setEnabled(False)
            self.lineEdit_technician.setStyleSheet("QLineEdit { border: none; font-size:14px; }")
            self.button_forward_1 = QPushButton("▶")
            self.button_forward_1.setStyleSheet(link_sheet)
            self.button_forward_1.clicked.connect(self.spinbox_1_forward)
            self.spinbox_frame_1 = QFrame()
            self.spinbox_layout_1 = QHBoxLayout(self.spinbox_frame_1)
            self.spinbox_layout_1.addWidget(self.button_back_1, 1)
            self.spinbox_layout_1.addWidget(self.lineEdit_technician, 4)
            self.spinbox_layout_1.addWidget(self.button_forward_1, 1)
            self.spinbox_1_option = self.userList_upper_case
            self.lineEdit_technician.setText(self.spinbox_1_option[self.spinbox_1_index])
            self.lineEdit_technician.textChanged.connect(self.reset_style_sheet_tech)
            label_full_scale = QLabel("Full Scale")
            label_full_scale.setStyleSheet("font-size:16px;")
            label_full_scale.setAlignment(Qt.AlignLeft|Qt.AlignBottom)
            self.lineEdit_full_scale = QLineEdit()
            self.lineEdit_full_scale.setMaxLength(5)
            self.lineEdit_full_scale.setValidator(self.int_validator)
            self.lineEdit_full_scale.setAlignment(Qt.AlignLeft|Qt.AlignTop)
            self.lineEdit_full_scale.textChanged.connect(self.reset_style_sheet_full_scale)
            self.lineEdit_full_scale.setText(self.setup_full_scale)
            label_psi_type = QLabel("PSI Type")
            label_psi_type.setStyleSheet("font-size:16px;")
            label_psi_type.setAlignment(Qt.AlignLeft|Qt.AlignBottom)
            self.comboBox_psi_type = QComboBox()
            self.comboBox_psi_type.addItem("")
            self.comboBox_psi_type.addItem("PSIG")
            self.comboBox_psi_type.addItem("PSID")
            self.comboBox_psi_type.addItem("PSIA")
            self.comboBox_psi_type.model().item(0).setEnabled(False)
            self.comboBox_psi_type.setFixedWidth((self.width-80)/3)
            self.comboBox_psi_type.currentIndexChanged.connect(self.input_barometer)
            self.comboBox_psi_type.setStyleSheet("text-align:center;")
            self.comboBox_psi_type.activated.connect(self.reset_style_sheet_psi_type)
            self.label_barometer = QLabel("Atmospheric PSI")
            self.label_barometer.setStyleSheet("font-size:16px;color:transparent;")
            self.label_barometer.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
            self.lineEdit_barometer = QLineEdit()
            self.lineEdit_barometer.setFixedWidth((self.width-80)/2)
            self.lineEdit_barometer.setEnabled(False)
            self.lineEdit_barometer.setAlignment(Qt.AlignLeft|Qt.AlignTop)
            self.lineEdit_barometer.setStyleSheet(line_edit_sheet_disabled)
            self.lineEdit_barometer.textChanged.connect(self.reset_style_sheet_barometer)
            self.lineEdit_barometer.setValidator(self.int_validator)
            self.comboBox_psi_type.setCurrentIndex(self.setup_psi_type_index)
            self.label_current_rcal = QLabel("R-Cal")
            self.label_current_rcal.setStyleSheet("font-size:16px;")
            self.label_current_rcal.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
            self.lineEdit_current_rcal = QLineEdit()
            self.lineEdit_current_rcal.setAlignment(Qt.AlignLeft|Qt.AlignTop)
            self.lineEdit_current_rcal.textChanged.connect(self.reset_style_sheet_current_rcal)
            self.lineEdit_current_rcal.setText(self.setup_current_rcal)
            self.layout_grid_1 = QGridLayout()
            self.layout_grid_1.addWidget(label_full_scale,0,0,Qt.AlignBottom)
            self.layout_grid_1.addWidget(self.label_current_rcal,0,1,Qt.AlignBottom)
            self.layout_grid_1.addWidget(self.lineEdit_full_scale,1,0,Qt.AlignTop)
            self.layout_grid_1.addWidget(self.lineEdit_current_rcal,1,1,Qt.AlignTop)
            self.layout_grid_1.setHorizontalSpacing(20)
            self.layout_grid_2 = QGridLayout()
            self.layout_grid_2.addWidget(label_psi_type,2,0,Qt.AlignLeft | Qt.AlignBottom)
            self.layout_grid_2.addWidget(self.label_barometer,2,1,Qt.AlignLeft | Qt.AlignBottom)
            self.layout_grid_2.addWidget(self.comboBox_psi_type,3,0,Qt.AlignLeft | Qt.AlignTop)
            self.layout_grid_2.addWidget(self.lineEdit_barometer,3,1,Qt.AlignLeft | Qt.AlignTop)
            self.layout_grid_2.setHorizontalSpacing(20)
            self.form = QVBoxLayout(self.top_frame)
            self.form.addStretch(3)
            self.form.addWidget(self.label_technician,-1, Qt.AlignBottom)
            self.form.addWidget(self.spinbox_frame_1,-1, Qt.AlignTop)
            self.form.addWidget(self.label_property_number,-1, Qt.AlignBottom)
            self.form.addWidget(self.lineEdit_property_number,-1, Qt.AlignTop)
            self.form.addStretch(1)
            self.form.addLayout(self.layout_grid_1,1)
            self.form.addStretch(1)
            self.form.addLayout(self.layout_grid_2,1)
            self.form.addStretch(2)
            self.form.setSpacing(2)
            self.label_title.setText("Calibrate")


    # Resets fields which have errors

    def reset_style_sheet_full_scale(self, widget):
        if len(self.lineEdit_full_scale.text()) > 0:
            self.lineEdit_full_scale.setStyleSheet(self.ui_style_sheet)

    def reset_style_sheet_current_rcal(self, widget):
        if len(self.lineEdit_current_rcal.text()) > 0:
            self.lineEdit_current_rcal.setStyleSheet(self.ui_style_sheet)

    def reset_style_sheet_psi_type(self, widget):
        if self.comboBox_psi_type.currentIndex() != 0:
            self.comboBox_psi_type.setStyleSheet("")

    def reset_style_sheet_barometer(self, widget):
        if len(self.lineEdit_barometer.text()) > 0:
            self.lineEdit_barometer.setStyleSheet(self.ui_style_sheet)

    def reset_style_sheet_tech(self):
        if self.spinbox_1_index != 0:
            self.lineEdit_technician.setStyleSheet(style)
            self.lineEdit_technician.setStyleSheet("QLineEdit { border: none; font-size:14px; }")


'''
  _
 |_) |  _ _|_
 |   | (_) |_

 '''

class PlotCanvas(FigureCanvas):

    def __init__(self, parent=MainWindow, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.patch.set_alpha(0.0)
        matplotlib.style.use('dark_background')
        matplotlib.rcParams['font.family'] = 'sans-serif'
        matplotlib.rcParams['font.sans-serif'] = ['Bahnschrift']
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

        self.op = QGraphicsOpacityEffect(self)
        self.op.setOpacity(0.2) #0 to 1 will cause the fade effect to kick in
        self.setGraphicsEffect(self.op)
        self.setAutoFillBackground(True)

        self.cmap = matplotlib.colors.ListedColormap(["OrangeRed","RebeccaPurple","MediumTurquoise","RebeccaPurple","OrangeRed"])
        var = 0.8325
        self.norm = matplotlib.colors.Normalize(vmin=-1*var,vmax=var)

        self.plot()



    def plot(self, _init = True, x=[0,400,800,1200,1600,2000,2000,1600,1200,800,400,0],y=[2.4254,8.5509,14.6393,20.7161,26.789,32.835,32.834,26.7674,20.6804,14.5967,8.5129,2.4026], z=[0,-0.5,-0.499207613,0.49900742637,0.50,-0.378206777,-0.281492641,-0.115511857,0.116562688,0.20677017,0.302693763,0.474917687],span=2000):

        self.ax = self.figure.add_subplot(111)
        self.ax_2 = self.ax.twinx()
        self.ax_3 = self.ax_2.twiny()
        self.ax_4 = self.ax.twinx()

        if _init == True:
            self.ax.set_yticklabels([])
            self.ax.set_xticklabels([])

        for spine in ['bottom','left','right','top']:
            self.ax_2.spines[spine].set_visible(False)
        self.ax_2.set_yticklabels([])
        self.ax_2.yaxis.set_ticks_position('none')

        for spine in ['bottom','left','right','top']:
            self.ax_3.spines[spine].set_visible(False)
        self.ax_3.set_xticklabels([])
        self.ax_3.xaxis.set_ticks_position('none')

        for spine in ['bottom','left','right','top']:
            self.ax_4.spines[spine].set_visible(False)
        self.ax_4.set_yticklabels([])
        self.ax_4.yaxis.set_ticks_position('none')

        self.ax.set_facecolor((0.10980,  0.18824,  0.21176))
        self.ax.xaxis.grid(color=(0.16863,  0.27843,  0.30980))
#        self.ax.yaxis.grid(color=(0.16863,  0.27843,  0.30980))
        for spine in ['bottom','left','right','top']:
            self.ax.spines[spine].set_color((0.54902,  0.76471,  0.83137))
        self.ax.tick_params(axis='x', colors=(0.54902,  0.76471,  0.83137))

        self.ax.yaxis.set_ticks_position('none')
        self.ax.xaxis.set_ticks_position('none')

        self.draw()

    def updateData(self, ticks=True, x=[0,400,800,1200,1600,2000,2000,1600,1200,800,400,0],y=[2.4254,8.5509,14.6393,20.7161,26.789,32.835,32.834,26.7674,20.6804,14.5967,8.5129,2.4026],z=[0,0.127556574,0.133207613,0.100742637,0.055462793,-0.078206777,-0.081492641,-0.015511857,-0.016562688,-0.00677017,0.002693763,-0.074917687], span=2000):

        self.ax.clear()
        self.ax_2.clear()
        self.ax_3.clear()
        self.ax_4.clear()

        if len(x) > 0:
            self.ax_3.plot([-100,span + 100],[0,0], color='MediumTurquoise',alpha=0.5)
        self.ax_2.scatter(x,z, c=z, norm=self.norm, cmap=self.cmap)

        self.ax_2.set_xlim(0, span)

        if len(z) > 0:
            if max(z) >= 0.5:
                self.ax_2.set_ylim(-2*max(z),max(z)*2)
                self.ax_3.fill_between([0,span],[100,100],y2=[0.5,0.5], alpha=0.3, color='OrangeRed')
                if min(z) <= -0.5:
                    self.ax_3.fill_between([0,span],[-0.5,-0.5],y2=[-100,-100], alpha=0.3, color='OrangeRed')
                else:
                    self.ax_3.fill_between([0,span],[-0.5,-0.5],y2=[-100,-100], alpha=0.05, color='OrangeRed')

            elif min(z) <= -0.5:
                self.ax_2.set_ylim(2*min(z),-2*min(z))
                self.ax_3.fill_between([0,span],[-0.5,-0.5],y2=[-100,-100], alpha=0.3, color='OrangeRed')
                if max(z) >= 0.5:
                    self.ax_3.fill_between([0,span],[100,100],y2=[0.5,0.5], alpha=0.3, color='OrangeRed')
                else:
                    self.ax_3.fill_between([0,span],[100,100],y2=[0.5,0.5], alpha=0.05, color='OrangeRed')
            else:
                 self.ax_2.set_ylim(-0.5,0.5)
        else:
            self.ax_2.set_ylim(-0.5,0.5)

        self.ax_3.set_xlim(0, span)

        if 7 > len(x) >= 1:
            line_index_x = min(x)+span/5*(len(x)-1)
        elif 12 >= len(x) >= 7:
            line_index_x = 0

        if 12 > len(x) >= 2:
            self.ax_4.plot( [ line_index_x, x[int(len(x)-1)] ], [ 0 , y[len(y)-1] ], alpha=0.3 )

        for spine in ['bottom','left','right','top']:
            self.ax_2.spines[spine].set_visible(False)
        self.ax_2.set_yticklabels([])
        self.ax_2.yaxis.set_ticks_position('none')

        for spine in ['bottom','left','right','top']:
            self.ax_3.spines[spine].set_visible(False)
        self.ax_3.set_xticklabels([])
        self.ax_3.xaxis.set_ticks_position('none')

        for spine in ['bottom','left','right','top']:
            self.ax_4.spines[spine].set_visible(False)
        self.ax_4.set_yticklabels([])
        self.ax_4.yaxis.set_ticks_position('none')

        self.ax.plot(x,y,marker='|', markersize=15, color='aquamarine')

        self.ax.set_facecolor((0.10980,  0.18824,  0.21176))
        self.ax.xaxis.grid(color=(0.16863,  0.27843,  0.30980))
        for spine in ['bottom','left','right','top']:
            self.ax.spines[spine].set_color((0.54902,  0.76471,  0.83137))
        self.ax.tick_params(axis='x', colors=(0.54902,  0.76471,  0.83137))
        self.ax.set_yticklabels([])
        self.ax.yaxis.set_ticks_position('none')
        self.ax.xaxis.set_ticks_position('none')
        self.ax.locator_params(axis='y', nbins=6)

        self.ax.set_xlim(0, span)
        self.ax.set_ylim(bottom=0)
        self.ax_4.set_ylim(bottom=0)

        if 7 > len(x) >= 1:
            self.ax.fill_between(x,y,alpha=0.05)
            self.ax.fill_between([ line_index_x, x[int(len(x)-1)] ], [ 0 , y[len(y)-1] ], alpha=0.05, color="DeepSkyBlue")
        if 12 >= len(x) >= 7:
            self.ax_4.set_ylim(bottom=0,top=max(y)+max(y)*0.05)
            self.ax.fill_between([x[len(x)-1],span],[y[len(x)-1], max(y)],alpha=0.1)
            self.ax.fill_between([ line_index_x, x[int(len(x)-1)] ], [ 0 , y[len(y)-2] ], alpha=0.03, color="DeepSkyBlue")
            if 12 > len(x):
                self.ax.fill_between(x,y,y2=linspace(0 ,y[len(y)-1], len(y)), alpha=0.03, color="DeepSkyBlue")

        if ticks != True:
            self.ax.set_xticklabels([])
            self.op.setOpacity(0.2)
        else:
            self.op.setOpacity(1)

        self.draw()



class Monitor(QWidget):

    def __init__(self, parent = MainWindow):
        super(Monitor, self).__init__(parent)
        self.width, self.height = 360, 120
        self.ui_style_sheet = "QWidget {background-color: rgb(30, 53, 61);} QLabel {color: rgb(114, 160, 173);} QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent rgb(69, 119, 133) transparent; } QLineEdit:focus {border-color: transparent transparent #2eecff transparent;}"
        self.setStyleSheet(self.ui_style_sheet)
        self.initUI()
        self.finish_form = False

    def initUI(self):

        button_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                              QPushButton:hover{color: #2eecff;}'''
        last_calibrated_sheet = "QLabel { font-size:12px;color:rgb(69, 119, 133) };"
        comboBox_sheet = ''' QComboBox{font-family:Bahnschrift;font-size:14px;border: 0px;color:rgb(113, 188, 209);background-color:transparent;selection-background-color:transparent;padding: 0px 0px 0px 0px;}'''
        link_sheet = ''' QPushButton{font-family:Bahnschrift;font-size:16px;border: 0px;color:rgb(113, 188, 209);padding: 0px 0px 0px 0px;}
                         QPushButton:hover{color: #2eecff;}'''
        line_edit_sheet_disabled = " QLineEdit{ border-width: 2px; border-style: solid; border-color: transparent transparent transparent transparent; } QLineEdit:focus {border-color: transparent transparent transparent transparent;}"

        label_title = QLabel("Calibrate")
        label_title.setStyleSheet("font-size:26px;color: rgb(140, 195, 212)")

        self.top_frame = QFrame(self)
        self.top_frame.setContentsMargins(20,25,20,40)
        self.top_frame.setFixedSize(self.width, self.height)

        self.label_steps = QLabel("STEP 1/40", self)
        self.label_steps.setStyleSheet("font-size:14px;color:rgb(69, 119, 133);")
        self.label_steps.move(30,30)

        form = QVBoxLayout(self.top_frame)
        form.addWidget(label_title,1,Qt.AlignBottom)
        form.addStretch(1)
        form.setSpacing(1)
        self.setFixedSize(self.width,self.height)


# WINDOWS
if __name__ == '__main__':
     app = QCoreApplication.instance()
     if app is None:
         app = QApplication([])

     app_icon = QIcon()
     app_icon.addFile(logo)
     app.setWindowIcon(app_icon)
     db = QFontDatabase.addApplicationFont(fnt)
     view = MainWindow()
     view.show()

     try:
         from IPython.lib.guisupport import start_event_loop_qt5
         start_event_loop_qt5(app)
     except ImportError:
         app.exec_()
