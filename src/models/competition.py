from peewee import *
from .base import BaseModel
from datetime import datetime

class Competition(BaseModel):
    name = CharField(unique=True)
    created_at = TimestampField(default=datetime.now)  # Campo para la fecha de creación
    updated_at = TimestampField(default=datetime.now)  # Campo para la fecha de actualización


    class Meta:
        table_name = 'competitions'
