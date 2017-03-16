# -*- coding: utf-8 -*-
import sqlite3

#http://tools.wmflabs.org/wsexport/logs.sqlite

sqlite_file = '~/Downloads/logs.sqlite' 
#sqlite_file = 'http://tools.wmflabs.org/wsexport/logs.sqlite'

conn = sqlite3.connect(sqlite_file)
c = conn.cursor()

query = "SELECT TITLE,FORMAT,COUNT(*) as DWDCNT FROM CREATION where lang='ta' GROUP BY TITLE,FORMAT  ;"


outfile= open("report.csv","w")

aBookDetail = {}

allFormats = ["atom","epub","epub-2","epub-3","htmlz","mobi","odt","pdf",
            "pdf-a4","pdf-a5","pdf-a6","pdf-letter","rtf","txt","xhtml"]

aBookDetail["title"] = None
for aFormat in allFormats:
    aBookDetail[aFormat] = 0

c.execute(query)

ReportList = c.fetchall()
conn.close()

i = 1

for aline in ReportList: 
    booktitle,bookformat,bookcount = aline
    booktitle= unicode(booktitle)
    bookformat=unicode(bookformat)
    bookcount = unicode(bookcount)

    if aBookDetail["title"] == None :
       aBookDetail["title"] = booktitle
       aBookDetail[bookformat] = bookcount
      
    elif aBookDetail["title"] ==  booktitle :
       aBookDetail[bookformat] = bookcount
    else:
       aCSVLine = aBookDetail["title"]
       aCSVLine = aCSVLine + ',' + ','.join([(aBookDetail[aform]) 
                   for aform in allFormats])+ "\n"


       #aCSVLine = unicode(aCSVLine) +',' + unicode(',').join([unicode(aBookDetail[aform]) 
       #            for aform in allFormats])+unicode("\n")
       #outfile.write(aCSVLine)
       print aCSVLine
       for aFormat in allFormats:
           aBookDetail[aFormat] = 0 
       aBookDetail["title"] = booktitle
       aBookDetail[bookformat] = bookcount
  
aCSVLine = aBookDetail["title"]
aCSVLine = aCSVLine +',' + ','.join([str(aBookDetail[aform]) 
             for aform in allFormats])+"\n"

outfile.write(aCSVLine)


outfile.close()


