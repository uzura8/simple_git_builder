from app import db
from app.models.base import Base


class Transaction(Base):
    """
    transaction model
    """
    __tablename__ = 'transaction'
    id = db.Column('id', db.Integer, primary_key = True)
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
    def create(self, kwargs, service_id=0):
        if service_id:
            trs_id = TransactionService.get_transaction_id_by_id(service_id)
            if trs_id:
                try:
                    trs = self.get_one_by_id(trs_id)
                    if trs:
                        return trs
                except KeyError:
                    return
        transaction = self(
            account_code=kwargs['account_code'],
            name=kwargs['name'],
            amount=kwargs['amount'],
            date=kwargs['date'],
            category_id=kwargs['category_id']
        )
        db.session.add(transaction)
        db.session.commit()

        if service_id:
            db.session.add(TransactionService(
                id=service_id,
                transaction_id=transaction.id
            ))
            db.session.commit()

        return transaction


class TransactionService(Base):
    """
    transaction_service model
    """
    __tablename__ = 'transaction_service'
    id = db.Column('id', db.BigInteger, primary_key=True, \
                                        autoincrement=False)
    transaction_id = db.Column('transaction', db.Integer, \
        db.ForeignKey('transaction.id', ondelete='CASCADE'), \
        nullable=False, unique=True)


    @classmethod
    def get_transaction_id_by_id(self, id):
        try:
            trs_service = self.get_one_by_id(id)
            if not trs_service:
                return 0
            return trs_service.transaction_id
        except KeyError:
            return 0
