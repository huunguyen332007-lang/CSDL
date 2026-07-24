import csv
def them():
    name=input('Enter your name: ')
    age=input('Enter your age: ')
    nationality=input('Enter your nation: ')
    vitri=input('Enter your vitri: ')
    number=input('Enter your soao: ')
    with open("Persion.csv","a",newline='', encoding='utf-8') as f: #newline ko chen them dong null vao nua
        f=csv.DictWriter(f,fieldnames=["ten","tuoi","quoctich","vitri","soao"])
        f.writerow({"ten":name,"tuoi":age,"quoctich":nationality,"vitri":vitri,"soao":number})
        print(f"Đã thêm thành công {name} vào hang chơi cho MU ở vị trí {vitri} với số áo {number}")
if __name__=='__main__':
    them()
