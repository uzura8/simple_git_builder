from sqlalchemy.orm.exc import NoResultFound
from app import db
from .base import Base

class SiteConfig(Base):
    """
    site_config model
    """
    __tablename__ = 'site_config'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), index=True, unique=True)
    value = db.Column('value', db.Text)

    @classmethod
    def get_value_by_name(self, name):
        try:
            config = self.query.filter(self.name == name).one()
            return config.value
        except NoResultFound:
            return None

    @classmethod
    def get_dict(self):
        try:
            rows = self.query.all()
            configs = {}
            for row in rows:
                key = row.name
                configs[key] = row.value
            return configs
        except NoResultFound:
            return None

    @classmethod
    def save(self, name, value):
        try:
            config = self.query.filter(self.name == name).one()
            if value == config.value:
                return
            config.value = value
        except KeyError:
            config = self(
                name=name,
                value=value
            )
        db.session.add(config)
        db.session.commit()
        return config
