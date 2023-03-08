import binance as bn
import pandas as pd
import time


class BinanceAPI():
    wrong_precision = ['BTCUSDT', 'BNBUSDT', 'ADAUSDT']

    def __init__(self, api_key, api_secret, test=False):
        self.client = bn.Client(
            api_key=api_key, api_secret=api_secret, testnet=test
        )

    def set_initial_data(self, interval, symbol):
        while True:
            try:
                self.data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.get_historical_klines(
                            symbol, interval,
                            klines_type= \
                                bn.enums.HistoricalKlinesType(2)
                        ),
                        columns=[
                            'timestamp', 'open', 'high', 'low',
                            'close', 'volume', 'close time',
                            'quote asset volume','number of trades',
                            'taker buy base asset volume',
                            'taker buy quote asset volume',
                            'can be ignored'
                        ]
                    )[:-1],
                    columns=[
                        'timestamp', 'open', 'high', 'low', 'close'
                    ]
                ).set_index('timestamp').astype(float)
                self.data.index = pd.to_datetime(
                    self.data.index, unit='ms', utc=True
                )
            except Exception as e:  
                time.sleep(0.5)
            else:
                break

    def update_data(self, interval, symbol):
        while True:
            try:
                last_data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.get_historical_klines(
                            symbol, interval, limit=2,
                            klines_type= \
                                bn.enums.HistoricalKlinesType(2)
                        ),
                        columns=[
                            'timestamp', 'open', 'high', 'low',
                            'close', 'volume', 'close time',
                            'quote asset volume','number of trades', 
                            'taker buy base asset volume',
                            'taker buy quote asset volume',
                            'can be ignored'
                        ]
                    )[:-1],
                    columns=[
                        'timestamp', 'open', 'high', 'low', 'close'
                    ]
                ).set_index('timestamp').astype(float)
                last_data.index = pd.to_datetime(
                    last_data.index, unit='ms', utc=True
                )
            except Exception as e:
                time.sleep(0.5)
            else:
                break
        if last_data.shape[0] == 1 and \
                last_data.index[-1] != self.data.index[-1]:
            self.data = pd.concat([self.data, last_data])
            return True

    def get_data(self, interval, symbol, start, end):
        while True:
            try:
                data = pd.DataFrame(
                    pd.DataFrame(
                        self.client.get_historical_klines(
                            symbol, interval, start, end,
                            klines_type= \
                                bn.enums.HistoricalKlinesType(2)
                        ),
                        columns=[
                            'timestamp', 'open', 'high', 'low',
                            'close', 'volume', 'close time',
                            'quote asset volume','number of trades',
                            'taker buy base asset volume',
                            'taker buy quote asset volume',
                            'can be ignored'
                        ]
                    )[:-1],
                    columns=[
                        'timestamp', 'open', 'high', 'low', 'close'
                    ]
                ).set_index('timestamp').astype(float)
                data.index = pd.to_datetime(
                    data.index, unit='ms', utc=True
                )
            except Exception as e:  
                time.sleep(0.5)
            else:
                break
        return data

    def price_precision(self, symbol):
        symbols_info = pd.DataFrame(
            self.client.futures_exchange_info()['symbols']
        ).set_index('symbol')
        return symbols_info.loc[symbol]['pricePrecision']

    def qty_precision(self, symbol):
        symbols_info = pd.DataFrame(
            self.client.futures_exchange_info()['symbols']
        ).set_index('symbol')
        return symbols_info.loc[symbol]['quantityPrecision']

    def futures_market_entry_long(
            self, symbol, order_size_type,
            margin_type, order_size, leverage):
        try:
            self.client.futures_change_margin_type(
                symbol=symbol, marginType=margin_type
            )
        except:
            pass
        try:
            leverage_info = self.client.futures_change_leverage(
                symbol=symbol, leverage=leverage
            )
            quote = self.client.futures_orderbook_ticker(symbol=symbol)
            price = float(quote['askPrice'])

            if order_size_type == 'percent':
                balance = pd.DataFrame(
                    self.client.futures_account_balance(symbol=symbol)
                ).set_index('asset')
                available_balance = float(
                    balance.loc['USDT']['balance']
                ) * leverage_info['leverage']
                qty = available_balance * order_size / 100 / price
            elif order_size_type == 'currency':
                available_balance = order_size * \
                    leverage_info['leverage']
                qty = available_balance / price
            
            symbols_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            price_precision = \
                symbols_info.loc[symbol]['pricePrecision']
            qty_precision = \
                symbols_info.loc[symbol]['quantityPrecision']
            qty = int(qty * 10 ** qty_precision) / 10 ** qty_precision
            deal_info = self.client.futures_create_order(
                symbol=symbol, side='BUY', type='MARKET', quantity=qty
            )
            avg_price = float(
                self.client.futures_get_order(
                    symbol=symbol, orderId=deal_info['orderId']
                )['avgPrice']
            )
            avg_price = int(
                avg_price * 10 ** price_precision
            ) / 10 ** price_precision
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Market buy order filled' + \
                '\nSymbol: ' + symbol + \
                '\nQuantity: ' + str(qty) + \
                '\nAvg price: ' + str(avg_price) + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_market_entry_short(
            self, symbol, order_size_type,
            margin_type, order_size, leverage):
        try:
            self.client.futures_change_margin_type(
                symbol=symbol, marginType=margin_type
            )
        except:
            pass
        try:
            leverage_info = self.client.futures_change_leverage(
                symbol=symbol, leverage=leverage
            )
            quote = self.client.futures_orderbook_ticker(symbol=symbol)
            price = float(quote['bidPrice'])

            if order_size_type == 'percent':
                balance = pd.DataFrame(
                    self.client.futures_account_balance(symbol=symbol)
                ).set_index('asset')
                available_balance = float(
                    balance.loc['USDT']['balance']
                ) * leverage_info['leverage']
                qty = available_balance * order_size / 100 / price
            elif order_size_type == 'currency':
                available_balance = order_size * \
                    leverage_info['leverage']
                qty = available_balance / price
            
            symbols_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            price_precision = \
                symbols_info.loc[symbol]['pricePrecision']
            qty_precision = \
                symbols_info.loc[symbol]['quantityPrecision']
            qty = int(qty * 10 ** qty_precision) / 10 ** qty_precision
            deal_info = self.client.futures_create_order(
                symbol=symbol, side='SELL', type='MARKET', quantity=qty
            )
            avg_price = float(
                self.client.futures_get_order(
                    symbol=symbol, orderId=deal_info['orderId']
                )['avgPrice']
            )
            avg_price = int(
                avg_price * 10 ** price_precision
            ) / 10 ** price_precision
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Market sell order filled' + \
                '\nSymbol: ' + symbol + \
                '\nQuantity: ' + str(qty) + \
                '\nAvg price: ' + str(avg_price) + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_limit_take_buy(self, symbol, order_size, price):
        try:
            qty = -float(
                pd.DataFrame(
                    self.client.futures_position_information()
                ).set_index('symbol').loc[symbol].loc['positionAmt']
            ) * order_size / 100
            exchange_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            symbol_info = exchange_info.loc[symbol]
            qty = int(
                qty * 10 ** symbol_info['quantityPrecision']
            ) / 10 ** symbol_info['quantityPrecision']

            if symbol in self.wrong_precision:
                price = int(
                    price * 10 ** (symbol_info['pricePrecision'] - 1)
                ) / 10 ** (symbol_info['pricePrecision'] - 1)
            else:
                price = int(
                    price * 10 ** symbol_info['pricePrecision']
                ) / 10 ** symbol_info['pricePrecision']

            deal_info = self.client.futures_create_order(
                symbol=symbol,
                side='BUY',
                type='LIMIT',
                timeInForce='GTC',
                quantity=qty,
                reduceOnly='true',
                price=price
            )
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Limit buy order activated' + \
                '\nSymbol: ' + deal_info['symbol'] + \
                '\nQuantity: ' + deal_info['origQty'] + \
                '\nPrice: ' + deal_info['price'] + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_limit_take_sell(self, symbol, order_size, price):
        try:
            qty = float(
                pd.DataFrame(
                    self.client.futures_position_information()
                ).set_index('symbol').loc[symbol].loc['positionAmt']
            ) * order_size / 100
            exchange_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            symbol_info = exchange_info.loc[symbol]
            qty = int(
                qty * 10 ** symbol_info['quantityPrecision']
            ) / 10 ** symbol_info['quantityPrecision']

            if symbol in self.wrong_precision:
                price = int(
                    price * 10 ** (symbol_info['pricePrecision'] - 1)
                ) / 10 ** (symbol_info['pricePrecision'] - 1)
            else:
                price = int(
                    price * 10 ** symbol_info['pricePrecision']
                ) / 10 ** symbol_info['pricePrecision']

            deal_info = self.client.futures_create_order(
                symbol=symbol,
                side='SELL',
                type='LIMIT',
                timeInForce='GTC',
                quantity=qty,
                reduceOnly='true',
                price=price
            )
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Limit sell order activated' + \
                '\nSymbol: ' + deal_info['symbol'] + \
                '\nQuantity: ' + deal_info['origQty'] + \
                '\nPrice: ' + deal_info['price'] + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_market_stop_buy(self, symbol, price):
        try:
            qty = -float(
                pd.DataFrame(
                    self.client.futures_position_information()
                ).set_index('symbol').loc[symbol].loc['positionAmt']
            )
            exchange_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            symbol_info = exchange_info.loc[symbol]

            if symbol in self.wrong_precision:
                price = int(
                    price * 10 ** (symbol_info['pricePrecision'] - 1)
                ) / 10 ** (symbol_info['pricePrecision'] - 1)
            else:
                price = int(
                    price * 10 ** symbol_info['pricePrecision']
                ) / 10 ** symbol_info['pricePrecision']

            deal_info = self.client.futures_create_order(
                symbol=symbol,
                side='BUY',
                type='STOP_MARKET',
                timeInForce='GTC',
                quantity=qty,
                reduceOnly='true',
                stopPrice=price
            )
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Stop buy order activated' + \
                '\nSymbol: ' + deal_info['symbol'] + \
                '\nQuantity: ' + deal_info['origQty'] + \
                '\nPrice: ' + str(price) + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_market_stop_sell(self, symbol, price):
        try:
            qty = float(
                pd.DataFrame(
                    self.client.futures_position_information()
                ).set_index('symbol').loc[symbol].loc['positionAmt']
            )
            exchange_info = pd.DataFrame(
                self.client.futures_exchange_info()['symbols']
            ).set_index('symbol')
            symbol_info = exchange_info.loc[symbol]

            if symbol in self.wrong_precision:
                price = int(
                    price * 10 ** (symbol_info['pricePrecision'] - 1)
                ) / 10 ** (symbol_info['pricePrecision'] - 1)
            else:
                price = int(
                    price * 10 ** symbol_info['pricePrecision']
                ) / 10 ** symbol_info['pricePrecision']

            deal_info = self.client.futures_create_order(
                symbol=symbol,
                side='SELL',
                type='STOP_MARKET',
                timeInForce='GTC',
                quantity=qty,
                reduceOnly='true',
                stopPrice=price
            )
            t = pd.to_datetime(
                    deal_info['updateTime'], unit='ms'
            ).strftime('%Y-%m-%d %H:%M')
            result = 'Stop sell order activated' + \
                '\nSymbol: ' + deal_info['symbol'] + \
                '\nQuantity: ' + deal_info['origQty'] + \
                '\nPrice: ' + str(price) + \
                '\nTime: ' + t + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_cancel_orders(self, symbol):
        try:
            self.client.futures_cancel_all_open_orders(
                symbol=symbol,
                countdownTime=0
            )
            result = 'Canceled active orders\nfor the pair ' + \
                symbol + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result

    def futures_cancel_stop(self, symbol):
        try:
            orders = self.client.futures_get_open_orders(symbol=symbol)
            stop_id = None

            for i in orders:
                if i['type'] == 'STOP_MARKET':
                    stop_id = i['orderId']

            self.client.futures_cancel_order(
                symbol=symbol, orderId=stop_id
            )
            result = 'Canceled active stop\nfor the pair ' + \
                symbol + '\n\n'
        except Exception as e:
            t = time.strftime('%Y-%m-%d %H:%M', time.gmtime())
            result = str(e) + '\nTime: ' + t + '\n\n'
            return result
        else:
            return result