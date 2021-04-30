#!/usr/bin/env python

import time
from datetime import datetime


import requests
from bs4 import BeautifulSoup
import pandas as pd

#Texting Stuff
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from smtplib import SMTP
import smtplib
import sys


def sendEmail(df_test):
    recipients = ['schefferandrew66@gmail.com'] 
    emaillist = [elem.strip().split(',') for elem in recipients]
    msg = MIMEMultipart()
    msg['Subject'] = "PRIMERS UPDATE"
    msg['From'] = 'schefferandrew66@gmail.com'

    html = """\
    <html>
    <head></head>
    <body>
        {0}
    </body>
    </html>
    """.format(df_test.to_html())

    part1 = MIMEText(html, 'html')
    msg.attach(part1)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    
    server.starttls()
    server.ehlo()
    server.login('schefferandrew66@gmail.com', 'Scheffer1!')

    server.sendmail(msg['From'], emaillist , msg.as_string())
    server.close()

    print("Done")

def print_date(base_url):
    print("Scraping " + str(base_url) + " at: ", end="")
    now = datetime.now()
    print(now)


baseurl = "https://www.brownells.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}


while (True):
    try:
        print_date(baseurl)

        k = requests.get('https://www.brownells.com/reloading/primers/index.htm?psize=480').text
        soup=BeautifulSoup(k,'html.parser')
        productlist = soup.find_all("div",{"class":"media listing"})


        data = []
        for product in productlist:
                bd = product.find("div",{"class":"bd"})

                #Get the link
                group1 = bd.find("div",{"class":"group1"})
                a_tag = group1.find("a",{"onclick":"GoogleClickActionEvent(this);"}) 
                link = baseurl + a_tag.get('href')

                #Get the Name
                name = a_tag.find("span", itemprop="name").text
                #print(name)

                #Get Price and Availability
                group2 = bd.find("div",{"class":"group2"})
                availability = group2.find("p",{"class":"status"}) 
                stock = availability.find("span").text
                #print(str(name) + ": " + str(stock))

                prc = group2.find("p",{"class":"prc"}) 
                low_price = prc.find("span", itemprop="lowPrice").text
                try:
                    high_price = prc.find("span", itemprop="highPrice").text
                except:
                    high_price = "N/A"
                
                priceRange = str(low_price) + " - " + str(high_price)

                primer = {"name": name, "price": priceRange, "Availability": stock, "link": link}
                data.append(primer)

        df = pd.DataFrame(data)

        #df['Availability'][17] = "(In Stock)"
        inStock = df[df["Availability"] == "(In Stock)"]
        if inStock.empty:
            print("There is nothing in stock")
            time.sleep(20)
        else:
            sendEmail(inStock)
            print(inStock)
            quit()

        
    except Exception as e:
        print("-------------------------------------")
        print("------- FAILED TO FETCH DATA --------")
        print("-------------------------------------")
        print("Error: " + str(e))
        time.sleep(5)






