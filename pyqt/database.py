import sqlite3

DB_CONN = "db.sqlite"

def get_db():
  conn = None
  try:
    conn = sqlite3.connect(DB_CONN)
  except sqlite3.Error as ex:
    print(str(ex))
  return conn

### USERS ###
def get_users():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, username, email FROM users ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    results = res.fetchall()
    db.close()
  except Exception as ex:
    print(str(ex))
  return results

### WEBLISTS ###
def get_weblists():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, name, value FROM weblists ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    results = res.fetchall()
    db.close()
  except Exception as ex:
    print(str(ex))
  return results

### BUDGETS ###
def get_budgets():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, name, description, currency, ownerid FROM budgets ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    rows = res.fetchall()
    db.close()
    for itemrow in rows:
      tmprow = []
      for item in itemrow:
        tmpvalue = str(item)
        tmprow.append(tmpvalue)
      results.append(tmprow)
  except Exception as ex:
    print(str(ex))
  return results

### BUDGETITEMS ###
def get_budgetitems():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, name, description, amount, category, recurrence, duedate, budgetid FROM budgetitems ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    rows = res.fetchall()
    db.close()
    for itemrow in rows:
      tmprow = []
      for item in itemrow:
        tmpvalue = str(item)
        tmprow.append(tmpvalue)
      results.append(tmprow)
  except Exception as ex:
    print(str(ex))
  return results

### ACCOUNTS ###
def get_accounts():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, name, description, accounttype, currency, ownerid FROM accounts ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    rows = res.fetchall()
    db.close()
    for itemrow in rows:
      tmprow = []
      for item in itemrow:
        tmpvalue = str(item)
        tmprow.append(tmpvalue)
      results.append(tmprow)
  except Exception as ex:
    print(str(ex))
  return results

### TRANSACTIONS ###
def get_transactions():
  results = []
  try:
    db = get_db()
    cur = db.cursor()
    sqlstmt = "SELECT id, datetimestamp, amount, convertedvalue, category, currency, name, description, accountid FROM transactions ORDER BY id ASC"
    res = cur.execute(sqlstmt)
    rows = res.fetchall()
    db.close()
    for itemrow in rows:
      tmprow = []
      for item in itemrow:
        tmpvalue = str(item)
        tmprow.append(tmpvalue)
      results.append(tmprow)
  except Exception as ex:
    print(str(ex))
  return results

