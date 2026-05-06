import warnings
from data_manager import DataManager
from Stock_screener import StockScreener
from time_manager import TimeManager
import time
from emailer import Email
from log import Log
from newsroom import Newsroom
import constans
warnings.filterwarnings("ignore")
ticker_list =[]

#get the date
timemanager = TimeManager()
yesterday =timemanager.yesterday
datamanager = DataManager()
screener = StockScreener()
mailer = Email()
log = Log()
news =Newsroom()

if not screener.check_market_closed(yesterday):
    exit()
if not screener.check_stock_data():
    exit()
datamanager.append_nifty_file(yesterday,screener.today_nifty_movement)
for i in range(1,51):
    time.sleep(5)
    if not screener.get_data(i,yesterday):
        continue
    historic_vol_mean=datamanager.return_volume_mean(screener.ticker)
    historic_delivery_mean = datamanager.return_delivery_mean(screener.ticker)
    nifty_movement =datamanager.nifty_movement(yesterday)
    # progress log
    result = (screener.p_change >3 and screener.traded_volume>1.5*historic_vol_mean and screener.delivery_percent >1.2*historic_delivery_mean and screener.p_change-nifty_movement >2)
    log.generate_log(yesterday,i,screener.ticker,screener.p_change,screener.traded_volume,historic_vol_mean,screener.delivery_percent,historic_delivery_mean,nifty_movement,result)
    if result:
        ticker_list.append(screener.ticker)


    datamanager.append_historic_data(yesterday,screener.ticker,screener.traded_volume,screener.delivery_percent)
#################end of for stock iterations#################


datamanager.remove_historic_data()
# mailer.send_mail(ticker_list)
news_body ="Below are the breakout stocks and the news that drove it(possibly!!). If the list and message below is empty, there were possibly no breakout for the day. Check logs\n"
for items in ticker_list:
    news_body += f"\n {items}:({constans.TICKER_TO_NAME.get(items,items)})\n"
    for (title,url) in news.get_news(items):
        news_body += f"{title}:{url}\n\n"
mailer.send_mail(news_body)






