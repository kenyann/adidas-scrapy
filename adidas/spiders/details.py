import scrapy
from scrapy.http import Request
from scrapy_playwright.handler import PageMethod
from datetime import datetime
import pandas as pd


class CrawlerSpider(scrapy.Spider):
    name = "detail"
    allowed_domains = "www.adidas.com"
    # start_urls = ["https://www.adidas.com/us/"]

    def start_requests(self):
        global url
        # url = "https://www.adidas.com/us/forum-low-cl-the-grinch-shoes/IG7066.html"

        # yield scrapy.Request(url, meta=dict(playwright=True, playwright_include_page=True,
        #                                     playwright_page_methods=[
        #                                         PageMethod(
        #                                             'click',  '//*[@id="fixed-content"]/section[2]'),
        #                                     ],
        #                                     errback=self.errback))
        df = pd.read_csv('boyshoe.csv')
        for url in df['url'][:5]:
            try:
                yield scrapy.Request(url, meta=dict(playwright=True, playwright_include_page=True,
                                                    playwright_page_methods=[
                                                        # PageMethod(
                                                        #     "wait_for_selector", "#fixed-content > section:nth-child(4)"),
                                                        PageMethod(
                                                            'click',  '//*[@id="fixed-content"]/section[2]'),
                                                    ],
                                                    errback=self.errback))
            except Exception as e:
                self.logger.error(f'Error at {url}, problem at {e}')

    async def parse(self, response):
        page = response.meta["playwright_page"]
        # screenshot = await page.screenshot(path=f"{response.request.url}.png", full_page=True)
        await page.close()
        # check if have more than one color
        try:
            color_available = response.xpath(
                '//*[@id="available-colors-label"]/text()').get()
            color = None

            if color_available:
                color = response.xpath(
                    '//*[@id="main-content"]/div[2]/div[2]/div[2]/div[3]/text()').get()
            else:
                color = response.xpath(
                    '//*[@id="main-content"]/div[2]/div[2]/div[2]/text()').get()
        except:
            color = ''
        # check if price has discount
        try:
            price = response.xpath(
                '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/text()').get()
            if price:
                price = response.xpath(
                    '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div[2]/text()').get().replace("$", "")
            else:
                price = response.xpath(
                    '//*[@id="main-content"]/div[2]/div[2]/div[1]/div[2]/div/div/div/div/text()').get().replace("$", "")
        except:
            price = ''
        # ---------------------------------------------------------------

        try:
            name = response.xpath(
                '//*[@id="main-content"]/div[2]/div[2]/div[1]/h1/span/text()').get()
        except:
            name = ''
        # ---------------------------------------------------------------

        try:
            description = response.xpath(
                '//*[@id="navigation-target-description"]/div/div/div/div/div[1]/h3/text()').get() + response.xpath('//*[@id="navigation-target-description"]/div/div/div/div/div[1]/p/text()').get()
        except Exception as e:
            description = ''
        # ---------------------------------------------------------------

        try:
            review_count = response.xpath('//*[@id="navigation-target-reviews"]/div/button/div[1]/div/h2/text()').get(
            ).replace("Reviews", "").replace('(', '').replace(')', ''),
        except:
            review_count = ''
        # ---------------------------------------------------------------
        try:
            avg_rating = response.xpath(
                '//*[@id="navigation-target-reviews"]/div/button/div[1]/div/div/span/text()').get(),
        except:
            avg_rating = ''
        yield {
            'name': name,
            'price': price,
            'description': description,
            'review_count': review_count,
            'avg_rating': avg_rating,
            'scraped_at': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'color': color,
            'brand': 'Adidas',
            'currency': 'USD',
            'url': response.request.url,
            'availability': 'INSTOCK'
        }

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()

# availability	avg_rating	brand	color	currency	description	images	name	price	review_count	scraped_at	url
