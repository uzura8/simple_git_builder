from app import db
from app.models.base import Base


class PriceDay(Base):
    """
    price_day model
    """
    __tablename__ = 'price_day'
    __table_args__ = (db.UniqueConstraint('brand_code', 'date',
                                        name='brand_code_date_unique_idx'),)
    id = db.Column('id', db.Integer, primary_key=True)
    brand_code = db.Column('brand_code', db.String(50), \
        db.ForeignKey('brand.code', ondelete='CASCADE'), \
        nullable=False)
    date = db.Column('date', db.Date, nullable=False)
    price = db.Column('price', db.Float, nullable=False)
    price_open = db.Column('price_open', db.Float, nullable=True)
    price_high = db.Column('price_high', db.Float, nullable=True)
    price_low = db.Column('price_low', db.Float, nullable=True)
    is_disabled = db.Column(db.Boolean(), default=False)
    brand = db.relation('Brand', order_by='Brand.code',
                           uselist=False, backref='price')


    def to_dict(self):
        is_disabled = True if self.is_disabled == 1 else False
        data = {
            'id': self.id,
            'brand_code': self.brand_code,
            'date': self.date,
            'price': self.price,
            'created_at': self.created_at,
            'is_disabled': is_disabled,
            'brand_name': self.brand.name,
        }
        return data


    @classmethod
    def create(self, kwargs):
        price = self(
            date=kwargs['date'],
            brand_code=kwargs['brand_code'],
            price=kwargs['price'],
            price_open=kwargs['price_open'],
            price_high=kwargs['price_high'],
            price_low=kwargs['price_low'],
        )
        db.session.add(price)
        db.session.commit()

        return price
