import matplotlib.markers as markers
import mplfinance as mpf
import functions as f
import pandas as pd
import numpy as np


class Strategy():
    # risk-management (backtesting / real trading)
    order_size_type = 'percent'   # 'percent' or 'currency'
    margin_type = 'ISOLATED'   # 'ISOLATED' or 'CROSSED'
    order_size = 99
    leverage = 1

    # risk-management (backtesting)
    initial_capital = 10000.0
    min_capital = 100.0
    commission = 0.075

    # trading
    stop_type = 1
    stop = 0.7
    trail_stop = 2
    take_percent = [3.0, 5.7, 9.0, 11.7, 14.8]
    take_volume = [10.0, 35.0, 25.0, 10.0, 20.0]

    # supertrend
    st_atr_period = 3
    st_factor = 21.8
    st_upper_band = 6.2
    st_lower_band = 3.4

    # RSI
    rsi_length = 6
    rsi_long_upper_bound = 30.0
    rsi_long_lower_bound = 22.0
    rsi_short_upper_bound = 76.0
    rsi_short_lower_bound = 54.0

    # RSI filter
    filter = 0
    ma_length = 18
    bb_mult = 1.5
    bb_long_bound = 39.0
    bb_short_bound = 76.0

    # addplot style
    uptrend_color = '#006400'
    downtrend_color = '#8B0000'
    take_price_color = '#00FF00'
    stop_price_color = '#FF0000'
    rsi_color = '#FFA500'
    rsi_long_bounds_color = '#228B22'
    rsi_short_bounds_color = '#CD5C5C'
    filter_color = '#000080'
    long_marker_color = '#008000'
    short_marker_color = '#FF0000'
    entry_marker = markers.CARETRIGHT
    exit_marker = markers.CARETLEFT
    marker_size = 80

    def backtest(self, exchange, data, symbol):
        # risk-management
        self.price_precision = exchange.price_precision(symbol)
        self.qty_precision = exchange.qty_precision(symbol)
        self.equity = self.initial_capital
        self.position_avg_price = np.nan
        self.liquidation_price = np.nan
        self.initial_position = np.nan
        self.position_size = np.nan
        self.entry_date = np.nan
        self.net_profit = np.nan

        self.take_price = [np.nan] * 5
        self.qty_take = [np.nan] * 5
        self.stop_price = np.nan
        self.stop_moved = False
        
        self.liquidations = {
            1: 99.5,
            2: 49.5,
            3: 32.8,
            4: 24.5,
            5: 19.5,
            6: 16.1,
            7: 13.8,
            8: 12.0,
            9: 10.6,
            10: 9.5,
            11: 8.6,
            12: 7.8,
            13: 7.2,
            14: 6.6,
            15: 6.2,
            16: 5.7,
            17: 5.4,
            18: 5.0,
            19: 4.8,
            20: 4.5,
        }

        # trade log
        self.log = pd.DataFrame(
            columns=[
                'deal_type', 'entry_date', 'exit_date',
                'position_avg_price', 'exit_price', 'position_size',
                'pnl', 'pnl_per', 'commission'
            ]
        )

        # signals
        self.entry_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.stop_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_1_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_2_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_3_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_4_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_5_long_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.entry_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.stop_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_1_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_2_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_3_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_4_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_5_short_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.shift_stop = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.exit_signals = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )

        # indicators
        self.super_trend = f.supertrend(
            data['high'], data['low'], data['close'],
            self.st_factor, self.st_atr_period
        )
        self.rsi = f.rsi(data['close'], self.rsi_length)
        self.change_stop = f.change(self.super_trend[4])
        self.ma_rsi = f.sma(self.rsi[4], self.ma_length)
        self.dev = f.stdev(self.rsi[4], self.ma_length)
        self.bb_upper_band = self.ma_rsi + self.dev * self.bb_mult
        self.bb_lower_band = self.ma_rsi - self.dev * self.bb_mult

        self.stop_line = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_line_1 = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_line_2 = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_line_3 = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_line_4 = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.take_line_5 = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.uptrend = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.downtrend = pd.Series(
            np.full(data.shape[0], np.nan), data.index
        )
        self.bb_long_bound_line = pd.Series(
            np.full(data.shape[0], self.bb_long_bound), data.index
        )
        self.bb_short_bound_line = pd.Series(
            np.full(data.shape[0], self.bb_short_bound), data.index
        )
        self.rsi_long_upper_bound_line = pd.Series(
            np.full(data.shape[0], self.rsi_long_upper_bound),
            data.index
        )
        self.rsi_long_lower_bound_line = pd.Series(
            np.full(data.shape[0], self.rsi_long_lower_bound),
            data.index
        )
        self.rsi_short_upper_bound_line = pd.Series(
            np.full(data.shape[0], self.rsi_short_upper_bound),
            data.index
        )
        self.rsi_short_lower_bound_line = pd.Series(
            np.full(data.shape[0], self.rsi_short_lower_bound),
            data.index
        )

        self.long = False
        self.short = False
        
        for i in range(data.shape[0]):
            # check of liquidation
            if self.long and data['low'][i] <= self.liquidation_price:
                self.long = False

                total_commission = round(
                    (self.position_size * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.position_size * self.liquidation_price \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.position_size * self.liquidation_price \
                        - (self.position_size * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.position_size * \
                        self.position_avg_price) + pnl) \
                        / (self.position_size * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price,
                        self.liquidation_price,
                        round(self.position_size, 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.stop_long_signals.iloc[i] = \
                    self.liquidation_price
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.entry_date = np.nan
                self.position_size = np.nan
                self.initial_position = np.nan
                self.liquidation_price = np.nan
                self.position_avg_price = np.nan 

                self.take_price[0] = np.nan
                self.take_price[1] = np.nan
                self.take_price[2] = np.nan
                self.take_price[3] = np.nan
                self.take_price[4] = np.nan
                self.qty_take[0] = np.nan
                self.qty_take[1] = np.nan
                self.qty_take[2] = np.nan
                self.qty_take[3] = np.nan
                self.qty_take[4] = np.nan

                self.stop_price = np.nan
                self.stop_moved = False

            if self.short and data['high'][i] >= self.liquidation_price:
                self.short = False

                total_commission = round(
                    (self.position_size * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.position_size * self.liquidation_price \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price \
                        - self.liquidation_price) \
                        * self.position_size) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.position_size * \
                        self.position_avg_price) + pnl) \
                        / (self.position_size * \
                        self.position_avg_price) - 1) * 100,
                    2
                )
                log_row = pd.DataFrame(
                    data=[[
                        'short', 
                        self.entry_date.strftime('%Y-%m-%d %H:%M'), 
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price,
                        self.liquidation_price,
                        round(self.position_size, 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.stop_short_signals.iloc[i] = \
                    self.liquidation_price
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.entry_date = np.nan
                self.position_size = np.nan
                self.initial_position = np.nan
                self.liquidation_price = np.nan
                self.position_avg_price = np.nan

                self.take_price[0] = np.nan
                self.take_price[1] = np.nan
                self.take_price[2] = np.nan
                self.take_price[3] = np.nan
                self.take_price[4] = np.nan
                self.position_size = np.nan
                self.qty_take[0] = np.nan
                self.qty_take[1] = np.nan
                self.qty_take[2] = np.nan
                self.qty_take[3] = np.nan
                self.qty_take[4] = np.nan

                self.stop_price = np.nan
                self.stop_moved = False

            # trading logic (longs)
            if self.long and data['low'][i] <= self.stop_price:
                self.long = False

                total_commission = round(
                    (self.position_size * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.position_size * self.stop_price \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.position_size * self.stop_price \
                        - (self.position_size * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.position_size * \
                        self.position_avg_price) + pnl) \
                        / (self.position_size * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.stop_price,
                        round(self.position_size, 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.stop_long_signals.iloc[i] = self.stop_price
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.entry_date = np.nan
                self.position_size = np.nan
                self.initial_position = np.nan
                self.liquidation_price = np.nan
                self.position_avg_price = np.nan 

                self.take_price[0] = np.nan
                self.take_price[1] = np.nan
                self.take_price[2] = np.nan
                self.take_price[3] = np.nan
                self.take_price[4] = np.nan
                self.qty_take[0] = np.nan
                self.qty_take[1] = np.nan
                self.qty_take[2] = np.nan
                self.qty_take[3] = np.nan
                self.qty_take[4] = np.nan

                self.stop_price = np.nan
                self.stop_moved = False
                
            if self.long:
                if self.stop_type == 1 and \
                        self.change_stop[i] and \
                        self.super_trend[5][i] < 0 and \
                        ((self.super_trend[4][i] * \
                        (100 - self.stop) / 100) > self.stop_price):
                    self.stop_price = \
                        self.super_trend[4][i] * \
                        (100 - self.stop) / 100
                    self.stop_price = int(
                        self.stop_price * 10 ** self.price_precision
                    ) / 10 ** self.price_precision
                    self.shift_stop.iloc[i] = data['close'][i]
                elif self.stop_type == 2 and \
                        not self.stop_moved and \
                        ((self.trail_stop == 1 and \
                        data['high'][i] > self.take_price[0]) or \
                        (self.trail_stop == 2 and \
                        data['high'][i] > self.take_price[1]) or \
                        (self.trail_stop == 3 and \
                        data['high'][i] > self.take_price[2]) or \
                        (self.trail_stop == 4 and \
                        data['high'][i] > self.take_price[3]) or \
                        (self.trail_stop == 5 and \
                        data['high'][i] > self.take_price[4])):
                    self.stop_moved = True
                    self.stop_price = self.position_avg_price
                    self.shift_stop.iloc[i] = data['close'][i]

            if self.long and data['high'][i] >= self.take_price[0] \
                    and not pd.isna(self.take_price[0]):
                total_commission = round(
                    (self.qty_take[0] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[0] * self.take_price[0] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.qty_take[0] * self.take_price[0] \
                        - (self.qty_take[0] * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[0] * self.position_avg_price) + \
                    pnl) / (self.qty_take[0] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[0],
                        self.qty_take[0], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_1_long_signals.iloc[i] = self.take_price[0]

                self.equity += pnl
                self.position_size -= self.qty_take[0]
                self.take_price[0] = np.nan
                self.qty_take[0] = np.nan

            if self.long and data['high'][i] >= self.take_price[1] \
                    and not pd.isna(self.take_price[1]):
                total_commission = round(
                    (self.qty_take[1] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[1] * self.take_price[1] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.qty_take[1] * self.take_price[1] \
                        - (self.qty_take[1] * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[1] * self.position_avg_price) + \
                    pnl) / (self.qty_take[1] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[1],
                        self.qty_take[1], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_2_long_signals.iloc[i] = self.take_price[1]

                self.equity += pnl
                self.position_size -= self.qty_take[1]
                self.take_price[1] = np.nan
                self.qty_take[1] = np.nan

            if self.long and data['high'][i] >= self.take_price[2] \
                    and not pd.isna(self.take_price[2]):
                total_commission = round(
                    (self.qty_take[2] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[2] * self.take_price[2] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.qty_take[2] * self.take_price[2] \
                        - (self.qty_take[2] * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[2] * self.position_avg_price) + \
                    pnl) / (self.qty_take[2] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[2],
                        self.qty_take[2], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_3_long_signals.iloc[i] = self.take_price[2]

                self.equity += pnl
                self.position_size -= self.qty_take[2]
                self.take_price[2] = np.nan
                self.qty_take[2] = np.nan

            if self.long and data['high'][i] >= self.take_price[3] \
                    and not pd.isna(self.take_price[3]):
                total_commission = round(
                    (self.qty_take[3] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[3] * self.take_price[3] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.qty_take[3] * self.take_price[3] \
                        - (self.qty_take[3] * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[3] * self.position_avg_price) + \
                    pnl) / (self.qty_take[3] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[3],
                        self.qty_take[3], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_4_long_signals.iloc[i] = self.take_price[3]

                self.equity += pnl
                self.position_size -= self.qty_take[3]
                self.take_price[3] = np.nan
                self.qty_take[3] = np.nan

            if self.long and data['high'][i] >= self.take_price[4] \
                    and not pd.isna(self.take_price[4]):
                total_commission = round(
                    (self.qty_take[4] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[4] * self.take_price[4] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    self.qty_take[4] * self.take_price[4] \
                        - (self.qty_take[4] * \
                        self.position_avg_price) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[4] * self.position_avg_price) + \
                    pnl) / (self.qty_take[4] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'long',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[4],
                        round(self.qty_take[4], 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_5_long_signals.iloc[i] = self.take_price[4]
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.position_size = np.nan
                self.take_price[4] = np.nan
                self.qty_take[4] = np.nan
                self.stop_price = np.nan
                self.stop_moved = False
                self.long = False

            if self.super_trend[5][i] < 0 and \
                    (data['close'][i] / \
                    self.super_trend[4][i] - 1) * 100 > \
                    self.st_lower_band and \
                    abs((self.super_trend[4][i] / \
                    data['close'][i] - 1) * \
                    100) < self.st_upper_band and \
                    self.rsi[4][i] < self.rsi_long_upper_bound and \
                    self.rsi[4][i] > self.rsi_long_lower_bound and \
                    not self.long and not self.short and \
                    (self.bb_upper_band[i] < self.bb_long_bound \
                    if self.filter else True) and \
                    self.equity >= self.min_capital:
                self.long = True

                self.position_avg_price = data['close'][i]

                if self.order_size_type == 'percent':
                    self.initial_position = \
                        self.equity * self.leverage \
                        * (self.order_size / 100.0)
                    self.position_size = self.initial_position \
                        * (1 - self.commission / 100) \
                        / self.position_avg_price
                elif self.order_size_type == 'currency':
                    self.initial_position = \
                        self.order_size * self.leverage
                    self.position_size = self.initial_position \
                        * (1 - self.commission / 100) \
                        / self.position_avg_price

                self.position_size = int(
                    self.position_size * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.initial_position = \
                    self.position_size * self.position_avg_price
                self.entry_date = data.index[i]
                self.entry_long_signals.iloc[i] = data['close'][i]

                self.liquidation_price = \
                    self.position_avg_price * (100 - \
                    self.liquidations[self.leverage]) / 100
                self.stop_price = self.super_trend[4][i] * \
                    (100 - self.stop) / 100
                self.take_price[0] = data['close'][i] * \
                    (100 + self.take_percent[0]) / 100
                self.take_price[1] = data['close'][i] * \
                    (100 + self.take_percent[1]) / 100
                self.take_price[2] = data['close'][i] * \
                    (100 + self.take_percent[2]) / 100
                self.take_price[3] = data['close'][i] * \
                    (100 + self.take_percent[3]) / 100
                self.take_price[4] = data['close'][i] * \
                    (100 + self.take_percent[4]) / 100

                self.qty_take[0] = self.position_size * \
                    self.take_volume[0] / 100
                self.qty_take[1] = self.position_size * \
                    self.take_volume[1] / 100
                self.qty_take[2] = self.position_size * \
                    self.take_volume[2] / 100
                self.qty_take[3] = self.position_size * \
                    self.take_volume[3] / 100
                self.qty_take[4] = self.position_size * \
                    self.take_volume[4] / 100

                self.liquidation_price = int(
                    self.liquidation_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.stop_price = int(
                    self.stop_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[0] = int(
                    self.take_price[0] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[1] = int(
                    self.take_price[1] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[2] = int(
                    self.take_price[2] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[3] = int(
                    self.take_price[3] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[4] = int(
                    self.take_price[4] * 10 ** self.price_precision
                ) / 10 ** self.price_precision

                self.qty_take[0] = int(
                    self.qty_take[0] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[1] = int(
                    self.qty_take[1] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[2] = int(
                    self.qty_take[2] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[3] = int(
                    self.qty_take[3] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[4] = self.position_size - \
                    (self.qty_take[0] + self.qty_take[1] + \
                    self.qty_take[2] + self.qty_take[3])

            # trading logic (shorts)
            if self.short and data['high'][i] >= self.stop_price:
                self.short = False

                total_commission = round(
                    (self.position_size * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.position_size * self.stop_price \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price \
                        - self.stop_price) \
                        * self.position_size) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.position_size * \
                        self.position_avg_price) + pnl) \
                        / (self.position_size * \
                        self.position_avg_price) - 1) * 100,
                    2
                )
                log_row = pd.DataFrame(
                    data=[[
                        'short', 
                        self.entry_date.strftime('%Y-%m-%d %H:%M'), 
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price,
                        self.stop_price,
                        round(self.position_size, 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.stop_short_signals.iloc[i] = self.stop_price
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.entry_date = np.nan
                self.position_size = np.nan
                self.initial_position = np.nan
                self.liquidation_price = np.nan
                self.position_avg_price = np.nan

                self.take_price[0] = np.nan
                self.take_price[1] = np.nan
                self.take_price[2] = np.nan
                self.take_price[3] = np.nan
                self.take_price[4] = np.nan
                self.position_size = np.nan
                self.qty_take[0] = np.nan
                self.qty_take[1] = np.nan
                self.qty_take[2] = np.nan
                self.qty_take[3] = np.nan
                self.qty_take[4] = np.nan

                self.stop_price = np.nan
                self.stop_moved = False    

            if self.short:
                if self.stop_type == 1 and \
                        self.change_stop[i] and \
                        self.super_trend[5][i] > 0 and \
                        ((self.super_trend[4][i] * \
                        (100 + self.stop) / 100) < self.stop_price):
                    self.stop_price = \
                        self.super_trend[4][i] * \
                        (100 + self.stop) / 100
                    self.stop_price = int(
                        self.stop_price * 10 ** self.price_precision
                    ) / 10 ** self.price_precision
                    self.shift_stop.iloc[i] = data['close'][i]
                elif self.stop_type == 2 and \
                        not self.stop_moved and \
                        ((self.trail_stop == 1 and \
                        data['low'][i] < self.take_price[0]) or \
                        (self.trail_stop == 2 and \
                        data['low'][i] < self.take_price[1]) or \
                        (self.trail_stop == 3 and \
                        data['low'][i] < self.take_price[2]) or \
                        (self.trail_stop == 4 and \
                        data['low'][i] < self.take_price[3]) or \
                        (self.trail_stop == 5 and \
                        data['low'][i] < self.take_price[4])):
                    self.stop_moved = True
                    self.stop_price = self.position_avg_price
                    self.shift_stop.iloc[i] = data['close'][i]

            if self.short and data['low'][i] <= self.take_price[0] \
                    and not pd.isna(self.take_price[0]):
                total_commission = round(
                    (self.qty_take[0] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[0] * self.take_price[0] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price - self.take_price[0]) \
                        * self.qty_take[0]) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[0] * self.position_avg_price) + \
                    pnl) / (self.qty_take[0] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )
                log_row = pd.DataFrame(
                    data=[[
                        'short',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[0],
                        self.qty_take[0], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_1_short_signals.iloc[i] = self.take_price[0]

                self.equity += pnl
                self.position_size -= self.qty_take[0]
                self.take_price[0] = np.nan
                self.qty_take[0] = np.nan

            if self.short and data['low'][i] <= self.take_price[1] \
                    and not pd.isna(self.take_price[1]):
                total_commission = round(
                    (self.qty_take[1] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[1] * self.take_price[1] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price - self.take_price[1]) \
                        * self.qty_take[1]) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[1] * self.position_avg_price) + \
                    pnl) / (self.qty_take[1] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'short',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[1],
                        self.qty_take[1], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_2_short_signals.iloc[i] = self.take_price[1]

                self.equity += pnl
                self.position_size -= self.qty_take[1]
                self.take_price[1] = np.nan
                self.qty_take[1] = np.nan      

            if self.short and data['low'][i] <= self.take_price[2] \
                    and not pd.isna(self.take_price[2]):
                total_commission = round(
                    (self.qty_take[2] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[2] * self.take_price[2] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price - self.take_price[2]) \
                        * self.qty_take[2]) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[2] * self.position_avg_price) + \
                    pnl) / (self.qty_take[2] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'short',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[2],
                        self.qty_take[2], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_3_short_signals.iloc[i] = self.take_price[2]

                self.equity += pnl
                self.position_size -= self.qty_take[2]
                self.take_price[2] = np.nan
                self.qty_take[2] = np.nan

            if self.short and data['low'][i] <= self.take_price[3] \
                    and not pd.isna(self.take_price[3]):
                total_commission = round(
                    (self.qty_take[3] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[3] * self.take_price[3] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price - self.take_price[3]) \
                        * self.qty_take[3]) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[3] * self.position_avg_price) + \
                    pnl) / (self.qty_take[3] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'short',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[3],
                        self.qty_take[3], pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_4_short_signals.iloc[i] = self.take_price[3]

                self.equity += pnl
                self.position_size -= self.qty_take[3]
                self.take_price[3] = np.nan
                self.qty_take[3] = np.nan     

            if self.short and data['low'][i] <= self.take_price[4] \
                    and not pd.isna(self.take_price[4]):
                total_commission = round(
                    (self.qty_take[4] * self.position_avg_price \
                        * self.commission / 100) + \
                        (self.qty_take[4] * self.take_price[4] \
                        * self.commission / 100),
                    2
                )
                pnl = round(
                    ((self.position_avg_price - self.take_price[4]) \
                        * self.qty_take[4]) - total_commission,
                    2
                )
                pnl_per = round(
                    (((self.qty_take[4] * self.position_avg_price) + \
                    pnl) / (self.qty_take[4] * \
                        self.position_avg_price) - 1) * 100,
                    2
                )

                log_row = pd.DataFrame(
                    data=[[
                        'short',
                        self.entry_date.strftime('%Y-%m-%d %H:%M'),
                        data.index[i].strftime('%Y-%m-%d %H:%M'),
                        self.position_avg_price, self.take_price[4],
                        round(self.qty_take[4], 8), pnl, pnl_per,
                        total_commission
                    ]],
                    columns=[
                        'deal_type', 'entry_date', 'exit_date',
                        'position_avg_price', 'exit_price',
                        'position_size', 'pnl',
                        'pnl_per', 'commission'
                    ]
                )
                self.log = pd.concat(
                    [self.log, log_row], ignore_index=True
                )

                self.take_5_short_signals.iloc[i] = self.take_price[4]
                self.exit_signals.iloc[i] = data['close'][i]

                self.equity += pnl
                self.position_size = np.nan
                self.take_price[4] = np.nan
                self.qty_take[4] = np.nan
                self.stop_price = np.nan
                self.stop_moved = False
                self.short = False

            if self.super_trend[5][i] > 0 and \
                    (self.super_trend[4][i] / \
                    data['close'][i] - 1) * 100 > \
                    self.st_lower_band and \
                    (self.super_trend[4][i] / \
                    data['close'][i] - 1) * 100 < \
                    self.st_upper_band and \
                    self.rsi[4][i] < self.rsi_short_upper_bound and \
                    self.rsi[4][i] > self.rsi_short_lower_bound and \
                    not self.long and not self.short and \
                    (self.bb_lower_band[i] > self.bb_short_bound \
                    if self.filter else True) and \
                    self.equity >= self.min_capital:
                self.short = True

                self.position_avg_price = data['close'][i]

                if self.order_size_type == 'percent':
                    self.initial_position = \
                        self.equity * self.leverage \
                        * (self.order_size / 100.0)
                    self.position_size = self.initial_position \
                        * (1 - self.commission / 100) \
                        / self.position_avg_price
                elif self.order_size_type == 'currency':
                    self.initial_position = \
                        self.order_size * self.leverage
                    self.position_size = self.initial_position \
                        * (1 - self.commission / 100) \
                        / self.position_avg_price

                self.position_size = int(
                    self.position_size * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.initial_position = \
                    self.position_size * self.position_avg_price
                self.entry_date = data.index[i]
                self.entry_short_signals.iloc[i] = data['close'][i]

                self.liquidation_price = \
                    self.position_avg_price * (100 + \
                    self.liquidations[self.leverage]) / 100
                self.stop_price = self.super_trend[4][i] * \
                    (100 + self.stop) / 100
                self.take_price[0] = data['close'][i] * \
                    (100 - self.take_percent[0]) / 100
                self.take_price[1] = data['close'][i] * \
                    (100 - self.take_percent[1]) / 100
                self.take_price[2] = data['close'][i] * \
                    (100 - self.take_percent[2]) / 100
                self.take_price[3] = data['close'][i] * \
                    (100 - self.take_percent[3]) / 100
                self.take_price[4] = data['close'][i] * \
                    (100 - self.take_percent[4]) / 100

                self.qty_take[0] = self.position_size * \
                    self.take_volume[0] / 100
                self.qty_take[1] = self.position_size * \
                    self.take_volume[1] / 100
                self.qty_take[2] = self.position_size * \
                    self.take_volume[2] / 100
                self.qty_take[3] = self.position_size * \
                    self.take_volume[3] / 100
                self.qty_take[4] = self.position_size * \
                    self.take_volume[4] / 100

                self.liquidation_price = int(
                    self.liquidation_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.stop_price = int(
                    self.stop_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[0] = int(
                    self.take_price[0] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[1] = int(
                    self.take_price[1] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[2] = int(
                    self.take_price[2] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[3] = int(
                    self.take_price[3] * 10 ** self.price_precision
                ) / 10 ** self.price_precision
                self.take_price[4] = int(
                    self.take_price[4] * 10 ** self.price_precision
                ) / 10 ** self.price_precision

                self.qty_take[0] = int(
                    self.qty_take[0] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[1] = int(
                    self.qty_take[1] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[2] = int(
                    self.qty_take[2] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[3] = int(
                    self.qty_take[3] * 10 ** self.qty_precision
                ) / 10 ** self.qty_precision
                self.qty_take[4] = self.position_size - \
                    (self.qty_take[0] + self.qty_take[1] + \
                    self.qty_take[2] + self.qty_take[3])

            self.stop_line.iloc[i] = self.stop_price
            self.take_line_1.iloc[i] = self.take_price[0]
            self.take_line_2.iloc[i] = self.take_price[1]
            self.take_line_3.iloc[i] = self.take_price[2]
            self.take_line_4.iloc[i] = self.take_price[3]
            self.take_line_5.iloc[i] = self.take_price[4]

            if self.super_trend[5][i] < 0:
                self.uptrend.iloc[i] = self.super_trend[4][i]
            else:
                self.downtrend.iloc[i] = self.super_trend[4][i]

        self.net_profit = round(self.equity - self.initial_capital, 2)

    def forwardtest(self, data):
        # signals
        self.entry_long_signals = pd.concat(
            [
                self.entry_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.stop_long_signals = pd.concat(
            [
                self.stop_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_1_long_signals = pd.concat(
            [
                self.take_1_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_2_long_signals = pd.concat(
            [
                self.take_2_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_3_long_signals = pd.concat(
            [
                self.take_3_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_4_long_signals = pd.concat(
            [
                self.take_4_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_5_long_signals = pd.concat(
            [
                self.take_5_long_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.entry_short_signals = pd.concat(
            [
                self.entry_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.stop_short_signals = pd.concat(
            [
                self.stop_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_1_short_signals = pd.concat(
            [
                self.take_1_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_2_short_signals = pd.concat(
            [
                self.take_2_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_3_short_signals = pd.concat(
            [
                self.take_3_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_4_short_signals = pd.concat(
            [
                self.take_4_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.take_5_short_signals = pd.concat(
            [
                self.take_5_short_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.shift_stop = pd.concat(
            [
                self.shift_stop,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )
        self.exit_signals = pd.concat(
            [
                self.exit_signals,
                pd.Series(np.nan, [data.index[-1]])
            ]
        )

        # indicators
        self.super_trend = f.r_supertrend(
            self.super_trend[0], self.super_trend[1],
            self.super_trend[2], self.super_trend[3], 
            self.super_trend[4], self.super_trend[5],
            data['high'], data['low'], data['close'],
            self.st_factor, self.st_atr_period    
        )
        self.rsi = f.r_rsi(
            self.rsi[0], self.rsi[1], self.rsi[2], self.rsi[3],
            self.rsi[4], data['close'], self.rsi_length
        )
        self.change_stop = f.r_change(
            self.change_stop, self.super_trend[4] 
        )


        self.ma_rsi = f.r_sma(
            self.ma_rsi, self.rsi[4], self.ma_length
        )
        self.dev = f.r_stdev(
            self.dev, self.rsi[4], self.ma_length
        )
        bb_upper_band_value = pd.Series(
            self.ma_rsi.iloc[-1] + self.dev.iloc[-1] * self.bb_mult,
            [data.index[-1]]
        )
        self.bb_upper_band = pd.concat(
            [self.bb_upper_band, bb_upper_band_value]
        )
        bb_lower_band_value = pd.Series(
            self.ma_rsi.iloc[-1] - self.dev.iloc[-1] * self.bb_mult,
            [data.index[-1]]
        )
        self.bb_lower_band = pd.concat(
            [self.bb_lower_band, bb_lower_band_value]
        )

        # check of liquidation
        if self.long and \
                data['low'].iloc[-1] <= self.liquidation_price:
            self.long = False

            self.stop_long_signals.iloc[-1] = \
                self.liquidation_price
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]

            self.liquidation_price = np.nan
            self.position_avg_price = np.nan 

            self.take_price[0] = np.nan
            self.take_price[1] = np.nan
            self.take_price[2] = np.nan
            self.take_price[3] = np.nan
            self.take_price[4] = np.nan

            self.stop_price = np.nan
            self.stop_moved = False

        if self.short and \
                data['high'].iloc[-1] >= self.liquidation_price:
            self.short = False

            self.stop_short_signals.iloc[-1] = \
                self.liquidation_price
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]

            self.liquidation_price = np.nan
            self.position_avg_price = np.nan

            self.take_price[0] = np.nan
            self.take_price[1] = np.nan
            self.take_price[2] = np.nan
            self.take_price[3] = np.nan
            self.take_price[4] = np.nan

            self.stop_price = np.nan
            self.stop_moved = False

        # trading logic (longs)
        if self.long and data['low'].iloc[-1] <= self.stop_price:
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]
            self.stop_long_signals.iloc[-1] = self.stop_price
            self.liquidation_price = np.nan
            self.position_avg_price = np.nan 
            self.take_price[0] = np.nan
            self.take_price[1] = np.nan
            self.take_price[2] = np.nan
            self.take_price[3] = np.nan
            self.take_price[4] = np.nan
            self.stop_price = np.nan
            self.stop_moved = False
            self.long = False
                
        if self.long:
            if self.stop_type == 1 and \
                    self.change_stop.iloc[-1] and \
                    self.super_trend[5].iloc[-1] < 0 and \
                    ((self.super_trend[4].iloc[-1] * \
                    (100 - self.stop) / 100) > self.stop_price):
                self.shift_stop.iloc[-1] = data['close'].iloc[-1]
                self.stop_price = \
                    self.super_trend[4].iloc[-1] * \
                    (100 - self.stop) / 100
                self.stop_price = int(
                    self.stop_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
            elif self.stop_type == 2 and \
                    not self.stop_moved and \
                    ((self.trail_stop == 1 and \
                    data['high'].iloc[-1] > self.take_price[0]) or \
                    (self.trail_stop == 2 and \
                    data['high'].iloc[-1] > self.take_price[1]) or \
                    (self.trail_stop == 3 and \
                    data['high'].iloc[-1] > self.take_price[2]) or \
                    (self.trail_stop == 4 and \
                    data['high'].iloc[-1] > self.take_price[3]) or \
                    (self.trail_stop == 5 and \
                    data['high'].iloc[-1] > self.take_price[4])):
                self.shift_stop.iloc[-1] = data['close'].iloc[-1]
                self.stop_price = self.position_avg_price
                self.stop_moved = True

        if self.long and data['high'].iloc[-1] >= self.take_price[0]:
            self.take_1_long_signals.iloc[-1] = self.take_price[0]
            self.take_price[0] = np.nan

        if self.long and data['high'].iloc[-1] >= self.take_price[1]:
            self.take_2_long_signals.iloc[-1] = self.take_price[1]
            self.take_price[1] = np.nan

        if self.long and data['high'].iloc[-1] >= self.take_price[2]:
            self.take_3_long_signals.iloc[-1] = self.take_price[2]
            self.take_price[2] = np.nan

        if self.long and data['high'].iloc[-1] >= self.take_price[3]:
            self.take_4_long_signals.iloc[-1] = self.take_price[3]
            self.take_price[3] = np.nan

        if self.long and data['high'].iloc[-1] >= self.take_price[4]:
            self.take_5_long_signals.iloc[-1] = self.take_price[4]
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]
            self.take_price[4] = np.nan
            self.stop_price = np.nan
            self.stop_moved = False
            self.long = False

        if self.super_trend[5].iloc[-1] < 0 and \
                (data['close'].iloc[-1] / \
                self.super_trend[4].iloc[-1] - \
                1) * 100 > self.st_lower_band and \
                abs((self.super_trend[4].iloc[-1] / \
                data['close'].iloc[-1] - 1) * \
                100) < self.st_upper_band and \
                self.rsi[4].iloc[-1] < self.rsi_long_upper_bound and \
                self.rsi[4].iloc[-1] > self.rsi_long_lower_bound and \
                not self.long and not self.short and \
                (self.bb_upper_band.iloc[-1] < self.bb_long_bound \
                if self.filter else True):
            self.entry_long_signals.iloc[-1] = \
                data['close'].iloc[-1]
            self.position_avg_price = data['close'].iloc[-1]
            self.liquidation_price = \
                self.position_avg_price * (100 - \
                self.liquidations[self.leverage]) / 100
            self.stop_price = self.super_trend[4].iloc[-1] * \
                (100 - self.stop) / 100
            self.take_price[0] = data['close'].iloc[-1] * \
                (100 + self.take_percent[0]) / 100
            self.take_price[1] = data['close'].iloc[-1] * \
                (100 + self.take_percent[1]) / 100
            self.take_price[2] = data['close'].iloc[-1] * \
                (100 + self.take_percent[2]) / 100
            self.take_price[3] = data['close'].iloc[-1] * \
                (100 + self.take_percent[3]) / 100
            self.take_price[4] = data['close'].iloc[-1] * \
                (100 + self.take_percent[4]) / 100
            self.liquidation_price = int(
                self.liquidation_price * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.stop_price = int(
                self.stop_price * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[0] = int(
                self.take_price[0] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[1] = int(
                self.take_price[1] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[2] = int(
                self.take_price[2] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[3] = int(
                self.take_price[3] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[4] = int(
                self.take_price[4] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.long = True

        # trading logic (shorts)
        if self.short and data['high'].iloc[-1] >= self.stop_price:
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]
            self.stop_short_signals.iloc[-1] = self.stop_price
            self.liquidation_price = np.nan
            self.position_avg_price = np.nan
            self.take_price[0] = np.nan
            self.take_price[1] = np.nan
            self.take_price[2] = np.nan
            self.take_price[3] = np.nan
            self.take_price[4] = np.nan
            self.stop_price = np.nan
            self.stop_moved = False
            self.short = False

        if self.short:
            if self.stop_type == 1 and \
                    self.change_stop.iloc[-1] and \
                    self.super_trend[5].iloc[-1] > 0 and \
                    ((self.super_trend[4].iloc[-1] * \
                    (100 + self.stop) / 100) < self.stop_price):
                self.shift_stop.iloc[-1] = data['close'].iloc[-1]
                self.stop_price = \
                    self.super_trend[4].iloc[-1] * \
                    (100 + self.stop) / 100
                self.stop_price = int(
                    self.stop_price * 10 ** self.price_precision
                ) / 10 ** self.price_precision
            elif self.stop_type == 2 and \
                    not self.stop_moved and \
                    ((self.trail_stop == 1 and \
                    data['low'].iloc[-1] < self.take_price[0]) or \
                    (self.trail_stop == 2 and \
                    data['low'].iloc[-1] < self.take_price[1]) or \
                    (self.trail_stop == 3 and \
                    data['low'].iloc[-1] < self.take_price[2]) or \
                    (self.trail_stop == 4 and \
                    data['low'].iloc[-1] < self.take_price[3]) or \
                    (self.trail_stop == 5 and \
                    data['low'].iloc[-1] < self.take_price[4])):
                self.shift_stop.iloc[-1] = data['close'].iloc[-1]
                self.stop_price = self.position_avg_price
                self.stop_moved = True

        if self.short and data['low'].iloc[-1] <= self.take_price[0]:
            self.take_1_short_signals.iloc[-1] = self.take_price[0]
            self.take_price[0] = np.nan

        if self.short and data['low'].iloc[-1] <= self.take_price[1]:
            self.take_2_short_signals.iloc[-1] = self.take_price[1]
            self.take_price[1] = np.nan     

        if self.short and data['low'].iloc[-1] <= self.take_price[2]:
            self.take_3_short_signals.iloc[-1] = self.take_price[2]
            self.take_price[2] = np.nan

        if self.short and data['low'].iloc[-1] <= self.take_price[3]:
            self.take_4_short_signals.iloc[-1] = self.take_price[3]
            self.take_price[3] = np.nan    

        if self.short and data['low'].iloc[-1] <= self.take_price[4]:
            self.take_5_short_signals.iloc[-1] = self.take_price[4]
            self.exit_signals.iloc[-1] = data['close'].iloc[-1]
            self.take_price[4] = np.nan
            self.stop_price = np.nan
            self.stop_moved = False
            self.short = False

        if self.super_trend[5].iloc[-1] > 0 and \
                (self.super_trend[4].iloc[-1] / \
                data['close'].iloc[-1] - 1) * 100 > \
                self.st_lower_band and \
                (self.super_trend[4].iloc[-1] / \
                data['close'].iloc[-1] - 1) * 100 < \
                self.st_upper_band and \
                self.rsi[4].iloc[-1] < self.rsi_short_upper_bound and \
                self.rsi[4].iloc[-1] > self.rsi_short_lower_bound and \
                not self.long and not self.short and \
                (self.bb_lower_band.iloc[-1] > self.bb_short_bound \
                if self.filter else True):
            self.entry_short_signals.iloc[-1] = data['close'].iloc[-1]
            self.position_avg_price = data['close'].iloc[-1]
            self.liquidation_price = \
                self.position_avg_price * (100 + \
                self.liquidations[self.leverage]) / 100
            self.stop_price = self.super_trend[4].iloc[-1] * \
                (100 + self.stop) / 100
            self.take_price[0] = data['close'].iloc[-1] * \
                (100 - self.take_percent[0]) / 100
            self.take_price[1] = data['close'].iloc[-1] * \
                (100 - self.take_percent[1]) / 100
            self.take_price[2] = data['close'].iloc[-1] * \
                (100 - self.take_percent[2]) / 100
            self.take_price[3] = data['close'].iloc[-1] * \
                (100 - self.take_percent[3]) / 100
            self.take_price[4] = data['close'].iloc[-1] * \
                (100 - self.take_percent[4]) / 100
            self.liquidation_price = int(
                self.liquidation_price * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.stop_price = int(
                self.stop_price * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[0] = int(
                self.take_price[0] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[1] = int(
                self.take_price[1] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[2] = int(
                self.take_price[2] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[3] = int(
                self.take_price[3] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.take_price[4] = int(
                self.take_price[4] * 10 ** self.price_precision
            ) / 10 ** self.price_precision
            self.short = True

        stop_line_value = pd.Series(self.stop_price, [data.index[-1]])
        self.stop_line = \
            pd.concat([self.stop_line, stop_line_value])
        take_line_1_value = pd.Series(
            self.take_price[0], [data.index[-1]]
         )
        self.take_line_1 = \
            pd.concat([self.take_line_1, take_line_1_value])
        take_line_2_value = pd.Series(
            self.take_price[1], [data.index[-1]]
         )
        self.take_line_2 = \
            pd.concat([self.take_line_2, take_line_2_value])
        take_line_3_value = pd.Series(
            self.take_price[2], [data.index[-1]]
         )
        self.take_line_3 = \
            pd.concat([self.take_line_3, take_line_3_value])
        take_line_4_value = pd.Series(
            self.take_price[3], [data.index[-1]]
         )
        self.take_line_4 = \
            pd.concat([self.take_line_4, take_line_4_value])
        take_line_5_value = pd.Series(
            self.take_price[4], [data.index[-1]]
         )
        self.take_line_5 = \
            pd.concat([self.take_line_5, take_line_5_value])

        if self.super_trend[5].iloc[-1] < 0:
            uptrend_value = pd.Series(
                self.super_trend[4].iloc[-1], [data.index[-1]]
            )
            self.uptrend = \
                pd.concat([self.uptrend, uptrend_value])
            downtrend_value = pd.Series(
                np.nan, [data.index[-1]]
            )
            self.downtrend = \
                pd.concat([self.downtrend, downtrend_value])
        else:
            uptrend_value = pd.Series(
                np.nan, [data.index[-1]]
            )
            self.uptrend = \
                pd.concat([self.uptrend, uptrend_value])
            downtrend_value = pd.Series(
                self.super_trend[4].iloc[-1], [data.index[-1]]
            )
            self.downtrend = \
                pd.concat([self.downtrend, downtrend_value])

        self.bb_long_bound_value = pd.Series(
            self.bb_long_bound, [data.index[-1]]
        )
        self.bb_long_bound_line = \
            pd.concat(
                [self.bb_long_bound_line, self.bb_long_bound_value]
            )
        self.bb_short_bound_value = pd.Series(
            self.bb_short_bound, [data.index[-1]]
        )
        self.bb_short_bound_line = \
            pd.concat(
                [self.bb_short_bound_line, self.bb_short_bound_value]
            )
        self.rsi_long_upper_bound_value = pd.Series(
            self.rsi_long_upper_bound, [data.index[-1]]
        )
        self.rsi_long_upper_bound_line = \
            pd.concat(
                [
                    self.rsi_long_upper_bound_line,
                    self.rsi_long_upper_bound_value
                ]
            )
        self.rsi_long_lower_bound_value = pd.Series(
            self.rsi_long_lower_bound, [data.index[-1]]
        )
        self.rsi_long_lower_bound_line = \
            pd.concat(
                [
                    self.rsi_long_lower_bound_line,
                    self.rsi_long_lower_bound_value
                ]
            )
        self.rsi_short_upper_bound_value = pd.Series(
            self.rsi_short_upper_bound, [data.index[-1]]
        )
        self.rsi_short_upper_bound_line = \
            pd.concat(
                [
                    self.rsi_short_upper_bound_line,
                    self.rsi_short_upper_bound_value
                ]
            )
        self.rsi_short_lower_bound_value = pd.Series(
            self.rsi_short_lower_bound, [data.index[-1]]
        )
        self.rsi_short_lower_bound_line = \
            pd.concat(
                [
                    self.rsi_short_lower_bound_line,
                    self.rsi_short_lower_bound_value
                ]
            )

    def get_addplot(self, chart_length, axes, strategy_graphics):
        addplot = [
            mpf.make_addplot(
                self.uptrend.tail(chart_length)
                    if strategy_graphics['supertrend'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.uptrend_color, width=2.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.downtrend.tail(chart_length)
                    if strategy_graphics['supertrend'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.downtrend_color, width=2.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_line_1.tail(chart_length)
                    if strategy_graphics['take-profits'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.take_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_line_2.tail(chart_length)
                    if strategy_graphics['take-profits'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.take_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_line_3.tail(chart_length)
                    if strategy_graphics['take-profits'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.take_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_line_4.tail(chart_length)
                    if strategy_graphics['take-profits'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.take_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_line_5.tail(chart_length)
                    if strategy_graphics['take-profits'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.take_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.stop_line.tail(chart_length)
                    if strategy_graphics['stop-loss'] > 0
                    else pd.Series(np.full(chart_length, np.nan)),
                color=self.stop_price_color, width=1.0, ax=axes[0]
            ),
            mpf.make_addplot(
                self.rsi[4].tail(chart_length)
                    if strategy_graphics['rsi'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.rsi_color, 
                width=1.5, ax=axes[2]
            ),
            mpf.make_addplot(
                self.rsi_long_upper_bound_line.tail(chart_length)
                    if strategy_graphics['rsi'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.rsi_long_bounds_color, 
                linestyle='--', width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.rsi_long_lower_bound_line.tail(chart_length)
                    if strategy_graphics['rsi'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.rsi_long_bounds_color, 
                linestyle='--', width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.rsi_short_upper_bound_line.tail(chart_length)
                    if strategy_graphics['rsi'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.rsi_short_bounds_color, 
                linestyle='--', width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.rsi_short_lower_bound_line.tail(chart_length)
                    if strategy_graphics['rsi'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.rsi_short_bounds_color,
                linestyle='--', width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.bb_upper_band.tail(chart_length)
                    if strategy_graphics['filter'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.filter_color, 
                width=1.5, ax=axes[2]
            ),
            mpf.make_addplot(
                self.bb_lower_band.tail(chart_length)
                    if strategy_graphics['filter'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.filter_color, 
                width=1.5, ax=axes[2]
            ),
            mpf.make_addplot(
                self.bb_long_bound_line.tail(chart_length)
                    if strategy_graphics['filter'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.filter_color, linestyle='--',
                width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.bb_short_bound_line.tail(chart_length)
                    if strategy_graphics['filter'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                panel=1, color=self.filter_color, linestyle='--',
                width=1.0, ax=axes[2]
            ),
            mpf.make_addplot(
                self.entry_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.entry_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.stop_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_1_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_2_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_3_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_4_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_5_long_signals.tail(chart_length)
                    if strategy_graphics['long signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.long_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.entry_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.entry_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.stop_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_1_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_2_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_3_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_4_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            ),
            mpf.make_addplot(
                self.take_5_short_signals.tail(chart_length)
                    if strategy_graphics['short signals'] > 0 
                    else pd.Series(np.full(chart_length, np.nan)),
                type='scatter',
                marker=self.exit_marker,
                markersize=self.marker_size,
                color=self.short_marker_color,
                ax=axes[0]
            )
        ]
        return addplot

    def trade(self, exchange, symbol):
        result = ''

        if not pd.isna(self.shift_stop.iloc[-1]):
            if self.long:
                result += exchange.futures_cancel_stop(symbol)
                result += exchange.futures_market_stop_sell(
                    symbol, self.stop_price
                )
            elif self.short:
                result += exchange.futures_cancel_stop(symbol)
                result += exchange.futures_market_stop_buy(
                    symbol, self.stop_price
                )

        if not pd.isna(self.exit_signals.iloc[-1]):
            result += exchange.futures_cancel_orders(symbol)

        if not pd.isna(self.entry_long_signals.iloc[-1]):
            result += exchange.futures_market_entry_long(
                symbol, self.order_size_type, self.margin_type,
                self.order_size, self.leverage
            )
            result += exchange.futures_market_stop_sell(
                symbol, self.stop_price
            )
            result += exchange.futures_limit_take_sell(
                symbol, self.take_volume[0], self.take_price[0]
            )
            result += exchange.futures_limit_take_sell(
                symbol, self.take_volume[1], self.take_price[1]
            )
            result += exchange.futures_limit_take_sell(
                symbol, self.take_volume[2], self.take_price[2]
            )
            result += exchange.futures_limit_take_sell(
                symbol, self.take_volume[3], self.take_price[3]
            )
            result += exchange.futures_limit_take_sell(
                symbol, 100, self.take_price[4]
            )

        if not pd.isna(self.entry_short_signals.iloc[-1]):
            result += exchange.futures_market_entry_short(
                symbol, self.order_size_type, self.margin_type,
                self.order_size, self.leverage
            )
            result += exchange.futures_market_stop_buy(
                symbol, self.stop_price
            )
            result += exchange.futures_limit_take_buy(
                symbol, self.take_volume[0], self.take_price[0]
            )
            result += exchange.futures_limit_take_buy(
                symbol, self.take_volume[1], self.take_price[1]
            )
            result += exchange.futures_limit_take_buy(
                symbol, self.take_volume[2], self.take_price[2]
            )
            result += exchange.futures_limit_take_buy(
                symbol, self.take_volume[3], self.take_price[3]
            )
            result += exchange.futures_limit_take_buy(
                symbol, 100, self.take_price[4]
            )

        if result != '':
            return result
        else:
            return None