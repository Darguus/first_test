import strategy as strat
import functions as f
import datetime as dt
import random as r
import time


class GA():
    # parameters
    iterations = 200
    mutation_prob = 90
    population_size = 50
    population_limit = 80
    #

    individual_len = 23
    best_score = float('-inf')

    stop_type_range = [i for i in range(1, 3)]
    stop_range = [i / 10 for i in range(5, 31)]
    trail_stop_range = [i for i in range(1, 6)]
    take_percent_1_range = [i / 10 for i in range(20, 46)]
    take_percent_2_range = [i / 10 for i in range(47, 76)]
    take_percent_3_range = [i / 10 for i in range(77, 116)]
    take_percent_4_range = [i / 10 for i in range(117, 146)]
    take_percent_5_range = [i / 10 for i in range(147, 241)]
    take_volume_list = [
        f.get_volume_list(r.sample(range(10, 95, 5), 4))
            for i in range(1000)
    ]
    st_atr_period_range = [i for i in range(3, 21)]
    st_factor_range = [i / 100 for i in range(2000, 2501, 5)]
    st_upper_band_range = [i / 10 for i in range(46, 71)]
    st_lower_band_range = [i / 10 for i in range(20, 37)]
    rsi_length_range = [i for i in range(6, 22)]
    rsi_long_upper_bound_range = [i for i in range(29, 51)]
    rsi_long_lower_bound_range = [i for i in range(1, 29)]
    rsi_short_upper_bound_range = [i for i in range(69, 101)]
    rsi_short_lower_bound_range = [i for i in range(50, 69)]
    filter_range = [i for i in range(2)]
    ma_length_range = [i for i in range(5, 26)]
    bb_mult_range = [i / 10 for i in range(15, 31)]
    bb_long_bound_range = [i for i in range(20, 51)]
    bb_short_bound_range = [i for i in range(50, 81)]

    dict_range = {
        1: stop_type_range,
        2: stop_range,
        3: trail_stop_range,
        4: take_percent_1_range,
        5: take_percent_2_range,
        6: take_percent_3_range,
        7: take_percent_4_range,
        8: take_percent_5_range,
        9: take_volume_list,
        10: st_atr_period_range,
        11: st_factor_range,
        12: st_upper_band_range,
        13: st_lower_band_range,
        14: rsi_length_range,
        15: rsi_long_upper_bound_range,
        16: rsi_long_lower_bound_range,
        17: rsi_short_upper_bound_range,
        18: rsi_short_lower_bound_range,
        19: filter_range,
        20: ma_length_range,
        21: bb_mult_range,
        22: bb_long_bound_range,
        23: bb_short_bound_range
    }

    def fitness_calculation(self, individual):
        strategy = strat.Strategy()
        strategy.stop_type = individual[0]
        strategy.stop = individual[1]
        strategy.trail_stop = individual[2]
        strategy.take_percent[0] = individual[3]
        strategy.take_percent[1] = individual[4]
        strategy.take_percent[2] = individual[5]
        strategy.take_percent[3] = individual[6]
        strategy.take_percent[4] = individual[7]
        strategy.take_volume[0] = individual[8][0]
        strategy.take_volume[1] = individual[8][1]
        strategy.take_volume[2] = individual[8][2]
        strategy.take_volume[3] = individual[8][3]
        strategy.take_volume[4] = individual[8][4]
        strategy.st_atr_period = individual[9]
        strategy.st_factor = individual[10]
        strategy.st_upper_band = individual[11]
        strategy.st_lower_band = individual[12]
        strategy.rsi_length = individual[13]
        strategy.rsi_long_upper_bound = individual[14]
        strategy.rsi_long_lower_bound = individual[15]
        strategy.rsi_short_upper_bound = individual[16]
        strategy.rsi_short_lower_bound = individual[17]
        strategy.filter = individual[18]
        strategy.ma_length = individual[19]
        strategy.bb_mult = individual[20]
        strategy.bb_long_bound = individual[21]
        strategy.bb_short_bound = individual[22]
        strategy.backtest(self.exchange, self.data, self.symbol)
        return strategy.net_profit

    def create_initial_population(self):
        self.individuals = [
            [r.choice(j) for j in self.dict_range.values()]
            for i in range(self.population_size)
        ]
        self.population = {
            self.fitness_calculation(self.individuals[i]):
                self.individuals[i]
            for i in range(self.population_size)
        }

    def selection(self):
        parent_1 = self.population[max(self.population)]
        population_copy = self.population.copy()
        del population_copy[max(self.population)]
        r_number = r.randint(0, 2)
        if r_number == 0:
            parent_2 = population_copy[max(population_copy)]
        elif r_number == 1:
            parent_2 = r.choice(list(population_copy.values()))
        elif r_number == 2:
            parent_2 = population_copy[min(population_copy)]
        self.parents = [parent_1, parent_2]

    def crossover(self):
        r_number = r.randint(0, 1)
        if r_number == 0:
            sep = r.randint(1, self.individual_len - 1)
            child_1 = self.parents[0][:sep] + self.parents[1][sep:]
            child_2 = self.parents[1][:sep] + self.parents[0][sep:]
            self.childs = [child_1, child_2]
        elif r_number == 1:
            sep_1 = r.randint(1, self.individual_len // 2 - 1)
            sep_2 = r.randint(
                self.individual_len // 2 + 1, self.individual_len - 1
            )
            child_1 = self.parents[0].copy()
            child_2 = self.parents[1].copy()
            child_1[sep_1:sep_2] = self.parents[1][sep_1:sep_2]
            child_2[sep_1:sep_2] = self.parents[0][sep_1:sep_2]
            self.childs = [child_1, child_2]

    def mutation(self):
         r_number = r.randint(0, 1)
         if r_number == 0:
             if r.randint(0, 100) <= self.mutation_prob:
                 gene_number = r.randint(1, self.individual_len)
                 gene_value = r.choice(self.dict_range[gene_number])
                 child_number = r.randint(0, 1)
                 self.childs[child_number][gene_number - 1] = \
                    gene_value
         elif r_number == 1:
             child_number = r.randint(0, 1)
             for i in range(self.individual_len):
                 if r.randint(0, 100) <= self.mutation_prob:
                     gene_value = r.choice(self.dict_range[i + 1])
                     self.childs[child_number][i] = gene_value

    def expand_population(self):
        score_1 = self.fitness_calculation(self.childs[0])
        score_2 = self.fitness_calculation(self.childs[1])
        self.population[score_1] = self.childs[0]
        self.population[score_2] = self.childs[1]

    def find_best_individual(self, iteration):
        if self.best_score < max(self.population):
            self.best_score = max(self.population)
            self.best_individual = self.population[self.best_score]

            f = open(self.chart + '.txt', 'a')
            print(
                'stop_type: ', self.best_individual[0], '\n',
                'stop: ', self.best_individual[1], '\n',
                'trail_stop: ', self.best_individual[2], '\n',
                'take_percent_1: ', self.best_individual[3], '\n',
                'take_percent_2: ', self.best_individual[4], '\n',
                'take_percent_3: ', self.best_individual[5], '\n',
                'take_percent_4: ', self.best_individual[6], '\n',
                'take_percent_5: ', self.best_individual[7], '\n',
                'take_volume_1: ', self.best_individual[8][0], '\n',
                'take_volume_2: ', self.best_individual[8][1], '\n',
                'take_volume_3: ', self.best_individual[8][2], '\n',
                'take_volume_4: ', self.best_individual[8][3], '\n',
                'take_volume_5: ', self.best_individual[8][4], '\n',
                'st_atr_period: ', self.best_individual[9], '\n',
                'st_factor: ', self.best_individual[10], '\n',
                'st_upper_band: ', self.best_individual[11], '\n',
                'st_lower_band: ', self.best_individual[12], '\n',
                'rsi_length: ', self.best_individual[13], '\n',
                'rsi_long_upper_bound: ', 
                    self.best_individual[14], '\n',
                'rsi_long_lower_bound: ', 
                    self.best_individual[15], '\n',
                'rsi_short_upper_bound: ', 
                    self.best_individual[16], '\n',
                'rsi_short_lower_bound: ', 
                    self.best_individual[17], '\n',
                'filter: ', self.best_individual[18], '\n',
                'ma_length: ', self.best_individual[19], '\n',
                'bb_mult: ', self.best_individual[20], '\n',
                'bb_long_bound: ', self.best_individual[21], '\n',
                'bb_short_bound: ', self.best_individual[22], '\n\n',
                self.trading_period, '\n',
                'Net profit = ' + str(self.best_score) + ' USDT\n',
                sep='', file=f
            )
            f.close()
            message = 'Iteration #' + str(iteration + 1) + ':\n' + \
                'Net profit = ' + str(self.best_score) + ' USDT\n\n'
            self.gui.output_window.insert('end', message)
            self.gui.update()

    def reduce_population(self):
        while len(self.population) > self.population_limit:
            del self.population[min(self.population)]

    def optimize(self, exchange, interval, symbol, start, end, gui):
        self.data = exchange.get_data(interval, symbol, start, end)
        self.trading_period = \
            str(self.data.index[0]) + ' - ' + str(self.data.index[-1])
        self.chart = str(symbol) + '_' + str(interval)
        self.exchange = exchange
        self.symbol = symbol
        self.gui = gui

        self.create_initial_population()
        for i in range(self.iterations):
            self.selection()
            self.crossover()
            self.mutation()
            self.expand_population()
            self.find_best_individual(i)
            self.reduce_population()
        self.best_score = float('-inf')

    def change_parameters(self, strategy):
        strategy.stop_type = self.best_individual[0]
        strategy.stop = self.best_individual[1]
        strategy.trail_stop = self.best_individual[2]
        strategy.take_percent[0] = self.best_individual[3]
        strategy.take_percent[1] = self.best_individual[4]
        strategy.take_percent[2] = self.best_individual[5]
        strategy.take_percent[3] = self.best_individual[6]
        strategy.take_percent[4] = self.best_individual[7]
        strategy.take_volume[0] = self.best_individual[8][0]
        strategy.take_volume[1] = self.best_individual[8][1]
        strategy.take_volume[2] = self.best_individual[8][2]
        strategy.take_volume[3] = self.best_individual[8][3]
        strategy.take_volume[4] = self.best_individual[8][4]
        strategy.st_atr_period = self.best_individual[9]
        strategy.st_factor = self.best_individual[10]
        strategy.st_upper_band = self.best_individual[11]
        strategy.st_lower_band = self.best_individual[12]
        strategy.rsi_length = self.best_individual[13]
        strategy.rsi_long_upper_bound = self.best_individual[14]
        strategy.rsi_long_lower_bound = self.best_individual[15]
        strategy.rsi_short_upper_bound = self.best_individual[16]
        strategy.rsi_short_lower_bound = self.best_individual[17]
        strategy.filter = self.best_individual[18]
        strategy.ma_length = self.best_individual[19]
        strategy.bb_mult = self.best_individual[20]
        strategy.bb_long_bound = self.best_individual[21]
        strategy.bb_short_bound = self.best_individual[22]