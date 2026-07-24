import csv
def xem():
    with open("Persion.csv","r", encoding='utf-8') as f:
        read=csv.DictReader(f)
        for row in read:
            print(f"Tên:{row["name"]} \t Tuổi:{row["age"]}\t Quốc tịch:{row["nationality"]}\t Vitri:{row["vitri"]}\t Số áo:{row["number"]}")
if __name__=='__main__':
    xem()