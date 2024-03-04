# Adidas Webscraping with Scrapy-Playwright

This project demonstrates how to scrape product information from the Adidas website using Scrapy with Playwright integration. By combining Scrapy's powerful web scraping capabilities with Playwright's browser automation, we can efficiently extract data from dynamic websites like Adidas.

## Requirements

- Python 3.x
- Scrapy
- Playwright
- Virtualenv (optional but recommended)

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/kenyann/adidas-scrapy
   cd adidas-webscraping

2. Create a virtual environment (opt but recommend)
    ```bash
    virtualenv venv
    source venv/bin/activate  # For Unix/Linux
    .\venv\Scripts\activate    # For Windows

3. Install the required packages:
    ```bash
    pip install -r requirements.txt

## Usage

To start the scraper, navigate to the project directory and run the following command:

```bash
scrapy crawl adidas
```

This will start the scraper and the scraped data will be stored in a file named output.json.