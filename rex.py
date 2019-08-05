# -*- coding: utf-8 -*-
#---------------------------------------------------------------------------------------#
#
#                               CREATED BY MAX H. FUNG, 2018
#                                  FOR AEROJET ROCKETDYNE
#
#---------------------------------------------------------------------------------------#


# cd /d C:\engapps\Anaconda2\
# activate rex
# python U:\MaxFung\Source_Code\REX_Dev\rex.py

# pyi-makespec --onedir --windowed U:\MaxFung\Source_Code\REX_Dev\rex.py

# https://stackoverflow.com/questions/50135676/pyinstaller-and-seaborn

# pyinstaller --onedir --windowed --icon=U:\MaxFung\Source_Code\REX_Dev\icon.ico U:\MaxFung\Source_Code\REX_Dev\rex.py





#                                                        IMPORTS

#_____________________________________________________________________________________________________________________#



from PyQt5.QtWidgets import (QApplication, QDialog, QHBoxLayout, QLabel, QMenu, QPushButton, QVBoxLayout, QFormLayout,
                             QLineEdit, QComboBox, QCompleter, QListWidget, QFrame, QWidget, QMessageBox, QStyleFactory,                    
                             QGraphicsOpacityEffect, QMainWindow, QGroupBox, QGridLayout, QTableView, QListView, 
                             QAbstractItemView, QDesktopWidget)

from PyQt5.QtCore import Qt, QCoreApplication, QStringListModel, QPropertyAnimation, QTimer, pyqtSignal, QAbstractTableModel, QModelIndex, QVariant, QPoint, QDir

from PyQt5.QtGui import QFont, QPixmap, QValidator, QIntValidator, QStandardItem, QStandardItemModel, QDoubleValidator, QIcon, QFontDatabase

import glob, os, sys

import visa
import pickle
from datetime import datetime

import numpy as np
import pandas as pd

from matplotlib import pyplot as plt
plt.ioff()

import seaborn as sns




#_____________________________________________________________________________________________________________________#


#                                                     ABOUT PAGE

#_____________________________________________________________________________________________________________________#




QApplication.setStyle(QStyleFactory.create("Fusion"))
style = 'background: rgb(48,58,59);color: white; font-family:bahnschrift;'
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
pickl = resource_path('pickle.pkl')
rex_bg = resource_path('rex_bg.jpg')
start_bg = resource_path('start_bg.jpg')
gurney = resource_path('gurney.png')
users = resource_path('users.txt')
visapkl = resource_path('VISA.pkl')
visa2pkl = resource_path('VISA2.pkl')
trans_data = resource_path('trans_data\\')
trans_data_setup = resource_path('trans_data\\setup\\')
trans_data_setup_pkl = resource_path('trans_data\\setup\\*.pkl')
temp1 = resource_path('trans_data\\graphics\\temp1.png')
temp2 = resource_path('trans_data\\graphics\\temp2.png')
fnt = resource_path("fonts\\bahnschrift.ttf")






class tm:
    
    def pfserr(p, m, rc, fs, mc, ma):
#       Calculates percent full scale error
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       rc = as-found R-Cal value in psi.
#       fs = full scale rating of TI.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        
        
#        m = m/1000
#        mc = mc/1000
#        ma = ma/1000
        
        
        
        p, m = np.asarray(p), np.asarray(m)
        pfserr = np.zeros(len(p))
        for n in range(0, len(p)):
            pfserr[n] = 100 * (rc * (m[n]-m[0])/(mc-ma) - p[n]) / fs
#            pfserr[n] = 100 * (p[n] - p[0] - rc *(m[n]-m[0])/(mc - ma)) / fs
#            pfserr[n] = 100 * ((p[n] - p[0] - rc * (((m[n]-m[0])/1000) / ((mc - ma)/1000))) / fs)
        return pfserr
    
    def rcal(p, m, mc, ma):
#       Calculates the R-Cal
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        p, m = np.asarray(p), np.asarray(m)
        s1, s2 = 0, 0
        for n in range(1, len(p) - 1):
            s1, s2 = s1 + (p[n] - p[0]) * (m[n] - m[0]), s2 + (m[n] - m[0])**2
        return (mc - ma) * s1 / s2    
    
    def pres(n, p, fs, trtype, b = 0):
#       Specifies and records nominal pressure for a point in the test.
#       n = point of data
#       p = array of pressure measurements (begins as array of zeros).
#       trtype = transducer type: 'psia', 'psid', or 'psig'.
#       fs = full scale rating of TI.
#       b = barometric pressure reading (psi)
        thres, msg = len(p)/2 -1, 'Set pressure to '
#       thres = "threshold" - the upper limit of upscale calibration
        if n <= thres:
            dp = fs / thres * n
        else:
            dp = fs / thres * (len(p) - 1 - n)
        p[n] = dp - b                               # ??? + or - b ???
        p[n] = round(p[n], 3)
        if b != 0 and p[n] < 0:
            trtype = 'PSIA'
            pres = msg + str(dp) + ' ' + trtype
        else:
            if b != 0:
                trtype = 'PSIG'
            pres = msg + str(p[n]) + ' ' + trtype
        return pres, p[n]
    
    def topsia(p, b):
#       Converts pressure data array in PSIG to PSIA using barometric reading
        return np.array(p) + b



class About(QDialog):
    
    def gurney(self, e):
        self.gurn += 1
        if (self.gurn % 2) == 0:
            pxmp = QPixmap(logo)
            self.maicon.setPixmap(pxmp)
        else:
            pxmp = QPixmap(gurney)
            self.maicon.setPixmap(pxmp)
        
    
    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        ver = "1.1.19"
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Fonts

        lFont = QFont(funte)
        lFont.setPointSize(8)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Main Icon
        self.gurn = 0
        self.maicon = QLabel()
        self.maicon.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.pxmp = QPixmap(logo)
        self.maicon.setPixmap(self.pxmp)
        
        self.maicon.mousePressEvent = self.gurney
        
        
#---------------------------------------------------------------------------------------------------------------------#

#   Version
        ver1 = QLabel("Version " + ver)
        ver1.setFont(QFont(funte, 11))
        ver1.setStyleSheet('color: white')
        ver1.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Created By

        auth2 = QLabel("Created by Max Fung in 2018")
        auth2.setFont(QFont(funte, 13))
        auth2.setStyleSheet('color: white')
        auth2.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        

        
#---------------------------------------------------------------------------------------------------------------------#
        
#   License
        lic = QLabel('\nThis software is dedicated to Rex Gurney, whos legacy as an engineer in Aerojet Rocketdyne\'s Metrology Department has pioneered the techniques and procedures utilized in this program.\n\nREX was originally intended to be a complete replacement for the HP-85A Computer that Rex used to code his original calibration programs. Due to time constraints, only his pressure transducer calibration exists here.\n')
        lic.setWordWrap(True)
        lic.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        lic.setFont(lFont)
        lic.setStyleSheet('color: white')
        
        
#---------------------------------------------------------------------------------------------------------------------#
        
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
        self.setFixedSize(380, 400)
        self.setWindowTitle('About')
        self.setLayout(layout)



#_____________________________________________________________________________________________________________________#


#                                                      LAUNCHER
        
#_____________________________________________________________________________________________________________________#


class Start(QMainWindow):

    def __init__(self, parent = None):
        super(Start, self).__init__(parent)
        
        w, h = 130, 25

#---------------------------------------------------------------------------------------------------------------------#

#   Font
        ma = QFont(funte, 45)
        ma.setBold(True)
        fb = QFont(funte, 9)
        fq = QFont(funte, 9)
        
        sf = QFont(funte, 4)
        spacer = QLabel("")
        spacer.setFont(sf)
        
#---------------------------------------------------------------------------------------------------------------------#

#   Main Icon 
        self.icon = QLabel()
        self.icon.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        pxmp = QPixmap(logo)
        self.icon.setPixmap(pxmp)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   New Calibration Menu      
        menu = QMenu()
        menu.setFont(QFont(funte, 8))
        menu.setStyleSheet('color: white; background: rgb(33, 40, 41);')
        menu.addAction('Pressure Transducer', self.newTrans)
#        menu.addAction('Analysis shortcut', self.shortcut)
#        menu.addAction('Cal shortcut', self.shortcut2)
        
#   New Calibration      
        self.new = QPushButton('New Calibration', self)
        self.new.setFont(fb)
        self.new.setFixedSize(w,h)
        self.new.setStyleSheet("color: white; background-color: Transparent; background-repeat:no-repeat; border: none;outline:none;")
        self.new.setMenu(menu)
        
#---------------------------------------------------------------------------------------------------------------------#

#   Property Manager    
        self.lcb = QPushButton('Property Manager', self)
        self.lcb.setFixedSize(w,h)
        self.lcb.setStyleSheet("color: white; background-color: Transparent; background-repeat:no-repeat; border: none;outline:none;")
        self.lcb.setFont(fb)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Quit       
        self.qb = QPushButton('❌', self)
        self.qb.setFixedSize(30,30)
#        self.qb.setGeometry()
        self.qb.setStyleSheet("color: #27c9d9; background-color: Transparent; background-repeat:no-repeat; border: none;outline:none;")
        self.qb.setFont(fq)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Layout
        
        btn = QHBoxLayout()
        btn.addWidget(self.new, 0, Qt.AlignRight | Qt.AlignTop)
        btn.addWidget(self.lcb, 0 , Qt.AlignLeft | Qt.AlignTop)
        btn.setSpacing(50)
        
        vbox = QVBoxLayout()
        vbox.addWidget(self.qb, 0, Qt.AlignRight | Qt.AlignTop)
        vbox.addWidget(self.icon, 0, Qt.AlignCenter | Qt.AlignVCenter)
        vbox.addLayout(btn)
        vbox.setContentsMargins(0, 0, 0, 20)
        vbox.setSpacing(10)
#        vbox.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)

#   Events
        self.icon.mousePressEvent = self.aboutClick
        self.lcb.clicked.connect(self.propManager)
        self.qb.clicked.connect(self.close)

#   Window Settings
        self.setWindowFlags(Qt.FramelessWindowHint)
#        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.borderRadius = 5
        self.draggable = True
        self.dragging_threshould = 5
        self.__mousePressPos = None
        self.__mouseMovePos = None
        
        allit = QWidget()
        allit.setLayout(vbox)
        
#        path = os.getcwd()[:-3] + 'start_bg.jpg'
        
        #C:/Users/E202770/Desktop/MetroAssist/start_bg.jpg
        self.setStyleSheet('QMainWindow {background: rgb(48,58,59);}')                   
        self.setFixedSize(400, 223)
        self.center()
        self.setCentralWidget(allit)
        self.setWindowTitle('REX')
        self.setWindowState(self.windowState() & ~Qt.WindowMinimized | Qt.WindowActive)
        self.activateWindow()
        self.unfade(allit, 2000)

        
#---------------------------------------------------------------------------------------------------------------------#
    
    def aboutClick(self, e):
        if e.button() == Qt.LeftButton:
            i = About(self)
            i.exec_()
#           event.accept()    NOTE: This closes the parent window!
#           i.show()          NOTE: i.show() in front of exec will open multiple instances
            
#---------------------------------------------------------------------------------------------------------------------#

#   Opens the Pressure Transducer Program:       
    def newTrans(self):
        i = Trans()
        i.show()
        self.close()
        i.exec_()
        
    def shortcut(self):
        i = TransAnalysis()
        i.show()
        self.close()
        i.exec_()
        
    def shortcut2(self):
        i = TransCalWindow()
        i.show()
        self.close()
        i.exec_()

#--------------------------------------------------------------------------------------------------------------------#

#   Loads a saved calibration:    
    def propManager(self):
        self.pM = PropertyManager(self)
        self.pM.show()

#---------------------------------------------------------------------------------------------------------------------#

#   Fade Effect
    def fade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
    
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start(QPropertyAnimation.DeleteWhenStopped)
    
    def unfade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
    
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        try:
            delta = QPoint (event.globalPos() - self.oldPos)
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPos()
        except:
            pass



#_____________________________________________________________________________________________________________________#


#                                                    UTILITIES

#_____________________________________________________________________________________________________________________#
        
        

#                                                      USERS
#_____________________________________________________________________________________________________________________#


class Users(QDialog):
    
#   Data Retrieval:
    def getdata(self, txt):
        arr = []
        with open(txt, 'r') as data:
            for line in data:
                arr.append(line.strip())
        data.close()
        return arr
    
    def deleteUser(self, txt, item):
        t = open(txt, 'r')
        lines = t.readlines()
        t.close()
        t = open(txt, 'w')
        for line in lines:
            if line != item + '\n':
                t.write(line)
        t.close()
        
    def deleteClick(self):
        try:
            self.sel = self.lw.selectedIndexes()[0]
            self.deleteUser(users, self.sel.data())
            self.lw.clear()
            self.t = self.getdata(users)
            self.t.sort()
            self.lw.addItems(self.t)
        except:
            pass
        
    def newUser(self):
        try:
            i = QDialog()
    
    #---------------------------------------------------------------------------------------------------------------------#
         
            #STYLE GUIDE
            
            #FONTS
            fnttit = QFont(funte, 13)
            fntbdy = QFont(funte, 10)
            fntbtn = QFont(funte, 8)
            
            #COLORS
            dimgray = 'color: white'
            gray = 'color: gray'
            
            #WINDOWS
            i.setContentsMargins(30,30,30,30)
            
            #SPACING
            d1 = QFrame()
            d1.setFrameShape(QFrame.HLine)
            d1.setFrameShadow(QFrame.Sunken)
            #create multiple
            
            sfont = QFont()
            sfont.setPointSize(1)
            space = QLabel(" ")
            space.setFont(sfont)
            #setSpacing is also useful
            
    #---------------------------------------------------------------------------------------------------------------------#
            
            
            title = QLabel("New Technician")
            title.setFont(fnttit)
            title.setStyleSheet(dimgray)
            
            i.l1 = QLabel("First Name")
            i.l1.setFont(fntbdy)
            i.l1.setStyleSheet(dimgray)
            i.l2 = QLabel("Last Name")
            i.l2.setFont(fntbdy)
            i.l2.setStyleSheet(dimgray)
            i.l3 = QLabel("Employee ID #")
            i.l3.setFont(fntbdy)
            i.l3.setStyleSheet(dimgray)
            self.le1 = QLineEdit()
            self.le1.setFont(fntbdy)
            self.le1.setStyleSheet(gray)
            self.le1.setMaxLength(19)
            self.le2 = QLineEdit()
            self.le2.setFont(fntbdy)
            self.le2.setStyleSheet(gray)
            self.le2.setMaxLength(19)
            self.le3 = QLineEdit()
            self.le3.setFont(fntbdy)
            self.le3.setStyleSheet(gray)
            self.le3.setMaxLength(6)
            onlyInt = QIntValidator()
            self.le3.setValidator(onlyInt)
            i.b1 = QPushButton("Create")
            i.b1.setFont(fntbtn)
            i.b1.setStyleSheet(dimgray)
            i.b2 = QPushButton("Cancel")
            i.b2.setFont(fntbtn)
            i.b2.setStyleSheet(dimgray)
            
            i.form = QFormLayout()
            i.form.addRow(i.l1, self.le1)
            i.form.addRow(i.l2, self.le2)
            i.form.addRow(i.l3, self.le3)
            i.form.setSpacing(15)
            
            i.hbox = QHBoxLayout()
            i.hbox.addWidget(i.b1)
            i.hbox.addWidget(i.b2)
            
            i.vbox = QVBoxLayout()
            i.vbox.addWidget(title)
            i.vbox.addWidget(space)
            i.vbox.addLayout(i.form)
            i.vbox.addWidget(space)
            i.vbox.addLayout(i.hbox)
    
            i.setWindowTitle("Add User")
            i.setLayout(i.vbox)
            i.setFixedSize(450, 300)
            
            i.b1.clicked.connect(self.newUserCreate)
            i.b1.clicked.connect(i.accept)
            i.b2.clicked.connect(i.reject)
            i.setStyleSheet(style)
            
            i.exec_()
        except:
            pass
        
    def newUserCreate(self):
        try:
            if self.le3.text() != '':
                fname = self.le1.text()
                lname = self.le2.text()
                eid = self.le3.text()
                string = lname + ', ' + fname + ' [' + eid + ']\n'
                t = open(users, 'r')
                lines = t.readlines()
                t.close()
                lines.insert(len(self.t), string)
                t = open(users, 'w')
                lines = "".join(lines)
                t.write(lines)
                t.close()
                self.lw.clear()
                self.t = self.getdata(users)
                self.t.sort()
                self.lw.addItems(self.t)
        except:
            pass
        
    def editUser(self):
        
        try:
            self.sel = self.lw.selectedIndexes()[0]
            string = self.sel.data()
            t = open(users, 'r')
            for num, line in enumerate(t,1):
                if string in line:
                    self.row = num
            t.close()
            string = string.split(', ')
            ln = string[0]
            string = string[1].split(' [')
            fn = string[0]
            eid = string[1][:-1]
            i = QDialog()
            
            #---------------------------------------------------------------------------------------------------------------------#
         
            #STYLE GUIDE
            
            #FONTS
            fnttit = QFont(funte, 13)
            fntbdy = QFont(funte, 10)
            fntbtn = QFont(funte, 8)
            
            #COLORS
            dimgray = 'color: white'
            gray = 'color: gray'
            
            #WINDOWS
            i.setContentsMargins(30,30,30,30)
            
            #SPACING
            d1 = QFrame()
            d1.setFrameShape(QFrame.HLine)
            d1.setFrameShadow(QFrame.Sunken)
            #create multiple
            
            sfont = QFont()
            sfont.setPointSize(1)
            space = QLabel(" ")
            space.setFont(sfont)
            #setSpacing is also useful
            
    #---------------------------------------------------------------------------------------------------------------------#
            
            title = QLabel("Change Technician Info")
            title.setFont(fnttit)
            title.setStyleSheet(dimgray)
            
            i.l1 = QLabel("First Name")
            i.l1.setFont(fntbdy)
            i.l1.setStyleSheet(dimgray)
            
            i.l2 = QLabel("Last Name")
            i.l2.setFont(fntbdy)
            i.l2.setStyleSheet(dimgray)
            
            i.l3 = QLabel("Employee ID #")
            i.l3.setFont(fntbdy)
            i.l3.setStyleSheet(dimgray)
            
            self.le1 = QLineEdit()
            self.le1.setFont(fntbdy)
            self.le1.setStyleSheet(gray)
            self.le1.setMaxLength(19)
            self.le1.setText(fn)
            
            self.le2 = QLineEdit()
            self.le2.setFont(fntbdy)
            self.le2.setStyleSheet(gray)
            self.le2.setMaxLength(19)
            self.le2.setText(ln)
            
            self.le3 = QLineEdit()
            self.le3.setFont(fntbdy)
            self.le3.setStyleSheet(gray)
            self.le3.setMaxLength(6)
            self.le3.setText(eid)
            
            onlyInt = QIntValidator()
            self.le3.setValidator(onlyInt)        
            
            i.b1 = QPushButton("Accept")
            i.b1.setFont(fntbtn)
            i.b1.setStyleSheet(dimgray)
    
            i.b2 = QPushButton("Cancel")
            i.b2.setFont(fntbtn)
            i.b2.setStyleSheet(dimgray)
            
            i.b1.clicked.connect(self.editUserCreate)
            i.b1.clicked.connect(i.accept)
            i.b2.clicked.connect(i.reject)
            
            i.form = QFormLayout()
            i.form.addRow(i.l1, self.le1)
            i.form.addRow(i.l2, self.le2)
            i.form.addRow(i.l3, self.le3)
            i.form.setSpacing(15)
            
            i.hbox = QHBoxLayout()
            i.hbox.addWidget(i.b1)
            i.hbox.addWidget(i.b2)
            
            i.vbox = QVBoxLayout()
            i.vbox.addWidget(title)
            i.vbox.addWidget(space)
            i.vbox.addLayout(i.form)
            i.vbox.addWidget(space)
            i.vbox.addLayout(i.hbox)
            
            i.setStyleSheet(style)
            i.setWindowTitle("Edit User")
            i.setLayout(i.vbox)
            i.setFixedSize(450, 300)
            
            i.exec_()
        except:
            pass
        
    def editUserCreate(self):
        fname = self.le1.text()
        lname = self.le2.text()
        eid = self.le3.text()
        string = lname + ', ' + fname + ' [' + eid + ']\n'
        t = open(users, 'r')
        lines = t.readlines()     
        t.close()
        lines[self.row - 1] = string
        t = open(users, 'w')
        lines = "".join(lines)
        t.write(lines)
        t.close()
        self.lw.clear()
        self.t = self.getdata(users)
        self.t.sort()
        self.lw.addItems(self.t)
      
