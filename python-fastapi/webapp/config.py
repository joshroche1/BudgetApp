import os

from .filesystem import read_file_lines

workingdir = os.getcwd()

def parse_config(filepath):
  result = {}
  linearr = read_file_lines(filepath)
  for tmpline in linearr:
    tmparr = tmpline.split("=")
    result[tmparr[0]] = tmparr[1]
  return result

class Settings():
  app_name: str = "Budget Application"
  database_vendor: str = ""
  database_host: str = ""
  database_port: str = ""
  database_name: str = ""
  database_user: str = ""
  database_password: str = ""
  base_dir: str = ""
  logfile_path: str = ""
  log_level: str = ""

  def __init__(self):
    configdict = parse_config("env")
    self.database_vendor = configdict["DATABASE_VENDOR"]
    self.database_host = configdict["DATABASE_HOST"]
    self.database_port = configdict["DATABASE_PORT"]
    self.database_name = configdict["DATABASE_NAME"]
    self.database_user = configdict["DATABASE_USER"]
    self.database_password = configdict["DATABASE_PASSWORD"]
    self.base_dir = workingdir
    self.logfile_path = configdict["LOGFILE_PATH"]
    self.log_level = configdict["LOG_LEVEL"]