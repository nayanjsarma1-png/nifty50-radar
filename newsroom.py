import os
import requests
import constans
from dotenv import load_dotenv
from datetime import date,timedelta

load_dotenv()

class Newsroom:
    def __init__(self):
        self.API_KEY =os.environ["API_KEY"]
        self.URL = "https://newsapi.org/v2/everything"
        self.PARAMETERS = {
            "apiKey": self.API_KEY,
            "language": "en",
            "from": (date.today() - timedelta(days=2)).isoformat(),
            "pageSize": 5
        }

    def get_news(self,ticker):
        self.PARAMETERS["q"] = constans.TICKER_TO_NAME.get(ticker,ticker)
        response = requests.get(url=self.URL, params=self.PARAMETERS)
        response.raise_for_status()
        data = response.json()["articles"]
        return [(item["title"],item["url"]) for item in data]