#   Init
    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        
        #---------------------------------------------------------------------------------------------------------------------#
     
        #STYLE GUIDE
        
        #FONTS
        fnttit = QFont(funte, 14)
        fntbdy = QFont(funte, 12)
        fntbtn = QFont(funte, 8)
        
        #COLORS
        dimgray = 'color: white'
        gray = 'color: #27c9d9'
        
        #WINDOWS
        self.setContentsMargins(30,30,30,30)
        self.setStyleSheet(style)
        
        #SPACING
        d1 = QFrame()
        d1.setFrameShape(QFrame.HLine)
        d1.setFrameShadow(QFrame.Sunken)
        #create multiple
        
        sfont = QFont()
        sfont.setPointSize(1)
        space = QLabel(" ")
        space.setFont(sfont)
        #setSpacing is also useful
        
        #---------------------------------------------------------------------------------------------------------------------#
        
        title = QLabel("Metrology Technicians")
        title.setFont(fnttit)
        title.setStyleSheet(dimgray)
        
        self.t = self.getdata(users)
        self.t.sort()
        
        self.lw = QListWidget()
        self.lw.addItems(self.t)
        self.lw.setFont(fntbdy)
        self.lw.setStyleSheet(gray)
        
        backButton = QPushButton("Done")
        backButton.setFixedWidth(90)
        backButton.clicked.connect(self.accept)
        backButton.setFont(fntbtn)
        backButton.setStyleSheet(dimgray)
        
        addButton = QPushButton("Add User")
        addButton.setFont(fntbtn)
        addButton.setStyleSheet(dimgray)
        addButton.clicked.connect(self.newUser)
        addButton.setFixedWidth(90)
        
        editButton = QPushButton("Edit User")
        editButton.clicked.connect(self.editUser)
        editButton.setFixedWidth(90)
        editButton.setFont(fntbtn)
        editButton.setStyleSheet(dimgray)
        
        deleteButton = QPushButton("Delete User")
        deleteButton.clicked.connect(self.deleteClick)
        deleteButton.setFixedWidth(90)
        deleteButton.setFont(fntbtn)
        deleteButton.setStyleSheet(dimgray)
        
        hbox = QHBoxLayout()
        hbox.addWidget(addButton)
        hbox.addWidget(editButton)
        hbox.addWidget(deleteButton)
        hbox.setAlignment(Qt.AlignRight)
        
        hbox2 = QHBoxLayout()
        hbox2.addWidget(backButton)
        hbox2.addLayout(hbox)
        
        vbox = QVBoxLayout()
        vbox.addWidget(title)
        vbox.addWidget(space)
        vbox.addWidget(space)
        vbox.addWidget(self.lw)
        vbox.addWidget(space)
        vbox.addWidget(space)
        vbox.addLayout(hbox2)
        
        self.setLayout(vbox)
        self.setWindowTitle('Configure Users')
        self.setFixedSize(530,350)
        
        
        
        
        
        
        
        
#                                               PROPERTY MANAGER
#_____________________________________________________________________________________________________________________#
        
#       Allows any property to be edited.        

class PropertyManager(QDialog):
    
#   Data Retrieval:
    
    def getdata(self):
        
        # thats gonna get you your pn pickles and their directories
        globby = glob.glob(trans_data_setup_pkl)
        
        
        # thats gonna give you just the property numbers
        globs = [self.path_leaf(path) for path in globby]
        return globs, globby
    
    def unpickle(self, globby, n):
        with open(globby[n], 'rb') as tommypickles:
            pkldata = pickle.load(tommypickles)
        return pkldata
    
    def unpicklepath(self, path):
        with open(path, 'rb') as tommypickles:
            pkldata = pickle.load(tommypickles)
        return pkldata
        
    def path_leaf(self, path):
        
        # separates the file from the path
        head, tail = os.path.split(path)
        
        
        #removes file extension
        tail = os.path.splitext(tail)[0]
        return tail

        
    def getdata2(self):
        # thats gonna get you your pn pickles and their directories
        globby = glob.glob(trans_data_setup_pkl)
        
        # thats gonna give you just the property numbers
        globs = [self.path_leaf(path) for path in globby]
        return globs, globby
    
    def popdata(self):
        try:
            path = trans_data
            self.datemodel = QStandardItemModel(self.datetabs)
            self.datetabs.setModel(self.datemodel)
            self.sel = self.tabs.selectedIndexes()[0]
            string = self.sel.data()
            num = 0
            for i in os.listdir(path):
                if os.path.isfile(os.path.join(path, i)) and string in i:
                    i = i[:-9]
                    print i
                    item = QStandardItem(i)
                    if num % 2 == 0:
                        self.datemodel.appendRow(item)
                        self.datetabs.setModel(self.datemodel)
                    num += 1
        except:
            pass
        


#   Init
    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        
    
        #DATA
        
        self.globs, self.globby = self.getdata()
        
        
#        self.pkldat = [self.unpickle(self.globby, index) for index
#        print(self.pkldat)
#        
#        x = self.pkldat
#        lc = x[0]
#        fs = x[3]
#        rc = x[4]
#        psi = x[5]
#        print(lc,fs,rc,psi)

#---------------------------------------------------------------------------------------------------------------------#
     
        #STYLE GUIDE
        
        #FONTS
#        fnttit = QFont(funte, 13)
#        fntbdy = QFont(funte, 10)
        fntbtn = QFont(funte, 8)
        
        #COLORS
        dimgray = 'color: white'
        
        #WINDOWS
        self.setContentsMargins(30,30,30,30)
        
        #SPACING
        d1 = QFrame()
        d1.setFrameShape(QFrame.HLine)
        d1.setFrameShadow(QFrame.Sunken)
        #create multiple
        
        sfont = QFont()
        sfont.setPointSize(1)
        space = QLabel(" ")
        space.setFont(sfont)
        #setSpacing is also useful
        
#---------------------------------------------------------------------------------------------------------------------#







#   TAB SETUP

        self.tabs = QListView(parent)
        self.tabs.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.tabs.setSelectionMode(QAbstractItemView.SingleSelection)
        self.tabs.setEditTriggers(QAbstractItemView.NoEditTriggers)
#        self.tabs.setHorizonta

        
        self.model = QStandardItemModel(self.tabs)

        
        item = QStandardItem('Pressure Tranducers')
        item.setFlags(Qt.NoItemFlags)        # item should not be selectable
        item.setForeground(Qt.gray)
        self.model.appendRow(item)
        
        
        self.tup = []
        
        for path in self.globby:
            x = self.unpicklepath(path)
            self.tup.append(x)
        
        for prop in self.globs:
            item = QStandardItem(prop)
            self.model.appendRow(item)

            
            
        self.tabs.setModel(self.model)
        self.tabs.setStyleSheet('color: #27c9d9')
        fnt = QFont(funte, 13)
        self.tabs.setFont(fnt)
            
        
        self.tabs.setMinimumWidth(100)
        self.tabs.selectionModel().selectionChanged.connect(self.popdata)
        
        path = QDir.rootPath()
        
        self.datetabs = QListView(parent)
        self.datemodel = QStandardItemModel(self.datetabs)
        
        self.datetabs.setStyleSheet('color: #27c9d9')
        self.datetabs.setFont(fnt)

#       ~TITLE
        title = QLabel()
        pxmp = QPixmap(logo)
        pxmp = pxmp.scaledToWidth(90)
        title.setPixmap(pxmp)
        title2 = QLabel("REX Property Manager")
        title2.setStyleSheet('color: white')
        font2 = QFont(funte, 13)
        title2.setFont(font2)
        
        
        titprop = QLabel("Properties")
        titprop.setStyleSheet('color: white')
        font3 = QFont(funte, 16)
        titprop.setFont(font3)
        
        titcal = QLabel("Calibrations")
        titcal.setStyleSheet('color: white')
        titcal.setFont(font3)
        
        
        



#      ~SEARCH
        
        self.search_label = QLabel("🔍")
        self.search_label.setStyleSheet('color:#27c9d9')
        self.search_label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.search_line = QLineEdit()
        self.search_line.setFixedWidth(160)
        self.search_line.setMaxLength(12)
        
        self.validator = Validator(self)
        self.search_line.setValidator(self.validator)
        
        self.search_layout = QHBoxLayout()
        self.search_layout.addWidget(self.search_label)
        self.search_layout.addWidget(self.search_line)
        self.search_layout.setAlignment(Qt.AlignRight)
        
        self.allComp = QCompleter(self)
        self.allComp.setCaseSensitivity(Qt.CaseInsensitive)
        self.allComp.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.allComp.setModel(self.model)
        
        self.tabs.setModel(self.allComp.completionModel())
        
        self.search_line.textChanged.connect(self.allComp.setCompletionPrefix)
        
        self.search_line.textChanged.connect(self.popdata)
        
        self.tabs.selectionModel().selectionChanged.connect(self.popdata)
        
        






#      ~SIDEBAR
        
        calibrateButton = QPushButton("View REX Analysis")
        calibrateButton.setFont(fntbtn)
        calibrateButton.setStyleSheet(dimgray)
        calibrateButton.setFixedSize(190, 30)
        calibrateButton.clicked.connect(self.calibrate)
#        self.sel = self.allView.selectedIndexes()[0]
        
        deleteButton = QPushButton("Delete Property")
        deleteButton.setFixedSize(190, 30)
        deleteButton.clicked.connect(self.deleteClick)
        deleteButton.setFont(fntbtn)
        deleteButton.setStyleSheet(dimgray)
        
        exitButton = QPushButton("Delete Test")
        exitButton.setFixedSize(190,30)
        exitButton.setFont(fntbtn)
        exitButton.setStyleSheet(dimgray)
        exitButton.clicked.connect(self.deleteTest)
        
        
        

 

       
