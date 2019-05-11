from datetime import datetime
from sqlalchemy.orm.exc import NoResultFound
from app import db

class Base(db.Model):
    __abstract__ = True

    created_at = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)


    @classmethod
    def get_one_by_pk(self, value, prop='id'):
        try:
            return self.query.filter(getattr(self, prop) == value).one()
        except NoResultFound:
            return None


    @classmethod
    def get_one_by_id(self, id):
        return self.get_one_by_pk(id)
