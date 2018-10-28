import sqlite3
from db import db


class CategoryModel(db.Model):
    __tablename__ = 'categories'
 
    id = db.Column(db.Integer, primary_key=True)
    category_uuid = db.Column(db.String(80))
    name = db.Column(db.String(80))

    def __init__(self, category_uuid, name):
        self.category_uuid = category_uuid
        self.name = name

    def json(self):
        return {'id':self.category_uuid, 'name': self.name}
    
    def save_entity(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name): # cls is used instead of self, this points to the current class
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, _id): # cls is used instead of self, this points to the current class
        return cls.query.filter_by(id=_id).first()

    @classmethod
    def find_by_uuid(cls, category_uuid): # cls is used instead of self, this points to the current class
        return cls.query.filter_by(category_uuid=category_uuid).first() 