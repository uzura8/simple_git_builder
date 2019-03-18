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
    accounts = {}
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


    def main(self, format='dict'):
        if not self.ses:
            self.set_session()

        self.set_accounts()
        transactions = self.scrape_accounts()
        #!!!!!!!!!!!!!!!!
        from pprint import pprint
        pprint(transactions)
        #!!!!!!!!!!!!!!!!


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


    def get_response(self, url):
        if not self.ses:
            self.ses = requests.session()
        r = self.ses.get(url)
        encoding = r.encoding if r.encoding != 'ISO-8859-1' else None
        return BeautifulSoup(r.content, 'html.parser', from_encoding=encoding)


    def set_accounts(self):
        target_url = self.get_url('accounts')
        soup = self.get_response(target_url)
        tables = soup.find_all(id='account-table')

        elms = tables[0].select('a')
        act_dict = self.scrape_account_links(elms, '/accounts/show_manual/')

        elms = tables[1].select('a')
        act_dict_auto = self.scrape_account_links(elms, '/accounts/show/')

        act_dict.update(act_dict_auto)
        self.update_accounts(act_dict)
        self.accounts = act_dict


    def update_accounts(self, act_dict):
        accounts = Account.query.all()
        if accounts:
            for account in accounts:
                code = account.code
                try:
                    name = act_dict[code]
                    if name != account.name:
                        account.name = name
                        accounts[code] = name
                        db.session.add(account)
                        db.session.commit()
                except KeyError:
                    account.delete()
                    db.session.commit()
        else:
            for code, name in act_dict.items():
                account = Account(code=code, name=name)
                db.session.add(account)
                db.session.commit()


    def scrape_account_links(self, elms, uri):
        accounts = {}
        for elm in elms:
            match = re.match(r'' + uri + '(.+)', elm['href'])
            if not match:
                continue
            code = match.group(1)
            name = elm.text.strip().replace('\u3000', ' ').replace(',', '')
            accounts[code] = name
        return accounts


    def scrape_accounts(self):
        for code, name in self.accounts.items():
            target_url = self.get_url('accounts/show/' + code)
            soup = self.get_response(target_url)
            elms = soup.find_all('tr', class_='transaction_list')
            self.scrape_transactions(elms, code)
            time.sleep(self.options['crawl_sleep_sec'])


    def scrape_transactions(self, elms, account_code):
        for elm in elms:
            trs = self.scrape_transaction(elm)
            if not trs:
                continue
            trs['account_code'] = account_code
            category_ids = self.get_category_ids(trs['categories'])
            trs['category_id'] = category_ids['parent']
            del trs['categories']
            Transaction.create(trs)


    def scrape_transaction(self, elm):
        transaction = {}

        target_elm = elm.find('td', class_='amount')
        amount = target_elm.text.strip().replace('\u3000', ' ').replace(',', '')
        if '振替' in amount:
            return
        transaction['amount'] = int(amount)

        items = elm['id'].split('-')
        transaction['id'] = items[2]

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

        return transaction


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
            parent = Category(name=parent_name, parent_id=1)
            db.session.add(parent)
            db.session.commit()
            parent_id = parent.id
        if child_name:
            child_id = Category.get_id_by_name(child_name)
            if not child_id:
                child = Category(name=child_name, parent_id=parent_id)
                db.session.add(child)
                db.session.commit()
                child_id = child.id

        return {'parent':parent_id, 'child':child_id}
