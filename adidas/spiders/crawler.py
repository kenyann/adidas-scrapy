import scrapy
from scrapy.http import Request
from scrapy_playwright.handler import PageMethod


class CrawlerSpider(scrapy.Spider):
    name = "crawler"
    # allowed_domains = "www.adidas.com"
    # start_urls = ["https://www.adidas.com/us/"]

    def start_requests(self):
        urls = [
            #         'https://www.adidas.com/us/men-clothing',
            # 'https://www.adidas.com/us/men-shoes',
            # 'https://www.adidas.com/us/men-accessories',
            # 'https://www.adidas.com/us/women-clothing',
            # 'https://www.adidas.com/us/women-shoes',
            # 'https://www.adidas.com/us/women-accessories',
            # 'https://www.adidas.com/us/boys-clothing',
            'https://www.adidas.com/us/boys-shoes',
            'https://www.adidas.com/us/girls-clothing',
            'https://www.adidas.com/us/girls-shoes',
            'https://www.adidas.com/us/kids-infant_toddler',
            'https://www.adidas.com/us/kids-accessories'
        ]

        for url in urls:
            try:
                yield scrapy.Request(url, meta=dict(playwright=True, playwright_include_page=True,
                                                    errback=self.errback))
            except Exception as e:
                self.logger.error(f'Error at {url}, reason is {e}')

        # url = 'https://www.adidas.com/us/men-athletic_sneakers?start=48'
        # yield scrapy.Request(url, meta=dict(playwright=True, playwright_include_page=True,
        #                                     errback=self.errback))

    async def parse(self, response):
        page = response.meta["playwright_page"]
        await page.close()

        container = response.xpath(
            '//*[@id="main-content"]/div/div[3]/div/div/div[2]/div[1]/div')

        items = container.css('div.grid-item')

        for item in items[1:]:
            try:
                yield {
                    'name': item.css('div > div > div > a > div > p.glass-product-card__title::text').get(),
                    'url': "https://www.adidas.com" + item.css('div > div > div > div > a.glass-product-card__assets-link::attr(href)').get(),
                    'images': item.css('div > div > div > div > a.glass-product-card__assets-link > img::attr(src)').get()
                }
            except Exception as e:
                self.logger.error(f"Error at {item}, {e}")
        try:
            next_page = response.css(
                '#main-content > div > div:nth-child(3) > div > div > div.col-s-12.col-l-24.no-x-padding-on-mobile___3dhA9 > div.pagination--container___3gNjN > div > div > div > div.pagination__control___3C268.pagination__control--next___329Qo.pagination_margin--next___3H3Zd > a::attr(href)').get()
            if next_page is not None:
                try:
                    next_page_url = "https://www.adidas.com" + next_page
                    self.logger.info(f'Requested at {next_page_url}')
                    yield scrapy.Request(next_page_url, meta=dict(
                        playwright=True,
                        playwright_include_page=True,
                        errback=self.errback,
                    ))
                except Exception as e:
                    self.logger.error(f"Error at next page is none'/n', {e}")
        except Exception as e:
            self.logger.error(f"No next page found, {e}")

    async def errback(self, failure):
        page = failure.request.meta["playwright_page"]
        await page.close()
