# -*- coding: utf-8 -*-
import scrapy


class TransferSaisonSpider(scrapy.Spider):
    name = 'transfer_saison'
    allowed_domains = ['https://www.transfermarkt.de']

    def start_requests(self):
        yield scrapy.Request('https://www.transfermarkt.de/1-bundesliga/transfers/wettbewerb/L1/plus/?saison_id={}&s_w=&leihe=0&leihe=1&intern=0&intern=1'.format(self.saison_id), self.parse)

    def parse(self, response):
        vereins_boxen =  response.css('div.box')
        for box in vereins_boxen:
            vereins_name =  box.xpath('./div/a/img/@alt').extract_first()
            vereins_id =  box.xpath('./div/a/@id').extract_first()
            #
            # print '-' * 80
            # print vereins_name
            # print '-' * 80

            for idx, tabelle in enumerate(box.css('div.responsive-table table')):

                for spieler in tabelle.css('tbody tr'):

                    richtung = idx == 0 and 'zugang' or 'abgang'
                    spieler_link = spieler.css('td div.di span a')
                    spieler_url = spieler.xpath('./td/div/span/a/@href').extract_first()
                    spieler_name = spieler_link.css('::text').extract_first()
                    spieler_id = spieler_link.xpath('./@id').extract_first()
                    marktwert = spieler.css('td.mw-transfer-cell ::text').extract_first()
                    abloese = ' '.join(spieler.css('td:nth-child(9) ::text').extract())
                    transfer_url = spieler.xpath('./td/a/@href').extract_first()

                    verein_transfer = spieler.xpath('./td[7]/a/img/@alt').extract_first()

                    #print richtung, spieler_name, markt_wert, abloese, verein_transfer

                    yield {
                        'richtung': richtung,
                        'spieler_name': spieler_name,
                        'spieler_link': spieler_url,
                        'spieler_id': spieler_id,
                        'marktwert': marktwert,
                        'abloese': abloese,
                        'verein': vereins_name,
                        'verein_transfer': verein_transfer,
                        'transfer_url': transfer_url
                    }
