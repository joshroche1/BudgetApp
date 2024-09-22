#!/usr/bin/python3

import bcrypt
import sqlite3
import sys

DB_CONN="db.sqlite"

def get_db():
  try:
    conn = sqlite3.connect(DB_CONN)
    return conn
  except sqlite3.Error as er:
    print(str(er))

def hash_passwd(password: str):
  bytestr = str.encode(password)
  passhash = bcrypt.hashpw(bytestr, bcrypt.gensalt())
  return passhash

def list_users():
  print("\n[User List]\n")
  db = get_db()
  cur = db.cursor()
  sqlcmd = "SELECT id,username,email FROM users;"
  userlist = cur.execute(sqlcmd)
  print("-----------------------")
  for user in userlist:
    print(user)
  db.close()
  print("-----------------------\n\n")

def add_user():
  try:
    print("\n[Add User]\n")
    username = input("Enter a username: ")
    email = input("Enter an email address: ")
    password = input("Enter a password: ")
    print("Username: "+username)
    print("Email:    "+email)
    confirm = input("Add this user [y/n]?")
    passhash = hash_passwd(password)
    db = get_db()
    cur = db.cursor()
    lastid = cur.execute("SELECT id FROM users ORDER BY id DESC LIMIT 1;")
    lastid += 1
    cur.execute("INSERT INTO users (id, username, email, password) VALUES (?, ?, ?, ?)", lastid, username, email, passhash)
    db.commit()
    print("User Added: "+username)
    db.close()
  except Exception as ex:
    print(str(ex))

def delete_user():
  print("\n[Delete User]\n")

def update_password():
  try:
    print("\n[Update Password]\n")
    list_users()
    userid = input("Enter a user ID: ")
    newpassword = input("Enter a new password: ")
    passhash = hash_passwd(newpassword)
    db = get_db()
    cur = db.cursor()
    sqlcmd = "UPDATE users SET password = ? WHERE id = ?;"
    cur.execute(sqlcmd, (passhash, userid))
    db.commit()
    print("Password Updated")
    db.close()
  except Exception as ex:
    print(str(ex))

def show_menu():
  print("\nUser Management Utility")
  print("=======================")
  print("[list]   - List users")
  print("[add]    - Add a user")
  print("[delete] - Delete a user")
  print("[update] - Update user password")
  print("[quit]   - Quit program")
  print("-----------------------")

def main():
  QUIT=0
  while QUIT < 1:
    show_menu()
    action = input("Enter a command: ")
    if action == "list": list_users()
    elif action == "add": add_user()
    elif action == "delete": delete_user()
    elif action == "update": update_password()
    elif action == "quit": QUIT = 1
  print("\nQUIT\n")
  sys.exit(0)

if __name__ == "__main__":
  main()