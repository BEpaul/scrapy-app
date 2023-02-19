import scrapy


class WinesItem(scrapy.Item):
    id = scrapy.Field() # 와인 인덱스
    korean_name = scrapy.Field() # 와인명(국)
    english_name = scrapy.Field() # 와인명(영)
    description = scrapy.Field() # 한줄 설명
    image = scrapy.Field() # 와인 이미지
    detail_info = scrapy.Field() # 와인 상세 정보
    favor_characteristic = scrapy.Field() # 와인 맛 특징
    information = scrapy.Field() # 와인 설명
    awards = scrapy.Field() # 수상 경력
    pass
