# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScrapyTeam(scrapy.Item):
    name = scrapy.Field()
    image = scrapy.Field()
    backgroundImage = scrapy.Field()
    backgroundImage2 = scrapy.Field()
    won = scrapy.Field()
    lost = scrapy.Field()
    tied = scrapy.Field()
    division = scrapy.Field()
    headCoach = scrapy.Field()
    stadium = scrapy.Field()
    owner = scrapy.Field()
    established = scrapy.Field()
    officialPage = scrapy.Field()
    timestamp =  scrapy.Field()



class ScrapyPlayer(scrapy.Item):
    nameTeam = scrapy.Field()
    name = scrapy.Field()
    image = scrapy.Field()
    status = scrapy.Field()
    number = scrapy.Field()
    position = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    age = scrapy.Field()
    experience = scrapy.Field()
    college = scrapy.Field()
    weight = scrapy.Field()
    arms = scrapy.Field()
    hands = scrapy.Field()
    hometown = scrapy.Field()
    timestamp =  scrapy.Field()

