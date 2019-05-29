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


    @classmethod
    def delete(self, pk_value, pk_prop='id'):
        if not pk_value:
            raise ValueError('{} is invalid'.format(pk_prop))
        try:
            item = self.get_one_by_pk(pk_value, pk_prop)
            item_dict = item.to_dict()
        except NoResultFound:
            raise ValueError('{} is invalid'.format(pk_prop))

        db.session.delete(item)
        db.session.commit()

        return item_dict
