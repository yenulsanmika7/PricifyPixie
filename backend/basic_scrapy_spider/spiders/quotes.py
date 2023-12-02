import json
import scrapy
from urllib.parse import urljoin
import re

class AmazonSearchProductSpider(scrapy.Spider):
    name = "amazon_search_product"

    custom_settings = {
        'CLOSESPIDER_ITEMCOUNT': 10  
    }

    def start_requests(self):
        keyword = getattr(self, 'keyword', 'trending')
        keyword_list = [keyword]
        for keyword in keyword_list:
            amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page=1'
            yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': 1})  

    def discover_product_urls(self, response):
        page = response.meta['page']
        keyword = response.meta['keyword'] 

        ## Discover Product URLs
        search_products = response.css("div.s-result-item[data-component-type=s-search-result]")
        for product_id, product in enumerate(search_products, start=1):
            relative_url = product.css("h2>a::attr(href)").get()
            product_url = urljoin('https://www.amazon.com/', relative_url).split("?")[0]
            yield scrapy.Request(url=product_url, callback=self.parse_product_data, meta={'keyword': keyword, 'page': page, 'url': product_url, 'product_id': product_id})
            
        ## Get All Pages
        if page == 1:
            available_pages = response.xpath(
                '//*[contains(@class, "s-pagination-item")][not(has-class("s-pagination-separator"))]/text()'
            ).getall()

            last_page = available_pages[-1]
            for page_num in range(2, int(last_page)):
                amazon_search_url = f'https://www.amazon.com/s?k={keyword}&page={page_num}'
                yield scrapy.Request(url=amazon_search_url, callback=self.discover_product_urls, meta={'keyword': keyword, 'page': page_num})


    def parse_product_data(self, response):
        image_data = json.loads(re.findall(r"colorImages':.*'initial':\s*(\[.+?\])},\n", response.text)[0])
        variant_data = re.findall(r'dimensionValuesDisplayData"\s*:\s* ({.+?}),\n', response.text)
        product_url = response.meta['url']
        price = response.css('.a-price .a-offscreen ::text').get("")
        description = response.css('.a-list-item::text').extract()

        quiz_text = response.css('.a-size-base ::text').get()
        answered_questions = re.findall(r'\d+', quiz_text)














        

        if not price:
            price = response.css('.a-price span[aria-hidden="true"] ::text').get("")
        yield {
            "id": response.meta['product_id'],
            "name": response.css("#productTitle::text").get("").strip(),
            "price": price,
            "stars": response.css("i[data-hook=average-star-rating] ::text").get("").strip(),
            "rating_count": response.css("#acrCustomerReviewText::text").get("").strip(),
            "description": description,
            "images": image_data,
            "variant_data": variant_data,
            "product_url": product_url,
            "question_count": answered_questions
        }