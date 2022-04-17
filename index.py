from python_bitvavo_api.bitvavo import Bitvavo
from time import sleep
import secret
import rsi
from colorama import Fore

bitvavo = Bitvavo({
  'APIKEY': secret.API_KEY,
  'APISECRET': secret.SECRET_KEY,
  'RESTURL': 'https://api.bitvavo.com/v2',
  'WSURL': 'wss://ws.bitvavo.com/v2/',
  'ACCESSWINDOW': 10000,
  'DEBUGGING': False
})

# Array of all tradeable assets
assets = []

def get_balance():
    response = bitvavo.balance({})
    for x in response:
        if x["symbol"] == "EUR":
            balance = x["available"]
            int(balance)
            return balance

def tradeAble():
    # List all listed assets
    markets = bitvavo.markets({})
    for x in markets:
        # Check if the asset is tradeable
        if x["status"] == "trading":
            # Check if quote is EUR
            if x["quote"] == "EUR":
                # Add tradeable asset to array
                assets.append(x["market"])

def trade():
    bal = get_balance()
    for x in assets:
        # Get asset
        _asset = x
        # Get RSI value
        _rsiValue = rsi.rsi(_asset)
        # Buy crypto
        if _rsiValue < 25:
            # Balance has to be above 5 EUR or equal
            if int(bal) >= 5:
                # List all prices
                price_asset = bitvavo.tickerPrice({})
                for market in price_asset:
                    if market['market'] == _asset:
                        price = market['price']
                        # Amount has been divided by 5, because that is the minimum amount to buy crypto
                        amount = 5 / float(price)
                        # Round by 4 decimals, because Bitvavo might give a error
                        amount = round(amount, 4)
                        response = bitvavo.placeOrder(_asset, 'buy', 'market', { 'amount': str(amount) })
                        print(response)
                        print(Fore.GREEN + "Bought:", _asset+Fore.RESET)
            else:
                print("Insufficient balance:", bal)
        # Sell crypto
        if _rsiValue > 75:
            response = bitvavo.balance({})
            for y in response:
                # Remove -EUR
                _crypto = _asset.rsplit('-', 1)[0]
                if y["symbol"] == _crypto:
                    asset_balance = y["available"]
                    if float(asset_balance) > 0:  
                        res = bitvavo.placeOrder(_asset, 'sell', 'market', { 'amount': asset_balance, })
                        print(res)
                        print(Fore.RED + "Sold:", _asset+Fore.RESET)


def startScript():
    print(Fore.YELLOW + "___Trading has been started___" + Fore.RESET)
    while True:
        limit = bitvavo.getRemainingLimit()
        print("You've left:", limit)
        # Check if limit is higher then 50, because overlapping 
        # that might result in a IP ban :(
        if limit > 50:
            tradeAble()
            trade() # This function will be created later. If so please uncomment this line.
            print("Waiting 100 seconds.")
            sleep(100)
        else:
            print("Limit has been reached")
            break


limit = bitvavo.getRemainingLimit()
print("You've left:", limit)
start = input("Do you want to start trading? y/n: ")

if start == "y":
    startScript()
else:
    print("No worries anytime you want!")