# -*- coding: utf-8 -*-

import scrapy

class SzSecurityHousingItem(scrapy.Item):
    #用户唯一id
    userid = scrapy.Field()
    #轮候排位
    seqno = scrapy.Field()

    #备案回执好
    applyNo = scrapy.Field()

    #申请人数
    num = scrapy.Field()

    #户籍所在地
    place = scrapy.Field()

    #姓名
    name = scrapy.Field()

    #身份证
    creditId = scrapy.Field()