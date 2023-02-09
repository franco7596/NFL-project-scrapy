import scrapy
from NFLScrapy.items import ScrapyPlayer
from datetime import datetime


class Roster_NFL_spider(scrapy.Spider):
    name = 'roster_NFL'
    start_urls = [
        'https://www.nfl.com/teams/'
    ]
    def parse(self, response):
        links = response.xpath(
            '//div[@class="d3-o-media-object__cta nfl-c-custom-promo__cta"]/a[1]/@href').getall()
        NamesTeam = response.xpath(
            '//div[@class="d3-o-media-object__body nfl-c-custom-promo__body"]//p/text()').getall()
        counter = 0
        for linkTeam in links:
            yield response.follow(linkTeam+'/roster', callback=self.parses_roster, cb_kwargs= {'nameTeam' : NamesTeam[counter]})
            counter += 1


    def parses_roster(self, response,  **kwargs):
        nameTeam = kwargs['nameTeam']
        playersLink = response.xpath('//a[@class="nfl-o-roster__player-name nfl-o-cta--link"]/@href').getall()
        for i in range(len(playersLink)):
            playerName = response.xpath(f'(//a[@class="nfl-o-roster__player-name nfl-o-cta--link"]/text())[{i+1}]').get() or ''
            playerNumber = response.xpath(f'(//tr/td[2]/text())[{i+1}]').get() or ''
            playerPosition = response.xpath(f'(//tr/td[3]/text())[{i+1}]').get() or ''
            playerStatus = response.xpath(f'(//tr/td[4]/text())[{i+1}]').get() or ''
            playerImage = response.xpath(f'(//td//img[@class="img-responsive/@src"])[{i+1}]').get() or None
            yield response.follow(playersLink[i], callback=self.parses_player, cb_kwargs= {'playerName':playerName , 'playerNumber':playerNumber, 'playerPosition':playerPosition, 'playerStatus':playerStatus,'playerImage':playerImage, 'nameTeam':nameTeam})


    def parses_player(self, response, **kwargs):
        nameTeam = kwargs['nameTeam']
        playerName = kwargs['playerName']
        playerNumber = kwargs['playerNumber']
        playerPosition = kwargs['playerPosition']
        playerStatus = kwargs['playerStatus']
        playerImageLazy = kwargs['playerImage']
        playerImage = ""
        if(playerImageLazy):
            playerImage = playerImageLazy.replace('/t_lazy','')
        playerHeight = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[1]').get() or ''
        playerWeight = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[2]').get() or ''
        playerArms = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[3]').get() or ''
        playerHands = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[4]').get() or ''
        playerExperience = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[5]').get() or ''
        playerCollege = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[6]').get() or ''
        playerAge = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[7]').get() or ''
        playerHometown = response.xpath('(//div[@class="nfl-c-player-info__value"]/text())[8]').get() or ''

        player = ScrapyPlayer()
        player['nameTeam'] = nameTeam
        player['name'] = playerName
        player['image'] = playerImage
        player['status'] = playerStatus
        player['number'] = playerNumber
        player['position'] = playerPosition
        player['height'] = playerHeight
        player['age'] = playerAge
        player['experience'] = playerExperience
        player['college'] = playerCollege
        player['weight'] = playerWeight
        player['arms'] = playerArms
        player['hands'] = playerHands
        player['hometown'] = playerHometown
        player['timestamp'] = datetime.today().strftime('%Y-%m-%d')
        yield player
