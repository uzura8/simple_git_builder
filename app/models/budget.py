from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.dialects.mysql import ENUM
from app import db
from app.models import Base, Category


class Budget(Base):
    __tablename__ = 'budget'
    id = db.Column(db.Integer, primary_key=True)
    category_id = db.Column(db.Integer,
                            db.ForeignKey('category.id', ondelete='CASCADE'), \
                            nullable=False, unique=True)
    amount = db.Column('amount', db.Integer, nullable=False, default=0)
    type = db.Column(ENUM('variable', 'fixed'), \
                        nullable=False, default='variable')
    category = db.relation('Category', order_by='Category.id',
                           uselist=False, backref='budget')


    def to_dict(self):
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'amount': self.amount,
            'category_name': self.category.name,
            'category_sublabel': self.category.sublabel,
        }
        return data


    @classmethod
    def get_one_by_cate_id(self, cate_id):
        try:
            item = self.query.filter(self.category_id == cate_id).one()
            return item
        except NoResultFound:
            return None


    @classmethod
    def get_all(self):
        try:
            budgets = Category.query.\
                outerjoin(self, Category.id==self.category_id).with_entities(
                    self.id,
                    Category.id,
                    self.amount,
                    Category.name.label('category_name'),
                    Category.sublabel.label('category_sublabel')
                ).filter(Category.parent_id == 1).\
                order_by(Category.sort_no.asc()).all()
            items = []
            for item in budgets:
                items.append({
                    'id':int(item[0] or 0),
                    'category_id':int(item[1] or 0),
                    'amount':int(item[2] or 0),
                    'category_name':item[3],
                    'category_sublabel':item[4],
                })
            return items

        except NoResultFound:
            return None


    @classmethod
    def create(self, cate_id=0, amount=0):
        item = self.get_one_by_cate_id(cate_id)
        if not item:
            item = self(category_id=cate_id)

        item.amount=amount
        db.session.add(item)
        db.session.commit()

        return item
