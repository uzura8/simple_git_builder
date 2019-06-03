import datetime
import calendar
#from sqlalchemy import func
from app import db
from app.common.util import search_dicts
from . import Category, Transaction, Budget


class Performance():

    @staticmethod
    def get_sums_all(year, month):
        sums = []

        parent_cates = Category.query.filter(Category.parent_id == 1).\
                        order_by(Category.sort_no.asc()).all()
        if not parent_cates:
            return None

        _, lastday = calendar.monthrange(year, month)

        budgets = [item.to_dict() for item in Budget.query.all()]

        for parent_cate in parent_cates:
            cate_ids = Category.get_leaf_ids(parent_cate.id, True)
            budget = search_dicts('category_id', parent_cate.id, budgets)
            val = db.session.query(db.func.sum(Transaction.amount)).\
                filter(Transaction.is_disabled == False).\
                filter(db.and_(
                    Transaction.date >= datetime.date(year, month, 1),
                    Transaction.date <= datetime.date(year, month, lastday),
                )).\
                filter(Transaction.category_id.in_(cate_ids)).one()
            val_year = db.session.query(db.func.sum(Transaction.amount)).\
                filter(Transaction.is_disabled == False).\
                filter(db.and_(
                    Transaction.date >= datetime.date(year, 1, 1),
                    Transaction.date <= datetime.date(year, month, lastday),
                )).\
                filter(Transaction.category_id.in_(cate_ids)).one()
            sums.append({
                'id':parent_cate.id,
                'name':parent_cate.name,
                'sublabel':parent_cate.sublabel,
                'is_monthly':parent_cate.is_monthly,
                'leaf_ids':cate_ids,
                'sum':val[0] if val[0] is not None else 0,
                'sum_year':val_year[0] if val_year[0] is not None else 0,
                'budget':budget['amount'] if budget is not None else 0
            })

        return sums
