#!/usr/bin/python3


csvfile = "db-txactions.sql"
sqlfile = "fixed-txactions.sql"

infile = open(csvfile, "r")
outfile = open(sqlfile, "w")

inlines = infile.readlines()

content = ""
x = 1

for iline in inlines:
  tmparr = iline.split(',')
  tmpline = "INSERT INTO transactions VALUES (" + str(x) + "," + tmparr[1] + "," + tmparr[2] + "," + tmparr[3] + "," + tmparr[4] + "," + tmparr[5] + "," + tmparr[6] + "," + tmparr[7] + "," + tmparr[8]
  content += tmpline
  x += 1

outfile.write(content)

infile.close()
outfile.close()
#
