import csv
def xoa(x,n):
    with open(x, 'r',encoding="utf-8") as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        a=[]
        for firstcl in rows:
           a.append(firstcl['name'])
        if n not in a:
            print(f"{n} khong co trong hang")
        mainrow = reader.fieldnames
        newrow=[row for row in rows if row['name'] !=n]
    with open(x, 'w',newline='',encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=mainrow)
        writer.writeheader()
        writer.writerows(newrow)
if __name__ == '__main__':
    name=input("nhập tên: ")
    xoa('Persion.csv',name)