import scrapy
from NFLScrapy.items import ScrapyTeam
from datetime import datetime


class Teams_NFL_spider(scrapy.Spider):
    name = 'teams_NFL'
    start_urls = [
        'https://www.nfl.com/teams/'
    ]
    def parse(self, response):
        links = response.xpath(
            '//div[@class="d3-o-media-object__cta nfl-c-custom-promo__cta"]/a[1]/@href').getall()
        backgraundImage = response.xpath(
            '//div[@class="d3-o-media-object d3-o-media-object--horizontal d3-o-media-object--vertical-center nfl-c-custom-promo__content"]/@style').getall()
        officialPages = response.xpath(
            '//div[@class="d3-o-media-object__cta nfl-c-custom-promo__cta"]/a[2]/@href').getall()

        counter = 0
        for linkTeam in links:
            yield response.follow(linkTeam, callback=self.parses_Teams, cb_kwargs= {'backgraundImages' : backgraundImage[counter], 'officialPage': officialPages[counter]})
            counter += 1

    def parses_Teams(self, response, **kwargs):

        teamImageStyle = kwargs['backgraundImages']
        officialPage = kwargs['officialPage']
        nameTeam = response.xpath('//div[@class="nfl-c-team-header__title"]/text()').get()
        division = response.xpath('//div[@class="nfl-c-team-header__ranking nfl-u-hide-empty"]/text()').get()
        resultsGames = response.xpath('//div[@class="nfl-c-team-header__stats nfl-u-hide-empty"]/text()').get()
        infoTeam = response.xpath('//div[@class="nfl-c-team-info__info-value"]/text()').getall()
        lazyLogo = response.xpath('//figure[@class="nfl-c-team-header__logo"]//img/@src').get()
        logo = lazyLogo.replace('/t_lazy','')
        teamImageback = teamImageStyle.replace('background-image:url(','').replace(')','')
        teamImageback2 = response.xpath('//figure[@class="nfl-c-team-header__background"]//img/@src').get()
        won=resultsGames.split()[0]
        lost=resultsGames.split()[2]
        tied=resultsGames.split()[4]

        team = ScrapyTeam()
        team['name'] = nameTeam
        team['image']  = logo
        team['backgroundImage']  = teamImageback
        team['backgroundImage2']  = teamImageback2
        team['won']  = won
        team['lost']  = lost
        team['tied']  = tied
        team['division']  = division
        team['headCoach']  = infoTeam[0]
        team['stadium']  = infoTeam[1]
        team['owner']  = infoTeam[2].split(',')
        team['established']  = infoTeam[3]
        team['officialPage']  = officialPage
        team['timestamp']  =  datetime.today().strftime('%Y-%m-%d')
        yield team
