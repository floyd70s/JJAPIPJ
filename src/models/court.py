from peewee import *
from .base import BaseModel
from datetime import datetime

class Court(BaseModel):
    id = AutoField()  # Define el campo id como llave primaria autonumérica
    competition_id = IntegerField()
    state_id = IntegerField(default=1)
    name = CharField(unique=True)
    created_at = TimestampField(default=datetime.now)  # Campo para la fecha de creación
    updated_at = TimestampField(default=datetime.now)  # Campo para la fecha de actualización

    class Meta:
        table_name = 'courts'

    @staticmethod
    def getCourtId(courtName):
        # Buscar el ID del court por su nombre
        court = Court.select(Court.id).where(
            Court.name == courtName
        ).first()

        if court:
            return court.id
        else:
            return None