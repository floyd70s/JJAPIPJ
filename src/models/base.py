from peewee import Model, MySQLDatabase

# Configuración de la base de datos
db = MySQLDatabase(
    'lexpress',
    user='root',
    password='',
    host='localhost',
    port=3306
)
# Modelo base
class BaseModel(Model):
    class Meta:
        database = db
