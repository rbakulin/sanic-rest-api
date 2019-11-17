from peewee import *
from playhouse.db_url import connect

DATABASE = 'postgresql://root:example@localhost:5432/dogs'
database = connect(DATABASE)


class BaseModel(Model):
    class Meta:
        database = database


class Breed(BaseModel):
    name = CharField(max_length=50, null=False)
    size = CharField(max_length=50, null=False, choices=(
        ('small', 'Small'),
        ('medium', 'Medium'),
        ('big', 'Big'),
    ), default='medium')


class Dog(BaseModel):
    name = CharField(max_length=50, null=False)
    color = CharField(max_length=50, null=False, choices=(
        ('black', 'Black'),
        ('white', 'White'),
        ('grey', 'Grey'),
        ('brown', 'Brown'),
    ), default='grey')
    birthday = DateField(null=False)
    breed = ForeignKeyField(Breed, backref='dogs', null=False, default=1)
    vaccinated = BooleanField(null=False, default=True)


def create_tables():
    database.connect()
    database.create_tables([Breed, Dog])
