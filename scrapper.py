import requests
from bs4 import BeautifulSoup
import pandas as pd


baseurl = "https://www.brownells.com"
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'}

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
print(df)





