from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app import db
from sqlalchemy_mptt.mixins import BaseNestedSets

class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class SiteConfig(db.Model, TimestampMixin):
    """
    site_config model
    """
    __tablename__ = 'site_config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    value = db.Column('value', db.Text)

    @classmethod
    def get_value_by_name(self, name):
        try:
            config = self.query.filter(self.name == name).one()
            return config.value
        except NoResultFound:
            return None

    @classmethod
    def get_dict(self):
        try:
            rows = self.query.all()
            configs = {}
            for row in rows:
                key = row.name
                configs[key] = row.value
            return configs
        except NoResultFound:
            return None

    @classmethod
    def save(self, name, value):
        try:
            config = self.query.filter(self.name == name).one()
            if value == config.value:
                return
            config.value = value
        except KeyError:
            config = self(
                name=name,
                value=value
            )
        db.session.add(config)
        db.session.commit()
        return config


class Account(db.Model, TimestampMixin):
    """
    account model
    """
    __tablename__ = 'account'
    code = db.Column('code', db.String(50), nullable=False, primary_key = True)
    name = db.Column('name', db.String(256), nullable=False)
    #transaction = db.relationship('Transaction')

    @classmethod
    def get_dict(self):
        try:
            rows = self.query.all()
            assoc = {}
            for row in rows:
                key = row.code
                assoc[key] = row.name
            return assoc
        except NoResultFound:
            return assoc


class Transaction(db.Model, TimestampMixin):
    """
    transaction model
    """
    __tablename__ = 'transaction'
    id = db.Column('id', db.BigInteger, primary_key = True, autoincrement=False)
    account_code = db.Column('account_code', db.String(50), \
        db.ForeignKey('account.code', onupdate='CASCADE', ondelete='CASCADE'), \
        nullable=False)
    name = db.Column('name', db.String(512), nullable=False)
    amount = db.Column('amount', db.Integer, nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    account = db.relation('Account', order_by='Account.code',
                           uselist=False, backref='transaction')


    def to_dict(self):
        data = {
            'id': self.id,
            'account_code': self.account_code,
            'name': self.name,
            'amount': self.amount,
            'date': self.date,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'account_name': self.account.name,
        }
        return data


    @classmethod
    def get_one_by_id(self, id):
        try:
            return self.query.filter(self.id == id).one()
        except NoResultFound:
            return None

    @classmethod
    def create(self, kwargs):
        try:
            transaction = self.get_one_by_id(kwargs['id'])
            if transaction:
                return transaction
        except KeyError:
            return

        transaction = self(
            id=kwargs['id'],
            account_code=kwargs['account_code'],
            name=kwargs['name'],
            amount=kwargs['amount'],
            date=kwargs['date'],
            category_id=kwargs['category_id']
        )
        db.session.add(transaction)
        db.session.commit()
        return transaction


class Category(db.Model, TimestampMixin, BaseNestedSets):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(256), index=True, unique=True)
    transactions = db.relationship('Transaction', backref='transaction', lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @classmethod
    def get_id_by_name(self, name):
        try:
            category = self.query.filter(self.name == name).one()
            return category.id
        except NoResultFound:
            return None

    @classmethod
    def get_categories(self, name='root', is_json=False):
        categories = self.query.all()
        for item in categories:
            if item.name != name:
                continue
            if not is_json:
                return item.drilldown_tree()
            return item.drilldown_tree(json=True, json_fields=self.cat_to_json)

    @staticmethod
    def cat_to_json(item):
        return {
            'id': item.id,
            'name': item.name
        }


def setup_fixurtes():
    if Category.query.count() == 0:
        db.session.add(Category(name='root'))
        db.session.commit()
