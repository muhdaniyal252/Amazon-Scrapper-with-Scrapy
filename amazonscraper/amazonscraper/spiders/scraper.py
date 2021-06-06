import scrapy
from ..items import AmazonscraperItem

class AmazonScraperSpider(scrapy.Spider):
    name = 'amazonscraper'
    start_urls = [
        'https://www.amazon.com/s?i=computers-intl-ship&bbn=16225007011&rh=n%3A16225007011&dc&qid=1614171444&ref=sr_ex_n_1'
    ]

    item = AmazonscraperItem()

    def parse(self,response):
        links = response.xpath('//a[@class="a-link-normal acs_tile__title-image aok-block a-text-normal"]')

        for link in links:
            product_category = link.css('div span::text').extract()[0].strip()
            follow_link = link.css('::attr(href)').get()
            yield response.follow(follow_link,
                                  callback = self.scrap_product_names,
                                  meta = {'product_category': product_category})



    def scrap_product_names(self,response): 
        product_category = response.meta.get('product_category')
        
        product_names = response.css('span.a-size-base-plus.a-color-base.a-text-normal::text').extract()
        for product_name in product_names:
            self.item['product_name'] = product_name
            self.item['product_category'] = product_category
            yield self.item

        
        last_page = response.xpath('//li[@class="a-disabled a-last"]')

        if not last_page:
            next_page = response.xpath('//li[@class="a-last"]/a/@href').extract()[0]
            yield response.follow(next_page,
                                  callback = self.scrap_product_names,
                                  meta = {'product_category': product_category})

            