import csv
def tim(x,name=None,soao=None):
    found=False
    with open(x,'r',encoding="utf-8") as f:
        reader = csv.reader(f)
        rows=list(reader)
        for row in rows[1:]:
            if row[0] == name or row[4] == soao:
                found = True
                break
        if found==True:
            if name!=None:
                print(f"{name} đã vào trong hang")
            else:
                print(f"ý chí số {soao} đã được Mân Đàn kế thừa")
        elif found==False:
            if name==None:
                print(f"chưa có mân đàn nào có số áo là {soao}")
            else:
                print(f"{name} khong co trong hang")
if __name__=='__main__':
    name=input("Nhập tên cần tìm: ")
    soao=input("nhap số áo cần tìm: ")
    print(name)
    print(soao)
    tim('Persion.csv',name,soao)