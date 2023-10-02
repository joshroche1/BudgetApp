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
def create_txaction(idval, datetimestamp, amount, category, currency, name, description, accountid, datetimeformat):
  db = get_db()
  error = None
  if error is not None:
    print(error)
  else:
    timestamp = parse_date(datetimestamp, datetimeformat)
    convertval = float(amount) * 0.93
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
print("CSV Format:\n[TIME|NAME|DESCRIPTION|CATEGORY|AMOUNT]\n")
filename = input("> ")
print("\nEnter currency [EUR]/[USD]\n")
currency = input("> ")
print("\nEnter date time format:\n[Y-m-d]\n[Y/m/d]\n[Y.m.d]\n[d.m.y]\n")
datetimeformat = input("> ")
accountid = input("Account ID > ")

if filename.find("Q") > -1:
  print("\nEXIT")
  sys.exit(0)
elif filename.find("q") > -1:
  print("\nEXIT")
  sys.exit(0)
elif len(filename) > 0:
  intid = 4000
  print("\Import File: " + filename + "\n")
  csvfile = open('upload/'+filename, 'r')
  for csvline in csvfile:
    tmparr = csvline.split(',')
    txdtime = tmparr[0]
    txcat = tmparr[3]
    txname = tmparr[1]
    txdesc = tmparr[2]
    txamt = tmparr[4]
    # idval, datetimestamp, amount, category, currency, name, description, accountid
    if not create_txaction(intid, txdtime, txamt, txcat, currency, txdesc, txname, accountid, datetimeformat):
      print("Could not insert transaction")
    else:
      print("Insert transaction: " + str(intid))
    intid += 1
  print("\nDONE")
else:
  print("\nEXIT")
  sys.exit(0)
