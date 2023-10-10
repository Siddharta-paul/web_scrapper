import csv
import asyncio
from pyppeteer import launch


async def main():
    count = 0
    
    browser = await launch()
    page = await browser.newPage()
    await page.goto('https://www.jiomart.com/c/groceries/2')
    
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
        const products = document.querySelectorAll(".jm-col-4.jm-mt-base"); //selecting the entire product card
        const data = [];
        for (let product of products) {
            const nameElement = product.querySelector('div.plp-card-details-name.line-clamp.jm-body-xs.jm-fc-primary-grey-80');
            const name = nameElement ? nameElement.innerText.trim() : '';

            const linkElement = product.querySelector("plp-card-wrapper plp_product_list viewed")

            const link = nameElement ? 'https://www.jiomart.com/c/groceries/' + nameElement.getAttribute('href') : '';

            const mrpElement = product.querySelector('.jm-body-xxs.jm-fc-primary-grey-60.line-through.jm-mb-xxs');
            const mrp = mrpElement ? mrpElement.innerText.trim().substring(1) : 0;
            
            const discountElement = product.querySelector('.jm-heading-xxs.jm-mb-xxs');
            const discount = discountElement ? discountElement.innerText.trim().substring(1) : 0;

            const discountpercentageElement = product.querySelector('.jm-badge');
            const discountpercent = discountpercentageElement ? discountpercentageElement.innerText.trim() : 0;

            data.push({ 'Name': name, 'Link': link, 'MRP': mrp, 'DiscountedPrice': discount, 'DiscountPercent': discountpercent });
              
        }
        return data;
    }''')

    with open('jiomartdata.csv', mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=['Name', 'Link', 'MRP', 'DiscountedPrice', 'DiscountPercent'])
        writer.writeheader()
        for data in productData:
            writer.writerow(data)
    
    await browser.close()

asyncio.get_event_loop().run_until_complete(main())
