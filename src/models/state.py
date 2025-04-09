from peewee import *
from .base import BaseModel
from datetime import datetime

class State(BaseModel):
    description = CharField(unique=True)
    tag = CharField(unique=True)

    class Meta:
        table_name = 'states'

    @staticmethod
    def getStateId(stateName, tag):
        # Buscar el ID del court por su nombre
        state = State.select(State.id).where(
            (State.description == stateName) and (State.tag == tag)
        ).first()

        if state:
            return state.id
        else:
            return 13 #Estado no definido