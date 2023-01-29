import scrapy, json, re

prov_dict = {   "alberta"       : 48, 
                "columbia"      : 59,
                "manitoba"      : 46,
                "newfoundland"  : 10,
                "brunswick"     : 13,
                "scotia"        : 12,
                "northwest"     : 61,
                "nunavut"       : 62,
                "prince"        : 11,
                "ontario"       : 35,
                "québec"        : 24,
                "saskatchewan"  : 47,
                "yukon"         : 60
            }

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

        categories = ["Prince_Edward_Island"]

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
        else:
            categories = []
        
        res_dct = { 'fire_department_name': response.xpath("//meta[@property='og:title']/@content").get(),
                    'categories': categories}

        res_dct["pruid"] = self._reverse_map_province(categories)

        # check if department is is still active
        res_dct["active"] = all([not i.lower().startswith("defunct") for i in categories])
        
        # industrial vs public fire departments
        res_dct["industrial"] = any([i.lower().find("industrial") >= 0  for i in categories])
        
        # first nations fire departments
        res_dct["first_nations"] = any([i.lower().find("first nations") >= 0  for i in categories])

        for loc in locations:

            res_dct['locations'] = loc 

            res_dct['fire_station_name'] = loc['title'].strip()
            res_dct['lat'] = loc['lat']
            res_dct['lon'] = loc['lon']

            yield res_dct

    @staticmethod
    def _reverse_map_province(x):
    
        prov_dict = {   "alberta"       : 48, 
                        "columbia"      : 59,
                        "manitoba"      : 46,
                        "newfoundland"  : 10,
                        "brunswick"     : 13,
                        "scotia"        : 12,
                        "northwest"     : 61,
                        "nunavut"       : 62,
                        "prince"        : 11,
                        "ontario"       : 35,
                        "québec"        : 24,
                        "saskatchewan"  : 47,
                        "yukon"         : 60
                    }
        
        for k,v in prov_dict.items():
            if any([i.lower().find(k) >= 0 for i in x]):
                return v
        
        return -1




        