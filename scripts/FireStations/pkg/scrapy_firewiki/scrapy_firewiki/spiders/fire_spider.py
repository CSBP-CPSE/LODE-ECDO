import scrapy, json, re

class FireSpider(scrapy.Spider):
    name = "fire"

    def start_requests(self):
        base_url = "https://fire.fandom.com/wiki/"

        categories = [  "Alberta", 
                        "British_Columbia", 
                        "First_Nations", 
                        "Manitoba", 
                        "New_Brunswick", 
                        "Newfoundland_and_Labrador", 
                        "Northwest_Territories",
                        "Nova_Scotia",
                        "Nunavut",
                        "Ontario", 
                        "Prince_Edward_Island",
                        "Québec",
                        "Saskatchewan",
                        "Yukon"
                    ]

        urls = [ "%sCategory:%s" % (base_url, c) for c in categories ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

        

    def parse(self, response):

        # follow up on other category pages
        yield from response.follow_all(xpath="//a[contains(@class, 'category-page__member-link')]", callback=self.parse)

        # check if Google map exists
        gm = response.xpath("//div[@class='mapdata']/text()").get()

        if gm:
            locations = json.loads(gm)['locations']
        else:
            locations = []

        # check for user-set categories
        rlconf = response.xpath("//script[contains(text(), 'RLCONF')]/text()").get().replace('\n','')

        ptn = re.compile(r'"wgCategories":(\[.*?\])')

        if ptn.search(rlconf):
            categories = json.loads(ptn.findall(rlconf)[0])

        yield { 'title': response.xpath("//meta[@property='og:title']/@content").get(),
                'locations': locations,
                'categories': categories}





        