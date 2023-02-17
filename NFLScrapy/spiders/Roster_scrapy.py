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
        # yield response.follow(links[0]+'/roster', callback=self.parses_roster, cb_kwargs= {'nameTeam' : NamesTeam[counter]})
        for linkTeam in links:
            yield response.follow(linkTeam+'/roster', callback=self.parses_roster, cb_kwargs= {'nameTeam' : NamesTeam[counter]})
            counter += 1


    def parses_roster(self, response,  **kwargs):
        nameTeam = kwargs['nameTeam']
        cantPlayers = response.xpath('//tbody/tr').getall()
        playersLink = []
        for i in range(len(cantPlayers)):
            playersLink.append( response.xpath(f'//tbody/tr[{i+1}]//a[@class="nfl-o-roster__player-name nfl-o-cta--link"]/@href').get() or "")
        for i in range(len(playersLink)):
            playerName = response.xpath(f'//tbody/tr[{i+1}]//a[@class="nfl-o-roster__player-name nfl-o-cta--link"]/text()').get() or response.xpath(f'//tbody/tr[{i+1}]//span/text()').get()
            playerNumber = response.xpath(f'//tbody/tr[{i+1}]/td[2]/text()').get() or ''
            playerPosition = response.xpath(f'//tbody/tr[{i+1}]/td[3]/text()').get() or ''
            playerStatus = response.xpath(f'//tbody/tr[{i+1}]/td[4]/text()').get() or ''
            playerImage = response.xpath(f'//tbody/tr[{i+1}]//img[@class="img-responsive"]/@src').get() or ''
            if(playersLink[i] != "" ):
                yield response.follow(playersLink[i], callback=self.parses_player, cb_kwargs= {'playerName':playerName , 'playerNumber':playerNumber, 'playerPosition':playerPosition, 'playerStatus':playerStatus,'playerImage':playerImage, 'nameTeam':nameTeam})
            else:
                player = ScrapyPlayer()
                player['nameTeam'] = nameTeam
                player['name'] = playerName
                player['image'] = playerImage
                player['status'] = playerStatus
                player['number'] = playerNumber
                player['position'] = playerPosition
                player['height'] = ""
                player['age'] = ""
                player['experience'] = ""
                player['college'] = ""
                player['weight'] = ""
                player['arms'] = ""
                player['hands'] = ""
                player['hometown'] = ""
                player['timestamp'] = datetime.today().strftime('%Y-%m-%d')
                yield player


    def parses_player(self, response, **kwargs):
        nameTeam = kwargs['nameTeam']
        playerName = kwargs['playerName']
        playerNumber = kwargs['playerNumber']
        playerPosition = kwargs['playerPosition']
        playerStatus = kwargs['playerStatus']
        playerImageLazy = kwargs['playerImage']
        playerImage = ""
        if(playerImageLazy != ''):
            playerImage = playerImageLazy.replace('/t_lazy','')
        playerHeight = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Height")]/following-sibling::div/text()').get() or ''
        playerWeight = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Weight")]/following-sibling::div/text()').get() or ''
        playerArms = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Arms")]/following-sibling::div/text()').get() or ''
        playerHands = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Hands")]/following-sibling::div/text()').get() or ''
        playerExperience = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Experience")]/following-sibling::div/text()').get() or ''
        playerCollege = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"College")]/following-sibling::div/text()').get() or ''
        playerAge = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Age")]/following-sibling::div/text()').get() or ''
        playerHometown = response.xpath('//div[@class="nfl-c-player-info__key" and contains(.,"Hometown")]/following-sibling::div/text()').get() or ''

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


    def parses_player_without_link(self, kwargs):
        nameTeam = kwargs['nameTeam']
        playerName = kwargs['playerName']
        playerNumber = kwargs['playerNumber']
        playerPosition = kwargs['playerPosition']
        playerStatus = kwargs['playerStatus']
        playerImageLazy = kwargs['playerImage']
        playerImage = ""
        if(playerImageLazy != ''):
            playerImage = playerImageLazy.replace('/t_lazy','')

        player = ScrapyPlayer()
        player['nameTeam'] = nameTeam
        player['name'] = playerName
        player['image'] = playerImage
        player['status'] = playerStatus
        player['number'] = playerNumber
        player['position'] = playerPosition
        player['height'] = ""
        player['age'] = ""
        player['experience'] = ""
        player['college'] = ""
        player['weight'] = ""
        player['arms'] = ""
        player['hands'] = ""
        player['hometown'] = ""
        player['timestamp'] = datetime.today().strftime('%Y-%m-%d')
        yield player
