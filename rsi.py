import yfinance as yf
import csv

blocked = []

def rsi(assetName):
    if assetName not in blocked:
        # [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]
        # Start to download the history of the asset
        crypto = yf.download(
            tickers = assetName,
            period = "90m",
            interval = "1m"
        )
        # Add crypto to csv file that we will be reading later.
        crypto["Adj Close"].to_csv("crypto.csv")
        adj_close = []
        rows = []
        # Open csv file
        with open("crypto.csv", 'r') as cryptofile:
            # creating a csv reader object
            csvreader = csv.reader(cryptofile)
            # extracting each data row one by one
            for row in csvreader:
                rows.append(row)
            num = csvreader.line_num
        for row in rows[:num]:
            adj_close.append(row[1])

        # Remove first row
        adj_close.pop(0)
        change = []
        i = -1
        for close in adj_close:
            close = float(adj_close[i]) - float(close) 
            i += 1
            change.append(close)

        # Check if the asset is downloaded
        if len(change) > 1:
            # Remove first row because we started the change at -1
            change.pop(0)
            upward_mvt = []
            downward_mvt = []
            # 
            for movement in change:
                if movement > 0:
                    upward_mvt.append(movement)
                else:
                    # Set downward movement back to positive
                    downward_mvt.append(-movement)
            
            # Get average of a array
            def average(lst):
                return sum(lst) / len(lst)

            upward_mvt_3 = []
            downward_mvt_3 = []
            # Check if upward_mvt does have data in it.
            if len(upward_mvt) > 1:
                # This is bad code I know, but it works so don't mind me if I do.
                upward_mvt_3.append(upward_mvt[0])
                upward_mvt_3.append(upward_mvt[1])
                upward_mvt_3.append(upward_mvt[2])
                downward_mvt_3.append(downward_mvt[0])
                downward_mvt_3.append(downward_mvt[1])
                downward_mvt_3.append(downward_mvt[2])

                upward_mvt.pop(0)
                upward_mvt.pop(0)
                upward_mvt.pop(0)
                downward_mvt.pop(0)
                downward_mvt.pop(0)
                downward_mvt.pop(0)

                avg_upward_mvt_3 = average(upward_mvt_3)
                avg_downward_mvt_3 = average(downward_mvt_3)
                # This part might be hard to understand for you.
                # Please open stuff/rsi.xlsx to find out what we did there.
                for x in upward_mvt_3:
                    avg_upward_mvt = (avg_upward_mvt_3 * 9 + x) / 10
                else:
                    boolUp = False
                    for x in upward_mvt:
                        if boolUp == False:
                            up_avg = (avg_upward_mvt * 9 + x) / 10
                            boolUp = True
                        else:
                            up_avg = (up_avg * 9 + x) / 10

                for y in downward_mvt_3:
                    avg_downward_mvt = (avg_downward_mvt_3 * 9 + y) / 10
                else:
                    boolDown = False
                    for u in downward_mvt:
                        if boolDown == False:
                            down_avg = (avg_downward_mvt * 9 + u) / 10
                            boolDown = True
                        else: 
                            down_avg = (down_avg * 9 + x) / 10
                # Calculate rs
                rs = up_avg / down_avg 
                # Calculate rsi
                rsi = 100-100/(rs + 1)
                print("Asset:", assetName, "is @", rsi)
                return rsi
            else:
                blocked.append(assetName)
                return 50
        else:
            blocked.append(assetName)
            return 50
    else:
        return 50


"""# x = ["BTC-EUR", "1INCH-EUR", "AAVE-EUR", "ADA-EUR", "ADX-EUR", "AE-EUR","AION-EUR","ZRX-EUR","ZIL-EUR","DOGE-EUR","YFI-EUR","XVG-EUR","XTZ-EUR","XRP-EUR","XLM-EUR","XEM-EUR","WTC-EUR","WAVES-EUR",]
x = ["BTC-EUR","ETH-EUR","USDT-EUR","BNB-EUR","USDC-EUR","XRP-EUR","SOL-EUR","ADA-EUR","AVAX-EUR","DOGE-EUR"]
i = 0
while True:
    i += 1
    print("Number:", i)
    for y in x:
        rsi(y)
    sleep(17)"""