import os


def read_file(filepath: str):
  result = ""
  try:
    readfile = open(filepath, "r")
    result = readfile.read()
    readfile.close()
  except Exception as ex:
    result = str(ex)
  return result

def read_file_lines(filepath: str):
  result = ""
  try:
    readfile = open(filepath, "r")
    result = readfile.readlines()
    readfile.close()
  except Exception as ex:
    result = str(ex)
  return result

def write_file(filepath: str, content: str):
  result = ""
  try:
    writefile = open(filepath, "w")
    writefile.write(content)
    writefile.close()
    result = filepath
  except Exception as ex:
    result = str(ex)
  return result

def delete_file(filepath: str):
  result = ""
  try:
    if os.path.exists(filepath):
      os.remove(filepath)
      result = filepath
    else:
      result = "File not found: " + filepath
  except Exception as ex:
    result = str(ex)
  return result

#