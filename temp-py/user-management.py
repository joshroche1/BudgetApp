#!/usr/bin/python3
import functools
import sys
import bcrypt
import sqlite3


def get_db():
  try:
    conn = sqlite3.connect('db.sqlite')
    return conn
  except sqlite3.Error as er:
    print(str(er))

def hash_password(password: str):
  bytestr = str.encode(password)
  passhash = bcrypt.hashpw(bytestr, bcrypt.gensalt())
  return passhash 

def password_complexity_check(password):
  return True
#  specialchars = ["!","@","#","$","%","^","&","*","(",")"]
#  specialcharsfound = False
#  tmppwd = password
#  if len(tmppwd) <= 9:
#    return False
#  for x in specialchars:
#    if tmppwd.find(x) > 0:
#      specialcharsfound = True
#      tmppwd = tmppwd.replace(x,"")
#  if specialcharsfound == False:
#    return False
#  elif len(tmppwd) < 4:
#    return False
#  elif tmppwd.isalnum() == False:
#    return False
#  else:
#    return True
#  return False

def create_user(email, username, password):
  db = get_db()
  error = None
  if not email:
    email = ""
  if not username:
    error = "Username is required"
  if not password:
    error = "Password is required"
  if not password_complexity_check(password):
    error = "Password must be at least 9 characters in length and contain alphanumeric characters and at least 1 of the following symbols: !@#$%^&*()"
  if error is not None:
    print(error)
  else:
    passhash = hash_password(password)
    try:
      sql = "INSERT INTO users (email,username,password) values ('" + email + "','" + username + "',?);"
      db.execute(sql, (passhash,))
      db.commit()
      db.close()
    except sqlite3.Error as er:
      print(str(er))
      return False
    return True
  return False

def update_password(user_id,password):
  db = get_db()
  error = None
  if not user_id: error = "User ID required"
  if not password: error = "New Password required"
  if not password_complexity_check(password):
    error = "Password must be at least 9 characters in length and contain alphanumeric characters and at least 1 of the following symbols: !@#$%^&*()"
  try:
    sql = "SELECT * FROM users WHERE id = ?;"
    user = db.execute(sql, (user_id))
  except sqlite3.Error as er:
    error = str(er)
  if user is None:
    error = "User not found"
  if error is not None:
    print(error)
    return False
  else:
    passhash = hash_password(password)
    try:
      passhash = hash_password(password)
      sql = "UPDATE users set password = ? WHERE id = ?;"
      db.execute(sql, (passhash,user_id))
      db.commit()
      db.close()
    except sqlite3.Error as er:
      print(str(er))
      return False
    return True
  return False

def get_users():
  db = get_db()
  sql = "SELECT * FROM users;"
  users = db.execute(sql)
  print("ID   EMAIL   USERNAME\n=====================\n")
  for user in users:
    msg = "" + str(user[0]) + "   " + user[1] + "   " + user[2] + "   " + str(user[3])
    print(msg)

def get_user(user_id):
  db = get_db()
  sql = "SELECT * FROM users WHERE id = " + user_id + ";"
  users = db.execute(sql)
  print("ID   EMAIL   USERNAME\n=====================\n")
  for user in users:
    msg = "" + str(user[0]) + "   " + user[1] + "   " + user[2] + "   " + str(user[3])
    print(msg)

def delete_user(user_id):
  db = get_db()
  try:
    sql = "DELETE FROM users WHERE id = " + user_id + ";"
    db.execute(sql)
    db.commit()
    db.close()
  except sqlite3.Error as er:
    print(str(er))
    return False
  return True


print("Scam Fighters Ban Utility - User Management Tool\n[1] Add User\n[2] List Users\n[3] Update User Password\n[4] Delete User\n[5/q] QUIT\n")
command1 = input("> ")

if command1.find("5") > -1:
  print("\nEXIT")
  sys.exit(0)
elif command1.find("1") > -1:
  print("\nAdd User\n")
  email = input("Enter an email: ")
  username = input("Enter a username: ")
  password = input("Enter a password: ")
  result = create_user(email,username,password)
  if result is False:
    print("Could not create user")
    sys.exit(1)
  else:
    print("Successfully created user: " + username)
    sys.exit(0)
elif command1.find("2") > -1:
  print("\nList Users\n")
  get_users()
  print("EXIT")
  sys.exit(0)
elif command1.find("3") > -1:
  print("\nUpdate User Password\n")
  get_users()
  user_id = input("Enter the ID of the user to update their password: ")
  password = input("Enter the new password: ")
  get_user(user_id)
  result = update_password(user_id,password)
  if result is False:
    print("Could not update user password")
    sys.exit(1)
  else:
    print("Successfully updated user password")
  sys.exit(0)
elif command1.find("4") > -1:
  print("\nDelete User\n")
  get_users()
  print("Enter the ID of the user to delete")
  user_id = input("> ")
  result = delete_user(user_id)
  if result is False:
    print("Could not delete user")
    sys.exit(0)
  else:
    print("Successfully deleted user")
    sys.exit(0)
elif command1.find("q") > -1:
  print("\nEXIT")
  sys.exit(0)
else:
  print("\nEXIT")
  sys.exit(0)
