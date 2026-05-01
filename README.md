# NIFTY 50 Breakout Screener

A fully automated stock screener that runs daily against the NIFTY 50 index, identifies institutional breakout candidates using a multi-factor filter, fetches related news, and delivers everything to your inbox.

Built by a systems engineer who got tired of manually watching 50 stocks.

---

## What it actually does

Every trading day, the screener pulls EOD data for all 50 NIFTY 50 constituents and runs each one through four filters simultaneously. A stock only makes the cut if it clears all four:

1. **Price moved more than 3%** — eliminates noise and minor fluctuations
2. **Volume was more than 1.5x its 30-day average** — confirms the move had participation behind it, not just thin trading
3. **Delivery percentage was more than 1.2x its 30-day average** — this is the institutional signal. Delivery % measures shares that were actually taken for settlement vs intraday positions. Elevated delivery means real money moved, not speculators
4. **Outperformed the NIFTY 50 index by at least 2 percentage points** — filters out stocks that just rode the tide. If the whole market was up 2% and your stock was up 3%, that's not a breakout

Stocks that pass all four get flagged, and the screener fetches the top 5 recent news articles for each one before firing off a single email with the full picture.

---

## Project structure

```
├── main.py              # Orchestrator — wires everything together
├── Stock_screener.py    # NSE API calls, market status check, per-stock data fetch
├── data_manager.py      # All CSV operations — reads, writes, rolling window maintenance
├── time_manager.py      # Finds last available trading date, handles weekends and holidays
├── newsroom.py          # NewsAPI integration — fetches headlines per breakout ticker
├── emailer.py           # SMTP email delivery via Gmail
├── log.py               # Per-run audit log — every stock screened, every ratio computed
├── constans.py          # NSE ticker to full company name mapping for all 50 NIFTY stocks
├── stock_output.csv     # Rolling 30-day volume and delivery history per ticker (seed manually)
├── nifty_movement.csv   # Rolling NIFTY 50 daily % change history (seed manually)
└── log.csv              # Audit trail of every screening run
```

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/YOUR_USERNAME/stock-screener.git
cd stock-screener
```

### 2. Install dependencies

```bash
pip install jugaad-data pandas requests python-dotenv
```

### 3. Create your `.env` file

```
MY_EMAIL=your_gmail@gmail.com
PASSWORD=your_gmail_app_password
RECIPIENT=recipient@gmail.com
API_KEY=your_newsapi_key
```

**Gmail App Password** — not your regular Gmail password. Go to Google Account → Security → 2-Step Verification → App Passwords and generate one specifically for this script.

**NewsAPI key** — free tier at [newsapi.org](https://newsapi.org). 100 requests/day, more than enough.

### 4. Seed the CSV files

Before the first run you need historical data to calculate rolling averages against. Create `stock_output.csv` and `nifty_movement.csv` with at least 30 days of data per ticker. Headers:

**stock_output.csv**
```
Call_date,Ticker,volume,Delivery %
```

**nifty_movement.csv**
```
Call_date,nifty_pchange
```

**log.csv**
```
Date,Stock_Iteration,ticker,pchange,vol_ratio,delivery_ratio,vs_nifty,pass/fail
```

### 5. Run

```bash
python main.py
```

---

## How the rolling window works

The screener maintains exactly 30 rows per ticker in `stock_output.csv`. Each run appends one new row and drops the oldest row for each ticker — the window slides forward daily. This keeps the rolling means current without the file growing indefinitely.

Duplicate protection is built in — if the script crashes mid-run and you restart it, already-processed tickers won't be double-written.

---

## Scheduling

The script is designed to run once daily after NSE publishes EOD data — typically after 7 PM IST. NSE has a T+2 settlement lag on historical delivery data, so the screener automatically walks back to find the most recent available trading date rather than assuming yesterday always has data.

For automated scheduling, use [cron-job.org](https://cron-job.org) to trigger a GitHub Actions `workflow_dispatch` at a fixed time daily. GitHub's native cron scheduler is unreliable — it delays and drops jobs under load.

---

## Data sources

- **Market data** — [jugaad-data](https://github.com/jugaad-py/jugaad-data), a Python wrapper for NSE's historical and live endpoints
- **News** — [NewsAPI](https://newsapi.org), searched by company name per breakout ticker
- **Live index data** — NSE live endpoint via jugaad-data's `NSELive()`

Note: jugaad-data scrapes NSE's private API endpoints. It works until NSE changes something, at which point it breaks until the maintainer patches it. This is the known fragility of this stack.

---

## Limitations

- Screens only NIFTY 50 constituents — the 50 largest stocks by market cap on NSE
- Delivery data has a T+2 lag — you're acting on 2-day-old signals, not same-day
- jugaad-data reliability is dependent on NSE not changing their endpoints
- NewsAPI free tier limits to articles from the past month and 100 requests/day

---

## What's next

- Replace jugaad-data with Zerodha Kite Connect for a reliable, paid data source
- Expand beyond NIFTY 50 to NIFTY 500
- Add backtesting — check how many flagged stocks actually continued moving in the same direction over the following 3-5 days
- News sentiment scoring to rank articles by relevance

---

## Author

Systems Engineer at a major Medical Co. by day, system builder/automator by night
