from jugaad_data.nse import stock_df,NSELive


class StockScreener:
    def __init__(self):
        self.n = NSELive()
        self.stock_data = None
        self.today_nifty_movement = None
        self.ticker = None
        self.delivery_percent=None
        self.traded_volume = None
        self.p_change = None

    def check_market_closed(self,date):
        try:
            df = stock_df(symbol="INFY", from_date=date, to_date=date, series="EQ")
            return True
        except Exception as e:
            print(f"Check below error code {e}")
            return False

    def check_stock_data(self):
        try:
            self.stock_data = self.n.live_index("NIFTY 50")["data"]
            self.today_nifty_movement = self.stock_data[0]["pChange"]
            return True
        except Exception as e:
            print(f"Failed to fetch data due to {e}")
            return False

    def get_data(self,iteration,date):
        try:
            self.ticker = self.stock_data[iteration]["symbol"]
            delivery_df = stock_df(symbol=self.ticker, from_date=date, to_date=date, series="EQ")
            self.delivery_percent = delivery_df["DELIVERY %"].values[0]
            self.traded_volume = delivery_df["VOLUME"].values[0]
            previous_close = delivery_df["PREV. CLOSE"].values[0]
            current_close = delivery_df["CLOSE"].values[0]
            self.p_change = ((current_close - previous_close) / previous_close) * 100
            return True
        except Exception as e:
            print(f"skipping {self.ticker} for {e}")
            return False

            






