import pandas as pd

class Log:
    def __init__(self):
        self.log_data = pd.read_csv("log.csv")
        self.output_df = None
        self.log_data["Date"]= pd.to_datetime(self.log_data["Date"],format="mixed")

    def check_duplicate(self,date,ticker):
        already_exists = ((self.log_data["Date"]==pd.Timestamp(date)) & (self.log_data["ticker"]==ticker))
        return already_exists.any()


    def generate_log(self,date,iteration,ticker,pchange,traded_volume,volume_mean,delivery_percent,delivery_mean,nifty_movement,result):
        self.output_df=pd.DataFrame({
            "Date":[date],
            "Stock_Iteration":[iteration],
            "ticker":[ticker],
            "pchange":[pchange],
            "vol_ratio":[traded_volume/volume_mean],
            "delivery_ratio":[delivery_percent/delivery_mean],
            "vs_nifty": [pchange-nifty_movement],
            "pass/fail":[result]
        })
        if not self.check_duplicate(date,ticker):
            self.output_df.to_csv("log.csv",index=False,header=False,mode="a")