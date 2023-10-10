import csv
import asyncio
from pyppeteer import launch

async def main():
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.bigbasket.com/cl/foodgrains-oil-masala/?nc=nb')

    productData = await page.evaluate('''() => {
        const products = document.querySelectorAll("div.item.prod-deck.row.ng-scope");
        const data = [];
        for (let product of products) {
            const nameElement = product.querySelector('a.ng-binding');
            const name = nameElement ? nameElement.innerText.trim() : '';
            const link = nameElement ? 'https://www.bigbasket.com' + nameElement.getAttribute('href') : '';
            const mrpElement = product.querySelector('.mp-price');
            const mrp = mrpElement ? mrpElement.innerText.split(' ')[1] : 0;
            const discountElement = product.querySelector('.discnt-price');
            const discount = discountElement ? discountElement.innerText.split(' ')[1] : 0;
            data.push({ 'Name': name, 'Link': link, 'MRP': mrp, 'DiscountedPrice': discount });  
        }
        return data;
    }''')

    with open('products.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Link', 'MRP', 'DiscountedPrice'])
        writer.writeheader()
        for data in productData:
            writer.writerow(data)
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