#   LAYOUTS
        
        bigtits = QVBoxLayout()
        bigtits.addWidget(title, 0, Qt.AlignBottom)
        bigtits.addWidget(title2, 0, Qt.AlignTop)
        bigtits.setSpacing(0)
        

        
        
        top = QHBoxLayout()
        top.addLayout(bigtits)
        

        btnblock = QHBoxLayout()
        btnblock.addWidget(calibrateButton)
        btnblock.addWidget(QLabel(""))
        btnblock.addWidget(exitButton)
        btnblock.setAlignment(Qt.AlignBottom)
        
        sidebarLayout = QVBoxLayout()
        sidebarLayout.addWidget(deleteButton, 0, Qt.AlignBottom | Qt. AlignCenter)
        

        
        proptop = QHBoxLayout()
        proptop.addWidget(titprop, 0, Qt.AlignLeft)
        proptop.addLayout(self.search_layout)
        
        body = QVBoxLayout()
        body.addLayout(proptop)
        body.addWidget(self.tabs)
        body.addLayout(sidebarLayout)
        
        selector = QVBoxLayout()
        selector.addWidget(titcal, 0, Qt.AlignTop)
        selector.addWidget(self.datetabs)
        selector.addLayout(btnblock)
        
        
        body2 = QHBoxLayout()
        body2.addLayout(body)
        body2.addWidget(QLabel("                "))
        body2.addLayout(selector)
        
        main = QVBoxLayout()
        main.addLayout(top)
        main.addWidget(space)
        main.addWidget(space)
        main.addLayout(body2)

        self.setStyleSheet(style)
        self.setLayout(main)
        self.setWindowTitle('Property Manager')
        self.resize(950,650)
        self.setMinimumHeight(400)
        
        self.token = 0
        
    def closeEvent(self, event):
        if self.token == 0:
            event.accept()
        

    def deleteClick(self):
        try:
            self.tabs.selectedIndexes()[0]
            qm = QMessageBox.question(self, 'Delete Property', "\nAre you sure you want to delete this property?\n\nAll of its test data will be deleted.\n",QMessageBox.Yes | QMessageBox.No,QMessageBox.No)
            if qm == QMessageBox.Yes:
                self.deleteConfirm()
            elif qm == QMessageBox.No:
                pass
        except:
            pass
                
    def deleteTest(self):
        try:
            self.datetabs.selectedIndexes()[0]
            qm = QMessageBox.question(self, 'Delete Test', "Are you sure you want to delete this test?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if qm == QMessageBox.Yes:
                self.deleteItemConfirm()
            elif qm == QMessageBox.No:
                pass
        except:
            pass
        
    def deleteConfirm(self):
        sel = self.tabs.selectedIndexes()[0]
        string = sel.data()
        os.remove(trans_data_setup + string + '.pkl')
        path = trans_data
        for i in os.listdir(path):
            if os.path.isfile(os.path.join(path, i)) and string in i:
                print path + i
                os.remove(path + i)
        for item in self.model.findItems(string):
            self.model.removeRow(item.row())
        self.datemodel = QStandardItemModel(self.datetabs)
        self.datetabs.setModel(self.datemodel)
        
        
    def deleteItemConfirm(self):
        sel = self.datetabs.selectedIndexes()[0]
        string = sel.data()
        path = trans_data
        for i in os.listdir(path):
           if os.path.isfile(os.path.join(path, i)) and string in i:
               os.remove(path + i)
        for item in self.datemodel.findItems(string):
            self.datemodel.removeRow(item.row())

        
    def calibrate(self):
        try:
            sel = self.datetabs.selectedIndexes()[0]
            string = sel.data()
            print string
            pickledata = []
            i, x = string.rsplit('_',-1)
            x = x.rsplit('-',-1)
            x = x[0] + '/' + x[1] + '/' + x[2]
            pickledata.append(x)
            pickledata.append(i)
            print pickledata
            
            with open(pickl, 'wb') as f:
            	pickle.dump(pickledata, f, protocol=2)
            
            w = TransAnalysis()
            w.show()
            self.token = 1
        except:
            print 'not opening'
        
#---------------------------------------------------------------------------------------------------------------------#
            
    def starter(self):
        i = Start()
        i.show()



































#---------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------#
        


#   Validator Modification necessary for Property Number input:
        
class Validator(QValidator):
    def validate(self, string, pos):
        return QValidator.Acceptable, string.upper(), pos










#_____________________________________________________________________________________________________________________#
#                                           

#                                             PRESSURE TRANSDUCER PROGRAM

#_____________________________________________________________________________________________________________________#


#                                                CALIBRATION SETUP
#_____________________________________________________________________________________________________________________#
        
    
    
    
    

    
class Trans(QDialog):

#   Data Retrieval:

    
    def getdata(self):
        # thats gonna get you your pn pickles and their directories
        globby = glob.glob(trans_data_setup_pkl)
        
        # thats gonna give you just the property numbers
        globs = [self.path_leaf(path) for path in globby]
        return globs, globby
    
    def unpickle(self, globby, n):
        with open(globby[n], 'rb') as tommypickles:
            pkldata = pickle.load(tommypickles)
        return pkldata
        
    def path_leaf(self, path):
        
        
        # separates the file from the path
        head, tail = os.path.split(path)
        
        
        #removes file extension
        tail = os.path.splitext(tail)[0]
        
        return tail or os.path.basename(head)
    
    def oggetdata(self, txt):
        arr = []
        with open(txt, 'r') as data:
            for line in data:
                arr.append(line.strip())
        data.close()
        return arr

#---------------------------------------------------------------------------------------------------------------------#

    def __init__(self, parent = None):
        super(QDialog, self).__init__(parent)
        
        
        
        ttype = 'Pressure Transducer'
        
        title = "Calibration Setup - " + ttype
        font = QFont(funte, 13)
        titlel = QLabel(title)
        titlel.setFont(font)
        titlel.setStyleSheet('color: white')
        
        self.lewidth = 140
        self.ttwidth = 80
        self.setStyleSheet(style)

#---------------------------------------------------------------------------------------------------------------------#

#   Fonts
        bold = QFont(funte, 10)
        dimgray = "color: white"

#---------------------------------------------------------------------------------------------------------------------#
        
#   Date and Time
        dtl = QLabel("")
        dtl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.time = QLabel(" " + datetime.now().strftime("%m/%d/%Y %H:%M"))
        self.time.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
#---------------------------------------------------------------------------------------------------------------------#

#   Property Number
        pnlabel = QLabel("     Property Number")
        pnlabel.setStyleSheet(dimgray)
        pnlabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        pnlabel.setFont(bold)
        self.pnline = QLineEdit()
        self.pnline.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.pnline.setMaxLength(12)
        self.pnline.setFixedWidth(self.lewidth)
        
        self.check = False
        
#       Assures that input is in all caps:
        self.validator = Validator(self)
        self.pnline.setValidator(self.validator)
#       Remembers previously calibrated property numbers:
        pncompleter = QCompleter()
        self.pnline.setCompleter(pncompleter)
        pnmodel = QStringListModel()
        pncompleter.setModel(pnmodel)
        
        self.globs, self.globby = self.getdata()
        

        pnmodel.setStringList(self.globs)
        # If length of string is less than 7 return invalid
        # Don't have that yet
#       Checks property number to the database and autocompletes form if found:
        self.pnline.textChanged.connect(self.pnDatabase)
#       Configure Button for Property Database
#        pnconfig = QPushButton("Configure PNs")
#        pnconfig.setFixedWidth(100)
#        pnconfig.clicked.connect(self.pnsClick)
        self.lastCal = QLabel()
        self.pnline.setStyleSheet("color:"+blue)
        
        
#---------------------------------------------------------------------------------------------------------------------#

#   Last Calibrated
        self.lclabel = QLabel("      " + "A new Property will be created.")
        self.lclabel.setFont(bold)
        self.lclabel.setStyleSheet("color: gray")
        
        

#---------------------------------------------------------------------------------------------------------------------#
        
#   Technician
        tl = QLabel("Technician")
        tl.setStyleSheet(dimgray)
        tl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        tl.setFont(bold)
        self.tcb = QComboBox()
        self.titem = self.oggetdata(users)
        self.titem.sort()
        self.titem.insert(0, ' ')
        self.tcb.addItems(self.titem)
        self.tcb.model().item(0).setEnabled(False)
        self.tcb.setStyleSheet("color:"+blue)
        tconfig = QPushButton("Configure Users")
        tconfig.setFont(QFont(funte,8))
        tconfig.setStyleSheet(dimgray)
        tconfig.setFixedWidth(100)
        tconfig.clicked.connect(self.usersClick)
        
 
#---------------------------------------------------------------------------------------------------------------------#
        
#   Transducer Full-Scale
        
        fsl = QLabel("Full Scale Rating")
        fsl.setStyleSheet(dimgray)
        fsl.setFont(bold)
        fsl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.fs = QLineEdit()
        self.fs.setAlignment(Qt.AlignLeft |Qt.AlignTop)
        self.fs.setFixedWidth(100)
        self.fs.setMaxLength(5)
        self.fs.setStyleSheet("color:"+blue)
        self.onlyInt = QIntValidator()
        self.fs.setValidator(self.onlyInt)
        
        

#---------------------------------------------------------------------------------------------------------------------#

#   Transducer Type
        psil = QLabel("PSI Type")
        psil.setFont(bold)
        psil.setStyleSheet(dimgray)
        psil.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.psicb = QComboBox()
        self.psicb.addItem("")
        self.psicb.addItem("PSIG")
        self.psicb.addItem("PSID")
        self.psicb.addItem("PSIA")  
        self.psicb.model().item(0).setEnabled(False)
        self.psicb.setFixedWidth(self.ttwidth)
        self.psicb.currentIndexChanged.connect(self.baro)
        self.psicb.setStyleSheet("color:"+blue)
        
        
#---------------------------------------------------------------------------------------------------------------------#

#   Barometric Pressure (PSIA Only)
        self.bpl = QLabel("Barometer (PSIA)")
        self.bpl.setFont(bold)
        self.bpl.setStyleSheet("color: lightgray")
        self.bpin = QLineEdit()
        self.bpin.setFixedWidth(100)
        self.bpin.setEnabled(False)
        self.bpin.setStyleSheet("color:"+blue)
        

#---------------------------------------------------------------------------------------------------------------------#

#   Current R-Cal
        self.rcl = QLabel("Current R-Cal")
        self.rcl.setFont(bold)
        self.rcl.setStyleSheet(dimgray)
        self.rcl.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        self.rc = QLineEdit()
        self.rc.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self.rc.setFixedWidth(100)
        self.rc.setStyleSheet("color:"+blue)
        
        

#---------------------------------------------------------------------------------------------------------------------#

#   Sub Layouts
        tbox = QHBoxLayout()
        tbox.addWidget(self.tcb)
        tbox.addWidget(tconfig)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        d2 = QFrame()
        d2.setFrameShape(QFrame.HLine)
        d2.setFrameShadow(QFrame.Sunken)
        
        spacerfont = QFont()
        spacerfont.setPointSize(1)
        spacer = QLabel(" ")
        spacer.setFont(spacerfont)
        
        r2 = QVBoxLayout()
        r2.addWidget(pnlabel)
        
        r3 = QHBoxLayout()
        r3.addWidget(self.pnline, 0, Qt.AlignCenter)
        r3.addWidget(QLabel())
        
        self.grid = QGridLayout()
        self.grid.addWidget(fsl,0,0)
        self.grid.addWidget(self.rcl,0,1)
        self.grid.addWidget(self.fs,1,0)
        self.grid.addWidget(self.rc,1,1)
        self.grid.addWidget(psil,2,0)
        self.grid.addWidget(self.bpl,2,1)
        self.grid.addWidget(self.psicb,3,0)
        self.grid.addWidget(self.bpin,3,1)
        
        
        
        
        
        b1 = QPushButton("Create")
        b1.setFixedWidth(100)
        b1.setAutoDefault(True)
        b2 = QPushButton("Cancel")
        b2.setFixedWidth(100)
        b2.setAutoDefault(False)
        b1.clicked.connect(self.createClick)
        b2.clicked.connect(self.reject)
        b2.clicked.connect(self.starter)
        b1.setFont(QFont(funte,8))
        b1.setStyleSheet(dimgray)
        b2.setFont(QFont(funte,8))
        b2.setStyleSheet(dimgray)
        hbox = QHBoxLayout()
        hbox.addWidget(b2)
        hbox.addWidget(b1)
        hbox.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        
        vbox = QVBoxLayout()
        vbox.addWidget(dtl)
        
        hbox2 = QHBoxLayout()
        hbox2.addLayout(vbox)
        hbox2.addLayout(hbox)
        
        groupbox = QGroupBox()
        gbinside = QVBoxLayout()
        gbinside.addLayout(self.grid)
        groupbox.setLayout(gbinside)

#---------------------------------------------------------------------------------------------------------------------#

#   Main Layout
    
        form = QVBoxLayout()
        form.addWidget(titlel)
        form.addWidget(spacer)
        form.addWidget(spacer)
        form.addWidget(tl)
        form.addLayout(tbox)
        
        form.addWidget(spacer)
        form.addWidget(spacer)
        form.addWidget(divider)
        form.addWidget(spacer)
        form.addWidget(spacer)
        
        form.addLayout(r2)
        form.addLayout(r3)
        form.addWidget(self.lclabel)
        
        form.addWidget(groupbox)
        form.addWidget(spacer)
        form.addWidget(spacer)
        
        form.addLayout(hbox2)
        
        

#---------------------------------------------------------------------------------------------------------------------#
    
#   Window Settings
    
        self.setLayout(form)
        self.setFixedWidth(440)
        self.setWindowTitle('REX Setup')
        
        self.setTabOrder(b1, b2)
        self.setTabOrder(b2, tconfig)
        
        self.setContentsMargins(30,30,30,30)
        
        self.token = 0
        
        
        
#---------------------------------------------------------------------------------------------------------------------#        
    
    def closeEvent(self, event):
        if self.token == 1:
            event.accept()
        else:
            w = Start()
            w.show()
            event.accept()
            
    
#   Launches User Dialog
    def usersClick(self):
        i = Users()
        i.exec_()
        self.tcb.clear()
        self.titem = self.oggetdata(users)
        self.titem.sort()
        self.titem.insert(0, ' ')
        self.tcb.addItems(self.titem)
        self.tcb.model().item(0).setEnabled(False)
        self.tcb.setStyleSheet("color:"+blue)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Checks the Property Number to database and fills out form if found
    def pnDatabase(self, i):
        self.pnline.setStyleSheet("color:"+blue)
        
        if self.check == False:
            try:
                index = self.globs.index(i)
                self.pkldat = self.unpickle(self.globby, index)
                
                x = self.pkldat
                lc = x[0]
                fs = x[3]
                rc = x[4]
                psi = x[5]
                
                self.check = True
                
    
    
                self.lclabel.setText("     " + "Last Calibrated: " + str(lc))
                self.lclabel.setStyleSheet("color: gray")
    
                self.fs.setText(str(fs))
                self.fs.setReadOnly(True)
    
                self.rc.setText(str(round(float(rc),3)))
    
                index2 = self.psicb.findText(str(psi), Qt.MatchFixedString)
                
                if index2 >= 0:
                    self.psicb.setCurrentIndex(index2)
                
            except:
                pass
            
                
            
            
            
        elif self.check == True:
            self.check = False
            self.lclabel.setText("      " + "A new Property will be created.")
            self.lclabel.setStyleSheet("QLabel { color: gray };")
            self.fs.setReadOnly(False)
            
            
#---------------------------------------------------------------------------------------------------------------------#
            

            
#---------------------------------------------------------------------------------------------------------------------#
            
#       Barometric Input for PSIA
    def baro(self, i):
        if i == 3:
            self.bpl.setStyleSheet("")
            self.bpin.clear()
            self.bpin.setEnabled(True)
            self.bpl.setStyleSheet("QLabel { color: white };")

        else:
            self.bpl.setStyleSheet("QLabel { color: lightgray };")
            self.bpin.clear()
            self.bpin.setEnabled(False)
            
#---------------------------------------------------------------------------------------------------------------------#
            
    def starter(self):
        i = Start()
        i.show()
            
#---------------------------------------------------------------------------------------------------------------------#
            
#       Create New Test:
    def createClick(self):
        lineSs = "QLineEdit { background-color: #874646; color:"+blue+"}"
        comboSs = "QComboBox { background-color: #874646; color:"+blue+"}"
        self.labelSs = "QLabel { color: pink; }"
        n = 0
        self.msg = "     " + 'All required values must be present.'
        
        #TECHNICIAN
        if self.tcb.currentIndex() != 0:
            n = 1
        else:
            self.warning()
            self.tcb.setStyleSheet(comboSs)
            self.tcb.currentIndexChanged.connect(self.es1)
            self.tcb.currentIndexChanged.connect(self.kekedoyouloveme)
        
        #PROPERTYNUMBER
        if len(self.pnline.text()) >= 7:
            n = n + 1
        else:
            self.warning()
            self.pnline.setStyleSheet(lineSs)
            self.pnline.textChanged.connect(self.kekedoyouloveme)
        
        #FULLSCALE    
        if len(self.fs.text()) > 0:
            n = n + 1
        else:
            self.warning()
            self.fs.setStyleSheet(lineSs)
            self.fs.textChanged.connect(self.es2)
            self.fs.textChanged.connect(self.kekedoyouloveme)
        
        #PSITYPE
        if self.psicb.currentIndex() != 0:
            n = n + 1
        else:
            self.warning()
            self.psicb.setStyleSheet(comboSs)
            self.psicb.currentIndexChanged.connect(self.es3)
            self.psicb.currentIndexChanged.connect(self.kekedoyouloveme)
        
        #RCAL OR NONRCAL
        if self.rc.isEnabled():
            #RCAL
            if len(self.rc.text()) > 0:
                n = n + 1
            else:
                self.warning()
                self.rc.setStyleSheet(lineSs)
                self.rc.textChanged.connect(self.es4)
                self.rc.textChanged.connect(self.kekedoyouloveme)

        #NONRCAL
        else:
            n = n + 1
        #BARO OR NOT
        if self.bpin.isEnabled():
            #BARO
            if len(self.bpin.text()) > 0:
                n = n + 1
            else:
                self.warning()
                self.bpin.setStyleSheet(lineSs)
                self.bpin.textChanged.connect(self.es5)
                self.bpin.textChanged.connect(self.kekedoyouloveme)
                self.psicb.currentIndexChanged.connect(self.es5)
                self.psicb.currentIndexChanged.connect(self.kekedoyouloveme)
        #NOT
        else:
            n = n + 1
            
        if n == 6:
            self.setupData()
            self.token = 1
            c = TransCalWindow()
            self.close()
            c.show()
            
#---------------------------------------------------------------------------------------------------------------------#

#   Changes the status label next to the property number to tell the user Invalid Entries exist.
    def warning(self):
        self.lclabel.setText(self.msg)
        self.lclabel.setStyleSheet(self.labelSs)
        
#---------------------------------------------------------------------------------------------------------------------#

#   The ES def series will return the pink color of a field to normal when it becomes valid.
    def es1(self):
        self.tcb.setStyleSheet("")
    def es2(self):
        self.fs.setStyleSheet("")
    def es3(self):
        self.psicb.setStyleSheet("")
    def es4(self):
        self.rc.setStyleSheet("")
    def es5(self):
        self.bpin.setStyleSheet("")

#---------------------------------------------------------------------------------------------------------------------#

#   KeKe, Do you love me? (Drake - In My Feelings): changes the invalid entries label back to default when all the
#                                                   fields have returned valid. (Why the name?) I was bored.
    def kekedoyouloveme(self):
        n = 0
        self.msg = ''
        if self.tcb.currentIndex() != 0:
            n = 1
        if len(self.pnline.text()) >= 7:
            n = n + 1
        if len(self.fs.text()) > 0:
            n = n + 1
        if self.psicb.currentIndex() != 0:
            n = n + 1
        if self.rc.isEnabled():
            #RCAL
            if len(self.rc.text()) > 0:
                n = n + 1
        else:
            n = n + 1
        if self.bpin.isEnabled():
            if len(self.bpin.text()) > 0:
                n = n + 1
        else:
            n = n + 1
        if n == 6:
            self.lclabel.setText("     " + "A new Property will be created.")
            self.lclabel.setStyleSheet("QLabel { color: gray };")
            
#---------------------------------------------------------------------------------------------------------------------#        
            
#   Takes inputs from the Setup Dialog and puts them into a list: self.testData which is used as the input during
#   the duration of the test.
    def setupData(self):
        self.testData = []
#       Ordered alphabetically, as in file manager: lc.trans, pn.trans, trans.bp, trans.fs, trans.psitype, trans.rcal, trans.user
        time = self.time.text()
        time = time[1:]
        self.testData.append(time)                          #lc.trans.txt       [0]
        self.testData.append(self.pnline.text())            #pn.trans.txt       [1]
        if self.bpl.isEnabled():
            self.testData.append(self.bpin.text())          #trans.bp.txt       [2]
        else:
            self.testData.append("0.0")  
        self.testData.append(self.fs.text())                #trans.fs.txt       [3]
        if self.rc.isEnabled():
            self.testData.append(self.rc.text())            #trans.rcal.txt     [4]
        else:
            self.testData.append("NRC")
        self.testData.append(self.psicb.currentText() )     #trans.psitype.txt  [5]
        self.testData.append(self.tcb.currentText())        #trans.user.txt     [6]
#       self.writeData = [s + '\n' for s in self.testData]  #self.testData - used during test | self.writeData - (has '\n')
        
        with open(pickl, 'wb') as f:
            pickle.dump(self.testData, f,protocol=2)






       
#                                                   CALIBRATION TEST
#_____________________________________________________________________________________________________________________#


#---------------------------------------------------------------------------------------------------------------------#

class TransCalWindow(QMainWindow):
    
    def pfserr(self, p, m, rc, fs, mc, ma):
#       Calculates percent full scale error
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       rc = as-found R-Cal value in psi.
#       fs = full scale rating of TI.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        
        
#        m = m/1000
#        mc = mc/1000
#        ma = ma/1000
        
        
        
        p, m = np.asarray(p), np.asarray(m)
        pfserr = np.zeros(len(p))
        for n in range(0, len(p)):
            pfserr[n] = 100 * (rc * (m[n]-m[0])/(mc-ma) - p[n]) / fs
#            pfserr[n] = 100 * (p[n] - p[0] - rc *(m[n]-m[0])/(mc - ma)) / fs
#            pfserr[n] = 100 * ((p[n] - p[0] - rc * (((m[n]-m[0])/1000) / ((mc - ma)/1000))) / fs)
        return 

    
    def rcal(self, p, m, mc, ma):
#       Calculates the R-Cal
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        p, m = np.asarray(p), np.asarray(m)
        s1, s2 = 0, 0
        for n in range(1, len(p) - 1):
            s1, s2 = s1 + (p[n] - p[0]) * (m[n] - m[0]), s2 + (m[n] - m[0])**2
            
        return (mc - ma) * s1 / s2    
    
    def pres(self, n, p, fs, trtype, b = 0):
#       Specifies and records nominal pressure for a point in the test.
#       n = point of data
#       p = array of pressure measurements (begins as array of zeros).
#       trtype = transducer type: 'psia', 'psid', or 'psig'.
#       fs = full scale rating of TI.
#       b = barometric pressure reading (psi)
        thres, msg = len(p)/2 -1, 'Set pressure to '
#       thres = "threshold" - the upper limit of upscale calibration
        if n <= thres:
            dp = fs / thres * n
        else:
            dp = fs / thres * (len(p) - 1 - n)
        p[n] = dp - b                               # ??? + or - b ???
        p[n] = round(p[n], 3)
        if b != 0 and p[n] < 0:
            trtype = 'PSIA'
            pres = msg + str(dp) + ' ' + trtype
        else:
            if b != 0:
                trtype = 'PSIG'
            pres = msg + str(p[n]) + ' ' + trtype
        return pres, p[n]
    
    def topsia(self, p, b):
#       Converts pressure data array in PSIG to PSIA using barometric reading
        return np.array(p) + b
    
    def __init__(self, parent = None):
        super(QMainWindow, self).__init__(parent)
        
        try:
            with open(visapkl, 'rb') as visa:
                self.VISA = pickle.load(visa)
        
        except:
            with open(visapkl, 'wb') as f:
                pickle.dump('GPIB0::1::INSTR', f, protocol=2)
             
        try:
            with open(visa2pkl, 'rb') as visa:
                self.VISA2 = pickle.load(visa)
        except:
            with open(visa2pkl, 'wb') as f:
                pickle.dump('ASRL4::INSTR', f, protocol=2)
        
        
#---------------------------------------------------------------------------------------------------------------------#
     
        #STYLE GUIDE
        
        #FONTS
        fntbtn = QFont(funte, 12)
        
        #COLORS
        dimgray = 'color: white'
#        gray = 'color: gray'
        
        #SPACING
        d1 = QFrame()
        d1.setFrameShape(QFrame.HLine)
        d1.setFrameShadow(QFrame.Sunken)
        #create multiple
        
        sfont = QFont()
        sfont.setPointSize(1)
        space = QLabel(" ")
        space.setFont(sfont)
        #setSpacing is also useful
        
        self.setStyleSheet(style)
		
				
            
            

#   Back/Finish Buttons
        
        bw = 200 #ButtonWidth
        bh = 40
        
        self.btn_Finish = QPushButton("Finish")
        self.btn_Finish.setEnabled(False)
        self.btn_Finish.setFixedSize(bw, bh)
        self.btn_Finish.setAutoDefault(True)
        self.btn_Finish.setFont(fntbtn)
        self.btn_Finish.setStyleSheet('color: lightgray')
        
        self.btn_Next = QPushButton("Next >")
        self.btn_Next.setFixedSize(bw,bh)
        self.btn_Next.setFont(fntbtn)
        self.btn_Next.setStyleSheet(dimgray)
        self.btn_Next.clicked.connect(self.rex)
        
        self.btn_Back = QPushButton("<  Back")
        self.btn_Back.setFixedSize(bw, bh)
        self.btn_Back.clicked.connect(self.cancelClick)
        self.btn_Back.setFont(fntbtn)
        self.btn_Back.setStyleSheet(dimgray)
        
        self.btn_Cancel = QPushButton("Exit")
        self.btn_Cancel.setFixedSize(bw, bh)
        self.btn_Cancel.clicked.connect(self.quitClick)
        self.btn_Cancel.setFont(fntbtn)
        self.btn_Cancel.setStyleSheet(dimgray)
        
        self.i_b_ia =QPushButton('🔧')
        self.i_b_ia.clicked.connect(self.address)
        self.i_b_ia.setFixedSize(bh,bh)
        self.i_b_ia.setFont(fntbtn)
        self.i_b_ia.setStyleSheet('color:#27c9d9')
        
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Pickle Data
        with open(pickl, 'rb') as f:
            self.x = []
            self.x = pickle.load(f)

#---------------------------------------------------------------------------------------------------------------------#

#   Style Sheets
        
        ssgray = "color: gray"
        ssblue = "color: "+blue

#---------------------------------------------------------------------------------------------------------------------#
        
#   Fonts
        
        bigmsg_font = QFont(funte, 15)
        msg1_font = QFont(funte, 11)

#---------------------------------------------------------------------------------------------------------------------#
        
#   Information
        
        name = self.x[6].rsplit(', ', 1)[1]
        name = name.rsplit(' [',1)[0]


#---------------------------------------------------------------------------------------------------------------------#
        
#   REX
        
        
        # Trigger Button
        self.btn_Rex = QPushButton(self)
        self.btn_Rex.setFixedHeight(1)
        self.btn_Rex.setFixedWidth(1)
        self.btn_Rex.setStyleSheet("background-color:transparent;border:0;")
        self.btn_Rex.clicked.connect(self.rex)
        
        # Central Message
        
#        name = self.x[6]
        
        
        self.bigmsg = 'Hello, ' + name + '.\n\nI am the REX assistant. This console is intended to aid you in the calibration process.\n\nPlease follow all of the instructions carefully and double check your information.\n\nIf you need to repeat any steps, click the Back button.\n\nWhen you are ready to begin calibrating, press the spacebar or click within REX.'
#        self.unfade(self.bigmsg_label, 1000)
        self.rexmsg = QLabel(self.bigmsg)
        self.rexmsg.setFont(bigmsg_font)
        self.rexmsg.setWordWrap(True)
        self.rexmsg.setStyleSheet(ssblue)
        self.rexmsg.setAlignment(Qt.AlignVCenter)


        # Diagram
        self.rexD = QLabel()

        # Sub Message
        
        self.msg1 = ''
        self.msg1_label = QLabel(self.msg1)
        self.msg1_label.setFont(msg1_font)
        self.msg1_label.setWordWrap(True)
        self.msg1_label.setAlignment(Qt.AlignCenter)
        
        # STEPS
        
        self.step = -1
        self.bhandle = 0
        self.teststeps = 22
        self.triggered = 0
        self.mega = 0
        self.finishtoken = 0
        
        self.zp = np.zeros(1)
        self.zm = np.zeros(1)
        
        
        rexTitle = QLabel()
        pxmp = QPixmap(logo)
        pxmp = pxmp.scaledToWidth(120)
        rexTitle.setPixmap(pxmp)
        rexFont = QFont(funte, 45)
        rexFont.setBold(True)
        
        rexTitle2 = QLabel("Calibration Assistant\nPressure Transducer " + self.x[1])
        rexFont2 = QFont(funte, 14)
        rexTitle2.setFont(rexFont2)
        rexTitle2.setStyleSheet('color: white')
        
        title = QFont(funte, 16)
        
        i_title_title = "Calibrating Pressure Transducer " + self.x[1]
        
        self.i_title = QLabel(i_title_title)
        self.i_title.setFont(title)
        self.i_title.setStyleSheet("color: white")
        
        rexTop = QVBoxLayout()
        rexTop.setSpacing(0)
        rexTop.addWidget(rexTitle, 0, Qt.AlignBottom)
        rexTop.addWidget(rexTitle2, 0, Qt.AlignTop)
        rexTop.setAlignment(Qt.AlignVCenter)
        
        
#        lyt_title = QHBoxLayout()
#        lyt_title.setSpacing(0)
#        lyt_title.addLayout(rexTop)
#        lyt_title.addWidget(self.i_title, 0, Qt.AlignRight | Qt.AlignBottom)
#        lyt_title.setAlignment(Qt.AlignBottom)
        
        
        self.rexbox = QGroupBox()
        self.rexbox.mousePressEvent = self.rexClick
        self.rexbox.setContentsMargins(30,30,30,30)
        self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 1px solid #414745; border-radius: 3px; background; margin-top: 1ex;}')
        self.rexbox.setMaximumHeight(700)
        self.rexbox.setMaximumWidth(2880)
                
        # Instructions
        self.info = QVBoxLayout()
        self.info.addWidget(QLabel(""))
        self.info.addWidget(self.rexmsg)
        self.info.addStretch()
        
        self.frame = QWidget()
        self.frame.setContentsMargins(30,30,30,30)
        self.frame.setLayout(self.info)
        
        fader = QHBoxLayout()
        fader.addWidget(self.frame)
        
        self.rexbox.setLayout(fader)
        
        # Reader
        
        self.voltmeter = QLabel('Output Reading')
        self.voltmeter.setFont(QFont(funte, 12))
        self.voltmeter.setStyleSheet('color: white')
        self.voltmeter.setAlignment(Qt.AlignCenter)
        
        self.volts = QLabel('...')
        self.volts.setFont(QFont(funte, 20))
        self.volts.setStyleSheet('color: lightgray')
        self.volts.setAlignment(Qt.AlignCenter)
        
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        
        self.pressuregauge = QLabel('Pressure Reading')
        self.pressuregauge.setFont(QFont(funte, 12))
        self.pressuregauge.setStyleSheet('color: white')
        self.pressuregauge.setAlignment(Qt.AlignCenter)
            
        if self.x[5] == 'PSIA':
            self.psir = 'PSIG'
        else:
            self.psir = self.x[5]
                
#        if float(self.x[3]) > 1000:
#            self.mensor = "A?"
#        else:
#            self.mensor = "B?"
            
        self.press = QLabel('...')
                
#        print('Channel',self.mensor)
            
        self.press.setFont(QFont(funte, 20))
        self.press.setStyleSheet('color: lightgray')
        self.press.setAlignment(Qt.AlignCenter)
            
        grid = QGridLayout()
        grid.addWidget(self.voltmeter,0,0)
        grid.addWidget(self.volts,1,0)
        grid.setAlignment(Qt.AlignCenter)
        
        grid2 = QGridLayout()
        grid2.addWidget(self.pressuregauge,0,0)
        grid2.addWidget(self.press,1,0)
        grid2.setAlignment(Qt.AlignCenter)
            
        hayy = QHBoxLayout()
        hayy.addLayout(grid2)
        spacer = QLabel("")
        spsfnt = QFont()
        spsfnt.setPointSize(1)
        spacer.setFont(spsfnt)
        hayy.addWidget(spacer)
        hayy.addLayout(grid)
        hayy.addWidget(self.i_b_ia, 0, Qt.AlignRight)
            
        if width < 1500:
            wy = width*.02729167
        else:
            wy = width*.01729167
            
        ibox = QWidget()
        ibox.setLayout(hayy)
        ibox.setContentsMargins(wy,0,0,0)
    
        layei = QHBoxLayout()
        layei.addWidget(ibox)
            
            
        mbox = QGroupBox()
        mbox.setLayout(layei)
        mbox.setFixedWidth(550)
        mbox.setFixedHeight(height*.141379085)
            
            
#        else:
#            grid = QGridLayout()
#            grid.addWidget(self.voltmeter,0,0)
#            grid.addWidget(self.volts,1,0)
#            grid.setAlignment(Qt.AlignCenter)
#        
#            hayy = QHBoxLayout()
#            hayy.addLayout(grid)
#            hayy.addWidget(self.i_b_ia, 0, Qt.AlignRight)
#            
#            if width < 1500:
#                wy = width*.02729167
#            else:
#                wy = width*.05729167
#            
#            ibox = QWidget()
#            ibox.setLayout(hayy)
#            ibox.setContentsMargins(wy,0,0,0)
#        
#            layei = QHBoxLayout()
#            layei.addWidget(ibox)
#            
#            
#            mbox = QGroupBox()
#            mbox.setLayout(layei)
#            mbox.setFixedWidth(width*.26041667)
#            mbox.setFixedHeight(height*.141379085)
        
        lyt_title = QHBoxLayout()
        lyt_title.setSpacing(0)
        lyt_title.addLayout(rexTop)
        lyt_title.addWidget(mbox, 0, Qt.AlignVCenter)
        lyt_title.setAlignment(Qt.AlignBottom)
        
    

#---------------------------------------------------------------------------------------------------------------------#
        
#   Layouts
        
        # Quit/Finish Buttons
        self.lyt_btn = QHBoxLayout()
        self.lyt_btn.addWidget(self.btn_Rex)
#        self.lyt_btn.addWidget(self.i_b_ia, 0, Qt.AlignRight)
        self.lyt_btn.addWidget(self.btn_Next)
        self.lyt_btn.addWidget(self.btn_Finish, 0, Qt.AlignRight)
        self.lyt_btn.setAlignment(Qt.AlignRight)
        
        self.lyt_btn2 = QHBoxLayout()
        self.lyt_btn2.addWidget(self.btn_Cancel)
        self.lyt_btn2.addWidget(self.btn_Back)
        self.lyt_btn2.setAlignment(Qt.AlignLeft)
        
        self.lyt_bline = QHBoxLayout()
        self.lyt_bline.addLayout(self.lyt_btn2)
        self.lyt_bline.addLayout(self.lyt_btn)
        
        #Main Layout
        lyt_main = QVBoxLayout()
        lyt_main.addLayout(lyt_title)
        lyt_main.addWidget(space)
        lyt_main.addWidget(space)
        lyt_main.addWidget(space)
        lyt_main.addWidget(space)
        lyt_main.addWidget(self.rexbox)
        
        sublabel = QWidget()
        sublabellay = QVBoxLayout()
        sublabellay.addWidget(self.msg1_label)
        sublabel.setLayout(sublabellay)
        sublabel.setMinimumWidth(width*.79062958)
        sublabel.setFixedHeight(height*.05208333)
        
        
        lyt_main.addWidget(sublabel, 0, Qt.AlignCenter)
        lyt_main.addLayout(self.lyt_bline)
        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Window Format
        
        w, h = 900, 600
        
        frm = QFrame()
        self.setCentralWidget(frm)
        
        l, t, r, b = 100,40,100,40
        self.setContentsMargins(l,t,r,b)
        
        
        frm.setLayout(lyt_main)
        self.showFullScreen()
        self.setMinimumWidth(w)
        self.setMinimumHeight(h)
        self.setWindowTitle('REX Calibration Assistant')
        
        self.checkInst()
        
        try:
            self.readtimer = QTimer(self)
            self.readtimer.start(800)
            self.readtimer.timeout.connect(self.mVreading)
        except:
            pass
#        timer.timeout.connect(print(''))


#   CALL THE MULTIMETER        
    def callMulti(self):
        # VISA resource manager is created

        resourceManager = visa.ResourceManager()
        if len(resourceManager.list_resources()) > 0:
            try:
                # This opens up a session with a particular instrument
                session = resourceManager.open_resource(self.VISA)
                # I set a read termination for serial connections only
                if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                    session.read_termination = '\n'
            #       Send *IDN? and read the response
                session.write(self.multiCmd)
                idn = session.read()
                # Converts string into a float number
                idn = float(idn)*1000        
            #     Close the connection to the instrument
                session.close()
                # Close the resource manager
                resourceManager.close()    
                # Return the value
                return idn
            except:
                self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color: pink')
            self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid icon.')
        else:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color: pink')
            self.rexmsg.setText('I\'m sorry, your VISA connection has not been configured properly.\n')
            self.visaDNE()
    
#   CALL THE PRESSURE GAUGE    
    def callGauge(self):
        rm = visa.ResourceManager()
        if len(resourceManager.list_resources()) > 0:
            try:
                # If the gauge has been detected as a Mensor, it will automatically set the settings properly
                if self.gaugeID == 'Mensor':
                    gauge = rm.open_resource(self.VISA2, baud_rate = 57600, data_bits = 8, write_termination= '\n', read_termination = '\n')
                elif self.gaugeID == 'HEISE':
                    gauge = rm.open_resource(self.VISA2, baud_rate = 9600, data_bits = 8, write_termination= '*', read_termination = '*')
                else:
                    # Otherwise it opens based on the Keysight Connection Expert Settings
                    gauge = rm.open_resource(self.VISA2)
                    # Assumes a serial connection and sets a termination
                    gauge.read_termination = '\n'
                # Sends the correct command to the instrument
                gauge.write(self.gaugeCmd)
                # Reads the response
                idn = gauge.read()
                if idn[0] == 'E':
                    idn = idn[1:]
                idn = float(idn)
                gauge.close()
                rm.close()
                return idn
            except:
                pass
            
    def visaDNE(self):
        result = QMessageBox.warning(self, 'Instruments Not Found', "\nREX cannot perform the calibration unless a virtual instrument software architecture resource is found.\n\nPlease install the Keysight IO Libraries Suite or an equivalent VISA software.\n\nIf the software is installed, please add your instruments to the library and try again.\n", QMessageBox.Ok )
        if result == QMessageBox.Ok:
            self.finishtoken = -1
            self.close()
            Start()
#            w.show()
            
    def rexConnectionError(self):
        self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
        self.rexmsg.setStyleSheet('color: pink')
        self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid icon.')
    
    
    def checkInst(self):
        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(self.VISA)
            if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                session.read_termination = '\n'
            session.write('*IDN?')
            idn = session.read()
            
            try:
                idn.rsplit(-1,',')[0]
                self.multiID = 'SCPI'
                self.multiCmd = 'MEAS:VOLT:DC?'
            except:
                self.multiID = 'HP 3478A'
                self.multiCmd = '*IDN?'
        except:
            self.multiID = 'Custom'
            self.multiCmd = 'Enter Valid Command Here'
        
        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(self.VISA2)
            if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                session.read_termination = '\n'
                session.write('*IDN?')
                idn = session.read()
            else:
                print 'go'
                print session.resource_name
            
            try:
                self.gaugeID = idn.rsplit(',',-1)[0]
                print self.gaugeID
                if self.gaugeID == 'EMENSOR':
                    if float(self.x[3]) > 1000:
                        self.gaugeCmd = "A?"
                        self.gaugeID = 'Mensor'
                    else:
                        self.gaugeCmd = "B?"
                        self.gaugeID = 'Mensor'
                elif self.gaugeID == 'MENSOR':
                    if float(self.x[3]) > 1000:
                        self.gaugeCmd = "A?"
                        self.gaugeID = 'Mensor'
                    else:
                        self.gaugeCmd = "B?"
                        self.gaugeID = 'Mensor'
                else:
                    self.gaugeID = 'SCPI'
                    self.gaugeCmd = 'MEAS[:PRES][Enter Channel Here]?'
                
            except:
                self.gaugeID = 'Legacy (Non-SCPI)'
                self.gaugeCmd = 'Enter Valid Command Here'
                
            session.close()
            resourceManager.close()
        except:
            self.gaugeID = "Custom"
            self.gaugeCmd = "Enter Valid Command Here"
        

        
        
        
#---------------------------------------------------------------------------------------------------------------------#
    def mVreading(self):
        
        try:
            idn = self.callMulti()
            idn = round(float(idn),4)
            self.volts.setText(str(idn) + ' mV')
            self.volts.setStyleSheet('color: #27c9d9')
            
        except:
            self.volts.setText('Not Connected')
            self.volts.setStyleSheet('color: #874646')
            
        try:
            idn = self.callGauge()
            idn = round(float(idn),2)
            self.press.setText(str(idn) + ' ' + self.psir)
            self.press.setStyleSheet('color: #27c9d9')
        except:
            self.press.setText('N/A')
            self.press.setStyleSheet('color: gray')
            
    
    def address(self):
        
        with open(visapkl, 'rb') as visa:
            self.VISA = pickle.load(visa)
            
        with open(visa2pkl, 'rb') as visa:
            self.VISA2 = pickle.load(visa)
        
        i = QDialog()
        
        spacer = QLabel("")
        spacerfont = QFont(funte, 1)
        spacer.setFont(spacerfont)

        title = QFont(funte, 13)
        i.i_title = QLabel("REX Connection Aid")
        i.i_title.setFont(title)
        i.i_title.setStyleSheet("color: white")
        i.setContentsMargins(30,30,30,30)
        
        
        info = QLabel("Click the refresh ⟳ icon to check the connection on a changed VISA Address.\n\nTo find a valid VISA Address for the test instrument, use the Keysight Connection Expert located on the right side of the Windows taskbar at the bottom of your screen.\n\nSelect the Keysight IO Libraries Suite, then select the Connection Expert.\n\nThe VISA Address of the test instrument will be under GPIB-USB (GPIB0).\n\nNote that the Heise pressure gauge does not communicate properly with REX. If you intend to use automated pressure readings, connect to the Mensor through the Keysight/VISA Connection Expert.")
        info.setWordWrap(True)
        info.setStyleSheet("font-family: 'bahnschrift'; color: lightgray")
        i.l1 = QLabel("VISA Address (Voltmeter)")
        i.l1.setStyleSheet("font-family: 'bahnschrift'; color: white")
        self.le1 = QLineEdit()
        self.le1.setText(self.VISA)
        self.le1.setFixedWidth(170)
        self.le1.setStyleSheet("color: "+blue)
        
        i.l2 = QLabel("VISA Address (Gauge)")
        i.l2.setStyleSheet("font-family: 'bahnschrift'; color: white")
        self.le2 = QLineEdit()
        self.le2.setText(self.VISA2)
        self.le2.setFixedWidth(170)
        self.le2.setStyleSheet("color: "+blue)
  
        i.cs = QLabel("Connection Status         ")
        i.cs.setStyleSheet("font-family: 'bahnschrift'; color: white")
        self.isconnected = QLabel("Checking Connection...")
        self.isconnected.setStyleSheet('color: white')
        
        i.cs2 = QLabel("Connection Status         ")
        i.cs2.setStyleSheet("font-family: 'bahnschrift'; color: white")
        self.isconnected2 = QLabel("Checking Connection...")
        self.isconnected2.setStyleSheet('color: white')
        
        
        self.checktimer = QTimer(i)
        self.checktimer.start(1000)
        self.checktimer.timeout.connect(self.checkConnect)


        w = 80
        i.b1 = QPushButton("Accept")
        i.b1.setFixedWidth(w)
        i.b1.setFont(QFont(funte,8))
        i.b1.setStyleSheet('color: white')
        i.b2 = QPushButton("Cancel") 
        i.b2.setFixedWidth(w)
        i.b2.setStyleSheet('color: white')
        i.b2.setFont(QFont(funte,8))
        self.b3 = QPushButton("⟳")
        self.b3.setFixedWidth(30)
        self.b3.setFont(QFont(funte,8))
        self.b3.setStyleSheet('color: white')
        
        self.b4 = QPushButton("⚙️")
        self.b4.setFixedWidth(30)
        self.b4.setFont(QFont(funte,8))
        self.b4.setStyleSheet('color: #27c9d9')
        self.b4.clicked.connect(self.configVolt)
        
        self.b5 = QPushButton("⚙️")
        self.b5.setFixedWidth(30)
        self.b5.setFont(QFont(funte,8))
        self.b5.setStyleSheet('color: #27c9d9')
        self.b5.clicked.connect(self.configPres)
        
        
        self.le1.textChanged.connect(self.le1textChanged)
        self.le2.textChanged.connect(self.le2textChanged)
        i.b1.clicked.connect(i.accept)
        i.b1.clicked.connect(self.acceptAddress)
        i.b2.clicked.connect(i.reject)
        i.b2.clicked.connect(self.cancel)
        self.b3.setEnabled(False)
        self.b3.clicked.connect(self.refresh)
        
        divider = QFrame()
        divider.setFrameShape(QFrame.HLine)
        divider.setFrameShadow(QFrame.Sunken)
        
        lebtn = QHBoxLayout()
        lebtn.addWidget(self.le1)
        lebtn.addWidget(self.b4)
        
        lebtn2 = QHBoxLayout()
        lebtn2.addWidget(self.le2)
        lebtn2.addWidget(self.b5)
        
        i.form = QFormLayout()
        i.form.setSpacing(20)
        i.form.addRow(i.l1, lebtn)
        i.form.addRow(i.l2, lebtn2)
        
        i.hbox = QHBoxLayout()
        i.hbox.addWidget(self.b3)
        i.hbox.addWidget(i.b2)
        i.hbox.addWidget(i.b1)
        i.hbox.setAlignment(Qt.AlignRight)
        
        i.vbox = QVBoxLayout()
        i.vbox.addWidget(i.i_title)
        i.vbox.addWidget(spacer)
        i.vbox.addWidget(spacer)
        i.vbox.addLayout(i.form)
        i.vbox.addWidget(spacer)
        i.vbox.addWidget(divider)
        i.vbox.addWidget(spacer)
        i.vbox.addWidget(info)
        i.vbox.addWidget(spacer)
        i.vbox.addLayout(i.hbox)
        
        i.setStyleSheet(style)
        i.setWindowTitle("REX Connection Aid")
        i.setLayout(i.vbox)
        i.setFixedSize(460, 485)
        i.setWindowFlags(self.windowFlags() | Qt.CustomizeWindowHint)
        i.setWindowFlags(self.windowFlags() & ~Qt.WindowCloseButtonHint)
        i.exec_()
    
    def le1textChanged(self):
        self.b3.setEnabled(True)
    
    def le2textChanged(self):
        self.b4.setEnabled(True)
        
    def configVolt(self):
        
        i = QDialog()
        
        font = QFont(funte, 12)
        
        voltType = QLabel("Multimeter Type")
        voltType.setFont(font)
        self.voltType = QComboBox()
        self.voltType.addItems(["SCPI", "HP 3478A", "Custom"])
        index = self.voltType.findText(self.multiID, Qt.MatchFixedString)
        if index >= 0:
             self.voltType.setCurrentIndex(index)
        
        self.voltType.currentIndexChanged.connect(self.voltChange)
        
        voltCmd1 = QLabel("Query Command")
        voltCmd1.setFont(font)
        self.voltCmd1 = QLineEdit()
        self.voltCmd1.setFont(font)
        self.voltCmd1.setText(self.multiCmd)
        
        acceptBtn = QPushButton("Accept")
        acceptBtn.setFont(font)
        acceptBtn.clicked.connect(self.configVoltAccept)
        acceptBtn.clicked.connect(i.accept)
        
        rejectBtn = QPushButton("Cancel")
        rejectBtn.setFont(font)
        rejectBtn.clicked.connect(i.close)
        
        form = QFormLayout()
        form.setSpacing(20)
        form.addRow(voltType,self.voltType)
        form.addRow(voltCmd1, self.voltCmd1)
        
        hbox = QHBoxLayout()
        hbox.addWidget(rejectBtn)
        hbox.addWidget(acceptBtn)
        
        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)
        
        i.setStyleSheet(style)
        i.setLayout(vbox)
        i.setWindowTitle("Configure Multimeter")
        i.setContentsMargins(30,30,30,30)
        i.setFixedSize(460,200)
        i.exec_()
        
    def configVoltAccept(self):
        self.multiCmd = self.voltCmd1.text()
        self.multiID = str(self.voltType.currentText())
        
    def voltChange(self):
        self.multiID = str(self.voltType.currentText())
        if self.multiID == 'HP 3478A':
            self.voltCmd1.setText('*IDN?')
        elif self.multiID == 'SCPI':
            self.voltCmd1.setText('MEAS:VOLT:DC?')
        elif self.multiID == 'Custom':
            self.voltCmd1.setText('Enter Valid Command Here')
            
    def configPres(self):
        i = QDialog()
        i.setStyleSheet(style)
        
        font = QFont(funte, 12)
        
        
        presType = QLabel("Multimeter Type")
        presType.setFont(font)
        self.presType = QComboBox()
        self.presType.addItems(["SCPI", "Legacy (Non-SCPI)", "Custom"])
        
        index = self.presType.findText(self.gaugeID, Qt.MatchFixedString)
        if index >= 0:
             self.presType.setCurrentIndex(index)
        
        self.presType.currentIndexChanged.connect(self.presChange)
        
        presCmd1 = QLabel("Query Command")
        presCmd1.setFont(font)
        self.presCmd1 = QLineEdit()
        self.presCmd1.setFont(font)
        self.presCmd1.setText(self.gaugeCmd)
        acceptBtn = QPushButton("Accept")
        acceptBtn.setFont(font)
        acceptBtn.clicked.connect(self.configPresAccept)
        acceptBtn.clicked.connect(i.accept)
        rejectBtn = QPushButton("Cancel")
        rejectBtn.setFont(font)
        rejectBtn.clicked.connect(i.close)
        form = QFormLayout()
        form.setSpacing(20)
        form.addRow(presType,self.presType)
        form.addRow(presCmd1, self.presCmd1)
 
        hbox = QHBoxLayout()
        hbox.addWidget(rejectBtn)
        hbox.addWidget(acceptBtn)
        
        vbox = QVBoxLayout()
        vbox.addLayout(form)
        vbox.addLayout(hbox)

        i.setStyleSheet(style)
        i.setLayout(vbox)
        i.setWindowTitle("Configure Pressure Gauge")

        i.setContentsMargins(30,30,30,30)
        i.setFixedSize(460,200)
        i.exec_()
        
    def configPresAccept(self):

        self.gaugeCmd = self.presCmd1.text()

        self.gaugeID = str(self.presType.currentText())

        
    def presChange(self):
        self.gaugeID = str(self.presType.currentText())

        if self.gaugeID == 'Legacy (Non-SCPI)':
            self.presCmd1.setText('Enter Valid Command Here')
        elif self.gaugeID == 'SCPI':
            self.presCmd1.setText('MEAS[:PRES]:[Channel Here]')
        elif self.gaugeID == 'Custom':
            self.presCmd1.setText('Enter Valid Command Here')
        
        

    
    def acceptAddress(self):
        self.VISA = self.le1.text()
        self.VISA2 = self.le2.text()
        with open(visapkl, 'wb') as f:
            pickle.dump(self.VISA, f, protocol=2)
        with open(visa2pkl, 'wb') as f:
            pickle.dump(self.VISA2, f, protocol=2)
        self.btn_Rex.setFocus(True)
