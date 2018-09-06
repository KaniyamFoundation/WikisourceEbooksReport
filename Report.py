# -*- coding: utf-8 -*-
import sqlite3
import wget
import shutil 
import os
import time
from time import gmtime, strftime
import csv

if not os.path.isdir("./data"):
    os.mkdir("./data")



sqlite_file_Url  = "http://tools.wmflabs.org/wsexport/logs.sqlite"
sqlite_file = "logs.sqlite"
#sqlite_file = wget.download(sqlite_file_Url) 

#sqlite_file = 'logsApr01.sqlite'

def get_report(lang):
	conn = sqlite3.connect(sqlite_file)
	c = conn.cursor()

	query = "SELECT TITLE,FORMAT,COUNT(*) as DWDCNT FROM CREATION where lang='" + lang +"' GROUP BY TITLE,FORMAT  ;"
	print query

	outfile= open(lang + "/data/report.csv","w")

	aBookDetail = {}

	allFormats = ["atom","epub","epub-2","epub-3","htmlz","mobi","odt","pdf",
            "pdf-a4","pdf-a5","pdf-a6","pdf-letter","rtf","txt","xhtml"]

	aBookDetail["title"] = None
	aCSVLine = "Title"
	for aFormat in allFormats:
    		aBookDetail[aFormat] = 0

	aCSVLine = aCSVLine + ',' + ','.join([ aform 
                   for aform in allFormats]) + ",Total\n" 

	outfile.write(aCSVLine)

	c.execute(query)

	ReportList = c.fetchall()
	conn.close()

	i = 1

	for aline in ReportList: 
    		booktitle,bookformat,bookcount = aline
    		booktitle = booktitle.replace(",","")
    
    # Reading Very First Line and populating Dictionary
    		if aBookDetail["title"] == None :
       	
			aBookDetail["title"] = booktitle
       
       			aBookDetail[bookformat] = bookcount
       
       			aBookDetail["total"] = 0 
       			aBookDetail["total"] =  aBookDetail["total"] + bookcount 
       
    #Reading Same book detail and populating Dictionary  
    		elif aBookDetail["title"] ==  booktitle :
       			aBookDetail[bookformat] = bookcount
       			aBookDetail["total"] =  aBookDetail["total"] + bookcount 
       
    #Reading Differnt Book,Processing Dict Contents and Write to File
		else:
       			aCSVLine = aBookDetail["title"]

       			aCSVLine = aCSVLine + ',' + ','.join([ str(aBookDetail[aform]) 
                   		for aform in allFormats]) + "," + str(aBookDetail["total"] )+"\n"
       # Write to a File
       #print(aCSVLine.encode('utf-8'))
       			outfile.write(str(aCSVLine.encode('utf-8'))) 

       			for aFormat in allFormats:
           			aBookDetail[aFormat] = 0 
       			aBookDetail["title"] = booktitle
    
       			aBookDetail[bookformat] = bookcount
       			aBookDetail["total"] = 0 
       			aBookDetail["total"] =  aBookDetail["total"] + bookcount 
  
	aCSVLine = aBookDetail["title"]
	aCSVLine = aCSVLine +',' + ','.join([str(aBookDetail[aform]) 
             for aform in allFormats])+"," + str(aBookDetail["total"] )+"\n"

# Writing Last Book Details
#print(aCSVLine)
	outfile.write(str(aCSVLine.encode('utf-8')))
	outfile.close()

#shutil.move('logs.sqlite','data/logs.sqlite')




	with open(lang +'/data/report.csv') as sample, open(lang +'/data/report_reverse_sorted.csv', "w") as out:
    		csv1=csv.reader(sample,delimiter=',')
    		header = next(csv1, None)
    		csv_writer = csv.writer(out,delimiter=',')
    		if header:
        		csv_writer.writerow(header)
    		csv_writer.writerows(sorted(csv1, key=lambda x:int(x[16]),reverse=True))




	timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())




	with open(lang+"/data/report_reverse_sorted.csv") as fin:
    		headerline = fin.next()
    		total = 0
    		for row in csv.reader(fin,delimiter=','):
        		total += int(row[16])



	total_time = open(lang+'/data/time_total.html','w')

	total_time.write('<link href="../css/bootstrap.min.css" rel="stylesheet">\n')
	total_time.write("<p align='right'> This list is updated daily once. Last update was on  " + timestamp + "<br/>")
	total_time.write(" Total downloads =   " + str(total) + "</p>")
	total_time.close()

get_report('ta')
get_report('te')
get_report('bn')

shutil.move('logs.sqlite','data/logs.sqlite')

