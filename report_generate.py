# -*- coding: utf-8 -*-
import os
from time import gmtime, strftime
import csv
import mysql.connector
import time
from mysql.connector import Error


def get_report(lang):
    while True:
        try:
            db_config = {
                'host': os.getenv("HOST_DB"),
                'user': os.getenv("DB_USER_NAME"),
                'password': os.getenv("DB_USER_PASSWORD"),
                'database': os.getenv("DB_NAME")
                }
            conn = mysql.connector.connect(**db_config)
            if conn.is_connected():
                print("Successfully connected to the database")
                break
        except Error as e:
            print(f"Error: {e}, retrying in 5 seconds...")
            time.sleep(5)
            
    c = conn.cursor()


    query = "SELECT title, format, COUNT(*) as DWDCNT FROM books_generated WHERE lang='" + lang + "' GROUP BY title, format;"
    print(query)

    if not os.path.exists(f"{lang}/data"):
        os.makedirs(f"{lang}/data")

    outfile = open(f"{lang}/data/report.csv", "w", newline='')

    aBookDetail = {}
    allFormats = ["atom", "epub", "epub-2", "epub-3", "htmlz", "mobi", "odt", "pdf", "pdf-a4", "pdf-a5", "pdf-a6", "pdf-letter", "rtf", "txt", "xhtml"]

    aBookDetail["title"] = None
    aCSVLine = "Title"
    for aFormat in allFormats:
        aBookDetail[aFormat] = 0


    aCSVLine = aCSVLine + ',' + ','.join([aform for aform in allFormats]) + ",Total\n"
    outfile.write(aCSVLine)

    c.execute(query)
    ReportList = c.fetchall()
    # print("report list ", ReportList)
    conn.close()

    for aline in ReportList:
        print("aline" , aline)
        booktitle, bookformat, bookcount = aline
        booktitle = booktitle.decode("utf-8").replace(",", "")

        if aBookDetail["title"] is None:
            aBookDetail["title"] = booktitle
            aBookDetail[bookformat] = bookcount
            aBookDetail["total"] = 0
            aBookDetail["total"] += bookcount
        elif aBookDetail["title"] == booktitle:
            aBookDetail[bookformat] = bookcount
            aBookDetail["total"] += bookcount
        else:
            aCSVLine = aBookDetail["title"]
            
            aCSVLine = aCSVLine + ',' + ','.join([str(aBookDetail[aform]) for aform in allFormats]) + "," + str(aBookDetail["total"]) + "\n"
            outfile.write(aCSVLine)

            for aFormat in allFormats:
                aBookDetail[aFormat] = 0
            aBookDetail["title"] = booktitle
            aBookDetail[bookformat] = bookcount
            aBookDetail["total"] = 0
            aBookDetail["total"] += bookcount

    aCSVLine = aBookDetail["title"]
    print(aBookDetail)
    aCSVLine = aCSVLine + ',' + ','.join([str(aBookDetail[aform]) for aform in allFormats]) + "," + str(aBookDetail["total"]) + "\n"
    outfile.write(aCSVLine)
    outfile.close()

    # Sorting the CSV report
    with open(f'{lang}/data/report.csv', newline='') as sample, open(f'{lang}/data/report_reverse_sorted.csv', "w", newline='') as out:
        csv1 = csv.reader(sample, delimiter=',')
        header = next(csv1, None)
        csv_writer = csv.writer(out, delimiter=',')
        if header:
            csv_writer.writerow(header)
        csv_writer.writerows(sorted(csv1, key=lambda x: int(x[16]), reverse=True))

    timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    # Calculate the total number of downloads
    total = 0
    with open(f'{lang}/data/report_reverse_sorted.csv', newline='') as fin:
        headerline = next(fin)
        for row in csv.reader(fin, delimiter=','):
            total += int(row[16])

    total_time = open(f'{lang}/data/time_total.html', 'w')
    total_time.write('<link href="../css/bootstrap.min.css" rel="stylesheet">\n')
    total_time.write(f"<p align='right'>This list is updated daily once. Last update was on {timestamp}<br/>")
    total_time.write(f"Total downloads = {total}</p>")
    total_time.close()

# Run the report for different languages
get_report('ta')
get_report('te')
get_report('bn')
