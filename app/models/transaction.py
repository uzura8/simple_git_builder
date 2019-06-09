from app import db
from app.models.base import Base


class Example(Base):
    """
    example model
    """
    __tablename__ = 'example'
    id = db.Column('id', db.Integer, primary_key = True)
    account_code = db.Column('account_code', db.String(50), \
        db.ForeignKey('account.code', onupdate='CASCADE', ondelete='CASCADE'), \
        nullable=False)
    name = db.Column('name', db.String(512), nullable=False)
    amount = db.Column('amount', db.Integer, nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    is_disabled = db.Column(db.Boolean(), default=False)
    account = db.relation('Account', order_by='Account.code',
                           uselist=False, backref='example')


    def to_dict(self):
        is_disabled = True if self.is_disabled == 1 else False
        data = {
            'id': self.id,
            'account_code': self.account_code,
            'name': self.name,
            'amount': self.amount,
            'date': self.date,
            'created_at': self.created_at,
            'is_disabled': is_disabled,
            'account_name': self.account.name,
        }
        return data


    @classmethod
    def create(self, kwargs, service_id=0):
        example = self(
            account_code=kwargs['account_code'],
            name=kwargs['name'],
            amount=kwargs['amount'],
            date=kwargs['date'],
        )
        db.session.add(example)
        db.session.commit()

        return example
