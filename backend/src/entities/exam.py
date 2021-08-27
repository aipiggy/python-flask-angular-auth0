# coding=utf-8

from sqlalchemy import Column, String
from .entity import Entity, Base
from marshmallow import Schema, fields

class Exam(Entity, Base):
    __tablename__ = 'exams'
    
    title = Column(String(250))
    description = Column(String(250))
    
    def __init__(self, title, description, long_description, created_by):
        Entity.__init__(self, created_by)
        self.title = title
        self.description = description
        self.long_description = long_description
        
class ExamSchema(Schema):
    id = fields.Number()
    title = fields.Str()
    description = fields.Str()
    long_description = fields.Str()
    created_at = fields.DateTime()
    updated_at = fields.DateTime()
    last_updated_by = fields.Str()
    