#!/usr/bin/python3
import functools
import sys
import bcrypt
import sqlite3
from datetime import datetime


def get_db():
  try:
    conn = sqlite3.connect('db.sqlite')
    return conn
  except sqlite3.Error as er:
    print(str(er))

def parse_date(datetimestamp: str, dateformat: str):
  result = ""
  currentdate = datetime.now().strftime('%Y-%m-%d')
  try:
    if dateformat == "Y-m-d":
      tmp1 = datetimestamp.split('-')
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "Y/m/d":
      tmp1 = datetimestamp.split("/")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "Y.m.d":
      tmp1 = datetimestamp.split(".")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = str(tmp1[0]) + "-" + str(tmp1[1]) + "-" + str(tmp1[2])
    elif dateformat == "d.m.y":
      tmp1 = datetimestamp.split(".")
      if len(tmp1) != 3: return "Wrong length"
      if not tmp1[0].isdecimal(): return "1 not decimal"
      if not tmp1[1].isdecimal(): return "2 not decimal"
      if not tmp1[2].isdecimal(): return "3 not decimal"
      result = "20" + str(tmp1[2]) + "-" + str(tmp1[1]) + "-" + str(tmp1[0])
    else:
      return currentdate
  except Exception as ex:
    print(str(ex))
    result = currentdate
  return result

### id | datetimestamp | amount | convertedvalue | category | currency |   name   | description | accountid
def create_txaction(idval, datetimestamp, datetimeformat, amount, category, currency, name, description, accountid, convertvalue):
  db = get_db()
  error = None
  if error is not None:
    print(error)
  else:
    timestamp = parse_date(datetimestamp, datetimeformat)
    convertval = float(amount) * float(convertvalue)
    convertedval = float("{:.2f}".format(convertval))
    try:
      sqlcmd = "INSERT INTO transactions (id,datetimestamp,amount,convertedvalue,category,currency,description,name,accountid) values ('"
      sqlvals = str(idval) + "','" + timestamp + "','" + str(amount) + "','" + str(convertedval) + "','" + category + "','" + currency + "','" + name + "','" + description + "','" + str(accountid) + "');"
      sqlcmd += sqlvals
      print(sqlcmd)
      db.execute(sqlcmd)
      db.commit()
      db.close()
    except sqlite3.Error as er:
      print(str(er))
      return False
    return True
  return False


print("Import CSV into SQLite3 db\n\nPlease Enter Filename\n\n[Q/q] QUIT\n")
filename = input("> ")
newcurrency = input("Currency [USD/EUR]> ")
print("Date/Time Format\n Y-m-d\n d.m.y\n")
dtformat = input("> ")
accountid = input("Account ID> ")
convertvalue = input("Conversion Rate [USD->EUR=0.93]> ")
coldtime = input("Column [Date/Time]> ")
colcat = input("Column [Category]>")
colname = input("Column [Name]>")
coldesc = input("Column [Description]>")
colamt = input("Column [Amount]>")

if filename.find("Q") > -1:
  print("\nEXIT")
  sys.exit(0)
elif filename.find("q") > -1:
  print("\nEXIT")
  sys.exit(0)
elif len(filename) > 0:
  intid = int(accountid) * 10000
  print("\Import File: " + filename + "\n")
  csvfile = open('upload/'+filename, 'r')
  for csvline in csvfile:
    tmparr = csvline.split(',')
    txdtime = tmparr[int(coldtime)]
    txcat = tmparr[int(colcat)]
    txname = tmparr[int(colname)]
    txdesc = tmparr[int(coldesc)]
    txamt = tmparr[int(colamt)]
    # idval, datetimestamp, amount, category, currency, name, description, accountid
    if not create_txaction(intid, txdtime, dtformat, txamt, txcat, newcurrency, txdesc, txname, accountid, convertvalue):
      print("Could not insert transaction")
    else:
      print("Insert transaction: " + str(intid))
    intid += 1
  print("\nDONE")
else:
  print("\nEXIT")
  sys.exit(0)
