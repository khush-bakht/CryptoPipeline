#strategies/strategy_pipeline/generator.py
import random
import pandas as pd
from strategies.strategy_pipeline.utils.indicator_utils import INDICATORS


class StrategyGenerator:
    def __init__(self, config):
        self.config = config

    def generate_strategy(self,index):
    
        strategy = {
            'name': f"{self.config['base_filename']}_{self.config['prefix']}{index}",
            'exchange': self.config['exchange'],
            'symbol': random.choice(self.config['symbol_list']),
            'time_horizon': random.choice(self.config['time_horizons'])
        }
        for indicator in INDICATORS:
            strategy[indicator] = random.choice([True, False])
        return strategy

