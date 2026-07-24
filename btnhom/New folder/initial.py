from them import them
from xem import xem
from xoa import xoa
from tim import tim
while True:
    print("""
    MU MUÔN NĂM SIUUUUUUUUUUUUUUUU
    1 : Thoát
    2 : Xem
    3 : Chỉnh sửa
    4 : Tìm kiếm
    5 :glory glory ManUnite :))""")
    choice=input("Nhập số mày chọn: ")
    if choice.isdigit() and 0<int(choice)<6:
        choice=int(choice)
        if choice==1:#thoats
            print("Chúc mừng bạn đã ra khỏi hang!!! vui lòng chọn đội khác :Đ")
            break
        if choice==2:#xem toan bo danh sach
            xem()
            continue
        elif choice==3:#chinh sua
            while True:
                print("""
                1 : Thêm
                2 : Xoá
                3 : Quay lại
                """)
                n=input("Nhập số mày chọn: ")
                if n.isdigit() and 0<int(n)<4:
                    if int(n)==3:
                        break
                    if int(n)==1:
                        them()
                        #vị trí in ra màn hình chữ in thành công
                        break
                    if int(n)==2:
                        n=input("nhập tên cần xoá:")
                        xoa("Persion.csv",n)
                        break
                else:
                    print("biết đọc không,chọn lại: ")
        elif choice==4:
            while True:
                print("""
                1: Tìm theo tên
                2:Tìm theo Số áo""")
                n=input("chọn phương thức nhập của bạn: ")
                if n.isdigit() and 0<int(n)<3:
                    if int(n)==1:
                        name=input("nhập tên cần tìm: ")
                        tim("Persion.csv",name,None)
                        break
                    if int(n)==2:
                        soao=input("nhập số áo cần tìm: ")
                        tim("Persion.csv",None,soao)
                        break
                    else :
                        print("nhập lại")
                        continue
        elif choice==5:
            pass
    else:
        print("biết chọn không")