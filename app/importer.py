import os
import pandas as pd
from flask import current_app
from app.models import PriceDay


class Importer:
    base_dir = ''
    options = {}
    brand = None
    df = None
    line = None


    def __init__(self, options={}):
        print('Start import')


    def __del__(self):
        print('End import')


    def init(self, brand):
        self.base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'

        if not brand:
            raise Exception('brand is required')

        try:
            config = current_app.config['IMPORTER_OPTIONS'][brand]
        except KeyError:
            raise Exception('brand is invalid')

        for key, val in config.items():
            try:
                self.options[key] = config[key]
            except KeyError:
                self.options[key] = val

        self.brand = brand


    def main(self, brand, mode=''):
        if not mode:
            mode = 'all'

        accept_modes = ['all']
        if mode and not mode in accept_modes:
            raise Exception('Invalid Argument')

        self.init(brand)
        self.set_df()
        getattr(self, 'exec_{}'.format(brand))()


    def set_df(self):
        path = '{}{}'.format(self.base_dir, self.options['input_file'])
        self.df = pd.read_csv(path, sep='\t', skiprows=1)


    def exec_jp_topix(self):
        self.df = self.df[self.df['日付'] != '日付']
        self.df = self.df.iloc[::-1]


        for index, row in self.df.iterrows():
            vals = {}
            vals['date'] = row['日付'].replace('/', '-')
            vals['brand_code'] = 'jp_topix'
            vals['price'] = row['終値']
            vals['price_open'] = row['始値']
            vals['price_high'] = row['高値']
            vals['price_low'] = row['安値']
            PriceDay.create(vals)
