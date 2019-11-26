from peewee import Model
from playhouse.db_url import connect

DATABASE = 'postgresql://root:example@db:5432/dogs'
database = connect(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database



