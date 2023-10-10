const fs = require('fs');
const puppeteer = require('puppeteer');

async function main() {
  let count = 0;

  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  await page.goto('https://www.bigbasket.com/cl/foodgrains-oil-masala/?nc=nb#!page=3');

  // Get the height of the rendered page
  const pageHeight = await page.evaluate('document.body.scrollHeight');

  while (count !== 3) {
    // Scroll to the bottom of the page
    await page.evaluate('window.scrollTo(0, document.body.scrollHeight)');
    // Wait for the new content to load
    count++;

    await page.waitForTimeout(10000);
    // Calculate the new height of the page
    const newPageHeight = await page.evaluate('document.body.scrollHeight');
    if (newPageHeight === pageHeight) {
      console.log('Scrapped up to page', count);
      // If the page hasn't grown, we've reached the end of the content
      break;
    } else {
      pageHeight = newPageHeight;
    }
  }

  const productData = await page.evaluate(() => {
    const products = document.querySelectorAll('div.item.prod-deck.row.ng-scope');
    const data = [];
    for (let product of products) {
      const nameElement = product.querySelector('a.ng-binding');
      const name = nameElement ? nameElement.innerText.trim() : '';
      const link = nameElement ? 'https://www.bigbasket.com' + nameElement.getAttribute('href') : '';
      const mrpElement = product.querySelector('.mp-price');
      const mrp = mrpElement ? mrpElement.innerText.split(' ')[1] : 0;
      const discountElement = product.querySelector('.discnt-price');
      const discount = discountElement ? discountElement.innerText.split(' ')[1] : 0;

      const discountPercentageElement = product.querySelector('.save-price.ng-scope .ng-binding');
      const discountPercent = discountPercentageElement ? discountPercentageElement.innerText.trim() : 0;

      data.push({ 'Name': name, 'Link': link, 'MRP': mrp, 'DiscountedPrice': discount, 'DiscountPercent': discountPercent });
    }
    return data;
  });

  const csvData = productData.map((data) => {
    return `${data.Name},${data.Link},${data.MRP},${data.DiscountedPrice},${data.DiscountPercent}`;
  });

  const csvContent = ['Name,Link,MRP,DiscountedPrice,DiscountPercent', ...csvData].join('\n');
  fs.writeFileSync('bigbasketdata1.csv', csvContent);

  await browser.close();
}

main();
