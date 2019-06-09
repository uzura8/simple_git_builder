from sqlalchemy.orm.exc import NoResultFound
from app import db
from app.models.base import Base


class Account(Base):
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


    def to_dict(self):
        data = {
            'code': self.code,
            'name': self.name,
        }
        return data


#def setup_fixurtes():
#    if Account.query.count() == 0:
#        db.session.add(Account(code='manual', name='手入力'))
#        db.session.commit()
