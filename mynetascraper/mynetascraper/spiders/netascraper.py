import scrapy

from dbbackend.db_session import ConstituencyData, SessionLocal


class NetascraperSpider(scrapy.Spider):
    name = "netascraper"
    allowed_domains = ["myneta.info"]
    start_urls = ["https://myneta.info/LokSabha2024/"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_session = SessionLocal()

    def parse(self, response):
        divs = response.xpath("//div[contains(@class, 'w3-dropdown-click')]")
        for i, div in enumerate(divs):
            constituencies_div = div.xpath(".//div[starts-with(@id, 'item')]")
            state_ut_name = div.xpath(".//button[contains(@onclick, 'handle_dropdown')]")[0].xpath('normalize-space(.)').get()
            constituencies_anchors = constituencies_div.xpath(".//a")
            for i, constituency_obj in enumerate(constituencies_anchors[1:]):
                print(f"Constituencies: {i+1}/{len(constituencies_anchors) - 1}")
                text = constituency_obj.xpath("normalize-space(.)").get()
                href = constituency_obj.xpath("@href").get()
                constituency_id = href.split("&")[1].split("=")[1]
                entry = ConstituencyData(id=constituency_id, state_or_ut = state_ut_name, constituency=text, href=href)
                self.db_session.add(entry)
            self.db_session.commit()
            print(f"State/UT: {i+1}/{len(divs)}")
        print("Test")
