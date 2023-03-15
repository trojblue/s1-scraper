import scrapy
from scrapy.http import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
import json
import csv

class DiscuzSpiderSpider(CrawlSpider):
    name = 'discuz_spider'
    allowed_domains = ['www.saraba1st.com']
    start_urls = ['https://www.saraba1st.com/2b/forum-6-1.html']
    page_count = 1  # Add this line

    rules = (
        Rule(LinkExtractor(allow=r'forum-6-\d+.html'), callback='parse_item', follow=True),
    )

    all_items = {}

    def parse_item(self, response: HtmlResponse):
        rows = response.xpath('//*[@id="threadlisttableid"]/tbody[contains(@id, "normalthread")]')

        for row in rows:
            post_url = row.xpath('.//td[contains(@class, "icn")]/a/@href').get()

            item = {
                'id': row.xpath('@id').get(),
                'title': row.xpath('.//a[contains(@class, "s xst")]/text()').get(),
                'post_url': response.urljoin(post_url),
                'date': row.xpath('.//td[contains(@class, "by")][1]/em/span/text()').get(),
                'original_poster': row.xpath('.//td[contains(@class, "by")][1]/cite/a/text()').get(),
                'last_reply_date': row.xpath('.//td[contains(@class, "by")][2]/em/a/text()').get(),
                'last_reply_author': row.xpath('.//td[contains(@class, "by")][2]/cite/a/text()').get(),
                'type_str': row.xpath('.//th/em/a/text()').get(),
                'type_id': row.xpath('.//th/em/a/@href').re_first(r'typeid=(\d+)'),
                'reply_count': row.xpath('.//td[contains(@class, "num")]/a/text()').get(),
                'view_count': row.xpath('.//td[contains(@class, "num")]/em/text()').get()
            }
            self.page_count += 1

            # Save the items to a CSV file every 10 pages
            if self.page_count % 10 == 0:
                with open('forum-6.csv', 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=item.keys())
                    writer.writeheader()
                    for item in self.all_items.values():
                        writer.writerow(item)

            # Deduplicate items using the id field and store in a class-level dictionary.
            self.all_items[item['id']] = item

        self.page_count += 1

        # Save the items to a CSV file every 10 pages
        if self.page_count % 10 == 0:
            with open('forum-6.csv', 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=item.keys())
                writer.writeheader()
                for item in self.all_items.values():
                    writer.writerow(item)
