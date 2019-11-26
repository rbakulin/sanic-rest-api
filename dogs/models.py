from dogs.database import BaseModel, database
from peewee import CharField, DateField, ForeignKeyField, BooleanField


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
