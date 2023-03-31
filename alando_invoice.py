import pdfplumber
import pandas as pd
import os
import pymysql
import pandas as pd


def connect_mysql(host, user, password, database):
    # 打开数据库连接
    db = pymysql.connect(host=host,
                         user=user,
                         password=password,
                         database=database)
    return db

def insert_invoice_info(db, INVOICE, PAGE, Description, Reference, Quantity, Price, Amount):
    cursor = db.cursor()
    # SQL 插入语句
    sql = "INSERT INTO `alando发票`.`alando_invoice`(`INVOICE`, `PAGE`, `Description`, `Reference`, `Quantity`, " \
          "`Price`, `Amount`)" \
          "VALUES('%s','%s','%s','%s','%s','%s','%s')" % (
              INVOICE, PAGE, Description, Reference, Quantity, Price, Amount)
    cursor.execute(sql)
    db.commit()

host, user, password, database = ('localhost', 'yuan', '123456', 'alando发票')
db = connect_mysql(host, user, password, database)


def get_invoice_info(file,invoice_location):
    INVOICE = file.replace(".pdf","")
    with pdfplumber.open(invoice_location) as pdf:
        for page in pdf.pages:
            PAGE = len(pdf.pages)
            print("PAGE...............")
            contenu = page.extract_text()
            contenu = contenu.split("\n")
            a = 0
            for line in contenu:
                a = a + 1
                if "Description" in line:
                    start_line = a
                if "VAT amount Exempt" in line or "See next page" in line or "Exempt of VAT Ar" in line:
                    end_line = a - 1
                    print(end_line)
            for x in range(start_line, end_line):
                text_line = contenu[x].replace(". ", "")
                text_line_split = contenu[x].split(" ")
                if "DUTY" in text_line_split:
                    Description = text_line_split[1]
                    Reference = text_line_split[2]
                    Quantity = text_line_split[3]
                    try:
                        Price = text_line_split[4]
                        Amount = text_line_split[5]
                    except:
                        Amount = ""
                        Price = ""
                else:

                    try:
                        Amount = str(text_line_split[-1])
                        Price = text_line_split[-2]
                        Quantity = text_line_split[-3]
                        Reference = text_line_split[-4]
                        Description = text_line.replace(Amount, "") \
                            .replace(Price, "") \
                            .replace(Quantity, "") \
                            .replace(Reference, "") \
                            .replace("  ", "").replace(". ", "")
                    except:
                        Amount = ""
                        Price = ""
                        Quantity = ""
                        Reference = ""
                        Description = text_line
                insert_invoice_info(db,INVOICE, PAGE, Description, Reference, Quantity, Price, Amount)



doc_invoice_alando = "C:/Users/fuqin/Desktop/Alando 发票/"
files = os.listdir(doc_invoice_alando)
for file in files:
    invoice_location = doc_invoice_alando + file
    print(invoice_location)
    get_invoice_info(file,invoice_location)
