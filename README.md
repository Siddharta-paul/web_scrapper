### Web Scraper for Different websites

This Python script utilizes the Pyppeteer library to scrape product data from the required website. It navigates to the required page and extracts product names, links, MRP (Maximum Retail Price), and discounted prices. The scraped data is then saved into a CSV file for further analysis or use.

#### Prerequisites

Make sure you have the following installed:

- Python 3 or above, you can download it from: [Download Python](https://www.python.org/downloads/)
- Pyppeteer: Install it using `pip install pyppeteer`.

#### How to Use

1. **Clone the Repository:**
   ```
   git clone https://github.com/Siddharta-paul/web_scrapper.git
   cd web_scrapper
   ```

2. **Install Dependencies:**
   ```
   pip install pyppeteer
   ```

3. **Run the Script:**
   ```
   python script_name.py
   ```

   The script will launch a headless browser, scrape the product data, and save it to a CSV file named `products.csv`.

#### CSV Output

The scraped data will be saved in a CSV file named `file_name.csv` with the following columns:
 (Note give the names of columns as per required info.)
- `Name`: Product name
- `Link`: URL link to the product page on BigBasket
- `MRP`: Maximum Retail Price of the product
- `DiscountedPrice`: Discounted price of the product

#### Note

I used this webscrapper script to explore the field of scrapping data. This is just for learning purpose.

Feel free to customize the script to scrape data from different categories or modify the data fields as per your requirements.

Happy scraping! 🚀