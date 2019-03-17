from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app import db
from flask import current_app
from sqlalchemy_mptt.mixins import BaseNestedSets

class TimestampMixin(object):
    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


class Account(db.Model, TimestampMixin):
    """
    account model
    """
    __tablename__ = 'account'
    code = db.Column('code', db.String(20), nullable=False, primary_key = True)
    name = db.Column('name', db.String(256), nullable=False)
    transaction = db.relationship('Transaction')


class Transaction(db.Model, TimestampMixin):
    """
    transaction model
    """
    __tablename__ = 'transaction'
    id = db.Column('id', db.BigInteger, primary_key = True, autoincrement=False)
    account_code = db.Column('account_code', db.String(20), \
        db.ForeignKey('account.code', onupdate='CASCADE', ondelete='CASCADE'), \
        nullable=False)
    name = db.Column('name', db.String(200), nullable=False)
    amount = db.Column('amount', db.Integer, nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

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
    name = db.Column(db.String(400), index=True, unique=True)
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


def setup_fixurtes():
    if Account.query.count() == 0:
        accounts = []
        for key, val in current_app.config['SCRAPE_INFOS']['accounts'].items():
            accounts.append(Account(code=key, name=val['label']))
        db.session.add_all(accounts)
        db.session.commit()

    if Category.query.count() == 0:
        db.session.add(Category(name='root'))
        db.session.commit()
