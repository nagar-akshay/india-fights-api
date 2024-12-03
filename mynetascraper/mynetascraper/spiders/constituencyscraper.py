import time
import pandas as pd
import scrapy
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
from dbbackend.db_session import SessionLocal, ConstituencyData, CandidateData


# Helper function to prepare the link
def prepare_link(url):
    base = "https://myneta.info/LokSabha2024/"
    if not url.startswith(base):
        return base + url
    return url


def asset_liability_extractor(text):
    return int(text.split('~')[0].strip().split('Rs')[1].strip().replace(",", ""))


class ConstituencyscraperSpider(scrapy.Spider):
    def __init__(self):
        # Initialize Selenium WebDriver with options
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--no-sandbox")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.db_session = SessionLocal()

    def start_requests(self):
        # Query all links from the database
        links = self.db_session.query(ConstituencyData).all()
        for link in links:
            self.parse_table(prepare_link(link.href))

    def parse_table(self, url):
        try:
            self.driver.get(url)
            time.sleep(2)  # Allow time for the page to fully load

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            table = soup.find('table', {'class': 'w3-bordered'})
            table_headers = ['SNo', 'candidate', 'party', 'criminal_cases', 'education', 'age', 'total_assets',
                             'liabilities']

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
                        except Exception:
                            row_dict[table_headers[cell_idx]] = 0

                row_dict['winner'] = winner
                row_dict['constituency_id'] = int(url.split("&")[1].split("=")[1])
                self.db_session.add(CandidateData(**row_dict))

            self.db_session.commit()
        except Exception as e:
            print(f"Exception occurred: {e}")
            self.db_session.rollback()

    def close(self):
        self.driver.quit()
        self.db_session.close()



