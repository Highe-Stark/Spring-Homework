import datetime
import time
import threading


def scanf(record, *args):
    templist = record.split("\t")
    dic = dict()
    for i in args:
        for j in templist:
            if j.find(i) != -1:
                temp_index = j.find(":")
                key = j[temp_index+1:]
                break
        dic[i] = key
    return dic


class Order:
    def __init__(self, buyer_id="", good_id="", amount=0, price=0, done=True):
        self.buyer_id = buyer_id
        self.good_id = good_id
        self.amount = amount
        self.price = price
        self.done = done


class Buyer:
    def __init__(self, buyer_name=""):
        self.buyer_name = buyer_name
        self.order_list = []


class Good:
    def __init__(self, good_name="", price=0):
        self.good_name = good_name
        self.price = price
        self.order_list = []


class alibaba:
    def __init__(self):
        self.order = dict()
        self.buyer = dict()
        self.good = dict()

    def addorder(self, record):
        temp = scanf(record, "orderid", "buyerid", "goodid", "amount", "price", "done")
        if temp["done"] == "true":
            temp["done"] = True
        else:
            temp["done"] = False
        temp["amount"] = eval(temp["amount"])
        temp["price"] = eval(temp["price"])
        self.order[temp["orderid"]] = Order(temp["buyerid"], temp["goodid"], temp["amount"], temp["price"], temp["done"])
        self.buyer[temp["buyerid"]].order_list.append(temp["orderid"])
        self.good[temp["goodid"]].order_list.append(temp["orderid"])

    def addbuyer(self, record):
        temp = scanf(record, "buyerid", "buyername")
        self.buyer[temp["buyerid"]] = Buyer(temp["buyername"])

    def addgood(self, record):
        temp = scanf(record, "goodid", "good_name", "price")
        temp["price"] = eval(temp["price"])
        self.good[temp["goodid"]] = Good(temp["good_name"], temp["price"])

    def query(self, sign, iden):
        if sign == "o":
            try:
                print "Order id:", iden, "\tBuyer:" + self.buyer[self.order[iden].buyer_id].buyer_name, \
                    "\tGood:" + self.good[self.order[iden].good_id].good_name,\
                    "\tAmount:", self.order[iden].amount, "\tPrice:", self.order[iden].price,\
                    "\tAmount * Price:", self.order[iden].amount * self.order[iden].price
            except:
                print "Not Found"
        elif sign == "b":
            try:
                sum = 0
                for i in self.buyer[iden].order_list:
                    if self.order[i].done == True:
                        sum += self.order[i].price * self.order[i].amount
                print "Buyer id:", iden, "\tBuyer:" + self.buyer[iden].buyer_name, "\tTotal Number of Orders:", \
                len(self.buyer[iden].order_list), "\tTotal amount of payment:"+str(sum)
            except:
                print "Not Found"
        elif sign == "g":
            try:
                count_order = len(self.good[iden].order_list)
                count_saled = 0
                for i in self.good[iden].order_list:
                    if self.order[i].done == True:
                        count_saled += 1
                print "Good id:", iden, "\tGood name:", self.good[iden].good_name, "\tTotal number of orders:", \
                    count_order, "\tTotal number of saled:", count_saled
            except:
                print "Not Found"
        else:
            print "Invalid Input"


def op(file, flag):
    global ali
    fp = open("data\\" + file, "r")
    fr = fp.readline()
    while fr != "":
        if flag == 0 or flag == 1:
            ali.addbuyer(fr)
        elif flag >= 2 and flag <= 4:
            ali.addgood(fr)
        fr = fp.readline()
    fp.close()


def opo(file):
    global ali
    fp = open("data\\" + file, "r")
    fr = fp.readline()
    while fr != "":
        ali.addorder(fr)
        fr = fp.readline()
    fp.close()



time_start = datetime.datetime.now()
print "Loading..."
ali = alibaba()
thr = []
file_list = ["buyer.0.0", "buyer.1.1", "good.0.0", "good.1.1", "good.2.2"]
for t_i in xrange(5):
    sthread = threading.Thread(target=op, args=(file_list[t_i], t_i))
    sthread.setDaemon(True)
    sthread.start()
    thr.append(sthread)
for t_j in xrange(5):
    thr[t_j].join()
thr = []
file_list = ["order.0.0", "order.0.3", "order.1.1", "order.2.2"]
for t_i in xrange(4):
    sthread = threading.Thread(target=opo, args=(file_list[t_i],))
    sthread.setDaemon(True)
    sthread.start()
    thr.append(sthread)
for t_j in xrange(4):
    thr[t_j].join()
time_end = datetime.datetime.now()
delta_time = time_end - time_start
print "Number of total orders:", len(ali.order)
print delta_time, "s"
while True:
    req = raw_input("Need Query? (Y/N) ")
    if req == "N" or req == "n":
        break
    signa = raw_input("Search \"order id\" or \"buyer id\" or \"good id\", type \"o\" or \"b\" or \"g\" to continue\n")
    q_id = raw_input("id:")
    q_start = datetime.datetime.now()
    ali.query(signa, q_id)
    q_end = datetime.datetime.now()
    print "query completed in", q_end - q_start
