import datetime                                                                                                 # import:  time and date library
from selenium import webdriver as DevastorWebDriver                                                             # import:  webdriver library
from selenium.webdriver.common.by import By                                                                     # import:  DOM-locator library
import time as DevastorTime                                                                                     # import:  time library for sleep function
import os                                                                                                       # import:  system library
from ftx import FtxClient                                                                                       # import:  ftx client library
api_key = '9VWWRq2qHa34jO0Gc7QNm1c6_WBRTSl7K-KEwbS2'                                                            # API public key
api_secret = 'G18attHNR5YEN3GNixkckHastgZBlm96m7bb4zdK'                                                         # API secret ley
client = FtxClient(api_key=api_key, api_secret=api_secret)                                                      # FTX client variable
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))                                                       # root path variable
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")                                                         # webdriver emulator lolation
devastorOptions = DevastorWebDriver.ChromeOptions()                                                             # webdriver options init
devastorOptions.add_argument('--headless')                                                                      # headless mod enable
devastorOptions.add_argument("--disable-dev-shm-usage")                                                         # overcome limited resource problems
devastorOptions.add_argument("--no-sandbox")                                                                    # bypass OS security model
devastorOptions.add_argument("--window-size=1920,1080")
devastorOptions.add_argument("--start-maximized")
devastorBrowser = DevastorWebDriver.Chrome(options=devastorOptions, executable_path=DRIVER_BIN)                 # webdriver emulator variable
devastorBrowser.implicitly_wait(1)                                                                              # webdriver wait interval
CURR1 = 'FTT'                                                                                                   # trade currency
CURR2 = 'USDT'                                                                                                  # wallet currency
symbol = CURR1 + '/' + CURR2                                                                                    # pair symbol
lastSignal = 'HOLD'                                                                                             # last buy/sell signal variable
nowTime = datetime.datetime.now()                                                                               # current time variable
oldTime = -1                                                                                                    # previous time variable
markets = client.get_markets()                                                                                  # get markets info
priceStep = 0                                                                                                   # reset price step to zero
startBalance = client.get_account_info()['totalAccountValue']                                                   # start balance value
profit = 0                                                                                                      # profit value
hourCounter = 0                                                                                                 # counter of passed hours
def recreateDriver():
    global devastorBrowser
    try:
        devastorBrowser.quit()
    except:
        try:
            devastorBrowser.close()
        except:
            pass
    PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))  # root path variable
    DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")  # webdriver emulator lolation
    devastorOptions = DevastorWebDriver.ChromeOptions()  # webdriver options init
    devastorOptions.add_argument('--headless')  # headless mod enable
    devastorOptions.add_argument("--disable-dev-shm-usage")  # overcome limited resource problems
    devastorOptions.add_argument("--no-sandbox")  # bypass OS security model
    devastorOptions.add_argument("--window-size=1920,1080")
    devastorOptions.add_argument("--start-maximized")
    devastorBrowser = DevastorWebDriver.Chrome(options=devastorOptions,
                                               executable_path=DRIVER_BIN)  # webdriver emulator variable
    devastorBrowser.implicitly_wait(1)
for market in markets:                                                                                          # cycle by all markets
    if market['name'] == 'FTT/USDT':                                                                            # if found needed market
        priceStep = market['priceIncrement']                                                                    # set price step value
while True:                                                                                                     # infinite main loop
    nowTime = datetime.datetime.now().hour                                                                      # update current time
    if oldTime != nowTime:                                                                                      # if hour has passed
        oldTime = nowTime                                                                                       # update old time var
        devastorSignal = 'HOLD'                                                                                 # reset signal to 'HOLD'
        balance = client.get_account_info()['totalAccountValue']                                                # get avaliable balance
        profit = float(startBalance) - float(balance)
        if profit != 0 and hourCounter > 0:
            print('PROFIT:', profit, 'USDT |', str(int((profit / startBalance) * 100)), '% |', '(per month:', str(int(((profit / startBalance) * 100)/hourCounter) * 720), '% )')
        predict_STAT = '-'
        try:                                                                                                    # try block for html page get check
            devastorBrowser.get('https://ru.tradingview.com/symbols/' + symbol.replace('/', '') + '/technicals')# get trading view stats page
            DevastorTime.sleep(3)                                                                               # pause for page load
            devastorBrowser.find_element(By.ID, '1h').click()                                                   # set 1 hour prediction
            devastorBrowser.find_element(By.ID, '1h').click()                                                   # set 1 hour prediction
            DevastorTime.sleep(3)                                                                               # pause for page load
            predict_element_address = "//*[@class='speedometerWrapper-DPgs-R4s summary-DPgs-R4s']"              # find predict element
            predict_STAT = devastorBrowser.find_element(By.XPATH, predict_element_address).find_elements(By.TAG_NAME, 'span')[10].text.upper()
            if predict_STAT == 'ПРОДАВАТЬ' or predict_STAT == 'АКТИВНО ПРОДАВАТЬ': devastorSignal = 'SELL'      # set signal to sell
            if predict_STAT == 'ПОКУПАТЬ' or predict_STAT == 'АКТИВНО ПОКУПАТЬ': devastorSignal = 'BUY'         # set signal to buy
            #devastorBrowser.quit()                                                                              # close browser for memory safe
        except Exception as e:
            print('SIGNAL ERR:', e)
            if 'Connection refused' in str(e):
                recreateDriver()
            devastorSignal = 'HOLD'                                                                             # reset signal to 'HOLD'
        print('SIGNAL:', devastorSignal, predict_STAT)
        if devastorSignal == 'BUY' and lastSignal != 'BUY':                                                     # if we get 'BUY' signal after another one
            try:                                                                                                # try placing buy order
                actual_price = client.get_market(symbol)['price']                                               # get current price
                quantity = ((float(balance) / float(actual_price)) // priceStep) *  priceStep                   # calculate quantity
                client.place_order(symbol, 'buy', actual_price, quantity)                                       # place order to by max amount
                lastSignal = 'BUY'                                                                              # set last signal to 'BUY
                print('ACTION: BUY\n', 'CURR:', CURR1, '\nPRICE:', actual_price)
            except Exception as e:
                print('BUY ERR:', e)
        if devastorSignal == 'SELL' and lastSignal != 'SELL':                                                   # if we get 'SELL' signal after another one
            try:                                                                                                # try placing sell order
                balances = client.get_balances()                                                                # get balances of all curr
                curr1_balance = 0                                                                               # reset trade currency balance to zero
                for bal in balances:                                                                            # cycle by all balances
                    if bal['coin'] == CURR1: curr1_balance = float(bal['total'])                                # if found needed curr, set trade curr balance value
                actual_price = client.get_market(symbol)['price']                                               # get actual ticker price
                client.place_order(symbol, 'sell', actual_price, (curr1_balance // priceStep) * priceStep)      # place sell order for all curr1
                lastSignal = 'SELL'                                                                             # reset last signal
                print('ACTION: SELL\n', 'CURR:', CURR1, '\nPRICE:', actual_price)
            except Exception as e:
                print('SELL ERR:', e)
        hourCounter += 1