from bs4 import BeautifulSoup
import urllib2
import sqlite3
import requests
conn=sqlite3.connect('cs_virtual.db')
conn.execute("DELETE from data;")
conn.commit()
conn.close()
for i in xrange(1,3):
    i=str(i)
    uh=urllib2.urlopen("https://internshala.com/internships/virtual-computer%20science-internship/page-"+i)
    data=BeautifulSoup(uh,'lxml')
    table = data.findAll("div", { "class" : "individual_internship_header" })
    header=[]
    for new in table:
        link=""
        name=""
        company=""
        counter=0
        for row in new.findAll("h4"):
            for flink in row.findAll("a"):
                if counter==0:
                    link= flink['href']
                    name= flink.text
                    counter+=1
                else:
                    company=flink.text

        header.append((str(link),str(name),str(company)))
    table = data.findAll("div", { "class" : "individual_internship_details" })
    details=[]
    for new in table:
        date=""
        duration=""
        applyby=""
        stipend=""
        row = new.find("div", { "class" : "table-responsive" })

        row= row.find("table", { "class" : "table" })
        row=row.find("tbody")
        row=row.find("tr")
        counter=0
        for i in row.findAll("td"):
            if counter==0:
                date=i.find("div").text
                date=str(date).strip()
            elif counter==1:
                duration=i.text
                duration=str(duration).strip()
            elif counter==2:
                stipend=i.text
                stipend=str(stipend).strip()
            elif counter==4:
                applyby=i.text
                applyby=str(applyby).strip()
                counter=0
            counter+=1

        details.append((date,duration,stipend,applyby))


    rough_data=zip(header,details)
    final_data=[]
    for value in rough_data:
        final_data.append(value[0]+value[1])

    conn=sqlite3.connect('cs_virtual.db')
    for value in final_data:
        link=value[0]
        name=value[1]
        company=value[2]
        date=value[3]
        duration=value[4]
        stipend=value[5]
        applyby=value[6]
        conn.execute("INSERT INTO data(`name`,`company`,`date`,`duration`,`applyby`,`stipend`,`link`) VALUES (?,?,?,?,?,?,?);",(name,company,date,duration,applyby,stipend,link))
    conn.commit()
    conn.close()