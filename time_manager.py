from jugaad_data.nse import stock_df
from datetime import date, timedelta


class TimeManager:
    def __init__(self):
        self.yesterday = self.get_last_trading_date()

    def get_last_trading_date(self):
        last_trading_date = date.today() - timedelta(days=2)
        max_lookback = 10  # don't go back more than 10 days
        for _ in range(max_lookback):
            try:
                df = stock_df(symbol="INFY", from_date=last_trading_date, to_date=last_trading_date, series="EQ")
                if not df.empty:
                    return last_trading_date
            except Exception as e:
                print(f"Error code {e}")
            last_trading_date -= timedelta(days=1)
        raise RuntimeError("Could not determine last trading date within 10 days lookback")