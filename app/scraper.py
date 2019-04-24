import os
import re
import time
from datetime import datetime, timedelta
import requests
import pickle
from flask import current_app
from bs4 import BeautifulSoup
from app import db
from app.models import Account, Transaction, Category
#from urllib.parse import urljoin

class Scraper:
    options = {}
    headers = {}
    ses = None
    base_dir = os.path.dirname(os.path.abspath(__file__)) + '/../'
    session_obj_path = os.path.join(base_dir, 'var/session.bin')

    def __init__(self, options={}):
        config = current_app.config['SCRAPE_OPTIONS']
        for key, val in config.items():
            try:
                self.options[key] = options[key]
            except KeyError:
                self.options[key] = val
        self.headers = {'User-Agent': self.options['user_ua']}


    def main(self, format='dict', mode=''):
        if not mode:
            mode = 'month'

        accept_modes = ['month', 'all_month', 'cate', 'all']
        if mode and not mode in accept_modes:
            raise Exception('Invalid Argument')

        if not self.ses:
            self.set_session()

        if mode in ['cate', 'all']:
            self.scrape_large_cates()

        if mode in ['month', 'all_month', 'all']:
            accounts = self.get_accounts()
            month_num = 12 if mode == 'all_month' else 1
            month_dates = self.get_month_dates(month_num)
            self.scrape_accounts(accounts, month_dates)


    def set_session(self):
        if self.ses:
            pass
        if os.path.exists(self.session_obj_path):
            edited_dt = datetime.fromtimestamp(os.stat(self.session_obj_path).st_mtime)
            expire = timedelta(minutes=self.options['session_expire_min'])
            expire_dt = edited_dt + expire
            now_dt = datetime.now()
            if expire_dt > now_dt:
                with open(self.session_obj_path, 'rb') as f:
                    self.ses = pickle.load(f)
        if not self.ses:
            self.login()


    def get_url(self, path):
        return '{}/{}'.format(self.options['base_url'], path)


    def login(self):
        url = self.get_url('session')
        token = self.getToken()
        params = {
            'utf8': '✓',
            'authenticity_token':token,
            'sign_in_session_service[email]': self.options['user_id'],
            'sign_in_session_service[password]': self.options['user_pass'],
            'commit': 'ログイン',
        }
        headers = self.headers
        headers['Origin'] = self.options['base_url']
        headers['Upgrade-Insecure-Requests'] = '1'
        headers['Referer'] = self.get_url('users/sign_in')
        headers['Content-Type'] = 'application/x-www-form-urlencoded'
        res = self.ses.post(url, data=params, headers=self.headers)
        res.raise_for_status() # rise exception, if error

        # save session
        f = open(self.session_obj_path, 'wb')
        pickle.dump(self.ses, f)
        f.close()

        return self.ses


    def getToken(self):
        target_url = self.get_url('users/sign_in')
        soup = self.get_response(target_url)
        elms = soup.findAll(attrs={'name': 'authenticity_token'})
        return elms[0]['value']


    def get_response(self, url, cookies={}):
        if not self.ses:
            self.ses = requests.session()
        r = self.ses.get(url, cookies=cookies)
        encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
        return BeautifulSoup(r.content, 'html.parser', from_encoding=encoding)


    def get_accounts(self):
        target_url = self.get_url('accounts')
        soup = self.get_response(target_url)
        tables = soup.find_all(id='account-table')

        if len(tables) == 2:
            elms = tables[0].select('a')
            accounts_manual = self.scrape_account_links(elms, '/accounts/show_manual/')
            table_index = 1
        else:
            accounts_manual = []
            table_index = 0

        elms = tables[table_index].select('a')
        accounts = self.scrape_account_links(elms, '/accounts/show/')
        accounts.extend(accounts_manual)

        self.update_accounts(accounts)
        return accounts


    def update_accounts(self, accounts):
        model_accounts = Account.query.filter(Account.code != 'manual').all()
        if model_accounts:
            for model_account in model_accounts:
                code = model_account.code
                account = next(item for item in accounts \
                                                if item['code'] == code)
                if not account:
                    model_account.delete()
                    db.session.commit()
                else:
                    if model_account.name != account['name']:
                        model_account.name = account['name']
                        db.session.add(model_account)
                        db.session.commit()
        else:
            for account in accounts:
                model_account = Account(
                    code=account['code'],
                    name=account['name']
                )
                db.session.add(model_account)
                db.session.commit()


    def scrape_account_links(self, elms, uri):
        accounts = []
        for elm in elms:
            match = re.match(r'' + uri + '(.+)', elm['href'])
            if not match:
                continue
            code = match.group(1)
            name = elm.text.strip().replace('\u3000', ' ').replace(',', '')
            is_manual = True if uri == '/accounts/show_manual/' else False
            accounts.append({'code':code, 'name':name, 'is_manual':is_manual})
        return accounts


    def scrape_accounts(self, accounts, month_dates):
        for account in accounts:
            for month_date in month_dates:
                self.scrape_account(account, month_date)


    def scrape_account(self, account, month_date):
        code = account['code']
        is_manual = account['is_manual']
        uri = 'accounts/show_manual/' if is_manual else 'accounts/show/'
        target_url = self.get_url(uri + code)
        cookies = dict(cf_last_fetch_from_date=month_date)
        soup = self.get_response(target_url, cookies=cookies)
        elms = soup.find_all('tr', class_='transaction_list')
        self.scrape_transactions(elms, code)
        time.sleep(self.options['crawl_sleep_sec'])


    def scrape_transactions(self, elms, account_code):
        for elm in elms:
            result = self.scrape_transaction(elm)
            if not result:
                continue

            trs = result[0]
            service_id = result[1]
            trs['account_code'] = account_code
            category_ids = self.get_category_ids(trs['categories'])
            trs['category_id'] = category_ids['parent']
            del trs['categories']
            Transaction.create(trs, service_id=service_id)


    def scrape_transaction(self, elm):
        transaction = {}

        target_elm = elm.find('td', class_='amount')
        amount = target_elm.text.strip().replace('\u3000', ' ').replace(',', '')
        if '振替' in amount:
            return
        transaction['amount'] = int(amount)

        items = elm['id'].split('-')
        service_id = items[2]

        name_elm = elm.find('td', class_='content')
        transaction['name'] = name_elm.text.strip().replace('\u3000', ' ')

        target_elm = elm.find('td', class_='date')
        items = target_elm['data-table-sortable-value'].split('-')
        transaction['date'] = items[0].replace('/', '-')

        transaction['categories'] = {}
        target_elm = elm.find('a', class_='v_l_ctg')
        transaction['categories']['parent'] = target_elm.text.strip() \
                                                if target_elm else ''
        target_elm = elm.find('a', class_='v_m_ctg')
        transaction['categories']['child'] = target_elm.text.strip() \
                                                if target_elm else ''

        return transaction, service_id


    def scrape_large_cates(self):
        target_url = self.get_url('large_category_spending_types/edit')
        soup = self.get_response(target_url)
        elms = soup.find_all('tr', class_='large_category')
        for elm in elms:
            target_elm = elm.find('th')
            cate_name = target_elm.text.strip()
            Category.save(name=cate_name, parent_id=1)


    def get_category_ids(self, names):
        parent_id = 0
        child_id = 0
        try:
            parent_name = names['parent']
        except IndexError:
            parent_name = ''

        try:
            child_name = names['child']
        except IndexError:
            child_name = ''

        if not parent_name:
            return {'parent':parent_id, 'child':child_id}

        parent_id = Category.get_id_by_name(parent_name)
        if not parent_id:
            parent = Category.save(name=parent_name, parent_id=1)
            parent_id = parent.id
        if child_name:
            child_id = Category.get_id_by_name(child_name)
            if not child_id:
                child = Category.save(name=child_name, parent_id=parent_id)
                child_id = child.id

        return {'parent':parent_id, 'child':child_id}


    @staticmethod
    def get_month_dates(month_num):
        dates = []
        today = datetime.today()
        date = datetime(today.year, today.month, 1)
        for i in range(month_num):
            dates.append(date.strftime('%Y/%m/%d'))
            lastmonth = date + timedelta(days=-1)
            date = datetime(lastmonth.year, lastmonth.month, 1)

        return dates
