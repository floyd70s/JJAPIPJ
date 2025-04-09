from peewee import *
from .base import BaseModel
from .user import User
from datetime import datetime

class Preference(BaseModel):
    id = AutoField()          # id como un campo autonumerado
    user = ForeignKeyField(User, backref='preferences', on_delete='CASCADE')
    rut = CharField(max_length=20, unique=True, null=False)  # RUT no puede ser nulo y debe ser único
    password = CharField(max_length=255, null=False)  # Campo para la contraseña
    created_at = TimestampField(default=datetime.now)  # Campo para la fecha de creación
    updated_at = TimestampField(default=datetime.now)  # Campo para la fecha de actualización

    class Meta:
        table_name = 'preferences'