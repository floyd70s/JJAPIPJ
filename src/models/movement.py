from peewee import *
from .base import BaseModel
from datetime import datetime

class Movement(BaseModel):
    id = AutoField()  # id como un campo autonumerado
    folio = CharField(max_length=10, null=False)
    case_id = IntegerField(null=False)  # Relación con el case_id
    procedure_date = DateTimeField(null=True)  # Campo para la fecha del procedimiento
    diligence = CharField(max_length=250, null=True)  # Campo para la descripción
    description = CharField(max_length=250, null=True)  # Campo para la descripción
    json = TextField(null=True)
    created_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP")])
    updated_at = DateTimeField(constraints=[SQL("DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")])


    class Meta:
        table_name = 'movements'