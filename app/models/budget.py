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
    sort_no = db.Column(db.Integer, nullable=True)
    type = db.Column(ENUM('variable', 'fixed'), \
                        nullable=False, default='variable')
    category = db.relation('Category', order_by='Category.id',
                           uselist=False, backref='budget')


    def to_dict(self):
        data = {
            'id': self.id,
            'category_id': self.category_id,
            'amount': self.amount,
            'sort_no': self.sort_no,
            'created_at': self.created_at,
            'category_name': self.category.name,
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
    def get_max_sort_no(self):
        try:
            item = self.query.order_by(Budget.sort_no.desc()).limit(1).one()
            return item.sort_no
        except NoResultFound:
            return 0


    @classmethod
    def get_all(self):
        try:
            budgets = Category.query.\
                outerjoin(self, Category.id==self.category_id).with_entities(
                    self.id,
                    Category.id,
                    self.amount,
                    Category.name.label('category_name')
                ).filter(Category.parent_id == 1).\
                order_by(Category.id.asc()).all()
                #).order_by(Budget.sort_no.asc()).all()
            #dicts = [item.to_dict() for item in items]
            items = []
            for item in budgets:
                items.append({
                    'id':int(item[0] or 0),
                    'category_id':int(item[1] or 0),
                    'amount':int(item[2] or 0),
                    'category_name':item[3],
                })
            return items

        except NoResultFound:
            return None


    @classmethod
    def create(self, cate_id=0, amount=0):
        item = self.get_one_by_cate_id(cate_id)
        if not item:
            item = self(
                category_id=cate_id,
                sort_no = self.get_max_sort_no() + 10
            )

        item.amount=amount
        db.session.add(item)
        db.session.commit()

        return item
