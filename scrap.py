from bs4 import BeautifulSoup
import requests
import pandas as pd

webpage = requests.get('https://www.jiomart.com/c/groceries/2')

sp = BeautifulSoup(webpage.content, 'html.parser')

#print(sp.text)

title = sp.find_all('span', 'clsgetname')
sellprice = sp.find_all("span", {"id" :"final_price"})
originalprice = sp.find_all(['strike', 'price'])
discount = sp.find_all('span', 'dis_section')


titleloop = [titles.text for titles in title]
sellpriceloop = [sell.text for sell in sellprice]
originalpriceloop = [orig.text for orig in originalprice]
discountloop = [discount.text for discount in discount]


data = {
    'Name_of_product':titleloop,
    'Selling_price':sellpriceloop,
    'Original_price':originalpriceloop,
    'Discount_offered':discountloop
}
#print(len(titleloop))
#print(len(sellpriceloop))
#print(len(originalpriceloop))
#print(len(discountloop))
 
df = pd.DataFrame(data, columns=[
     'Name_of_product',
     'Original_price',
     'Discount_offered',
     'Selling_price'
     ])

#add a path to your local device
df.to_csv(r'D:\webscrapper\jiomart.csv')

print()