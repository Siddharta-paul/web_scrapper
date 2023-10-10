import csv
import asyncio
from pyppeteer import launch


async def main():
    count = 0
    
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.bigbasket.com/cl/foodgrains-oil-masala/?nc=nb#!page=3')
    
        # Get the height of the rendered page
    page_height = await page.evaluate('document.body.scrollHeight')

    while count != 3:
        # Scroll to the bottom of the page
        await page.evaluate('window.scrollTo(0, document.body.scrollHeight)')
        # Wait for the new content to load
        count+=1

        await asyncio.sleep(10)
        # Calculate the new height of the page
        new_page_height = await page.evaluate('document.body.scrollHeight')
        if new_page_height == page_height:
            print("scrapped upto page" , count)
            # If the page hasn't grown, we've reached the end of the content
            break
        else:
            page_height = new_page_height

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

            
            const discountpercentageElement = product.querySelector('.save-price.ng-scope .ng-binding');
            const discountpercent = discountpercentageElement ? discountpercentageElement.innerText.trim() : 0;

            data.push({ 'Name': name, 'Link': link, 'MRP': mrp, 'DiscountedPrice': discount, 'DiscountPercent': discountpercent });
        }
        return data;
    }''')

    with open('bigbasketdata1.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Link', 'MRP', 'DiscountedPrice', 'DiscountPercent'])
        writer.writeheader()
        for data in productData:
            writer.writerow(data)
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
