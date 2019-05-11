from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.base import Base


class TransactionPreset(Base):
    """
    transaction_preset model
    """
    __tablename__ = 'transaction_preset'
    id = db.Column('id', db.Integer, primary_key = True)
    name = db.Column('name', db.String(512), nullable=False)
    transaction_name = db.Column('transaction_name', db.String(512),
                            nullable=True)
    amount = db.Column('amount', db.Integer, nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'),
                            nullable=True)
    account_code = db.Column('account_code', db.String(50),
                            db.ForeignKey('account.code', ondelete='CASCADE'),
                            nullable=False)
    account = db.relation('Account', order_by='Account.code',
                            uselist=False, backref='transaction_preset')


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'transaction_name': self.transaction_name,
            'amount': self.amount,
            'category_id': self.category_id,
            'account_code': self.account_code,
        }

        if self.account_code and self.account:
            data['account_name'] = self.account.name

        return data


    @classmethod
    def save(self, kwargs, self_id=0):
        if not self_id:
            try:
                if not len(kwargs['name']):
                    raise ValueError('name is required')
            except KeyError:
                raise ValueError('name is required')

        if self_id:
            try:
                item = self.get_one_by_id(self_id)
            except NoResultFound:
                raise ValueError('id is invalid')

            try:
                if kwargs['name'] is not None:
                    item.name = kwargs['name']
            except KeyError:
                pass

        else:
            item = self(
                name=kwargs['name'],
            )

        try:
            if kwargs['transaction_name'] is not None:
                item.transaction_name = kwargs['transaction_name']
        except KeyError:
            pass

        try:
            if kwargs['category_id'] is not None:
                item.category_id = kwargs['category_id']
        except KeyError:
            pass

        try:
            if kwargs['account_code'] is not None:
                item.account_code = kwargs['account_code']
        except KeyError:
            pass

        try:
            if kwargs['amount'] is not None:
                item.amount = kwargs['amount']
        except KeyError:
            pass

        db.session.add(item)
        db.session.commit()

        return item


    @classmethod
    def delete(self, self_id):
        if not self_id:
            raise ValueError('id is invalid')
        try:
            item = self.get_one_by_id(self_id)
        except NoResultFound:
            raise ValueError('id is invalid')

        db.session.delete(item)
        db.session.commit()

        return item
