# -*- coding: utf-8 -*-
import scrapy
import urllib
from urlparse import urlparse
from scrapy.http import Request
from scrapy.selector import Selector
from scrapy.contrib.loader import ItemLoader
from linkedin_crawler.items import LinkedinCrawlerItem
from w3lib.html import replace_escape_chars, remove_tags
from scrapy.contrib.loader.processor import Compose, MapCompose


class LinkedinSpider(scrapy.Spider):
    name = "linkedin"
    allowed_domains = ["linkedin.com"]
    start_urls = (
        'https://www.linkedin.com/jobs2/directory/companies-a/',
        'https://www.linkedin.com/jobs2/directory/companies-b/',
        'https://www.linkedin.com/jobs2/directory/companies-c/',
        'https://www.linkedin.com/jobs2/directory/companies-d/',
        'https://www.linkedin.com/jobs2/directory/companies-e/',
        'https://www.linkedin.com/jobs2/directory/companies-f/',
        'https://www.linkedin.com/jobs2/directory/companies-g/',
        'https://www.linkedin.com/jobs2/directory/companies-h/',
        'https://www.linkedin.com/jobs2/directory/companies-i/',
        'https://www.linkedin.com/jobs2/directory/companies-j/',
        'https://www.linkedin.com/jobs2/directory/companies-k/',
        'https://www.linkedin.com/jobs2/directory/companies-l/',
        'https://www.linkedin.com/jobs2/directory/companies-m/',
        'https://www.linkedin.com/jobs2/directory/companies-n/',
        'https://www.linkedin.com/jobs2/directory/companies-o/',
        'https://www.linkedin.com/jobs2/directory/companies-p/',
        'https://www.linkedin.com/jobs2/directory/companies-q/',
        'https://www.linkedin.com/jobs2/directory/companies-r/',
        'https://www.linkedin.com/jobs2/directory/companies-s/',
        'https://www.linkedin.com/jobs2/directory/companies-t/',
        'https://www.linkedin.com/jobs2/directory/companies-u/',
        'https://www.linkedin.com/jobs2/directory/companies-v/',
        'https://www.linkedin.com/jobs2/directory/companies-w/',
        'https://www.linkedin.com/jobs2/directory/companies-x/',
        'https://www.linkedin.com/jobs2/directory/companies-y/',
        'https://www.linkedin.com/jobs2/directory/companies-z/',
        'https://www.linkedin.com/jobs2/directory/companies-other/',
        'https://www.linkedin.com/jobs2/directory/region-alabama/',
        'https://www.linkedin.com/jobs2/directory/region-arizona/',
        'https://www.linkedin.com/jobs2/directory/region-arkansas/',
        'https://www.linkedin.com/jobs2/directory/region-california/',
        'https://www.linkedin.com/jobs2/directory/region-colorado/',
        'https://www.linkedin.com/jobs2/directory/region-connecticut/',
        'https://www.linkedin.com/jobs2/directory/region-delaware/',
        'https://www.linkedin.com/jobs2/directory/region-district-of-columbia/',
        'https://www.linkedin.com/jobs2/directory/region-florida/',
        'https://www.linkedin.com/jobs2/directory/region-georgia/',
        'https://www.linkedin.com/jobs2/directory/region-illinois/',
        'https://www.linkedin.com/jobs2/directory/region-indiana/',
        'https://www.linkedin.com/jobs2/directory/region-iowa/',
        'https://www.linkedin.com/jobs2/directory/region-kansas/',
        'https://www.linkedin.com/jobs2/directory/region-kentucky/',
        'https://www.linkedin.com/jobs2/directory/region-louisiana/',
        'https://www.linkedin.com/jobs2/directory/region-maryland/',
        'https://www.linkedin.com/jobs2/directory/region-massachusetts/',
        'https://www.linkedin.com/jobs2/directory/region-michigan/',
        'https://www.linkedin.com/jobs2/directory/region-minnesota/',
        'https://www.linkedin.com/jobs2/directory/region-mississippi/',
        'https://www.linkedin.com/jobs2/directory/region-missouri/',
        'https://www.linkedin.com/jobs2/directory/region-nebraska/',
        'https://www.linkedin.com/jobs2/directory/region-nevada/',
        'https://www.linkedin.com/jobs2/directory/region-new-hampshire/',
        'https://www.linkedin.com/jobs2/directory/region-new-jersey/',
        'https://www.linkedin.com/jobs2/directory/region-new-mexico/',
        'https://www.linkedin.com/jobs2/directory/region-new-york/',
        'https://www.linkedin.com/jobs2/directory/region-north-carolina/',
        'https://www.linkedin.com/jobs2/directory/region-ohio/',
        'https://www.linkedin.com/jobs2/directory/region-oklahoma/',
        'https://www.linkedin.com/jobs2/directory/region-oregon/',
        'https://www.linkedin.com/jobs2/directory/region-pennsylvania/',
        'https://www.linkedin.com/jobs2/directory/region-rhode-island/',
        'https://www.linkedin.com/jobs2/directory/region-south-carolina/',
        'https://www.linkedin.com/jobs2/directory/region-tennessee/',
        'https://www.linkedin.com/jobs2/directory/region-texas/',
        'https://www.linkedin.com/jobs2/directory/region-utah/',
        'https://www.linkedin.com/jobs2/directory/region-virginia/',
        'https://www.linkedin.com/jobs2/directory/region-washington/',
        'https://www.linkedin.com/jobs2/directory/region-wisconsin/'

    )

    def parse(self, response):
        hxs = Selector(response)
        company_and_location_selector = hxs.xpath('//*[@class="content"]/a/@href').extract()

        for i in company_and_location_selector:
            if "/jobs2/" in i:
                jobs2_url = "https://www.linkedin.com" + i
                yield Request(jobs2_url, callback=self.parse_jobs2)

            else:
                full_url = "https://www.linkedin.com" + i
                yield Request(full_url, callback=self.parse_all_pages)

    def parse_jobs2(self, response):
        yield Request(response.url, callback=self.parse)

    def parse_all_pages(self, response):
        hxs = Selector(response)

        for i in range(100):
            page_num = response.url + "?sort=relevance&page_num={0}&trk=jserp_pagination_{0}".format(i)
            yield Request(page_num, callback=self.parse_jobs)

    def parse_jobs(self, response):
        hxs = Selector(response)
        job_selector = hxs.xpath('//h2/a/@href').extract()[1:]

        for i in job_selector:
            yield Request(i, callback=self.parse_items)

    def parse_items(self, response):
        """ This function parses a sample job page.

            @url https://www.linkedin.com/jobs2/view/66769906?trk=jserp_job_details_text
            @returns items 1
            @scrapes company_logo company_name job_title job_date
            @scrapes job_location job_experience job_function employment_type
            @scrapes industry job_description apply_link company_description
            @scrapes company_youtube_video
            """
        l = ItemLoader(item=LinkedinCrawlerItem(), response=response)
        l.default_output_processor = MapCompose(lambda v: v.strip(), replace_escape_chars)

        #l.add_value('page_url', response.url)
        l.add_xpath('company_logo', '//*[@class="logo-container"]/a/img/@src')
        l.add_xpath('company_name', ".//*[@id='top-card']/div[1]/div[2]/h2/a/span/text()")
        l.add_xpath('job_title', '//h1/text()')
        l.add_xpath('job_date', ".//*[@id='top-card']/div[1]/div[2]/div[1]/text()")
        l.add_xpath('job_location', ".//*[@id='top-card']/div[1]/div[2]/h2/span/span[1]/text()")
        l.add_xpath('job_experience', ".//*[@id='top-card']/div[3]/div[1]/ul[1]/li[1]/div[2]/text()")
        l.add_xpath('job_function', ".//*[@id='top-card']/div[3]/div[1]/ul[1]/li[2]/div[2]/text()")
        l.add_xpath('employment_type', ".//*[@id='top-card']/div[3]/div[1]/ul[1]/li[3]/div[2]/text()")
        l.add_xpath('industry', ".//*[@id='top-card']/div[3]/div[1]/ul[2]/li[1]/div[2]/text()")
        l.add_xpath('job_description', '//*[@class="description-module container"]/div/div/div/text()|\
            //*[@class="description-module container"]//strong/text()|\
            //*[@class="description-module container"]//li/text()|\
            //*[@class="description-module container"]/div/div/div//ul/li/text()|\
            //*[@class="description-module container"]/div/div/div/strong/span/text()')

        apply_link_selector = response.xpath(".//*[@id='offsite-apply-button']/@href").extract()[0]

        parsed = urlparse(apply_link_selector)
        url_of_job = parsed.query[39:]

        url_of_job = urllib.unquote(url_of_job)

        l.add_value('apply_link', url_of_job)

        l.add_xpath('company_description', './/*[@id="company-module"]/div/div[1]/text()|\
            .//*[@id="company-module"]/div/div[1]//strong/text()')

        l.add_xpath('company_youtube_video', ".//*[@id='company-module']/div/div[2]/object/param[2]/@value")

        return l.load_item()
