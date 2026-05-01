import pandas as pd


class DataManager:
        def __init__(self):
            self.historic_data = pd.read_csv("stock_output.csv")
            self.historic_nifty = pd.read_csv("nifty_movement.csv")
            self.historic_nifty["Call_date"] = pd.to_datetime(self.historic_nifty["Call_date"], format="mixed")
            self.historic_data["Call_date"] = pd.to_datetime(self.historic_data["Call_date"], format="mixed")

        def return_volume_mean(self,ticker):
            return self.historic_data[self.historic_data["Ticker"]==ticker]["volume"].mean()

        def return_delivery_mean(self, ticker):
            return self.historic_data[self.historic_data["Ticker"] == ticker]["Delivery %"].mean()

        def nifty_movement(self,date):
            return self.historic_nifty[self.historic_nifty["Call_date"]==pd.Timestamp(date)]["nifty_pchange"].values[0]
        def check_duplicates_historic(self, ticker, date):
            already_exists = (
                    (self.historic_data["Ticker"] == ticker) &
                    (self.historic_data["Call_date"] == pd.Timestamp(date))
            )
            return already_exists.any()

        def check_duplicates_nifty(self,date):
            already_exists = self.historic_nifty["Call_date"]==pd.Timestamp(date)
            return already_exists.any()

        def append_historic_data(self,date,ticker,traded_volume,delivery):
            if not self.check_duplicates_historic(ticker,date):
                output_df = pd.DataFrame({
                    "Call_date": [date],
                    "Ticker": [ticker],
                    "volume": [traded_volume],
                    "Delivery %": [delivery]
                })
                output_df.to_csv("stock_output.csv", mode="a", index=False, header=False)

        def append_nifty_file(self,date,nifty_movement):
            if not self.check_duplicates_nifty(date):
                output_df =pd.DataFrame({
                    "Call_date":[date],
                    "nifty_pchange":[nifty_movement]
                })
                output_df.to_csv("nifty_movement.csv", mode="a", index=False, header=False)

        def remove_historic_data(self):
            self.historic_data = pd.read_csv("stock_output.csv")
            self.historic_data["Call_date"] = pd.to_datetime(self.historic_data["Call_date"],format="mixed")
            oldest_date_index = [group_df["Call_date"].idxmin() for (ticker, group_df) in self.historic_data.groupby("Ticker")]
            self.historic_data = self.historic_data.drop(oldest_date_index)
            self.historic_data.to_csv("stock_output.csv", index=False)












