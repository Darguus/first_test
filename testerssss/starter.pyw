import binance_api as api
import strategy as strat
import tester
import gui
import ga


exchange = api.BinanceAPI(
    '',   # API Key
    ''    # Secret Key
)
symbol = 'BTCUSDT'
interval = '1h'   # https://python-binance.readthedocs.io/en/latest/constants.html

root = gui.GUI(
    exchange, symbol, interval,
    strat.Strategy(), ga.GA(), tester.Tester()
)

if __name__ == '__main__':
    root.mainloop()