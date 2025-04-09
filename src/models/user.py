from peewee import *
from .base import BaseModel
from datetime import datetime

class User(BaseModel):
    id = BigAutoField()  # id como un campo BIGINT
    name = CharField(max_length=255, null=False)  # Nombre del usuario
    email = CharField(max_length=255, null=False, unique=True)  # Email único
    email_verified_at = TimestampField(null=True)  # Campo para la fecha de verificación del email
    password = CharField(max_length=255, null=False)  # Contraseña
    remember_token = CharField(max_length=100, null=True)  # Token de recordación
    last_name = CharField(max_length=100, null=True)  # Apellido
    rut = CharField(max_length=100, null=False)  # RUT del usuario
    phone_number = CharField(max_length=100, null=True)  # Número de teléfono
    status = CharField(max_length=100, null=True)  # Estado del usuario

    class Meta:
        table_name = 'users'