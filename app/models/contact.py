from sqlalchemy.dialects.mysql import TINYINT
from app import db
from app.models.base import Base
from app.common.string import random_str


class Contact(Base):
    """
    contact model
    """
    __tablename__ = 'contact'
    code = db.Column('code', db.String(6), primary_key=True)
    status = db.Column(TINYINT, nullable=False)
    subject = db.Column(db.String(64), nullable=False)
    content = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(128), nullable=False)
    tel = db.Column(db.String(12), nullable=True)
    name = db.Column(db.String(256), nullable=True)
    name_phonetic = db.Column(db.String(256), nullable=True)
    contact_type = db.Column(TINYINT, nullable=True)
    ip = db.Column(db.String(32), nullable=True)
    ua = db.Column(db.String(256), nullable=True)


    def to_dict(self):
        data = {
            'code': self.code,
            'status': self.status,
            'contact_type': self.contact_type,
            'subject': self.subject,
            'content': self.content,
            'email': self.email,
            'tel': self.tel,
            'name': self.name,
            'name_phonetic': self.name_phonetic,
            'created_at': self.created_at,
        }
        return data


    @classmethod
    def create(self, kwargs, status=0):
        item = self(
            code=random_str(6, True),
            status=status,
            contact_type=kwargs['contact_type'],
            subject=kwargs['subject'],
            content=kwargs['content'],
            email=kwargs['email'],
            tel=kwargs['tel'],
            name=kwargs['name'],
            name_phonetic=kwargs['name_phonetic'],
            ip=kwargs['ip'],
            ua=kwargs['ua'],
        )
        db.session.add(item)
        db.session.commit()

        return item
