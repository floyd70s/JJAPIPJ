from peewee import *
from .base import BaseModel
from datetime import datetime

class Audience(BaseModel):
    id = AutoField()  # id como un campo autonumerado con BIGINT
    user_id = BigIntegerField(null=False)  # Relación con el state_id
    competition_id = BigIntegerField(null=True)  # Relación con el competition_id
    court = CharField(max_length=100, null=False)
    ruc = CharField(max_length=100, null=False)  # Campo para el RUC
    audience_date = DateTimeField(null=True)  # Campo para la fecha de audiencia
    json = TextField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")])


    class Meta:
        table_name = 'audiences'