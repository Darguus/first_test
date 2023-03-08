import pandas as pd
import numpy as np


class Tester():
    def calculate_performance(self, log, initial_capital):
        self.equity = \
            pd.concat(
                [pd.Series(initial_capital), log.pnl],
                ignore_index=True  
            ).cumsum()
        self.equity.index += 1

        try:
            gross_profit = log.loc[:, ['deal_type','pnl']]. \
                query('pnl > 0').groupby('deal_type'). \
                    agg('sum', numeric_only=True)
        except:
            pass
        try:
            all_gross_profit = round(
                gross_profit.pnl.sum(), 2
            )
            all_gross_profit_per = round(
                all_gross_profit / initial_capital * 100, 2
            )
        except:
             all_gross_profit = 0.0
             all_gross_profit_per = 0.0
        try:
            long_gross_profit = round(
                gross_profit.at['long', 'pnl'], 2
            )
            long_gross_profit_per = round(
                long_gross_profit / initial_capital * 100, 2
            )
        except:
            long_gross_profit = 0.0
            long_gross_profit_per = 0.0
        try:
            short_gross_profit = round(
                gross_profit.at['short', 'pnl'], 2
            )
            short_gross_profit_per = round(
                short_gross_profit / initial_capital * 100, 2
            )
        except:
            short_gross_profit = 0.0
            short_gross_profit_per = 0.0

        try:
            gross_loss = log.loc[:, ['deal_type','pnl']]. \
                query('pnl <= 0').groupby('deal_type'). \
                    agg('sum', numeric_only=True)
        except:
            pass
        try:
            all_gross_loss = round(
                abs(gross_loss.pnl.sum()), 2
            )
            all_gross_loss_per = round(
                all_gross_loss / initial_capital * 100, 2
            )
        except:
            all_gross_loss = 0.0
            all_gross_loss_per = 0.0
        try:
            long_gross_loss = round(
                abs(gross_loss.at['long', 'pnl']), 2
            )
            long_gross_loss_per = round(
                long_gross_loss / initial_capital * 100, 2
            )
        except:
            long_gross_loss = 0.0
            long_gross_loss_per = 0.0
        try:
            short_gross_loss = round(
                abs(gross_loss.at['short', 'pnl']), 2
            )
            short_gross_loss_per = round(
                short_gross_loss / initial_capital * 100, 2
            )
        except:
            short_gross_loss = 0.0
            short_gross_loss_per = 0.0

        try:
            all_net_profit = round(
                all_gross_profit - all_gross_loss, 2
            )
            all_net_profit_per = round(
                all_net_profit / initial_capital * 100, 2
            )
        except:
            all_net_profit = 0.0
            all_net_profit_per = 0.0
        try:
            long_net_profit = round(
                long_gross_profit - long_gross_loss, 2
            )
            long_net_profit_per = round(
                long_net_profit / initial_capital * 100, 2
            )
        except:
            long_net_profit = 0.0
            long_net_profit_per = 0.0
        try:
            short_net_profit = round(
                short_gross_profit - short_gross_loss, 2
            )
            short_net_profit_per = round(
                short_net_profit / initial_capital * 100, 2
            )
        except:
            short_net_profit = 0.0
            short_net_profit_per = 0.0

        try:
            drawdowns = []
            drawdowns_per = []
            max_equity = self.equity.iloc[0]
            for i in range(1, self.equity.shape[0]):
                if self.equity.iloc[i] > max_equity:
                    max_equity = self.equity.iloc[i]
                if self.equity.iloc[i] < self.equity.iloc[i - 1]:
                    min_equity = self.equity.iloc[i]
                    drawdown = min_equity - max_equity
                    drawdown_per = (min_equity / max_equity - 1) * 100
                    drawdowns.append(drawdown)
                    drawdowns_per.append(drawdown_per)
            all_max_drawdown = round(abs(min(drawdowns)), 2)
            all_max_drawdown_per = round(abs(min(drawdowns_per)), 2)
        except:
            all_max_drawdown = 0.0
            all_max_drawdown_per = 0.0

        try:
            all_skew = round(log.pnl_per.skew(), 3)
        except:
            all_skew = np.nan

        try:
            if all_gross_loss != 0:
                all_profit_factor = round(
                    all_gross_profit / all_gross_loss, 3
                )
            else:
                all_profit_factor = np.nan
        except:
            all_profit_factor = np.nan
        try:
            if long_gross_loss != 0:
                long_profit_factor =  round(
                    long_gross_profit / long_gross_loss, 3
                )
            else:
                long_profit_factor = np.nan
        except:
            long_profit_factor = np.nan
        try:
            if short_gross_loss != 0:
                short_profit_factor = round(
                    short_gross_profit / short_gross_loss, 3
                )
            else:
                short_profit_factor = np.nan
        except:
            short_profit_factor = np.nan

        try:
            commission_paid = log.loc[:, ['deal_type','commission']]. \
                groupby('deal_type').agg('sum', numeric_only=True)
        except:
            pass
        try:
            all_commission_paid = round(
                commission_paid.commission.sum(), 2
            )
        except:
            all_commission_paid = 0.0
        try:
            long_commission_paid = round(
                commission_paid.at['long', 'commission'], 2
            )
        except:
            long_commission_paid = 0.0
        try:
            short_commission_paid = round(
                commission_paid.at['short', 'commission'], 2
            )
        except:
            short_commission_paid = 0.0

        all_total_closed_trades = int(log.shape[0])
        long_total_closed_trades = int(
            log.query('deal_type == "long"').shape[0]
        )
        short_total_closed_trades = int(
            log.query('deal_type == "short"').shape[0]
        )

        all_number_winning_trades = int(log.query('pnl > 0').shape[0])
        long_number_winning_trades = int(
            log.query('deal_type == "long" and pnl > 0').shape[0]
        )
        short_number_winning_trades = int(
            log.query('deal_type == "short" and pnl > 0').shape[0]
        )

        all_number_losing_trades = int(log.query('pnl <= 0').shape[0])
        long_number_losing_trades = int(
            log.query('deal_type == "long" and pnl <= 0').shape[0]
        )
        short_number_losing_trades = int(
            log.query('deal_type == "short" and pnl <= 0').shape[0]
        )

        try:
            all_percent_profitable = round(
                all_number_winning_trades / 
                    all_total_closed_trades * 100,
                2
            )
        except:
            all_percent_profitable = np.nan
        try:
            long_percent_profitable = round(
                long_number_winning_trades / 
                    long_total_closed_trades * 100,
                2
            )
        except:
            long_percent_profitable = np.nan
        try:
            short_percent_profitable = round(
                short_number_winning_trades / 
                    short_total_closed_trades * 100,
                2
            )
        except:
            short_percent_profitable = np.nan

        try:
            all_avg_trade = round(log.pnl.mean(), 2)
            all_avg_trade_per = round(log.pnl_per.mean(), 2)
        except:
            all_avg_trade = np.nan
        try:
            long_avg_trade = round(
                log.query('deal_type == "long"').pnl.mean(), 2
            )
            long_avg_trade_per = round(
                log.query('deal_type == "long"').pnl_per.mean(), 2
            )
        except:
            long_avg_trade = np.nan
        try:
            short_avg_trade = round(
                log.query('deal_type == "short"').pnl.mean(), 2
            )
            short_avg_trade_per = round(
                log.query('deal_type == "short"').pnl_per.mean(), 2
            )
        except:
            short_avg_trade = np.nan

        try:
            all_avg_winning_trade = round(
                log.query('pnl > 0').pnl.mean(), 2
            )
            all_avg_winning_trade_per = round(
                log.query('pnl_per > 0').pnl_per.mean(), 2
            )
        except:
            all_avg_winning_trade = np.nan
        try:
            long_avg_winning_trade = round(
                log.query('deal_type == "long" and pnl > 0'). \
                    pnl.mean(), 2
            )
            long_avg_winning_trade_per = round(
                log.query('deal_type == "long" and pnl_per > 0'). \
                    pnl_per.mean(),
                2
            )
        except:
            long_avg_winning_trade = np.nan
        try:
            short_avg_winning_trade = round(
                log.query('deal_type == "short" and pnl > 0'). \
                    pnl.mean(), 2
            )
            short_avg_winning_trade_per = round(
                log.query('deal_type == "short" and pnl_per > 0'). \
                    pnl_per.mean(),
                2
            )
        except:
            short_avg_winning_trade = np.nan

        try:
            all_avg_losing_trade = round(
                abs(log.query('pnl <= 0').pnl.mean()), 2
            )
            all_avg_losing_trade_per = round(
                abs(log.query('pnl_per <= 0').pnl_per.mean()), 2
            )
        except:
            all_avg_losing_trade = np.nan
        try:
            long_avg_losing_trade = round(
                abs(log.query('deal_type == "long" and pnl <= 0'). \
                    pnl.mean()),
                2
            )
            long_avg_losing_trade_per = round(
                abs(log.query(
                    'deal_type == "long" and pnl_per <= 0'
                ).pnl_per.mean()),
                2
            )
        except:
            long_avg_losing_trade = np.nan
        try:
            short_avg_losing_trade = round(
                abs(log.query('deal_type == "short" and pnl <= 0'). \
                    pnl.mean()),
                2
            )
            short_avg_losing_trade_per = round(
                abs(log.query(
                    'deal_type == "short" and pnl_per <= 0'
                ).pnl_per.mean()),
                2
            )
        except:
            short_avg_losing_trade = np.nan

        try:
            all_ratio_avg_win_loss = round(
                all_avg_winning_trade / all_avg_losing_trade, 3
            )
        except:
            all_ratio_avg_win_loss = np.nan
        try:
            long_ratio_avg_win_loss = round(
                long_avg_winning_trade / long_avg_losing_trade, 3
            )
        except:
            long_ratio_avg_win_loss = np.nan
        try:
            short_ratio_avg_win_loss = round(
                short_avg_winning_trade / short_avg_losing_trade, 3
            )
        except:
            short_ratio_avg_win_loss = np.nan

        try:
            all_sortino_ratio = round(
                all_avg_trade_per / ((log.query('pnl_per <= 0'). \
                    pnl_per ** 2).mean() ** 0.5),
                3
            )
        except:
            all_sortino_ratio = np.nan

        try:
            all_largest_winning_trade = round(
                log.query('pnl > 0').max().loc['pnl'], 2
            )
            all_largest_winning_trade_per = round(
                log.query('pnl_per > 0').max().loc['pnl_per'], 2
            )
        except:
            all_largest_winning_trade = np.nan
        try:
            long_largest_winning_trade = round(
                log.query('deal_type == "long" and pnl > 0'). \
                    max().loc['pnl'], 
                2
            )
            long_largest_winning_trade_per = round(
                log.query('deal_type == "long" and pnl_per > 0'). \
                    max().loc['pnl_per'], 
                2
            )
        except:
            long_largest_winning_trade = np.nan
        try:
            short_largest_winning_trade = round(
                log.query('deal_type == "short" and pnl > 0'). \
                    max().loc['pnl'], 
                2
            )
            short_largest_winning_trade_per = round(
                log.query('deal_type == "short" and pnl_per > 0'). \
                    max().loc['pnl_per'], 
                2
            )
        except:
            short_largest_winning_trade = np.nan

        try:
            all_largest_losing_trade = round(
                abs(log.query('pnl <= 0').min().loc['pnl']), 2
            )
            all_largest_losing_trade_per = round(
                abs(log.query('pnl_per <= 0').min().loc['pnl_per']), 2
            )
        except:
            all_largest_losing_trade = np.nan
        try:
            long_largest_losing_trade = round(
                abs(log.query(
                    'deal_type == "long" and pnl <= 0'
                ).min().loc['pnl']),
                2
            )
            long_largest_losing_trade_per = round(
                abs(log.query(
                    'deal_type == "long" and pnl_per <= 0'
                ).min().loc['pnl_per']),
                2
            )
        except:
            long_largest_losing_trade = np.nan
        try:
            short_largest_losing_trade = round(
                abs(log.query(
                    'deal_type == "short" and pnl <= 0'
                ).min().loc['pnl']),
                2
            )
            short_largest_losing_trade_per = round(
                abs(log.query(
                    'deal_type == "short" and pnl_per <= 0'
                ).min().loc['pnl_per']),
                2
            )
        except:
            short_largest_losing_trade = np.nan

        self.performance_metrics = pd.DataFrame(
            {
                'Title': [
                    'Net profit, USDT',
                    'Net profit, %',
                    'Gross profit, USDT',
                    'Gross profit, %',
                    'Gross loss, USDT',
                    'Gross loss, %',
                    'Max drawdown, USDT',
                    'Max drawdown, %',
                    'Sortino ratio',
                    'Skew',
                    'Profit factor',
                    'Commission paid, USDT',
                    'Total closed trades',
                    'Number winning trades',
                    'Number losing trades',
                    'Percent profitable',
                    'Avg trade, USDT',
                    'Avg trade, %',
                    'Avg winning trade, USDT',
                    'Avg winning trade, %',
                    'Avg losing trade, USDT',
                    'Avg losing trade, %',
                    'Ratio avg win / avg loss',
                    'Largest winning trade, USDT',
                    'Largest winning trade, %',
                    'Largest losing trade, USDT',
                    'Largest losing trade, %',
            ],
                'All': [
                    all_net_profit,
                    all_net_profit_per,
                    all_gross_profit,
                    all_gross_profit_per,
                    all_gross_loss,
                    all_gross_loss_per,
                    all_max_drawdown,
                    all_max_drawdown_per,
                    all_sortino_ratio,
                    all_skew,
                    all_profit_factor,
                    all_commission_paid,
                    str(all_total_closed_trades),
                    str(all_number_winning_trades),
                    str(all_number_losing_trades),
                    all_percent_profitable,
                    all_avg_trade,
                    all_avg_trade_per,
                    all_avg_winning_trade,
                    all_avg_winning_trade_per,
                    all_avg_losing_trade,
                    all_avg_losing_trade_per,
                    all_ratio_avg_win_loss,
                    all_largest_winning_trade,
                    all_largest_winning_trade_per,
                    all_largest_losing_trade,
                    all_largest_losing_trade_per
                ],
                'Long': [
                    long_net_profit,
                    long_net_profit_per,
                    long_gross_profit,
                    long_gross_profit_per,
                    long_gross_loss,
                    long_gross_loss_per,
                    '',
                    '',
                    '',
                    '',
                    long_profit_factor,
                    long_commission_paid,
                    str(long_total_closed_trades),
                    str(long_number_winning_trades),
                    str(long_number_losing_trades),
                    long_percent_profitable,
                    long_avg_trade,
                    long_avg_trade_per,
                    long_avg_winning_trade,
                    long_avg_winning_trade_per,
                    long_avg_losing_trade,
                    long_avg_losing_trade_per,
                    long_ratio_avg_win_loss,
                    long_largest_winning_trade,
                    long_largest_winning_trade_per,
                    long_largest_losing_trade,
                    long_largest_losing_trade_per
                ],
                'Short': [
                    short_net_profit,
                    short_net_profit_per,
                    short_gross_profit,
                    short_gross_profit_per,
                    short_gross_loss,
                    short_gross_loss_per,
                    '',
                    '',
                    '',
                    '',
                    short_profit_factor,
                    short_commission_paid,
                    str(short_total_closed_trades),
                    str(short_number_winning_trades),
                    str(short_number_losing_trades),
                    short_percent_profitable,
                    short_avg_trade,
                    short_avg_trade_per,
                    short_avg_winning_trade,
                    short_avg_winning_trade_per,
                    short_avg_losing_trade,
                    short_avg_losing_trade_per,
                    short_ratio_avg_win_loss,
                    short_largest_winning_trade,
                    short_largest_winning_trade_per,
                    short_largest_losing_trade,
                    short_largest_losing_trade_per
                ]
            }
        )
        self.performance_metrics = \
            self.performance_metrics.fillna('').astype(str)

    def start_testing(
                self, exchange, interval, 
                symbol, start, end, strategy):
        self.data = exchange.get_data(interval, symbol, start, end) 
        self.strategy = strategy
        self.strategy.backtest(exchange, self.data, symbol)

        if self.strategy.log.shape[0] > 0:
            self.calculate_performance(
                self.strategy.log, self.strategy.initial_capital
            )
            return True
        else:
            return False