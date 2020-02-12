import socket
import threading
import logging
import csv

code = ""
desc = "banan"
amount = input("Amount:")
header = ["Code", "Description", "Amount"]
r = csv.reader(open('test.csv', 'a+' ),delimiter=";")

valueChange = input("valuechange")
changeVal = "{}{}".format("code:", valueChange)
print(changeVal)
class StockItem:
    def __init__(self, code, desc, amount):
        self.code = code
        self.desc = desc
        self.amount = amount

    def write_item(self):
        in_list = [self.code, self.desc, self.amount]
        with open('stock.csv', 'a', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow(in_list)

    def show_item(self):
        with open('stock.csv', 'r', newline='') as csv_file:
            for row in csv_file.readlines():
                if (self.code or self.amount or self.desc) in row:
                    print(row)

    def update_item(self):
        with open('stock.csv', 'a+', newline='') as csv_file:
            for row in csv_file:
                print(row)
        text = open("stock.csv", 'r')
        text = "".join([i for i in text]).replace(self.amount, changeVal)
        p = open('stock.csv', 'w')
        p.writelines(text)

class StockTracker(StockItem):
    def __init__(self, code, desc, amount):
        super().__init__(code, desc, amount)
        self.amount = amount



a = StockItem(code, desc, amount)
#a.write_item()
#a.show_item()
a.update_item()