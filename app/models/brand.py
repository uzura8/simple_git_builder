from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.base import Base


class Brand(Base):
    """
    brand model
    """
    __tablename__ = 'brand'
    code = db.Column('code', db.String(50), nullable=False, primary_key=True)
    name = db.Column('name', db.String(256), nullable=False)
    currency = db.Column('currency', db.String(20), nullable=False)

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


    def to_dict(self):
        data = {
            'code': self.code,
            'name': self.name,
            'currency': self.currency,
        }
        return data


def setup_fixurtes():
    if Brand.query.count() == 0:
        db.session.add(Brand(code='jp_topix', name='TOPIX', currency='yen'))
        db.session.commit()
