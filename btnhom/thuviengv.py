import mysql.connector
from PyQt6.QtWidgets import QWidget, QTableWidget, QTableWidgetItem, QLineEdit, QTabWidget, QLabel, QPushButton


class thuviengv(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        super().__init__()
        self.setGeometry(150, 70, 1200, 700)
        self.setWindowTitle("thuviengv")
        self.banggv=QTabWidget(self)
        self.banggv.setGeometry(0, 0, 1200, 650)

        #Bảng qlysach
        self.qlysach=QTableWidget(self)
        self.qlysach.setGeometry(430, 180, 256, 192)
        self.qlysach.setColumnCount(5)
        self.qlysach.setHorizontalHeaderLabels(["ID sách", "Tên sách", "Tác giả","NXB","Link mượn"])
        self.qlysach.setColumnWidth(0,50)
        self.qlysach.setColumnWidth(1,400)
        self.qlysach.setColumnWidth(2,180)
        self.qlysach.setColumnWidth(3,180)
        self.qlysach.setColumnWidth(4,380)

        self.qlymuon=QTableWidget(self)
        self.qlymuon.setGeometry(430, 180, 256, 192)
        self.qlymuon.setColumnCount(3)
        self.qlymuon.setHorizontalHeaderLabels(["Mã SV", "Tên SV", "Số lần đăng nhập"])
        self.qlymuon.setColumnWidth(0,500)
        self.qlymuon.setColumnWidth(1,500)
        self.qlymuon.setColumnWidth(2,200)

        self.banggv.addTab(self.qlysach, "MANAGER")
        self.banggv.addTab(self.qlymuon, "MUON")

        self.qlysach.setRowCount(len(data1))
        self.qlymuon.setRowCount(len(data2))
        # khai bao ham va du lieu
        self.data1 = data1
        self.data2 = data2
        self.themvaobang()

        self.them=QLabel("Thêm:",self)
        self.xoa=QLabel("Xoá:",self)
        self.xoa.setGeometry(5,675,40,25)
        self.them.setGeometry(5,650,45,25)
        self.xoa.setStyleSheet("background-color: rgb(173, 216, 230)")
        self.them.setStyleSheet("background-color: gray")
        self.xoaid=QLabel("Nhập ID",self)
        self.xoaid.setGeometry(45,675,90,25)
        self.xoaidsach=QLineEdit(self)
        self.xoaidsach.setGeometry(135,675,900-135,25)
        self.xoaid.setStyleSheet("background-color: rgb(255, 218, 185)")
        self.themid=QLabel("ID",self)
        self.themsach=QLabel("Tên",self)
        self.themtg=QLabel("Tác Giả",self)
        self.themnxb=QLabel("NXB",self)
        self.themid.setStyleSheet("background-color: white")
        self.themsach.setStyleSheet("background-color: white")
        self.themtg.setStyleSheet("background-color: white")
        self.themnxb.setStyleSheet("background-color: white")


        self.themsach.setGeometry(115,650,20,25)
        self.themid.setGeometry(45,650,20,25)
        self.themtg.setGeometry(535,650,40,25)
        self.themnxb.setGeometry(725,650,25,25)
        self.themidtext=QLineEdit(self)
        self.themidtext.setGeometry(65,650,50,25)
        self.themsachtext=QLineEdit(self)
        self.themsachtext.setGeometry(135,650,400,25)
        self.themtgtext=QLineEdit(self)
        self.themtgtext.setGeometry(575,650,150,25)
        self.themnxbtext=QLineEdit(self)
        self.themnxbtext.setGeometry(750,650,150,25)
        self.nutthem=QPushButton("Thêm",self)
        self.nutthem.setGeometry(900,650,40,25)
        self.nutxoa=QPushButton("Xoá",self)
        self.nutxoa.setGeometry(900,675,40,25)
        self.nutxoa.clicked.connect(self.deleterow)
        self.nutthem.clicked.connect(self.insertrow)

    #Thêm vao bảng sahcs  #Thêm vào bảng qlyhs
    def themvaobang(self):
        for idexhang, hang in enumerate(data1):
            for idexcot, cot in enumerate(hang):
                dulieu = QTableWidgetItem(str(cot))
                self.qlysach.setItem(idexhang, idexcot, dulieu)
        for idexhang, hang in enumerate(data2):
            for idexcot, cot in enumerate(hang):
                dulieu = QTableWidgetItem(str(cot))
                self.qlymuon.setItem(idexhang, idexcot, dulieu)


    def deleterow(self):
        self.dt=mysql.connector.connect(host="localhost",user="root",passwd="332007",database="thuvienhs")
        self.mycursor=self.dt.cursor()
        self.mycursor.execute("SELECT id FROM thuvienhs")
        b=self.mycursor.fetchall()
        if (self.xoaidsach.text(),) in b:
            self.mycursor.execute("DELETE FROM thuvienhs WHERE id = %s",(self.xoaidsach.text(),))
            self.dt.commit()
            for i in range(len(b)):
                if (self.xoaidsach.text(),) == b[i]:
                    self.qlysach.removeRow(i)
                    break
        self.dt.close()
    def insertrow(self):
        self.dt = mysql.connector.connect(host="localhost", user="root", passwd="332007", database="thuvienhs")
        self.mycursor = self.dt.cursor()
        if self.themidtext.text() and self.themsachtext.text() and self.themtgtext.text() and self.themnxbtext.text():
            self.mycursor.execute("INSERT INTO thuvienhs(id,tensach,tacgia,NXB) VALUES (%s,%s,%s,%s)",(self.themidtext.text(), self.themsachtext.text(), self.themtgtext.text(),self.themnxbtext.text()))
            self.dt.commit()
            a=self.qlysach.rowCount()
            self.qlysach.insertRow(a)
            self.qlysach.setItem(a,0,QTableWidgetItem(self.themidtext.text()))
            self.qlysach.setItem(a,1,QTableWidgetItem(self.themsachtext.text()))
            self.qlysach.setItem(a,2,QTableWidgetItem(self.themtgtext.text()))
            self.qlysach.setItem(a,3,QTableWidgetItem(self.themnxbtext.text()))
            self.qlysach.setItem(a,4,QTableWidgetItem("Chưa có"))


    def mousePressEvent(self, event):
        x = event.position()
        y = event.position()
        print(x, y)



#link mysql
db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="332007",
    database="thuvienhs"
)
cursor1=db.cursor()
cursor1.execute("SELECT * FROM thuvienhs")
data1=cursor1.fetchall()

cursor2=db.cursor()
cursor2.execute("SELECT * FROM qlyhs")
data2=cursor2.fetchall()
cursor1.close()
cursor2.close()







