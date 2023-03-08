import matplotlib.backends.backend_tkagg as bt
import matplotlib.pyplot as plt
import tkinter.ttk as ttk
import mplfinance as mpf
import datetime as dt
import tkinter as tk


class NavigationToolbar(bt.NavigationToolbar2Tk):
    toolitems = [t for t in bt.NavigationToolbar2Tk.toolitems if
                 t[0] in ('Home', 'Pan', 'Zoom', 'Save')]


class GUI(tk.Tk):
    app_name = 'Nugget'
    app_width = 1600
    app_height = 850
    chart_length = 141
    chart_type = 'candle'
    chart_style = mpf.make_mpf_style(
        marketcolors=mpf.make_marketcolors(
            up='#35a79b', down='#EF3434', inherit=True
        ),
        facecolor='#ffffff', edgecolor='#000000',
        figcolor='#ffffff', gridcolor='#EEEDED',
        gridstyle='-', gridaxis='both',
        y_on_right=True
    )
    chart_ylabel = ''
    chart_scale = dict(left=0.15, right=0.70, top=0.38, bottom=0.65)

    strategy_graphics = {
        'supertrend' : 1,
        'take-profits' : 1,
        'stop-loss' : 1,
        'rsi' : 1,
        'filter' : -1,
        'long signals': 1,
        'short signals': 1
    }

    def __init__(
        self, exchange, symbol, interval, strategy, ga, tester
    ):
        super().__init__()

        self.exchange = exchange
        self.symbol = symbol
        self.interval = interval
        self.strategy = strategy
        self.optimization = [ga, False]
        self.backtesting = tester
        self.automation = False
        
        self.title(self.app_name)
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        self.x = int((self.screen_width / 2 ) - (self.app_width / 2))
        self.y = int((self.screen_height / 2 ) - (self.app_height / 2))
        self.geometry(
            '{}x{}+{}+{}'.format(
                self.app_width, self.app_height, self.x, self.y
            )
        )

        main_menu = tk.Menu(self)
        self.config(menu=main_menu)
        symbol_menu = tk.Menu(main_menu, tearoff=0)
        symbol_menu.add_command(
            label='BTCUSDT', 
            command=lambda: self.set_symbol('BTCUSDT')
        )
        symbol_menu.add_command(
            label='BNBUSDT', 
            command=lambda: self.set_symbol('BNBUSDT')
        )
        symbol_menu.add_command(
            label='ETHUSDT', 
            command=lambda: self.set_symbol('ETHUSDT')
        )
        symbol_menu.add_command(
            label='BCHUSDT', 
            command=lambda: self.set_symbol('BCHUSDT')
        )
        symbol_menu.add_command(
            label='XRPUSDT', 
            command=lambda: self.set_symbol('XRPUSDT')
        )
        symbol_menu.add_command(
            label='EOSUSDT', 
            command=lambda: self.set_symbol('EOSUSDT')
        )
        symbol_menu.add_command(
            label='LTCUSDT', 
            command=lambda: self.set_symbol('LTCUSDT')
        )
        symbol_menu.add_command(
            label='TRXUSDT', 
            command=lambda: self.set_symbol('TRXUSDT')
        )
        symbol_menu.add_command(
            label='ETCUSDT', 
            command=lambda: self.set_symbol('ETCUSDT')
        )
        symbol_menu.add_command(
            label='LINKUSDT', 
            command=lambda: self.set_symbol('LINKUSDT')
        )
        symbol_menu.add_command(
            label='XLMUSDT', 
            command=lambda: self.set_symbol('XLMUSDT')
        )
        symbol_menu.add_command(
            label='ADAUSDT', 
            command=lambda: self.set_symbol('ADAUSDT')
        )
        symbol_menu.add_command(
            label='XMRUSDT', 
            command=lambda: self.set_symbol('XMRUSDT')
        )
        symbol_menu.add_command(
            label='DASHUSDT', 
            command=lambda: self.set_symbol('DASHUSDT')
        )
        symbol_menu.add_command(
            label='ZECUSDT', 
            command=lambda: self.set_symbol('ZECUSDT')
        )
        symbol_menu.add_command(
            label='XTZUSDT', 
            command=lambda: self.set_symbol('XTZUSDT')
        )
        symbol_menu.add_command(
            label='ATOMUSDT', 
            command=lambda: self.set_symbol('ATOMUSDT')
        )
        symbol_menu.add_command(
            label='ONTUSDT', 
            command=lambda: self.set_symbol('ONTUSDT')
        )
        symbol_menu.add_command(
            label='IOTAUSDT', 
            command=lambda: self.set_symbol('IOTAUSDT')
        )
        symbol_menu.add_command(
            label='BATUSDT', 
            command=lambda: self.set_symbol('BATUSDT')
        )
        main_menu.add_cascade(label='Symbol', menu=symbol_menu)
        interval_menu = tk.Menu(main_menu, tearoff=0)
        interval_menu.add_command(
            label='1 minute', 
            command=lambda: self.set_interval('1m')
        )
        interval_menu.add_command(
            label='3 minutes', 
            command=lambda: self.set_interval('3m')
        )
        interval_menu.add_command(
            label='5 minutes', 
            command=lambda: self.set_interval('5m')
        )
        interval_menu.add_command(
            label='15 minutes', 
            command=lambda: self.set_interval('15m')
        )
        interval_menu.add_command(
            label='30 minutes', 
            command=lambda: self.set_interval('30m')
        )
        interval_menu.add_command(
            label='1 hour', 
            command=lambda: self.set_interval('1h')
        )
        interval_menu.add_command(
            label='2 hours', 
            command=lambda: self.set_interval('2h')
        )
        interval_menu.add_command(
            label='4 hours', 
            command=lambda: self.set_interval('4h')
        )
        interval_menu.add_command(
            label='6 hours', 
            command=lambda: self.set_interval('6h')
        )
        interval_menu.add_command(
            label='8 hours', 
            command=lambda: self.set_interval('8h')
        )
        interval_menu.add_command(
            label='12 hours', 
            command=lambda: self.set_interval('12h')
        )
        interval_menu.add_command(
            label='1 day', 
            command=lambda: self.set_interval('1d')
        )
        interval_menu.add_command(
            label='3 days', 
            command=lambda: self.set_interval('3d')
        )
        main_menu.add_cascade(label='Interval', menu=interval_menu)
        main_menu.add_command(
            label='Settings',
            command=self.get_settings
        )
        main_menu.add_command(
            label='Optimization',
            command=self.set_optimization
        )
        main_menu.add_command(
            label='Backtesting',
            command=self.set_backtesting
        )
        main_menu.add_command(
            label='Automation',
            command=self.start_automation
        )

        self.output_window = tk.Text(self, bd=1, width=30)
        self.output_window.pack(side=tk.RIGHT, fill=tk.Y)

        self.exchange.set_initial_data(self.interval, self.symbol)
        figure, self.axes = mpf.plot(
            self.exchange.data.tail(self.chart_length),
            type=self.chart_type, style=self.chart_style,
            ylabel=self.chart_ylabel, returnfig=True,
            num_panels=2, scale_padding=self.chart_scale
        )
        self.axes[0].clear()
        self.axes[2].clear()
        self.strategy.backtest(
            self.exchange, self.exchange.data, self.symbol
        )
        addplot = self.strategy.get_addplot(
            self.chart_length, self.axes, self.strategy_graphics
        )
        mpf.plot(
            self.exchange.data.tail(self.chart_length),
            type=self.chart_type, style=self.chart_style,
            ylabel='', addplot=addplot, ax=self.axes[0]
        )
        title = 'Binance Futures • ' + \
            self.symbol + ' • ' + self.interval
        self.axes[0].set_title(
            label=title, fontsize=15, style='normal', loc='left'
        )
        self.canvas = bt.FigureCanvasTkAgg(figure, self)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        tool_bar = NavigationToolbar(self.canvas, self).update()
        self.canvas.draw()

        self.update_chart()

    def set_symbol(self, symbol):
        self.symbol = symbol
        self.draw_chart()

    def set_interval(self, interval):
        self.interval = interval
        self.draw_chart()

    def get_settings(self):
        def update_graphics_1():
            self.strategy_graphics['supertrend'] *= -1

        def update_graphics_2():
            self.strategy_graphics['take-profits'] *= -1

        def update_graphics_3():
            self.strategy_graphics['stop-loss'] *= -1

        def update_graphics_4():
            self.strategy_graphics['rsi'] *= -1

        def update_graphics_5():
            self.strategy_graphics['filter'] *= -1

        def update_graphics_6():
            self.strategy_graphics['long signals'] *= -1

        def update_graphics_7():
            self.strategy_graphics['short signals'] *= -1

        def change_settings():
            self.strategy.stop_type = int(entry_1.get())
            self.strategy.stop = float(entry_2.get())
            self.strategy.trail_stop = int(entry_3.get())
            self.strategy.take_percent[0] = float(entry_4.get())
            self.strategy.take_percent[1] = float(entry_5.get())
            self.strategy.take_percent[2] = float(entry_6.get())
            self.strategy.take_percent[3] = float(entry_7.get())
            self.strategy.take_percent[4] = float(entry_8.get())
            self.strategy.take_volume[0] = float(entry_9.get())
            self.strategy.take_volume[1] = float(entry_10.get())
            self.strategy.take_volume[2] = float(entry_11.get())
            self.strategy.take_volume[3] = float(entry_12.get())
            self.strategy.take_volume[4] = float(entry_13.get())
            self.strategy.st_atr_period = int(entry_14.get())
            self.strategy.st_factor = float(entry_15.get())
            self.strategy.st_upper_band = float(entry_16.get())
            self.strategy.st_lower_band = float(entry_17.get())
            self.strategy.rsi_length = int(entry_18.get())
            self.strategy.rsi_long_upper_bound = float(entry_19.get())
            self.strategy.rsi_long_lower_bound = float(entry_20.get())
            self.strategy.rsi_short_upper_bound = float(entry_21.get())
            self.strategy.rsi_short_lower_bound = float(entry_22.get())
            self.strategy.filter = int(entry_23.get())
            self.strategy.ma_length = int(entry_24.get())
            self.strategy.bb_mult = float(entry_25.get())
            self.strategy.bb_long_bound = float(entry_26.get())
            self.strategy.bb_short_bound = float(entry_27.get())

            self.draw_chart()

        strategy_param = {
            'stop_type': self.strategy.stop_type,
            'stop': self.strategy.stop,
            'trail_stop': self.strategy.trail_stop,
            'take_percent_1': self.strategy.take_percent[0],
            'take_percent_2': self.strategy.take_percent[1],
            'take_percent_3': self.strategy.take_percent[2],
            'take_percent_4': self.strategy.take_percent[3],
            'take_percent_5': self.strategy.take_percent[4],
            'take_volume_1': self.strategy.take_volume[0],
            'take_volume_2': self.strategy.take_volume[1],
            'take_volume_3': self.strategy.take_volume[2],
            'take_volume_4': self.strategy.take_volume[3],
            'take_volume_5': self.strategy.take_volume[4],
            'st_atr_period': self.strategy.st_atr_period,
            'st_factor': self.strategy.st_factor,
            'st_upper_band': self.strategy.st_upper_band,
            'st_lower_band': self.strategy.st_lower_band,
            'rsi_length': self.strategy.rsi_length,
            'rsi_long_upper_bound': self.strategy.rsi_long_upper_bound,
            'rsi_long_lower_bound': self.strategy.rsi_long_lower_bound,
            'rsi_short_upper_bound': self.strategy.rsi_short_upper_bound,
            'rsi_short_lower_bound': self.strategy.rsi_short_lower_bound,
            'filter': self.strategy.filter,
            'ma_length': self.strategy.ma_length,
            'bb_mult': self.strategy.bb_mult,
            'bb_long_bound': self.strategy.bb_long_bound,
            'bb_short_bound': self.strategy.bb_short_bound,
        }

        settings_window = tk.Tk()
        settings_window.title('Settings')
        frame_param = tk.LabelFrame(settings_window, text='Parameters')
        frame_param.grid(row=0, column=0, padx=5, pady=5, sticky=tk.NW)

        entry_1 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_2 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_3 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_4 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_5 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_6 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_7 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_8 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_9 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_10 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_11 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_12 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_13 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_14 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_15 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_16 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_17 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_18 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_19 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_20 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_21 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_22 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_23 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_24 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_25 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_26 = tk.Entry(frame_param, width=5, font=['Arial', '12'])
        entry_27 = tk.Entry(frame_param, width=5, font=['Arial', '12'])

        entry_1.insert(0, str(strategy_param['stop_type']))
        entry_2.insert(0, str(strategy_param['stop']))
        entry_3.insert(0, str(strategy_param['trail_stop']))
        entry_4.insert(0, str(strategy_param['take_percent_1']))
        entry_5.insert(0, str(strategy_param['take_percent_2']))
        entry_6.insert(0, str(strategy_param['take_percent_3']))
        entry_7.insert(0, str(strategy_param['take_percent_4']))
        entry_8.insert(0, str(strategy_param['take_percent_5']))
        entry_9.insert(0, str(strategy_param['take_volume_1']))
        entry_10.insert(0, str(strategy_param['take_volume_2']))
        entry_11.insert(0, str(strategy_param['take_volume_3']))
        entry_12.insert(0, str(strategy_param['take_volume_4']))
        entry_13.insert(0, str(strategy_param['take_volume_5']))
        entry_14.insert(0, str(strategy_param['st_atr_period']))
        entry_15.insert(0, str(strategy_param['st_factor']))
        entry_16.insert(0, str(strategy_param['st_upper_band']))
        entry_17.insert(0, str(strategy_param['st_lower_band']))
        entry_18.insert(0, str(strategy_param['rsi_length']))
        entry_19.insert(0, str(strategy_param['rsi_long_upper_bound']))
        entry_20.insert(0, str(strategy_param['rsi_long_lower_bound']))
        entry_21.insert(0, str(strategy_param['rsi_short_upper_bound']))
        entry_22.insert(0, str(strategy_param['rsi_short_lower_bound']))
        entry_23.insert(0, str(strategy_param['filter']))
        entry_24.insert(0, str(strategy_param['ma_length']))
        entry_25.insert(0, str(strategy_param['bb_mult']))
        entry_26.insert(0, str(strategy_param['bb_long_bound']))
        entry_27.insert(0, str(strategy_param['bb_short_bound']))

        label_1 = tk.Label(frame_param, text='stop_type')
        label_2 = tk.Label(frame_param, text='stop')
        label_3 = tk.Label(frame_param, text='trail_stop')
        label_4 = tk.Label(frame_param, text='take_percent_1')
        label_5 = tk.Label(frame_param, text='take_percent_2')
        label_6 = tk.Label(frame_param, text='take_percent_3')
        label_7 = tk.Label(frame_param, text='take_percent_4')
        label_8 = tk.Label(frame_param, text='take_percent_5')
        label_9 = tk.Label(frame_param, text='take_volume_1')
        label_10 = tk.Label(frame_param, text='take_volume_2')
        label_11 = tk.Label(frame_param, text='take_volume_3')
        label_12 = tk.Label(frame_param, text='take_volume_4')
        label_13 = tk.Label(frame_param, text='take_volume_5')
        label_14 = tk.Label(frame_param, text='st_atr_period')
        label_15 = tk.Label(frame_param, text='st_factor')
        label_16 = tk.Label(frame_param, text='st_upper_band')
        label_17 = tk.Label(frame_param, text='st_lower_band')
        label_18 = tk.Label(frame_param, text='rsi_length')
        label_19 = tk.Label(frame_param, text='rsi_long_upper_bound')
        label_20 = tk.Label(frame_param, text='rsi_long_lower_bound')
        label_21 = tk.Label(frame_param, text='rsi_short_upper_bound')
        label_22 = tk.Label(frame_param, text='rsi_short_lower_bound')
        label_23 = tk.Label(frame_param, text='filter')
        label_24 = tk.Label(frame_param, text='ma_length')
        label_25 = tk.Label(frame_param, text='bb_mult')
        label_26 = tk.Label(frame_param, text='bb_long_bound')
        label_27 = tk.Label(frame_param, text='bb_short_bound')

        entry_1.grid(row=0, column=0)
        entry_2.grid(row=1, column=0)
        entry_3.grid(row=2, column=0)
        entry_4.grid(row=3, column=0)
        entry_5.grid(row=4, column=0)
        entry_6.grid(row=5, column=0)
        entry_7.grid(row=6, column=0)
        entry_8.grid(row=7, column=0)
        entry_9.grid(row=8, column=0)
        entry_10.grid(row=9, column=0)
        entry_11.grid(row=10, column=0)
        entry_12.grid(row=11, column=0)
        entry_13.grid(row=12, column=0)
        entry_14.grid(row=13, column=0)
        entry_15.grid(row=14, column=0)
        entry_16.grid(row=15, column=0)
        entry_17.grid(row=16, column=0)
        entry_18.grid(row=17, column=0)
        entry_19.grid(row=18, column=0)
        entry_20.grid(row=19, column=0)
        entry_21.grid(row=20, column=0)
        entry_22.grid(row=21, column=0)
        entry_23.grid(row=22, column=0)
        entry_24.grid(row=23, column=0)
        entry_25.grid(row=24, column=0)
        entry_26.grid(row=25, column=0)
        entry_27.grid(row=26, column=0)

        label_1.grid(row=0, column=1, sticky=tk.W)
        label_2.grid(row=1, column=1, sticky=tk.W)
        label_3.grid(row=2, column=1, sticky=tk.W)
        label_4.grid(row=3, column=1, sticky=tk.W)
        label_5.grid(row=4, column=1, sticky=tk.W)
        label_6.grid(row=5, column=1, sticky=tk.W)
        label_7.grid(row=6, column=1, sticky=tk.W)
        label_8.grid(row=7, column=1, sticky=tk.W)
        label_9.grid(row=8, column=1, sticky=tk.W)
        label_10.grid(row=9, column=1, sticky=tk.W)
        label_11.grid(row=10, column=1, sticky=tk.W)
        label_12.grid(row=11, column=1, sticky=tk.W)
        label_13.grid(row=12, column=1, sticky=tk.W)
        label_14.grid(row=13, column=1, sticky=tk.W)
        label_15.grid(row=14, column=1, sticky=tk.W)
        label_16.grid(row=15, column=1, sticky=tk.W)
        label_17.grid(row=16, column=1, sticky=tk.W)
        label_18.grid(row=17, column=1, sticky=tk.W)
        label_19.grid(row=18, column=1, sticky=tk.W)
        label_20.grid(row=19, column=1, sticky=tk.W)
        label_21.grid(row=20, column=1, sticky=tk.W)
        label_22.grid(row=21, column=1, sticky=tk.W)
        label_23.grid(row=22, column=1, sticky=tk.W)
        label_24.grid(row=23, column=1, sticky=tk.W)
        label_25.grid(row=24, column=1, sticky=tk.W)
        label_26.grid(row=25, column=1, sticky=tk.W)
        label_27.grid(row=26, column=1, sticky=tk.W)

        frame_check = tk.LabelFrame(settings_window, text='Style')
        frame_check.grid(row=0, column=1, padx=5, pady=5, sticky=tk.NE)

        supertrend_button = tk.Checkbutton(
            frame_check, text='supertrend',
            command=update_graphics_1
        )
        take_profit_button = tk.Checkbutton(
            frame_check, text='take-profits',
            command=update_graphics_2
        )
        stop_loss_button = tk.Checkbutton(
            frame_check, text='stop-loss',
            command=update_graphics_3
        )
        rsi_button = tk.Checkbutton(
            frame_check, text='rsi',
            command=update_graphics_4
        )
        bb_button = tk.Checkbutton(
            frame_check, text='filter',
            command=update_graphics_5
        )
        long_signals_button = tk.Checkbutton(
            frame_check, text='long signals',
            command=update_graphics_6
        )
        short_signals_button = tk.Checkbutton(
            frame_check, text='short signals',
            command=update_graphics_7
        )

        if self.strategy_graphics['supertrend'] > 0:
            supertrend_button.select()

        if self.strategy_graphics['take-profits'] > 0:
            take_profit_button.select()

        if self.strategy_graphics['stop-loss'] > 0:
            stop_loss_button.select()

        if self.strategy_graphics['rsi'] > 0:
            rsi_button.select()

        if self.strategy_graphics['filter'] > 0:
            bb_button.select()

        if self.strategy_graphics['long signals'] > 0:
            long_signals_button.select()

        if self.strategy_graphics['short signals'] > 0:
            short_signals_button.select()

        supertrend_button.pack(anchor=tk.W)
        take_profit_button.pack(anchor=tk.W)
        stop_loss_button.pack(anchor=tk.W)
        rsi_button.pack(anchor=tk.W)
        bb_button.pack(anchor=tk.W)
        long_signals_button.pack(anchor=tk.W)
        short_signals_button.pack(anchor=tk.W)

        frame_buttons = tk.Frame(settings_window, borderwidth=5)
        frame_buttons.grid(row=1, column=0, columnspan=2)
        button = tk.Button(
            frame_buttons, text='Apply', bg='white', fg='black',
            command=change_settings
        )
        button.pack()

    def set_optimization(self):
        def start_optimization():
            try:
                start_date = int(
                    dt.datetime.strptime(
                        start_entry.get(), '%Y/%m/%d'
                    ).timestamp() * 1000
                )
                end_date = int(
                    dt.datetime.strptime(
                        end_entry.get(), '%Y/%m/%d'
                    ).timestamp() * 1000
                )
                if start_date > end_date: raise
            except:
                self.output_window.insert('end', 'Wrong input\n\n')
            else:
                settings_window.destroy()
                self.optimization[1] = True
                message = 'Optimization started\n\n'
                self.output_window.insert('end', message)
                self.update()
                self.optimization[0].optimize(
                    self.exchange, self.interval, self.symbol,
                    start_date, end_date, self
                )
                self.optimization[0].change_parameters(self.strategy)
                self.optimization[1] = False
                self.draw_chart()
                message = \
                    'Strategy parameters changed\n\n' + \
                    'Optimization completed\n\n'
                self.output_window.insert('end', message)

        settings_window = tk.Tk()
        settings_window.title('Testing period')
        window_width = 245
        window_height = 90
        x = int((self.screen_width / 2) - (window_width / 2))
        y = int((self.screen_height / 2) - (window_height / 2))
        settings_window.geometry(
            '{}x{}+{}+{}'.format(window_width, window_height, x, y)
        )
        frame_form = tk.Frame(settings_window, borderwidth=5)
        frame_form.pack()
        start_label = tk.Label(
            frame_form, text='Start date (yyyy/mm/dd): '
        )
        end_label = tk.Label(
            frame_form, text='End date (yyyy/mm/dd): '
        )
        start_entry = tk.Entry(
            frame_form, width=10, font=['Arial', '12']
        )
        end_entry = tk.Entry(
            frame_form, width=10, font=['Arial', '12']
        )
        start_label.grid(row=0, column=0, sticky=tk.W)
        start_entry.grid(row=0, column=1)
        end_label.grid(row=1, column=0, sticky=tk.W)
        end_entry.grid(row=1, column=1)
        frame_buttons = tk.Frame(settings_window, borderwidth=5)
        frame_buttons.pack(fill=tk.X)
        button = tk.Button(
            frame_buttons, text='Apply', bg='white', fg='black',
            command=start_optimization
        )
        button.pack()     

    def set_backtesting(self):
        def start_backtesting():
            try:
                start_date = int(
                    dt.datetime.strptime(
                        start_entry.get(), '%Y/%m/%d'
                    ).timestamp() * 1000
                )
                end_date = int(
                    dt.datetime.strptime(
                        end_entry.get(), '%Y/%m/%d'
                    ).timestamp() * 1000
                )
                if start_date > end_date: raise
            except:
                self.output_window.insert('end', 'Wrong input\n\n')
            else:
                settings_window.destroy()
                message = 'Backtesting started\n\n'
                self.output_window.insert('end', message)
                self.update()
                testing = self.backtesting.start_testing(
                    self.exchange, self.interval, self.symbol, 
                    start_date, end_date, self.strategy
                )

                if testing:
                    window_width = 1352
                    window_height = 870
                    figscale = 0.8
                    chart_ylabel = ''
                    chart_scale = dict(
                        left=0.15, right=0.65, top=0.57, bottom=1.05
                    )

                    tester_window = tk.Tk()
                    tester_window.title('Nugget')
                    x = int(
                        (self.screen_width / 2) - (window_width / 2)
                    )
                    y = int(
                        (self.screen_height / 2) - (window_height / 2)
                    )
                    tester_window.geometry(
                        '{}x{}+{}+{}'.format(
                            window_width, window_height, self.x, self.y
                        )
                    )

                    chart_figure, chart_axes = mpf.plot(
                        self.backtesting.data, type=self.chart_type,
                        style=self.chart_style, figscale=figscale,
                        ylabel=chart_ylabel, returnfig=True,
                        num_panels=2, scale_padding=chart_scale,
                        warn_too_much_data=100_000_000
                    )
                    chart_axes[0].clear()
                    chart_axes[2].clear()
                    addplot = self.backtesting.strategy.get_addplot(
                        self.backtesting.data.shape[0], 
                        chart_axes, self.strategy_graphics
                    )
                    mpf.plot(
                        self.backtesting.data, type=self.chart_type,
                        style=self.chart_style, ylabel='',
                        addplot=addplot, ax=chart_axes[0],
                        warn_too_much_data=100_000_000
                    )
                    title = 'Binance Futures • ' + \
                        self.symbol + ' • ' + self.interval
                    chart_axes[0].set_title(
                        label=title, fontsize=15,
                        style='normal', loc='left'
                    )
                    chart_canvas = bt.FigureCanvasTkAgg(
                        chart_figure, tester_window
                    )
                    chart_canvas.get_tk_widget().pack(
                        side=tk.TOP, fill=tk.BOTH, expand=True
                    )
                    chart_toolbar = NavigationToolbar(
                        chart_canvas, tester_window
                    )
                    chart_toolbar.update()
                    chart_toolbar.pack(side=tk.TOP, fill=tk.X)

                    frame_width = 1352
                    frame_height = 300
                    frame_tester = tk.Frame(
                        tester_window, 
                        height=frame_height,
                        width=frame_width
                    )
                    frame_tester.pack(
                        side=tk.BOTTOM, fill=tk.BOTH, expand=True
                    )

                    notebook = ttk.Notebook(frame_tester)
                    frame_1 = ttk.Frame(
                        notebook,
                        height=frame_height,
                        width=frame_width
                    )
                    frame_2 = ttk.Frame(
                        notebook,
                        height=frame_height,
                        width=frame_width
                    )
                    frame_3 = ttk.Frame(
                        notebook,
                        height=frame_height,
                        width=frame_width
                    )
                    frame_1.pack(fill=tk.BOTH, expand=True)
                    frame_2.pack(fill=tk.BOTH, expand=True)
                    frame_3.pack(fill=tk.BOTH, expand=True)
                    notebook.add(frame_1, text='Equity')
                    notebook.add(frame_2, text='Performance summary')
                    notebook.add(frame_3, text='List of trades')
                    notebook.pack(fill=tk.BOTH, expand=True)

                    x = list(self.backtesting.equity.index)
                    y = list(self.backtesting.equity)
                    equity_figure, equity_axes = plt.subplots(1)
                    equity_figure.tight_layout(
                        rect=(0, 0.01, 1.0205, 0.955)
                    )
                    equity_axes.plot(x, y, color='#4494c6')
                    equity_axes.fill_between(
                        x, min(y) * 0.99, y, alpha=0.7, color='#adcfe8'
                    )
                    equity_canvas = bt.FigureCanvasTkAgg(
                        equity_figure, frame_1
                    )
                    equity_toolbar = NavigationToolbar(
                        equity_canvas, frame_1
                    )
                    equity_toolbar.update()
                    equity_axes.axis(
                        xmin=1, xmax=len(x), ymin=min(y) * 0.99
                    )
                    equity_canvas.get_tk_widget().pack(
                        side=tk.TOP, fill=tk.BOTH, expand=True
                    )
                    equity_toolbar.pack(side=tk.BOTTOM, fill=tk.X)

                    table_1 = ttk.Treeview(
                        frame_2,
                        show='headings',
                        columns=('#1', '#2', '#3', '#4')
                    )
                    table_1.heading('#1', text='Title', anchor=tk.W)
                    table_1.heading('#2', text='All', anchor=tk.E)
                    table_1.heading('#3', text='Long', anchor=tk.E)
                    table_1.heading('#4', text='Short', anchor=tk.E)
                    table_1.column('#1', anchor=tk.W, width=1)
                    table_1.column('#2', anchor=tk.E, width=1)
                    table_1.column('#3', anchor=tk.E, width=1)
                    table_1.column('#4', anchor=tk.E, width=1)
                    scroll_bar_1 = ttk.Scrollbar(
                        frame_2, orient=tk.VERTICAL,
                        command=table_1.yview
                    )
                    table_1.configure(yscroll=scroll_bar_1.set)
                    scroll_bar_1.pack(side=tk.RIGHT, fill=tk.Y)
                    data = self.backtesting.performance_metrics
                    for i in range(data.shape[0]):
                        values = list(data.iloc[i])
                        table_1.insert('', tk.END, values=values)
                    table_1.pack(fill=tk.BOTH, expand=True)

                    table_2 = ttk.Treeview(
                        frame_3,
                        show='headings',
                        columns=(
                            '#1', '#2', '#3', '#4', '#5',
                            '#6', '#7', '#8', '#9'
                        )
                    )
                    table_2.heading('#1', text='Trade #', anchor=tk.W)
                    table_2.heading('#2', text='Type', anchor=tk.W)
                    table_2.heading(
                        '#3', text='Entry date/time', anchor=tk.W
                    )
                    table_2.heading(
                        '#4', text='Exit date/time', anchor=tk.W
                    )
                    table_2.heading(
                        '#5', text='Entry price, USDT', anchor=tk.E
                    )
                    table_2.heading(
                        '#6', text='Exit price, USDT', anchor=tk.E
                    )
                    table_2.heading(
                        '#7', text='Quantity, ' \
                            + self.symbol[:self.symbol.rfind('USDT')],
                        anchor=tk.E
                    )
                    table_2.heading(
                        '#8', text='Profit, USDT', anchor=tk.E
                    )
                    table_2.heading(
                        '#9', text='Profit, %', anchor=tk.E
                    )
                    table_2.column('#1', anchor=tk.W, width=1)
                    table_2.column('#2', anchor=tk.W, width=1)
                    table_2.column('#3', anchor=tk.W, width=1)
                    table_2.column('#4', anchor=tk.W, width=1)
                    table_2.column('#5', anchor=tk.E, width=1)
                    table_2.column('#6', anchor=tk.E, width=1)
                    table_2.column('#7', anchor=tk.E, width=1)
                    table_2.column('#8', anchor=tk.E, width=1)
                    table_2.column('#9', anchor=tk.E, width=1)
                    scroll_bar_2 = ttk.Scrollbar(
                        frame_3, orient=tk.VERTICAL,
                        command=table_2.yview
                    )
                    table_2.configure(yscroll=scroll_bar_2.set)
                    scroll_bar_2.pack(side=tk.RIGHT, fill=tk.Y)
                    data = self.backtesting.strategy.log
                    for i in range(data.shape[0]):
                        values = [i + 1]
                        values.extend(
                            list(data.iloc[i][:-1].astype(str))
                        )
                        table_2.insert('', tk.END, values=values)
                    table_2.pack(fill=tk.BOTH, expand=True)

                else:
                    message = 'No deals\n\n'
                    self.output_window.insert('end', message)

                self.draw_chart()
                message = 'Backtesting completed\n\n'
                self.output_window.insert('end', message)

        settings_window = tk.Tk()
        settings_window.title('Testing period')
        window_width = 245
        window_height = 90
        x = int((self.screen_width / 2) - (window_width / 2))
        y = int((self.screen_height / 2) - (window_height / 2))
        settings_window.geometry(
            '{}x{}+{}+{}'.format(window_width, window_height, x, y)
        )
        frame_form = tk.Frame(settings_window, borderwidth=5)
        frame_form.pack()
        start_label = tk.Label(
            frame_form, text='Start date (yyyy/mm/dd): '
        )
        end_label = tk.Label(
            frame_form, text='End date (yyyy/mm/dd): '
        )
        start_entry = tk.Entry(
            frame_form, width=10, font=['Arial', '12']
        )
        end_entry = tk.Entry(
            frame_form, width=10, font=['Arial', '12']
        )
        start_label.grid(row=0, column=0, sticky=tk.W)
        start_entry.grid(row=0, column=1)
        end_label.grid(row=1, column=0, sticky=tk.W)
        end_entry.grid(row=1, column=1)
        frame_buttons = tk.Frame(settings_window, borderwidth=5)
        frame_buttons.pack(fill=tk.X)
        button = tk.Button(
            frame_buttons, text='Apply', bg='white', fg='black',
            command=start_backtesting
        )
        button.pack()

    def start_automation(self):
        if not self.automation:
            self.automation = True
            self.output_window.insert('end', 'Automation enabled\n\n')
        else:
            self.automation = False
            self.output_window.insert('end', 'Automation disabled\n\n')

    def update_chart(self):
        if not self.optimization[1] and \
                self.exchange.update_data(self.interval, self.symbol):
            self.strategy.forwardtest(
                self.exchange.data
            )
            addplot = self.strategy.get_addplot(
                self.chart_length, self.axes, self.strategy_graphics
            )
            self.axes[0].clear()
            self.axes[2].clear()
            mpf.plot(
                self.exchange.data.tail(self.chart_length),
                type=self.chart_type, style=self.chart_style,
                ylabel='', addplot=addplot, ax=self.axes[0]
            )
            title = 'Binance Futures • ' + \
                self.symbol + ' • ' + self.interval
            self.axes[0].set_title(
                label=title, fontsize=15, style='normal', loc='left'
            )
            self.canvas.draw()

            if self.automation:
                deal_info = self.strategy.trade(
                    self.exchange, self.symbol
                )

                if deal_info is not None:
                    self.output_window.insert('end', deal_info)

        self.after(ms=5000, func=self.update_chart)

    def draw_chart(self):
        self.exchange.set_initial_data(
            self.interval, self.symbol
        )
        self.strategy.backtest(
            self.exchange, self.exchange.data, self.symbol
        )
        addplot = self.strategy.get_addplot(
            self.chart_length, self.axes, self.strategy_graphics
        )
        self.axes[0].clear()
        self.axes[2].clear()
        mpf.plot(
            self.exchange.data.tail(self.chart_length),
            type=self.chart_type, style=self.chart_style,
            ylabel='', addplot=addplot, ax=self.axes[0]
        )
        title = 'Binance Futures • ' + \
            self.symbol + ' • ' + self.interval
        self.axes[0].set_title(
            label=title, fontsize=15, style='normal', loc='left'
        )
        self.canvas.draw()