#        self.i_v_ia.setText(self.VISA)
        self.checktimer.stop()
        
        
    def refresh(self):
        self.VISA = self.le1.text()
        self.le1.setStyleSheet("color: "+blue)
        self.b3.setEnabled(False)
        self.VISA2 = self.le2.text()
        self.le2.setStyleSheet("color: "+blue)
        
    def cancel(self):
        with open(visapkl, 'rb') as visa:
            self.VISA = pickle.load(visa)
        self.btn_Rex.setFocus(True)
        self.checktimer.stop()
        
        
        
    
    def checkConnect(self):
        try:
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(self.VISA)
            if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                session.read_termination = '\n'
            session.write('*IDN?')
            session.read()
            session.close()
            resourceManager.close()
            self.le1.setStyleSheet('background-color: green; color:#27c9d9')

        except:
            self.le1.setStyleSheet('background-color: #874646; color:#27c9d9')
        
        try:
            rm = visa.ResourceManager()
            session = rm.open_resource(self.VISA2)
            if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                session.read_termination = '\n'
            session.write("*IDN?")
            session.read()
            session.close()
            rm.close()
            self.le2.setStyleSheet('background-color: green; color:#27c9d9')
        except:
            self.le2.setStyleSheet('background-color: #874646; color:#27c9d9')
        
            
            
    
    def rexClick(self, e):
        if e.button() == Qt.LeftButton:
            
            self.rex()
            
        else:
            pass
            
            
            
    def backClick(self):
