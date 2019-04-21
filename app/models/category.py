from sqlalchemy.orm.exc import NoResultFound
from app import db
from sqlalchemy_mptt.mixins import BaseNestedSets
from app.models.base import Base


class Category(Base, BaseNestedSets):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    transactions = db.relationship('Transaction', backref='transaction',
                                    lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)

    @classmethod
    def get_id_by_name(self, name):
        try:
            category = self.query.filter(self.name == name).one()
            return category.id
        except NoResultFound:
            return None

    @classmethod
    def get_all(self, name='root', is_json=False):
        categories = self.query.all()
        for item in categories:
            if item.name != name:
                continue
            if not is_json:
                return item.drilldown_tree()
            return item.drilldown_tree(json=True, json_fields=self.cat_to_json)

    @staticmethod
    def cat_to_json(item):
        return {
            'id': item.id,
            'name': item.name
        }


def setup_fixurtes():
    if Category.query.count() == 0:
        db.session.add(Category(name='root'))
        db.session.commit()
