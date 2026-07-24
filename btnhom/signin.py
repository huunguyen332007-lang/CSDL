import sys
from thuviengv import thuviengv
from thuvienhs import thuvienhs
from gvsign import gvmosign
from hssign import hsmosign
from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton
from PyQt6.QtGui import QPixmap

def checkclick():
    return True
class mainwindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setGeometry(400, 150,800,600)
        self.setWindowTitle("Sign-In LIBRARY")
        self.destop=QLabel(self)
        self.destop.resize(800,600)
        manhhinh = QPixmap("1.png")
        self.destop.setPixmap(manhhinh)
        self.destop.setScaledContents(True)
        self.nengv=QLabel(self)
        self.nenhs=QLabel(self)
        self.gv=QLabel("SIGN IN AS \nMANAGER",self)
        self.gv.setStyleSheet("font-size:20px;font-family:Goudy Stout;color:rgb(142,106,93)")
        self.gv.setGeometry(235,160,200,200)
        self.gv.setFixedWidth(400)
        self.hs=QLabel("SIGN IN AS \nEDUCATOR",self)
        self.hs.setGeometry(235,265,200,200)
        self.hs.setStyleSheet('font-size:20px;font-family:Goudy Stout;color:rgb(142,106,93)')
        self.hs.setFixedWidth(400)
        self.gvbutton=QPushButton("SIGN_IN",self)
        self.hsbutton=QPushButton("SIGN_IN",self)
        self.gvbutton.setGeometry(475,235,100,50)
        self.hsbutton.setGeometry(475,340,100,50)
        self.gvbutton.setStyleSheet("color: black; padding: 10px 20px;font-family:Pacifico;color:blue")
        self.hsbutton.setStyleSheet("color: black; padding: 10px 20px;font-family:Pacifico;color:blue")
        self.nengv.setGeometry(205,210,400,100)
        self.nengv.setStyleSheet("background-color: white")
        self.nenhs.setGeometry(205,310,400,100)
        self.nenhs.setStyleSheet("background-color: white")
        self.chaomung=QLabel(" WELCOME MYSLIBRARY\n                  LOGIN",self)
        self.chaomung.setStyleSheet("font-size:30px;font-family:Stencil;color:black")
        self.chaomung.setFixedWidth(500)
        self.chaomung.setFixedHeight(50)
        self.chaomung.move(210,145)
        if self.gvbutton.clicked.connect(checkclick):
            self.gvbutton.clicked.connect(lambda: css(self.gv,self.nengv,self.linegv))
            self.gvbutton.clicked.connect(self.gvmosign)
        if self.hsbutton.clicked.connect(checkclick):
            self.hsbutton.clicked.connect(lambda: css(self.hs,self.nenhs,self.linehs))
            self.hsbutton.clicked.connect(self.hsopensign)
        self.linegv=QLabel(self)
        self.linegv.setGeometry(450,280,15,0)
        self.linegv.setStyleSheet("background-color: white;border-radius:15%")
        self.linehs=QLabel(self)
        self.linehs.setGeometry(450,385,15,0)
        self.linehs.setStyleSheet("background-color: white;border-radius:15%")

        self.hswidget = None
        self.hsui = None
        self.gvwidget=None
        self.gvui = None

    def hsopensign(self):
        # Lấy cả Widget và UI object từ hàm hsmosign
        self.hswidget, self.hsui = hsmosign()
        # link signal (khi cửa sổ thực sự được tạo)
        self.hsui.dauhieu.connect(self.xulydulieuhs)

    def gvmosign(self):

        self.gvwidget, self.gvui = gvmosign()

        self.gvui.dauhieu2.connect(self.xulydulieugv)

    def xulydulieugv(self):
        print("xuly dữ liệu")
        def thuvien():
            self.gvwidget.close()
            self.mothuviengv = thuviengv()
            self.mothuviengv.show()
        QTimer.singleShot(700, thuvien)

    def xulydulieuhs(self):
        print("xuly dữ liệu")
        def thuvien():
            self.hswidget.close()
            self.mothuvienhs = thuvienhs()
            self.mothuvienhs.show()
        QTimer.singleShot(700, thuvien)

    def mousePressEvent(self,event):
        x=event.position()
        y=event.position()
        print(x,y)

def css(x,a,z):
    a.setStyleSheet("background-color:rgb(230, 230, 250);border-radius:15%;")
    x.setStyleSheet("font-size:20px;font-family:Goudy Stout;color:rgb(0, 0, 128)")
    if z.pos().y()==280:
        z.move(z.pos().x(),210)
    elif z.pos().y()==385:
        z.move(z.pos().x(),310)
    z.setFixedHeight(100)


    def doilai():
        a.setStyleSheet("background-color: white")
        x.setStyleSheet("font-size:20px;font-family:Goudy Stout;color:rgb(142,106,93)")
        z.setFixedHeight(0)
    QTimer.singleShot(200, doilai)



app=QApplication(sys.argv)
window=mainwindow()
window.show()
app.exec()

