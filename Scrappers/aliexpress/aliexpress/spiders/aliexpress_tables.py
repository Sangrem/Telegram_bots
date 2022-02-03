import scrapy


class AliexpressTabletsSpider(scrapy.Spider):
    name = 'aliexpress_tablets'
    allowed_domains = ['aliexpress.com']
    start_urls = ['https://www.aliexpress.com/category/200216607/tablets.html']

    custom_settings={ 'FEED_URI': "aliexpress_%(time)s.json",
                       'FEED_FORMAT': 'json'}

    def parse(self, response):

        print("procesing:"+response.url)
        # Извлечение данных с помощью селекторов CSS
        product_name=response.css('.item-title::text').extract()
        price_range=response.css('.price-current::text').extract()
        # Извлечение данных с использованием xpath
        orders=response.xpath("//em[@title='Total Orders']/text()").extract()
        company_name=response.xpath("//a[@class='store $p4pLog']/text()").extract()

        row_data=zip(product_name,price_range,orders,company_name)

        # извлечение данных строки
        for item in row_data:
            # создать словарь для хранения извлеченной информации
            scraped_info = {
                'page': response.url,
                'product_name': item[0],  # item[0] означает продукт в списке и т. д., индекс указывает, какое значение назначить
                'price_range': item[1],
                'orders': item[2],
                'company_name': item[3],
            }

            # генерируем очищенную информацию для скрапа
            yield scraped_info

        NEXT_PAGE_SELECTOR = '.ui-pagination-active+a::attr(href)'
        next_page = response.css(NEXT_PAGE_SELECTOR).extract_first()
        if next_page:
            yield scrapy.Request(
            response.urljoin(next_page),
            callback=self.parse)