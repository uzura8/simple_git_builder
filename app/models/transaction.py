#from datetime import datetime
from app import db
#from sqlalchemy_mptt.mixins import BaseNestedSets
from app.models.base import Base


class Transaction(Base):
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
    is_disabled = db.Column(db.Boolean(), default=False)
    account = db.relation('Account', order_by='Account.code',
                           uselist=False, backref='transaction')


    def to_dict(self):
        is_disabled = True if self.is_disabled == 1 else False
        data = {
            'id': self.id,
            'account_code': self.account_code,
            'name': self.name,
            'amount': self.amount,
            'date': self.date,
            'category_id': self.category_id,
            'created_at': self.created_at,
            'is_disabled': is_disabled,
            'account_name': self.account.name,
        }
        return data


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
