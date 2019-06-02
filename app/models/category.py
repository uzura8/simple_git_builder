from sqlalchemy.orm.exc import NoResultFound
from app import db
from sqlalchemy_mptt.mixins import BaseNestedSets
from app.models.base import Base


class Category(Base, BaseNestedSets):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), index=True, unique=True)
    sublabel = db.Column(db.String(128), nullable=True)
    sort_no = db.Column(db.Integer, nullable=True)
    is_monthly = db.Column(db.Boolean(), default=False)
    transactions = db.relationship('Transaction', backref='transaction',
                                    lazy='dynamic')

    def __repr__(self):
        return '<Category {}>'.format(self.name)


    def to_dict(self):
        data = {
            'id': self.id,
            'name': self.name,
            'sublabel': self.sublabel,
            'is_monthly': self.is_monthly,
        }
        return data


    @classmethod
    def get_one_by_name(self, name):
        try:
            item = self.query.filter(self.name == name).one()
            return item
        except NoResultFound:
            return None


    @classmethod
    def get_id_by_name(self, name):
        item = self.get_one_by_name(name)
        if not item:
            return None
        return item.id


    @classmethod
    def get_all(self, name='root', is_json=False):
        items = self.query.all()
        for item in items:
            if item.name != name:
                continue
            if not is_json:
                return item.drilldown_tree()
            return item.drilldown_tree(json=True, json_fields=self.cat_to_json)


    @staticmethod
    def cat_to_json(item):
        return {
            'id': item.id,
            'name': item.name,
            'sublabel': item.sublabel,
            'is_monthly': item.is_monthly,
        }


    @classmethod
    def get_max_sort_no(self):
        item = self.query.order_by(self.sort_no.desc()).limit(1).one()
        if not item or not item.sort_no:
            return 0

        return item.sort_no


    @staticmethod
    def get_leaf_ids(parent_id, is_include_parent=False):
        ids = []

        parent = Category.get_one_by_id(parent_id)
        if not parent:
            return ids

        if is_include_parent:
            ids.append(parent.id)

        children = Category.query.filter(db.and_(
            Category.left > parent.left,
            Category.right < parent.right,
        )).all()

        if not children:
            return ids

        for child in children:
            ids.append(child.id)

        return ids


    @classmethod
    def save_by_name(self, name, parent_id=0):
        if not name:
            raise ValueError("Argument 'name' requires values")

        item = self.get_one_by_name(name)
        if item:
            return item
        else:
            item = self(
                name=name,
                parent_id=parent_id,
                sort_no = self.get_max_sort_no() + 10
            )

        db.session.add(item)
        db.session.commit()

        return item


    @classmethod
    def save(self, kwargs, cate_id=0):
        if cate_id:
            try:
                item = self.get_one_by_id(cate_id)
            except KeyError:
                return

            is_updated = False
            try:
                if kwargs['sublabel']:
                    item.sublabel = kwargs['sublabel'],
                    is_updated = True
            except KeyError:
                pass

            try:
                if kwargs['is_monthly'] is not None:
                    item.is_monthly = bool(kwargs['is_monthly'])
                    is_updated = True
            except KeyError:
                pass


            if is_updated:
                db.session.add(item)
                db.session.commit()

        else:
            try:
                name = kwargs['name']
            except KeyError:
                raise ValueError('name is required')

            try:
                name = kwargs['parent_id']
            except KeyError:
                parent_id = 0

            item = self.save_by_name(name, parent_id)

        return item


def setup_fixurtes():
    if Category.query.count() == 0:
        db.session.add(Category(name='root'))
        db.session.commit()