#            print("STEP VALUE IN",self.step)
            if self.step > 0:
                self.step -= 2
                self.bhandle = 1
#                print("Calling REX...")
                self.rex()
#                print("REX Received")
            self.btn_Rex.setFocus(True)
    
    def cancelClick(self):
        if self.step < 1:
            w = Trans()
            self.close()
            w.show()
            index = w.tcb.findText(self.x[6], Qt.MatchFixedString)
            if index >= 0:
                w.tcb.setCurrentIndex(index)
            w.pnline.setText(self.x[1])
            w.fs.setText(self.x[3])
            w.rc.setText(self.x[4])
            index = w.psicb.findText(self.x[5], Qt.MatchFixedString)
            if index >= 0:
                w.psicb.setCurrentIndex(index)
                
            if self.x[5] == "PSIA":
                w.bpin.setText(self.x[2])
            w.exec_()
            
    def closeEvent(self, event):
        if self.finishtoken == 0:
            result = QMessageBox.warning(self, 'Exit Calibration', "\nAre you sure you want to exit the calibration?\n\nAll data will be lost.\n", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if result == QMessageBox.Yes:
                w = Start()
                w.show()
                event.accept()
                self.readtimer.stop()
            else:
                event.ignore()
                self.btn_Rex.setFocus(True)
        elif self.finishtoken == -1:
            w = Start()
            w.show()
            event.accept()
            try:
                self.readtimer.stop()
            except:
                pass
        else:
            event.accept()
            self.readtimer.stop()
            
            
        
    def quitClick(self):
        self.close()


#_______________________________________________________________________________________________________________________

    def rex(self):
        
        self.btn_Rex.setFocus(True)
        
        tm()

        try:
#           Create a connection (session) to the instrument
            resourceManager = visa.ResourceManager()
            session = resourceManager.open_resource(self.VISA)
#           For Serial and TCP/IP socket connections enable the read Termination Character, or read's will timeout
            if session.resource_name.startswith('ASRL') or session.resource_name.endswith('SOCKET'):
                session.read_termination = '\n'
            
#           Send *IDN? and read the response
            session.write('*IDN?')
            idn = session.read()
            idn = float(idn)*1000
            
#           Close the connection to the instrument
            session.close()
            resourceManager.close()
            
            dimgray = 'color: white'
            
#            ___________________________________________________________________________________________________________
            
            
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 1px solid ##414745; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color:#27c9d9')
            
            if self.step == -1:
                self.msg1_label.setText('To proceed, press the spacebar or click anywhere in REX.')
                self.bhandle = 0
                self.step = 0
            
            
#            ___________________________________________________________________________________________________________
                
            if self.x[5] == 'PSID':
                if self.step < 21:
                    self.fade(self.frame, 500)
            else:
                if self.step <= 18:
                    self.fade(self.frame, 500)
            
#            ___________________________________________________________________________________________________________
    
    
    
            if self.step == 0:
                self.btn_Back.setEnabled(False)
                self.btn_Back.setStyleSheet('color: lightgray')
                
                self.rexmsg.setText("Attach the test instrument and the pressure standard in parallel to the pressure source.\n\nLeave the pressure vented to atmosphere.")
                    
                if self.x[5] == 'PSID':
                    self.rexmsg.setText("Attach the test instrument and the pressure standard in parallel to the pressure source. Leave pressure vented to atmosphere.\n\nBecause " + self.x[1] + " is a differential pressure test instrument, connect the high side and leave the low side open, and determine the maximum rated line pressure.")
    
#            ___________________________________________________________________________________________________________
    
               
            if self.step == 1:
                self.btn_Back.setEnabled(True)
                self.btn_Back.clicked.connect(self.backClick)
                self.btn_Back.setStyleSheet('color: white')
                self.rexmsg.setText("Connect the power supply to the voltmeter and set the excitation voltage to the recommended voltage (Within +/-.05V is acceptable).\n\nRecord the volt reading by triggering REX.")

                

#            ___________________________________________________________________________________________________________
    
 
            if self.step == 2:
                if self.bhandle == 0:
                    self.eev = round(idn,4)
                self.rexmsg.setText("Activate the R-Cal and record the R-Cal millivoltage reading by triggering REX.")
                if self.bhandle == 0:
                    self.rexfeed()

#            ___________________________________________________________________________________________________________
                
              
            if self.step == 3:
                if self.bhandle == 0:
                    self.mc = round(idn,4)
                self.rexmsg.setText("Deactivate the R-Cal and record the atmospheric reference millivolt reading by triggering REX.")
                    
                if self.bhandle == 0:
                    self.p = np.zeros(12)
                    self.m = np.zeros(12)
                    if self.x[2] == '':
                        self.x[2] = 0
                    self.rexfeed()

                    
            if self.step == 3:
                self.msg1_label.setText('To proceed, press the spacebar or click anywhere in REX.')
                self.msg1_label.setStyleSheet('')
                self.msg1_label.setFont(QFont(funte, 11))
                    
            if self.step == 4:
                self.msg1_label.setText('⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪')
                self.msg1_label.setStyleSheet('color: #27c9d9')
                self.msg1_label.setFont(QFont(funte, 20))
                
#            ___________________________________________________________________________________________________________                    
                    
            if self.step in range(4, 17):
                                
#                    self.w.close()
                    
                i = self.step - 4
                    
                    
                m = self.step - 5
                
                    
#            ___________________________________________________________________________________________________________                    
#            ___________________________________________________________________________________________________________
                    
                bar = '⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪','⚫⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪','⚫⚫⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪','⚫⚫⚫⚪⚪⚪⚪⚪⚪⚪⚪⚪','⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚪⚪','⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪⚪','⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪⚪','⚫⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪⚪','⚫⚫⚫⚫⚫⚫⚫⚫⚪⚪⚪⚪','⚫⚫⚫⚫⚫⚫⚫⚫⚫⚪⚪⚪','⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚪⚪','⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚪','⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫⚫',

                if self.step in range(4, 16):
#                    print i, self.p, float(self.x[3]), self.x[5], float(self.x[2])
#                    print self.pres( i, self.p, float(self.x[3]), self.x[5], float(self.x[2]))
                        
                    string, __ = self.pres(i, self.p, float(self.x[3]), self.x[5], float(self.x[2]))
                        
                        
                    if self.bhandle == 0:
                        __, self.p[i] = self.pres(i, self.p, float(self.x[3]), self.x[5], float(self.x[2]))
                        
                    
#            ___________________________________________________________________________________________________________



                if self.step == 4:
                    if self.bhandle == 0:
                        self.ma = round(idn,4)
                        
                    self.rexmsg.setText('Starting Upscale Calibration:\n\n' + string + '\n\n\n\n')
                    if self.x[5] == 'PSIA':
                        self.rexmsg.setText('Starting Upscale Calibration:\n\nSet pressure to 0.0 PSIA by using the vacuum pump and absolute pressure gauge.\n\nUse the Enter key to input non-nominal pressure values when there is no pressure gauge connected to this computer.\n\n\n\n')
                        
                    try:
                        idn2 = self.callGauge()
#                        print idn2
#                        print 'Gauge is connected'
                        
                    except:
                        self.rexmsg.setText('Starting Upscale Calibration:\n\nSet pressure to 0.0 '+self.psir+' by using the vacuum pump and absolute pressure gauge.\n\nUse the Enter key to input non-nominal pressure values when there is no pressure gauge connected to this computer.\n\n\n\n')
                        
                    if self.bhandle == 0:
                        self.rexfeed()
                            
                        
    
#            ___________________________________________________________________________________________________________



                if self.step in range(5,16):
                        
                        
                    self.rexmsg.setText(string)
                    self.msg1_label.setText(bar[i])
                    if self.bhandle == 0:
                        self.m[m] = round(idn, 4)
                        
                        try:
                            idn2 = self.callGauge()
                            
                            self.p[m] = round(idn2, 4)
                                    
                        except:
                            pass
                                
                            
                if self.step == 15:
                    self.rexmsg.setText(string)
                    if self.x[5] == 'PSIA':
                        self.rexmsg.setText('Set pressure to 0.0 PSIA by using the vacuum pump and absolute pressure gauge.\n\nFor non-nominal pressures, press the enter key.')

#            ___________________________________________________________________________________________________________

                if self.step == 10:
                    self.rexmsg.setText('Starting Downscale Calibration:\n\n' + string)

#            ___________________________________________________________________________________________________________
                
                
               
            if self.step == 15:
                self.msg1_label.setText(bar[i])
                self.msg1_label.setStyleSheet('color: #27c9d9')
                self.msg1_label.setFont(QFont(funte, 20))

#            ___________________________________________________________________________________________________________
#            ___________________________________________________________________________________________________________
                
                            
            if self.step == 16:
                    
                # Prevents final m reading from being corrupted by back button
                m = 11
                self.m[m] = idn
                try:
                    idn2 = self.callGauge()
                    
                    self.p[m] = round(idn2, 4)
                            
                except:
                    pass
                                
                self.msg1_label.setText(bar[i])
                QTimer.singleShot(1500, self.clearMsg)


                self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid lightgreen; color: lightgreen; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
                self.rexmsg.setText('Calibration data acquisition is complete.\n\nPlease click \'Finish\' to proceed to the REX analysis of Pressure Transducer ' + self.x[1] + '.')
                self.rexmsg.setStyleSheet('color: lightgreen')
                
                
                self.btn_Finish.setEnabled(True)
                self.btn_Finish.clicked.connect(self.rexFinish)
                self.btn_Finish.setStyleSheet(dimgray)
                self.btn_Back.setEnabled(False)
                self.btn_Back.setStyleSheet('color: lightgray')
                self.btn_Next.setStyleSheet('color: lightgray')
                self.btn_Next.setEnabled(False)
                    
                self.btn_Finish.setFocus(True)
                self.rexbox.mousePressEvent = self.rexPause()
                self.btn_Rex.setEnabled(False)
            
                    
                    

#            ___________________________________________________________________________________________________________
#            ___________________________________________________________________________________________________________
#            ___________________________________________________________________________________________________________    

            # PRINT VALUES
#            if self.step in range(4,16):      
#                print('Pressure p[', i, ']: ', self.p[i])
#            if self.step in range(5, 17):
 #               print('Voltage m[', m, ']: ', self.m[m])
 #           if self.step in range(4,16):
 #               print(string)
 #           if self.step in range(5,17):
 #               print('Pressure p[',m,']: ',self.p[m])
  #          print('\n')
            
                
            if 4 < self.step < 16:
                if self.bhandle == 0:
                    if self.triggered == 0:
                        self.rexfeed()
                        
#               if 19 < self.step <= 19 + self.teststeps:

                
            self.bhandle = 0
            
            
            if self.x[5] == 'PSID':
                if self.step > 16:
                    if self.step < 20:
                        self.unfade(self.frame, 1000)
                    if self.step <= 18:
                        self.step += 1
                elif self.step <= 16:
                    self.unfade(self.frame, 1000)  #Stops from fading after the last unfade
                    self.step += 1
            else:
                    
                if self.step < 18:
                    self.unfade(self.frame, 1000)
                if self.step <= 16:
                    self.step += 1
                
                
   

                
                
                
            
        except:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.fade(self.frame, 500)
            self.rexmsg.setStyleSheet('color: pink')
            self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid icon.')
            self.unfade(self.frame, 1000)
            
        try:
            self.btn_Rex.clicked.disconnect()
            self.btn_Back.clicked.disconnect()
            self.rexbox.mousePressEvent = self.rexClick
            self.rexbox.mouseDoubleClickEvent = self.rexClick
            QTimer.singleShot(1000, self.rexOn)
        except:
            pass
#            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
#            self.fade(self.frame, 500)
#            self.rexmsg.setStyleSheet('color: pink')
#            self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid 🔧 icon.')
            self.unfade(self.frame, 1000)
        
        
    def rexOn(self):
        self.rexbox.mousePressEvent = self.rexClick
        try:
            self.btn_Rex.clicked.connect(self.rex)
            self.btn_Back.clicked.connect(self.backClick)
        except:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color: pink')
            self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid icon.')
        
    def rexPause(self):
        try:
            print 'REX: "I am processing your command, please wait."'
        except:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid #874646; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color: pink')
            self.rexmsg.setText('I\'m sorry, there seems to be a problem connecting to the output test instrument located at ' + self.VISA + '.\n\nI can help you change the VISA address, refresh the connection status, and display further instructions to do so if you click the REX Connection Aid icon.')
        
    def clearMsg(self):
        self.msg1_label.setText('')
        if self.step == 17:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid lightgreen; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
        
    def rexfeed(self):
        
        self.mega = 1
        
        r = self.step
        
        ttype = self.x[5]
        
        if self.triggered == 0:
            m = r - 5
        else:
            m = r - 6
            r -= 1
        
        self.words = self.rexmsg.text()
        
        if r == 2:
            self.rexmsg.setText('Excitation: ' + str(round(self.eev/1000, 4)) + ' V')
            
        if r == 3:
            self.rexmsg.setText('R-Cal Reading: ' + str(self.mc) + ' mV')
            
        if r == 4:
            self.rexmsg.setText('Atmospheric Reading: ' + str(self.ma) + ' mV')
            self.msg1_label.setText('')
            
        if 4 < r < 17:
            if self.x[5] == 'PSIA':
                self.rexmsg.setText('Pressure: ' + str(round(self.p[m] + float(self.x[2]), 4)) + ' ' + ttype + '\n\nOutput: ' + str(self.m[m]) + ' mV')
            else:
                self.rexmsg.setText('Pressure: ' + str(self.p[m]) + ' ' + ttype + '\n\nOutput: ' + str(self.m[m]) + ' mV')
                
            
        
        if r < 17:
            self.rexmsg.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
            self.rexmsg.setStyleSheet('color: lightgreen')
            
            self.fade(self.frame, 1000)
            self.unfade(self.frame, 1000)
        
        if self.triggered == 0:
            try:
    #            self.rexbox.mouseReleaseEvent = self.rexPause()
                self.btn_Rex.clicked.disconnect()
                self.btn_Back.clicked.disconnect()
            except:
                pass
            
        QTimer.singleShot(1100, self.rexfeedreset)
        
    def rexfeedreset(self):
        self.mega = 0

        self.rexmsg.setText(self.words)
        self.rexmsg.setStyleSheet("color:"+blue)
        self.rexmsg.setAlignment(Qt.AlignLeft)
        
        if self.step == 5:
            self.msg1_label.setText('⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪⚪')
            self.msg1_label.setStyleSheet('color: #27c9d9')
            self.msg1_label.setFont(QFont(funte, 20))
        
        if self.step < 17:
            self.fade(self.frame, 500)
            self.unfade(self.frame, 500)
            
        if self.step == 17:
            self.rexbox.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid lightgreen; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setStyleSheet('color: lightgreen')
        
        QTimer.singleShot(1000, self.rexOn)
        
#        timer2 = QTimer(self)
#        timer2.start(1000)
#        timer2.timeout.connect(self.mVreading)
#        timer2.timeout.connect(print(''))
        
        
#   Fade Effect
    def fade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start(QPropertyAnimation.DeleteWhenStopped)
    
    def unfade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        

#___NONNOMINAL VALUES _________________________________________________________________________________________________
        
    def keyPressEvent(self, qKeyEvent):
        
        if qKeyEvent.key() == Qt.Key_Return:
            if 4 < self.step < 17:
                
                self.w = QWidget()
                self.w.setStyleSheet(style)
                title = QLabel()
                title.setFont(QFont(funte, 13))
                title.setStyleSheet('color: white')
                self.line = QLineEdit()
                self.line.setFont(QFont(funte, 19))
                self.line.setStyleSheet('color: gray; background-color: transparent;')
                inf = QLabel("Press Enter to Input")
                inf.setFont(QFont(funte, 11))
                inf.setStyleSheet('color: lightgray')
                vbox = QVBoxLayout()
                vbox.addWidget(title)
                vbox.addWidget(self.line)
                vbox.addWidget(inf)
                self.w.setWindowTitle("REX Input")
                self.w.setLayout(vbox)
                self.w.setContentsMargins(10,10,10,10)
                self.w.setFixedSize(400,120)
                    
                title.setText("Input Non-Nominal Pressure")
                    
                validator = QDoubleValidator()
                self.line.setValidator(validator)
                self.line.returnPressed.connect(self.nom)
                if self.mega == 0:
                    self.w.show()    
                    
        else:
            try:
                super().keyPressEvent(qKeyEvent)
            except:
                pass
            
    def nom(self):
        if self.x[4] != "NRC":
            
            i = self.step - 5
            
            self.w.close()
            
            self.triggered = 1
            
            self.rex()
            
            self.p[i] = round(float(self.line.text()), 3)
            
            if self.x[5] == 'PSIA':
                if self.step == 8:
                    self.p[i] = self.p[i] - float(self.x[2]) 
                if self.step == 19:
                    self.p[i] = self.p[i] - float(self.x[2])
                round(self.p[i], 3)
                
                
            self.rexfeed()
            
            
            self.triggered = 0
            

            
    def zero(self):
        i = self.step - 17
        self.zp[i] = self.line.text()
        self.w.close()
        self.rex()

        
    def rexFinish(self):
        
        self.fade(self.rexmsg,800)
        self.rexmsg.setText("Configuring REX Analysis of " + self.x[1] + '...')
        self.unfade(self.rexmsg, 2000)
        
        pickledata = [0,0,0]
        
        if self.x[5] == 'PSIA':
            self.p = self.p + float(self.x[2])
        
        time = datetime.now().strftime("%m/%d/%Y %H:%M")
        
        # Convert Volt Readings to Millivolts
        self.m = self.m
        self.zm = self.zm
        
        self.x[0] = time
        
        self.oldrcal = self.x[4]
        
        pickledata[0] = self.x
        
        pickledata[1] = self.oldrcal, self.eev, self.mc, self.ma
        
        
        self.pfs = self.pfserr(self.p, self.m, float(self.x[4]), float(self.x[3]), self.mc, self.ma)
        
        self.updown = ['Up','Up','Up','Up','Up','Up','Down','Down','Down','Down','Down','Down']
        
        new_rcal = self.rcal(self.p,self.m, float(self.mc), float(self.ma))
        lpfs = self.pfserr(self.p, self.m, float(new_rcal), float(self.x[3]), self.mc, self.ma)
            
        pressure = 'Pressure (' + self.x[5] + ')'
            
        df = pd.DataFrame({pressure : self.p, "Output (mV)" : self.m, '% mV/Pressure' : lpfs, "As Found (% of FS)" : self.pfs, 'Scale' : self.updown})
            
            
    #   _________________________________________________________________________________
            
 

        
        d = self.x[0].rsplit("/",-1)
        d[2] = d[2].rsplit(" ", -1)[0]
        date = d[0] + "-" + d[1] + "-" + d[2]
        
        root = trans_data
        
        filename = self.x[1] + '_' + date + '_vals.pkl'
        
        with open(root + filename, 'wb') as f:
            pickle.dump(pickledata, f, protocol=2)
            
        
        with open(trans_data_setup + self.x[1] + '.pkl', 'wb') as f:
            pickle.dump(self.x, f, protocol=2)
            
        
        filename = self.x[1] + '_' + date + '_graph.csv'
        
        df.to_csv(root + filename)
        
        
        self.rexmsg.setText('Calibration Data for ' + self.x[1] + ' Saved...')
        
        oh= Start()
        try:
            w = TransAnalysis(oh)
        except:
            w = TransAnalysis()
            
        self.rexmsg.setText('Launching REX Analysis...')
        oh.show()
        w.show()
        
        self.finishtoken = 1
        self.close()
        
        

        
        #lc.trans.txt       [0]
        #pn.trans.txt       [1]
        #trans.bp.txt       [2]
        #trans.fs.txt       [3]
        #trans.rcal.txt     [4]
        #trans.psitype.txt  [5]
        #trans.user.txt     [6]
        
        
        



class TransAnalysis(QMainWindow):
    
    send_fig = pyqtSignal(str)

    def pfserr(self, p, m, rc, fs, mc, ma):
#       Calculates percent full scale error
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       rc = as-found R-Cal value in psi.
#       fs = full scale rating of TI.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        
        
#        m = m/1000
#        mc = mc/1000
#        ma = ma/1000
        
        
        
        p, m = np.asarray(p), np.asarray(m)
        pfserr = np.zeros(len(p))
        for n in range(0, len(p)):
            pfserr[n] = 100 * (rc * (m[n]-m[0])/(mc-ma) - p[n]) / fs
#            pfserr[n] = 100 * (p[n] - p[0] - rc *(m[n]-m[0])/(mc - ma)) / fs
#            pfserr[n] = 100 * ((p[n] - p[0] - rc * (((m[n]-m[0])/1000) / ((mc - ma)/1000))) / fs)
        return pfserr
    
    def rcal(self, p, m, mc, ma):
#       Calculates the R-Cal
#       p = array of pressure measurements.
#       m = array of transducer readings in mV.
#       mc = R-Cal millivolt reading.
#       ma = Atmospheric reference millivolt reading.
        p, m = np.asarray(p), np.asarray(m)
        s1, s2 = 0, 0
        for n in range(1, len(p) - 1):
            s1, s2 = s1 + (p[n] - p[0]) * (m[n] - m[0]), s2 + (m[n] - m[0])**2
        return (mc - ma) * s1 / s2    
    
    def pres(self, n, p, fs, trtype, b = 0):
#       Specifies and records nominal pressure for a point in the test.
#       n = point of data
#       p = array of pressure measurements (begins as array of zeros).
#       trtype = transducer type: 'psia', 'psid', or 'psig'.
#       fs = full scale rating of TI.
#       b = barometric pressure reading (psi)
        thres, msg = len(p)/2 -1, 'Set pressure to '
#       thres = "threshold" - the upper limit of upscale calibration
        if n <= thres:
            dp = fs / thres * n
        else:
            dp = fs / thres * (len(p) - 1 - n)
        p[n] = dp - b                               # ??? + or - b ???
        p[n] = round(p[n], 3)
        if b != 0 and p[n] < 0:
            trtype = 'PSIA'
            pres = msg + str(dp) + ' ' + trtype
        else:
            if b != 0:
                trtype = 'PSIG'
            pres = msg + str(p[n]) + ' ' + trtype
        return pres, p[n]
    
    def topsia(self, p, b):
#       Converts pressure data array in PSIG to PSIA using barometric reading
        return np.array(p) + b
    
    def __init__(self, parent = None):
        super(QMainWindow, self).__init__(parent)
        
#---------------------------------------------------------------------------------------------------------------------#
     
        #STYLE GUIDE
        
        #FONTS
        fntbtn = QFont(funte, 12)
        
        #COLORS
        dimgray = 'color: white'
        gray = 'color: #27c9d9'
        
        #SPACING
        d1 = QFrame()
        d1.setFrameShape(QFrame.HLine)
        d1.setFrameShadow(QFrame.Sunken)
        #create multiple
        
        sfont = QFont()
        sfont.setPointSize(1)
        space = QLabel(" ")
        space.setFont(sfont)
        #setSpacing is also useful
        
        self.setStyleSheet(style)

        
#---------------------------------------------------------------------------------------------------------------------#
        
#   Data
        
        with open(pickl, 'rb') as f:
            self.x = []
            self.x = pickle.load(f)
            
            #lc.trans.txt       [0]
            #pn.trans.txt       [1]
            #trans.bp.txt       [2]
            #trans.fs.txt       [3]
            #trans.rcal.txt     [4]
            #trans.psitype.txt  [5]
            #trans.user.txt     [6]
        print 'self.x', self.x
        print 'self.x[0]', self.x[0]
        d = self.x[0].rsplit("/",1)
        print 'd', d
        de = d[0].rsplit("/", 1)
        print 'de', de
        
        date = de[0] + "-" + de[1] + "-" + d[1]
        print date
        
        
        
        root = trans_data
        
        
        filename = self.x[1] + '_' + date + '_vals.pkl'
        
        print 'so', root+filename

        with open(root+filename, 'rb') as f:
            print 'so'
            self.vals = []
            print 'so'
            self.vals = pickle.load(f)
            print 'so'
            
        print 'so'     
            
        self.x = self.vals[0]
        
        
        self.chain = self.vals[1]
        
        
        self.oldrcal = self.chain[0]
        
        
        self.eev = self.chain[1]
        
        
        self.mc = self.chain[2]
        
        
        self.ma = self.chain[3]
        
        
        
#        self.vals
#        self.x     [0]
#        old r cal  [1]
#        excitation [2]
#        mc         [3]
#        ma         [4] 
        
        filename = self.x[1] + '_' + date + '_graph.csv'

        self.df = pd.read_csv(root + filename)
        
#        filename = self.x[1] + '_' + date + '_graph2.csv'
#
#        self.df2 = pd.read_csv(root + '/' + filename)
        
        
        
        self.linearcheck = self.df['% mV/Pressure'].tolist()
        
        self.asfoundfs = self.df['As Found (% of FS)'].tolist()
        
        
        
        affs = np.absolute(self.asfoundfs)
        
        rexavg = np.mean(affs)
        
        rexmax = max(affs)
        
        
        
        
        self.p = self.df['Pressure (' + self.x[5] + ')'].tolist()
        
        
        self.m = self.df['Output (mV)'].tolist()
        
        self.ogrexrating = 0

        
        if rexavg < .25:
            if rexmax < .5:
                self.rexrating = 1
        if .25 <= rexavg < .5:
            if rexmax < .5:
                self.rexrating = 2
        if .5 <= rexmax <= 1:
            self.rexrating = 3
        if rexmax > 1:
            self.rexrating = 4
        
            
        if self.rexrating > 1:
            
            self.ogrexrating = self.rexrating
            
            self.x[4] = self.rcal(self.p,self.m, float(self.mc), float(self.ma))
                # UPDATE THE R CAL DISPLAYED
                
            self.x[4] = str(round(self.x[4],3))
                
                
            self.pfs = self.pfserr(self.p, self.m, float(self.x[4]), float(self.x[3]), float(self.mc), float(self.ma))
                
            boole = all(i <= .5 for i in np.abs(self.pfs))
                
            if boole == False:
                self.rexrating = 5

        name = self.x[6].rsplit(', ', 1)[1]
        name = name.rsplit(' [',1)[0]
        

            
        


#---------------------------------------------------------------------------------------------------------------------#	

#   Contents
        
        # TITLE
        rextitle = QLabel()
        pxmp = QPixmap(logo)
        pxmp = pxmp.scaledToWidth(80)
        rextitle.setPixmap(pxmp)
        
        if self.x[4] != "NRC":
            prop = QLabel("Calibration Analysis\nPressure Transducer " + self.x[1])
        else:
            prop = QLabel("Non-R-Cal Pressure Transducer " + self.x[1])
            
        prop.setFont(QFont(funte, 13))
        prop.setStyleSheet(dimgray)

        
        # GRAPHS
        self.snsplot()
        self.snsplot2()
        
        
        
        
        plotpng1 = QPixmap(temp1)
        plotpng2 = QPixmap(temp2)
        
        self.plot1 = QLabel()
        self.plot1.setPixmap(plotpng1)
        self.plot2 = QLabel()
        self.plot2.setPixmap(plotpng2)


        self.dropdown1 = QComboBox()
        self.dropdown1.addItems(["This will have an archive of all calibrations on this instrument eventually"])

        self.dropdown1.currentIndexChanged.connect(self.update)

        p1t = 'R-Cal'
        
        self.p1title = QLabel(p1t)
        
        #TABLE
        self.df = self.df.round(3)
        self.tableView = QTableView()
        model = PandasModel(self.df)
        self.tableView.setModel(model)
        self.tableView.setColumnHidden(0, True)
        self.tableView.setColumnHidden(1, True)
        self.tableView.setColumnHidden(5, True)
        self.tableView.setFixedHeight(273)
        self.tableView.setFixedWidth(308)
        self.tableView.setStyleSheet(dimgray)
        self.tableView.setFont(fntbtn)
        self.tableView.setColumnWidth(4, 106)
        self.tableView.verticalHeader().setDefaultSectionSize(21)
        self.tableView.verticalHeader().setVisible(False)
        
#        self.tableView.setStyleSheet('QTableView::alternate-background-color: yellow;')
        
        self.plot1.mousePressEvent = self.openGraph1
        self.plot2.mousePressEvent = self.openGraph2
        
        
        
        #BOTTOM ROW
        b1 = QPushButton("Done")
        b1.setFont(fntbtn)
        b1.setStyleSheet(dimgray)
        b1.clicked.connect(self.exitClicked)
        b1.setFixedSize(200, 40)
        
        calby = QLabel("Calibrated by " + str(self.x[6]) + " on " + date)
        calby.setStyleSheet('color: white')
        calby.setFont(QFont(funte, 13))
        
        self.b2 = QPushButton("Screenshot")
        self.b2.clicked.connect(self.screenShot)
        self.b2.setFont(fntbtn)
        self.b2.setStyleSheet(dimgray)
        self.b2.setFixedSize(200, 40)
        
        #REX MESSAGE
        self.rexmsg = QLabel('')
        self.rexmsg.setFont(QFont(funte, 13))
        self.rexmsg.setStyleSheet('color:#27c9d9')
        
        
        
        
        
        
        # INFOBOX
        
        grid = QGridLayout()
        
        sz = 11
        
        pn1 = QLabel("Property Number   ")
        pn1.setFont(QFont(funte, sz))
        pn1.setStyleSheet(dimgray)
        grid.addWidget(pn1,0,0)
                     
        pn2 = QLabel(self.x[1])
        pn2.setFont(QFont(funte, sz))
        pn2.setStyleSheet(gray)
        grid.addWidget(pn2,0,1)        
                     
        tec1 = QLabel("Technician")
        tec1.setFont(QFont(funte, sz))
        tec1.setStyleSheet(dimgray)
        grid.addWidget(tec1,1,0)
                      
        tec2 = QLabel(self.x[6] + "     ")
        tec2.setFont(QFont(funte, sz))
        tec2.setStyleSheet(gray)   
        grid.addWidget(tec2,1,1)
        
        d1 = QLabel("Date")
        d1.setFont(QFont(funte, sz))
        d1.setStyleSheet(dimgray)   
        grid.addWidget(d1,2,0)
        
#        print('aye')
        
        date = self.x[0].rsplit(' ',1)[0]
        
        d2 = QLabel(date)
        d2.setFont(QFont(funte, sz))
        d2.setStyleSheet(gray)   
        grid.addWidget(d2,2,1)
        
                      
        r1 = QLabel("Range")
        r1.setFont(QFont(funte, sz))
        r1.setStyleSheet(dimgray)
        grid.addWidget(r1,3,0)          
                    
        r2 = QLabel(self.x[3] + ' ' + self.x[5])
        r2.setFont(QFont(funte, sz))
        r2.setStyleSheet(gray)
        grid.addWidget(r2,3,1)

                    
        e1 = QLabel("Excitation")
        e1.setFont(QFont(funte, sz))
        e1.setStyleSheet(dimgray)
        grid.addWidget(e1,0,2)   
      
                    
        e2 = QLabel(str(round(self.eev/1000, 4)) + ' V     ')
        e2.setFont(QFont(funte, sz))
        e2.setStyleSheet(gray)
        grid.addWidget(e2,0,3)            
                    
        ma1 = QLabel("Atmospheric Reading   ")
        ma1.setFont(QFont(funte, sz))
        ma1.setStyleSheet(dimgray)
        grid.addWidget(ma1,1,2)             
                     
        ma2 = QLabel(str(round(self.ma, 4)) + ' mV   ')
#        ma2 = QLabel(self.ma)
        ma2.setFont(QFont(funte, sz))
        ma2.setStyleSheet(gray)
        grid.addWidget(ma2,1,3) 

                     
        mc1 = QLabel("R-Cal Reading")
        mc1.setFont(QFont(funte, sz))
        mc1.setStyleSheet(dimgray)
        grid.addWidget(mc1,2,2)                     
                     
        mc2 = QLabel(str(round(self.mc, 4)) + ' mV   ')
#        mc2 = QLabel(self.mc)
        mc2.setFont(QFont(funte, sz))
        mc2.setStyleSheet(gray)
        grid.addWidget(mc2,2,3)
        
        afrc1 = QLabel("As-Found R-Cal")
        afrc1.setFont(QFont(funte, sz))
        afrc1.setStyleSheet(dimgray)
        grid.addWidget(afrc1,3,2)
        
                       
        afrc2 = QLabel(str(round(float(self.oldrcal), 5)) + ' ' + self.x[5] + '     ')
        afrc2.setFont(QFont(funte, sz))
        afrc2.setStyleSheet(gray)
        grid.addWidget(afrc2,3,3)
        
                       
        crc1 = QLabel("Valid R-Cal   ")
        crc1.setFont(QFont(funte, sz))
        crc1.setStyleSheet(dimgray)
        grid.addWidget(crc1,1,4)
        
        
        if self.rexrating == 1:
            crc2 = QLabel(str(round(float(self.oldrcal), 5)) + ' ' + str(self.x[5]) + '     ')
            crc2.setStyleSheet(gray)
        elif 1 < self.rexrating < 5:
            crc2 = QLabel(str(round(float(self.x[4]),5)) + ' ' + self.x[5] + '     ')
            crc2.setStyleSheet(gray)
        elif 5 < self.rexrating < 8:
            crc2 = QLabel(str(round(float(self.x[4]),5)) + ' ' + self.x[5] + '     ')
            crc2.setStyleSheet(gray)
        else:
            crc2 = QLabel('N/A')
            crc2.setStyleSheet('color: red')
            
            
        crc2.setFont(QFont(funte, sz))
        grid.addWidget(crc2,1,5)
                      
        fsrc1 = QLabel("Percent of Full Scale   ")
        fsrc1.setFont(QFont(funte, sz))
        fsrc1.setStyleSheet(dimgray)
        grid.addWidget(fsrc1,2,4)
        
        fsorc = round(float(self.oldrcal)/float(self.x[3]), 3) * 100
        fsrc = round( float(self.x[4])/float(self.x[3]), 3) * 100
        
        if self.rexrating == 1:
            fsrc2 = QLabel(str(round(float(fsorc),2)) + '%   ')
            fsrc2.setStyleSheet(gray)
        elif 1 < self.rexrating < 5:
            fsrc2 = QLabel(str(round(float(fsrc),2)) + '%   ')
            fsrc2.setStyleSheet(gray)
        elif 5 < self.rexrating < 8:
            fsrc2 = QLabel(str(round(float(fsrc),2)) + '%   ')
            fsrc2.setStyleSheet(gray)
        else:
            fsrc2 = QLabel('N/A')
            fsrc2.setStyleSheet('color: red')
        
        fsrc2.setFont(QFont(funte, sz))
        grid.addWidget(fsrc2,2,5)
        

        
        ibox = QGroupBox()
        ibox.setLayout(grid)
        
        
        
        
        

#---------------------------------------------------------------------------------------------------------------------#

#   Layouts
        
        bigtits = QVBoxLayout()
        bigtits.addWidget(rextitle, 0, Qt.AlignBottom)
        bigtits.addWidget(prop, 0, Qt.AlignTop)
        
        top = QHBoxLayout()
        top.addLayout(bigtits)
        top.addWidget(ibox)
        
        screen_resolution = app.desktop().screenGeometry()
        width, height = screen_resolution.width(), screen_resolution.height()
        
        wid = width - 216
        hei1 = height*.42317708 #325
        hei2 = height*.13020833 #100
        
        
        #414745
        graphgb = QGroupBox()
        graphgb.setMinimumHeight(hei1)
        graphgb.setMinimumWidth(wid)
        graphgb.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 1px solid #414745; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
        
        rexbar = QGroupBox()
        rexbar.setMinimumHeight(hei2)
        rexbar.setMinimumWidth(wid)
        rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 1px solid #414745; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
        
        
        graphs = QHBoxLayout()
        graphs.addWidget(self.plot1, 0, Qt.AlignRight)
        graphs.addWidget(self.plot2, 0, Qt.AlignLeft)
        
        data = QHBoxLayout()
        data.addWidget(self.tableView, 0, Qt.AlignCenter)
        data.addLayout(graphs)
        data.setAlignment(Qt.AlignCenter)
        
        gball = QVBoxLayout()
        gball.addLayout(data)
        
        graphgb.setLayout(gball)
        
        barrex = QVBoxLayout()
        barrex.addWidget(self.rexmsg)
        
        barwig = QWidget()
        barwig.setLayout(barrex)
        barwig.setContentsMargins(20,0,20,0)
        
        barlay = QVBoxLayout()
        barlay.addWidget(barwig)
        
        rexbar.setLayout(barlay)
        
        nuts = QHBoxLayout()
        nuts.addWidget(self.b2,0,Qt.AlignLeft)
        nuts.addWidget(b1, 0, Qt.AlignRight)
        
        layout_main = QVBoxLayout()
        layout_main.addLayout(top)
        layout_main.addWidget(space)
        layout_main.addWidget(graphgb, 0, Qt.AlignCenter)
        layout_main.addWidget(space)
        layout_main.addWidget(rexbar,0,Qt.AlignCenter)
        layout_main.addWidget(space)
        layout_main.addLayout(nuts)
        
        self.frm = QFrame()
        self.frm.setLayout(layout_main)
        self.setCentralWidget(self.frm)
        self.unfade(self.rexmsg, 2000)
        

#---------------------------------------------------------------------------------------------------------------------#
        
        

        
        if self.rexrating == 1:
            rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid lightgreen; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setText('Pressure Transducer ' + self.x[1] + ' has a REX Rating of 1. (Average Error: ' + str(round(rexavg, 2)) + '%, Maximum Error: ' + str(round(rexmax, 2)) + '%)\n\nThe as-found R-Cal is valid, and shall remain on the test instrument for the next interval. Thank you ' + name + ', the calibration is complete.')
            self.rexmsg.setStyleSheet('color: lightgreen')
            
            
            
        if self.ogrexrating == 2:
            rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid olivedrab; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setText('Pressure Transducer ' + self.x[1] + ' has a REX Rating of 2. (Average Error: ' + str(round(rexavg, 2)) + '%, Maximum Error: ' + str(round(rexmax, 2)) + '%)\n\nThe as-found R-Cal is invalid, and must be revised to ' + str(round(float(self.x[4]),3)) + ' for the next interval. Thank you ' + name + ', the calibration is complete.')
            self.rexmsg.setStyleSheet('color: olivedrab')
        
        if self.ogrexrating == 3:
            rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid goldenrod; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setText('Pressure Transducer ' + self.x[1] + ' has a REX Rating of 3. (Average Error: ' + str(round(rexavg, 2)) + '%, Maximum Error: ' + str(round(rexmax, 2)) + '%)\n\nThe as-found R-Cal is invalid, and must be revised to ' + str(round(float(self.x[4]),3)) + ' for the next interval. Thank you ' + name + ', the calibration is complete.')
            self.rexmsg.setStyleSheet('color: goldenrod')
            
            
        if self.ogrexrating == 4:
            rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid orange; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setText('Pressure Transducer ' + self.x[1] + ' has a REX Rating of 4. (Average Error: ' + str(round(rexavg, 2)) + '%, Maximum Error: ' + str(round(rexmax, 2)) + '%)\n\nThe as-found R-Cal is invalid, and must be revised to ' + str(round(float(self.x[4]),3)) + ' for the next interval. Thank you ' + name + ', the calibration is complete.')
            self.rexmsg.setStyleSheet('color: orange')
            
            
        if self.rexrating == 5:
            rexbar.setStyleSheet('QGroupBox::title {background-color: transparent; subcontrol-position: top left; oaddubgL 2 13px;} QGroupBox {border: 3px solid red; border-radius: 3px; background-image: url('+rex_bg+') 0 0 0 0 stretch stretch; margin-top: 1ex;}')
            self.rexmsg.setText('Pressure Transducer ' + self.x[1] + ' has excessive linearity issues and requires repair. (Average Error: ' + str(round(rexavg, 2)) + '%, Maximum Error: ' + str(round(rexmax, 2)) + '%)')
            self.rexmsg.setStyleSheet('color: pink')
            
            
        

            
            
            



#---------------------------------------------------------------------------------------------------------------------#

#   Window Format
        
        w, h = 1130, 690
        
        l, t, r, b = 100,50,100,50
        self.setContentsMargins(l,t,r,b)
    
        self.setMinimumWidth(w)
        self.setMinimumHeight(h)
        self.setWindowTitle('MetroAssist REX')
        self.showFullScreen()

#---------------------------------------------------------------------------------------------------------------------#

    def snsplot(self):
        
        sns.set()
        sns.set_style('whitegrid', {'font.family':'Arial', 'text.color':'white', 'xtick.color':'white', 'ytick.color':'white', 'axes.labelcolor' : 'white'})
        sns.set_context('talk')
        

        pressure = 'Pressure (' + self.x[5] + ')'
        
        sns.lmplot(x = pressure, y = 'Output (mV)', data = self.df)
        
#        mv = self.df['Output (mV)'].tolist()
        
#        plt.xlim(0,float(self.x[3])+float(self.x[3])/80)
#        plt.ylim(ymax = float(self.x[3])/3)
        
        if self.x[4] == 'NRC':
            tit = 'Pressure v. Output'
        else:
            tit = 'R-Cal'
            
        
        plt.title(tit)
        
        plt.savefig(temp1, dpi=60, transparent=True)
        plt.close()
        
        
        
    def snsplot2(self):
        
#        p = self.p
#        p.extend(self.p)
#        m = self.linearcheck
#        m.extend(self.asfoundfs)
#        i = 0
#        hu = []
#        while i < 12:
#            hu.append('As-Found')
#            i += 1
#        i = 0
#        while i < 12:
#            hu.append('')
#        
#        
#        dat = pd.DataFrame()
        
        sns.set()
        sns.set_style('whitegrid', {'font.family':'Arial', 'text.color':'white', 'xtick.color':'white', 'ytick.color':'white', 'axes.labelcolor' : 'white'})
        sns.set_context('talk')
        
        pressure = 'Pressure (' + self.x[5] + ')'
            
        yaxis = '% mV/Pressure'
            
        sns.lmplot(x = pressure, y = yaxis, hue = 'Scale', data = self.df, fit_reg = False)
        
        
#        plt.xlim(0,float(self.x[3])+float(self.x[3])/80)
        plt.ylim(ymin=-.5, ymax = .5)
        plt.yticks(np.arange(-.5, .5+.5, .5))
        plt.title('Linearity')
        plt.savefig(temp2, dpi=60, transparent=True)
        plt.close()
        
#---------------------------------------------------------------------------------------------------------------------#


#   Fade Effect
        
    def fade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(1)
        self.animation.setEndValue(0)
        self.animation.start(QPropertyAnimation.DeleteWhenStopped)
    
    def unfade(self, widget, d):
        self.effect = QGraphicsOpacityEffect()
        widget.setGraphicsEffect(self.effect)
        self.animation = QPropertyAnimation(self.effect, b"opacity")
        self.animation.setDuration(d)
        self.animation.setStartValue(0)
        self.animation.setEndValue(1)
        self.animation.start()
        
#---------------------------------------------------------------------------------------------------------------------#
        
        
#    Buttons
    def exitClicked(self):
        self.close()
        
    def screenShot(self):
        
        date = datetime.now()
        filename = self.x[1] + '_' + date.strftime('%Y-%m-%d_%H-%M-%S.jpg')
        
        path = os.getcwd() + '\\Screenshots\\' + filename
        
        p = self.frm.grab()
        p.save('Screenshots/' + filename, 'jpg')
        
        self.words = self.rexmsg.text()
        
        self.fade(self.rexmsg, 500)
        self.rexmsg.setText('Screenshot saved to ' + path)
        self.unfade(self.rexmsg, 1000)
        
        self.b2.setEnabled(False)
        
        QTimer.singleShot(5000, self.rexSet)
        
    def rexSet(self):
        self.fade(self.rexmsg, 500)
        self.rexmsg.setText(self.words)
        self.unfade(self.rexmsg, 1000)
        self.b2.setEnabled(True)
        
        
    def openGraph1(self, event):
        sns.set()
        
        pressure = 'Pressure (' + self.x[5] + ')'
        
        sns.lmplot(x = pressure, y = 'Output (mV)', data = self.df)
    
        
#        mv = self.df['Output (mV)'].tolist()
        
#        plt.xlim(0,float(self.x[3])+float(self.x[3])/80)
#        plt.ylim(ymax = float(self.x[3])/3)
        
        if self.x[4] == 'NRC':
            tit = 'Pressure v. Output'
        else:
            tit = 'R-Cal'
        
        plt.title(tit)
#        plt.margins(.30,.30)
        
    def openGraph2(self, event):
        sns.set()
        
        pressure = 'Pressure (' + self.x[5] + ')'
            
        yaxis = '% mV/Pressure'
            
        sns.lmplot(x = pressure, y = yaxis, hue = 'Scale', data = self.df, fit_reg = False)
        
        
#        plt.xlim(0,float(self.x[3])+float(self.x[3])/80)
        plt.ylim(ymin=-.5, ymax = .5)
        plt.yticks(np.arange(-.5, .5+.5, .5))
        plt.title('Linearity')
        


#        process = Popen('trans_data/' + filename, shell=True)
        
        
#CLASS TO READ PANDAS DATAFRAME
class PandasModel(QAbstractTableModel): 
    def __init__(self, df = pd.DataFrame(), parent=None): 
        QAbstractTableModel.__init__(self, parent=parent)
        self._df = df

    def headerData(self, section, orientation, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError, ):
                return QVariant()
        elif orientation == Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError, ):
                return QVariant()

    def data(self, index, role=Qt.DisplayRole):
        if role != Qt.DisplayRole:
            return QVariant()

        if not index.isValid():
            return QVariant()

        return QVariant(str(self._df.ix[index.row(), index.column()]))

    def setData(self, index, value, role):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        self._df.set_value(row, col, value)
        return True

    def rowCount(self, parent=QModelIndex()): 
        return len(self._df.index)

    def columnCount(self, parent=QModelIndex()): 
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]
        self.layoutAboutToBeChanged.emit()
        self._df.sort_values(colname, ascending= order == Qt.AscendingOrder, inplace=True)
        self._df.reset_index(inplace=True, drop=True)
        self.layoutChanged.emit()






#_____________________________________________________________________________________________________________________#
#                                                    EXECUTE PROGRAM
#_____________________________________________________________________________________________________________________#






if __name__ == '__main__': 
     app = QCoreApplication.instance()
     if app is None:
         app = QApplication([])
    
     app_icon = QIcon()
     app_icon.addFile(logo)
     app.setWindowIcon(app_icon)
     db = QFontDatabase.addApplicationFont(fnt)
     s = Start() 
     s.show()
 
     try: 
         from IPython.lib.guisupport import start_event_loop_qt5 
         start_event_loop_qt5(app) 
     except ImportError: 
         
         app.exec_()
         
# END