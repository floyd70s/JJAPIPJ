from datetime import datetime
from peewee import *
from .base import BaseModel


class Case(BaseModel):
    id = AutoField()  # id como un campo autonumerado
    court = CharField(max_length=250, null=False)  # Relación con el court_id (int)
    user_id = IntegerField(null=False)  # Relación con el state_id (int)
    state_id = IntegerField(null=False)  # Relación con el state_id (int)
    competition_id = IntegerField(null=False)  # Relación con el state_id (int)
    role = CharField(max_length=100, null=False)  # Campo para el rol
    entry_date = DateTimeField(null=False)  # Campo para la fecha de entrada
    titled = CharField(max_length=250, null=False)  # Campo para el título
    institution = CharField(max_length=250, null=False)  # Campo para la institución
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")])

    class Meta:
        table_name = 'cases'