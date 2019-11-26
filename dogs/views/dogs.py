from sanic.response import json
from peewee import fn, DoesNotExist, DataError

from dogs.models import Dog


async def show_root_message(request):
    return json(
        {'use api urls to work with data': ['api/dogs', 'api/breeds']}
    )


async def get_dogs(request):
    dogs = []

    for dog in Dog.select():
        dogs.append(
            {
                'id': dog.id,
                'name': dog.name,
                'color': dog.color,
                'birthday': dog.birthday,
                'breed': dog.breed.name,
                'vaccinated': dog.vaccinated,
            }
        )

    return json(dogs)


async def get_dog(request, dog_id: int):
    try:
        dog_to_show = Dog.get_by_id(dog_id)
    except DoesNotExist:
        status = {'error': f'can not find a dog with id {dog_id}'}
    else:
        status = {
            'id': dog_to_show.id,
            'name': dog_to_show.name,
            'color': dog_to_show.color,
            'birthday': dog_to_show.birthday,
            'breed': dog_to_show.breed.name,
            'vaccinated': dog_to_show.vaccinated,
        }

    return json(status)


async def get_dog_by_name(request, dog_name: str):
    """Search by dog's name"""
    try:
        dogs_to_show = Dog.select().where(fn.lower(Dog.name) == dog_name.lower())
    except DoesNotExist:
        status = {'error': f'can not find a dog with the name {dog_name}'}
    else:
        status = []
        for dog in dogs_to_show:
            print(str(dog.name).lower(), dog_name.lower(), str(dog.name).lower() == dog_name.lower())
            status.append(
                {
                    'id': dog.id,
                    'name': dog.name,
                    'color': dog.color,
                    'birthday': dog.birthday,
                    'breed': dog.breed.name,
                    'vaccinated': dog.vaccinated,
                }
            )
        if not status:
            status = {'error': f'can not find a dog with the name {dog_name}'}

    return json(status)


async def create_dog(request):
    dog_ro_create = request.json

    try:
        new_dog = Dog.create(
            name=dog_ro_create['name'],
            birthday=dog_ro_create['birthday'],
        )
        new_dog.save()
    except (TypeError, KeyError):
        status = {'error': 'name, birthday parameters are required'}
    except DataError:
        status = {'error': 'birthday parameter should be presented in format: mm-dd-yyyy'}
    else:
        new_dog.color = dog_ro_create.get('color', 'black')
        new_dog.breed = dog_ro_create.get('breed', 1)
        new_dog.vaccinated = dog_ro_create.get('vaccinated', 1)
        new_dog.save()

        status = {
            'success': 'dog has been created',
            'dog': {
                'id': new_dog.id,
                'name': new_dog.name,
                'birthday': new_dog.birthday,
                'color': new_dog.color,
                'breed': new_dog.breed.name,
                'vaccinated': new_dog.vaccinated,
            }
        }

    return json(status)


async def update_dog(request, dog_id: int):
    dog_updated = request.json
    try:
        dog_to_update = Dog.get_by_id(dog_id)
    except DoesNotExist:
        status = {'error': f'can not find a dog with id {dog_id}'}
    else:
        # If there are no some of fields in request, using fields from database instead
        dog_to_update.name = dog_updated.get('name', dog_to_update.name)
        dog_to_update.color = dog_updated.get('color', dog_to_update.color)
        dog_to_update.birthday = dog_updated.get('birthday', dog_to_update.birthday)
        dog_to_update.breed = dog_updated.get('breed', dog_to_update.breed)
        dog_to_update.vaccinated = dog_updated.get('vaccinated', dog_to_update.vaccinated)
        dog_to_update.save()

        status = {
            'success': 'dog has been updated',
            'dog': {
                'id': dog_to_update.id,
                'name': dog_to_update.name,
                'birthday': dog_to_update.birthday,
                'color': dog_to_update.color,
                'breed': dog_to_update.breed.name,
                'vaccinated': dog_to_update.vaccinated,
            }
        }

    return json(status)


async def delete_dog(request, dog_id: int):
    try:
        dog_to_delete = Dog.get(Dog.id == dog_id)
    except DoesNotExist:
        status = {'error': f'can not find a dog with id {dog_id}'}
    else:
        dog_to_delete.delete_instance()
        status = {'success': f'dog with id {dog_id} has been deleted'}

    return json(status)
