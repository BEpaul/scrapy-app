import scrapy
import urllib
from wines.items import WinesItem
from urllib.parse import urlparse
from urllib.parse import parse_qs
import re
import json

# 정규표현식을 이용하여 문자열 내 html 태그를 제거하는 메소드
def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

class WineSpider(scrapy.Spider):
    name = 'wine'
    allowed_domains = ['www.shinsegae-lnb.com']
    start_urls = ['http://www.shinsegae-lnb.com/product/wine?currentPage=1&orderBy=2&listSize=12&selectedWineType=0&selectedWineNation=0&selectedSugar=0&searchText=#orderBy']
        
    def parse(self, response):
        page = 83
        for i in range(page):
            url = f'http://www.shinsegae-lnb.com/product/wine?currentPage={i+1}&orderBy=2&listSize=12&selectedWineType=0&selectedWineNation=0&selectedSugar=0&searchText=#orderBy'

            yield scrapy.Request(url, callback = self.parse_pages)

    def parse_pages(self, response):
        default_url = 'http://www.shinsegae-lnb.com'

        for i in range(12):
            extra_url = response.css(f'#section2 > div > ul > li:nth-child({i+1}) > div > a::attr(href)').extract_first()
            if extra_url is None:
                yield scrapy.Request(url, callback = self.parse_page_detail)
                break

            url = urllib.parse.urljoin(default_url, extra_url)
            yield scrapy.Request(url, callback = self.parse_page_detail)

    

    def parse_page_detail(self, response):
        item = WinesItem()

        ## 와인 인덱스
        url = response.request.url
        parsed_url = urlparse(url)
        item['id'] = parse_qs(parsed_url.query)['id'][0]
        
        
        ## 와인명 (국)
        item['korean_name'] = response.css('#section2 > div > div.right_box > div.box1 > dl > dt::text').get()


        ## 와인명 (영)
        item['english_name'] = response.css('#section2 > div > div.right_box > div.box1 > dl > dd.etit::text').get()


        ## 한줄 설명
        item['description'] = response.css('#section2 > div > div.right_box > div.box1 > dl > dd.txt::text').get()
    

        ## 와인 이미지
        item['image'] = response.css('#section2 > div > div.left_box > img::attr(src)').get()


        ## 와인 상세 정보
        get_details = []
        for i in range(5):
             get_details.append(response.css(f'#section2 > div > div.right_box > div.box2 > ul > li.type{i+1} > span:nth-child(2)::text').get())
        
        detail_info = {
             "TYPE": get_details[0],
             "COUNTRY / WINERY": get_details[1],
             "GRAPE VARIETY": get_details[2],
             "CAPACITY": get_details[3],
             "FOOD MATCHING": get_details[4]
        }
        item['detail_info'] = detail_info
        

        ## 와인 맛 특징
        sweet_score = int(response.css('#section2 > div > div.right_box > div.box3 > dl:nth-child(1) > dd > span.on > p.num::text').get())
        acidity_score = int(response.css('#section2 > div > div.right_box > div.box3 > dl:nth-child(2) > dd > span.on > p.num::text').get())
        body_score = int(response.css('#section2 > div > div.right_box > div.box3 > dl:nth-child(3) > dd > span.on > p.num::text').get())
        
        favor_characteristic = {
             "당도": sweet_score,
             "산도": acidity_score,
             "바디": body_score
        }

        item['favor_characteristic'] = favor_characteristic
        

        ## 와인 설명
        raw_info = response.css('#section3 > div > div.left_box > dl > dd').get()
        
        # 정규표현식과 내장함수를 이용하여 html 태그 및 공백 제거
        clean_info = cleanhtml(raw_info)
        item['information'] = clean_info.strip()
        


        ## 수상 경력
        awards_list = response.css('#section3 > div > div.right_box > dl > dd > ul > li').getall()
        awards = []
        for raw_awards in awards_list:
            clean_awards = cleanhtml(raw_awards)
            awards.append(clean_awards.strip())
        
        item['awards'] = awards

        return item