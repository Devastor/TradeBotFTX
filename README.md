# TradeBotFTX
Simple trade bot for FTX. Get signals from tradingview 1D timeframe

What you need to start?

1. Download chromedriver (or other) for your system from https://chromedriver.chromium.org/downloads and put it in one folder with bot script
2. Create account at https://ftx.com/
3. Create API key for trading in your account
4. Create file data_FTX.txt and paste your API keys here like that, line by line
    API
    SECRET
5. Set CURR1 and CURR2 to your prefer currency for trading
6. Launch bot and enjoy DAY-timeframe autotrading

Some things:
1. Bot will trade on ALL your balance on current pair
2. You'll probably need to install 'selenium' and 'ftx' libraries (for ex. by 'pip install selenium ftx' command in console)
3. Advice for future: get your own VPS and put bot there for 24h auto-trading

