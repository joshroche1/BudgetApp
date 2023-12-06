import os
from datetime import datetime

from .config import Settings, workingdir


settings = Settings()


def read_file(filepath: str):
  fpath = workingdir + filepath
  readfile = open(fpath, "r")
  result = readfile.read()
  readfile.close()
  return result


def write_file(filepath: str, contents: str):
  try:
    file = open(filepath, "w")
    file.write(contents)
    file.close()
  except Exception as ex:
    print(str(ex))
    return str(ex)
  return filepath

def append_line(filepath: str, linestr: str):
  try:
    file = open(filepath, "a")
    file.write(linestr)
    file.close()
  except Exception as ex:
    print(str(ex))
    return str(ex)
  return filepath

def insert_line(filepath: str, linestr: str):
  #
  return 0

def delete_line(filepath: str, linestr: str):
  try:
    tmpfile = ""
    file = open(filepath, "r")
    filelines = file.readlines()
    for fline in filelines:
      if fline.find(linestr) < 0:
        tmpfile = tmpfile + fline
    file.close()
    writefile = open(filepath, "w")
    writefile.write(tmpfile)
    writefile.close()
  except Exception as ex:
    print(str(ex))
    return str(ex)
  return 0

def upload_file(filename: str, filecontents: str):
  result = ""
  try:
    print(filename)
    filepath = workingdir + settings.upload_dir + "/" + filename
    print(filepath)
    file = open(filepath, "w")
    file.write(filecontents)
    file.close()
    result = "File uploaded successfully: " + filename
  except Exception as ex:
    result = str(ex)
  print(result)
  return result

def get_uploaded_files():
  resultlist = []
  try:
    uploadpath = workingdir + settings.upload_dir
    resultlist = os.listdir(uploadpath)
  except Exception as ex:
    resultlist.append(str(ex))
  return resultlist

def delete_file(filename):
  result = ""
  try:
    filepath = workingdir + "/" + filename
    if os.path.exists(filepath):
      os.remove(filepath)
      result = "File removed: " + filename
    else:
      result = "File not found"
  except Exception as ex:
    result = str(ex)
  return result

def get_ical_file(recurrenceday, amount, description):
  try:
    currentdate = datetime.now()
    dayrecurrence = str(recurrenceday)
    if len(dayrecurrence) < 2: dayrecurrence  = "0" + dayrecurrence
    uidstamp = currentdate.strftime('%Y%m%d%H%M%S') + "@BUDGETAPP"
    datetimestamp = currentdate.strftime('%Y%m') + dayrecurrence + "T120000L"
    icalfile = open("/tmp/calfile.ical", "w")
    icalfile.write("BEGIN:VCALENDAR")
    icalfile.write("\nVERSION:2.0")
    icalfile.write("\nPRODID:-//budgetapp")
    icalfile.write("\nBEGIN:VEVENT")
    icalfile.write("\nUID:" + uidstamp)
    icalfile.write("\nTRANSP:TRANSPARENT")
    icalfile.write("\nDTSTART:" + datetimestamp)
    icalfile.write("\nDTEND:" + datetimestamp)
    icalfile.write("\nDTSTAMP:" + datetimestamp)
    icalfile.write("\nORGANIZER;CN=BudgetApp:mailto:budgetapp@app.org")
    icalfile.write("\nSUMMARY:" + str(amount))
    icalfile.write("\nDESCRIPTION:<p>" + description + "</p>")
    icalfile.write("\nLOCATION:https://www.paypal.com/")
    icalfile.write("\nEND:VEVENT")
    icalfile.write("\nEND:VCALENDAR")
    return "/tmp/calfile.ical"
  except Exception as ex:
    print(str(ex))
    return str(ex)

#