import mysql.connector
from PyQt6.QtWidgets import QWidget,QTableWidget,QTableWidgetItem
class thuvienhs(QWidget):
    def __init__(self):
        super().__init__()
        self.setMouseTracking(True)
        self.setWindowTitle("thuvienhs")
        self.setGeometry(150, 75, 1200, 700)
        self.bang=QTableWidget(self)
        self.bang.setGeometry(0, 50, 1200, 650)
        self.bang.setColumnCount(5)
        self.bang.setHorizontalHeaderLabels(["ID sách", "Tên sách", "Tác giả","NXB","Link mượn"])
        self.bang.setColumnWidth(0,50)
        self.bang.setColumnWidth(1,400)
        self.bang.setColumnWidth(2,180)
        self.bang.setColumnWidth(3,180)
        self.bang.setColumnWidth(4,380)
        self.bang.setRowCount(len(data))
        #khai bao ham va du lieu
        self.data=data
        self.themvaobang()

    def themvaobang(self):
        for idexhang, hang in enumerate(data):
            for idexcot, cot in enumerate(hang):
                dulieu=QTableWidgetItem(str(cot))
                self.bang.setItem(idexhang,idexcot,dulieu)
    def mousePressEvent(self,event):
        x=event.position()
        y=event.position()
        print(x,y)





#link mysql
db=mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="332007",
    database="thuvienhs"
)
cursor=db.cursor()
cursor.execute("SELECT * FROM thuvienhs")
data=cursor.fetchall()
