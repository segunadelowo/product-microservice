import sqlite3
from db import db


class ItemModel(db.Model):
    __tablename__ = 'items'
 
    id = db.Column(db.Integer, primary_key=True)
    item_uuid = db.Column(db.String(80))
    category_id = db.Column(db.Integer)
    supplier_id = db.Column(db.Integer)
    name = db.Column(db.String(80))
    description = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))



    def __init__(self, item_uuid,category_id,supplier_id,description,price,name):
        self.item_uuid = item_uuid
        self.category_id = category_id
        self.supplier_id = supplier_id
        self.name = name
        self.description = description
        self.price = price

    def json(self):
        return {'id':self.item_uuid, 'name': self.name, 'category_id':self.category_id, 'supplier_id':self.supplier_id,'description':self.description,'price':self.price}
    
    def save_entity(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self) 
        db.session.commit()

    @classmethod
    def find_by_name(cls, name): # c ls is used instead of self, this points to the current class
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_by_id(cls, id): # cls is used instead of self, this points to the current class
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_uuid(cls, item_uuid): # cls is used instead of self, this points to the current class
        return cls.query.filter_by(item_uuid=item_uuid).first() 