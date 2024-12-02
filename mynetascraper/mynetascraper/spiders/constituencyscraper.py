import pandas as pd
import scrapy
from bs4 import BeautifulSoup
# from scrapy_splash import SplashRequest

from dbbackend.db_session import SessionLocal, ConstituencyData, CandidateData


def prepare_link(url):
    base = "https://myneta.info/LokSabha2024/"
    if not url.startswith(base):
        return base + url
    return url

def asset_liability_extractor(text):
    return int(text.split('~')[0].strip().split('Rs')[1].strip().replace(",", ""))

class ConstituencyscraperSpider(scrapy.Spider):
    name = "constituencyscraper"
    allowed_domains = ["myneta.info"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.db_session = SessionLocal()

    def start_requests(self):
        # Query all links from the database
        links = self.db_session.query(ConstituencyData).all()
        for link in links:
            yield scrapy.Request(url=prepare_link(link.href), callback=self.parse_table)

    def parse_table(self, response):
        try:
            soup = BeautifulSoup(response.text, 'lxml')
            table = soup.find('table', {'class': 'w3-bordered'})
            table_headers = ['SNo', 'candidate', 'party', 'criminal_cases', 'education', 'age', 'total_assets', 'liabilities']
            for i, row in enumerate(table.find_all('tr')[1:]):
                winner = i == 0
                row_dict = {}
                for cell_idx, cell in enumerate(row.find_all(['td', 'tr'])):
                    if cell_idx == 1:
                        anchor = cell.find('a')
                        row_dict['full_name'] = anchor.text
                        row_dict['id'] = anchor['href'].split("=")[1]
                    if cell_idx in [2, 4]:
                        row_dict[table_headers[cell_idx]] = cell.text.strip()
                    if cell_idx in [3, 5]:
                        row_dict[table_headers[cell_idx]] = int(cell.text.strip())
                    if cell_idx in [6, 7]:
                        try:
                            row_dict[table_headers[cell_idx]] = asset_liability_extractor(cell.text)
                        except Exception as e:
                            row_dict[table_headers[cell_idx]] = 0
                row_dict['winner'] = winner
                row_dict['constituency_id'] = int(response.url.split("&")[1].split("=")[1])
                self.db_session.add(CandidateData(**row_dict))
            self.db_session.commit()
        except Exception as e:
            print("Exception occurred")
            self.db_session.rollback()


