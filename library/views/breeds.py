from sanic.response import json
from peewee import DoesNotExist

from library.database import Breed


async def get_breeds(resquest):
    breeds = []

    for breed in Breed.select():
        breeds.append(
            {
                'name': breed.name,
                'size': breed.size,
            }
        )

    return json(breeds)


async def get_breed(request, breed_id: int):
    try:
        breed_to_show = Breed.get_by_id(breed_id)
    except DoesNotExist:
        status = {'error': f'can not find a breed with id {breed_id}'}
    else:
        status = {
            'id': breed_to_show.id,
            'name': breed_to_show.name,
            'color': breed_to_show.size,
        }

    return json(status)


async def create_breed(request):
    breed_ro_create = request.json

    try:
        new_breed = Breed.create(
            name=breed_ro_create['name'],
        )
        new_breed.save()
    except (TypeError, KeyError):
        status = {'error': 'name parameter is required'}
    else:
        new_breed.size = breed_ro_create.get('size', 'medium')
        new_breed.save()

        status = {
            'success': 'breed has been created',
            'breed': {
                'id': new_breed.id,
                'name': new_breed.name,
                'size': new_breed.size,
            }
        }

    return json(status)


async def update_breed(request, breed_id: int):
    breed_updated = request.json
    try:
        breed_to_update = Breed.get_by_id(breed_id)
    except DoesNotExist:
        status = {'error': f'can not find a breed with id {breed_id}'}
    else:
        # If there are no some of fields in request, using fields from database instead
        breed_to_update.name = breed_updated.get('name', breed_to_update.name)
        breed_to_update.size = breed_updated.get('size', breed_to_update.size)
        breed_to_update.save()

        status = {
            'success': 'breed has been updated',
            'breed': {
                'id': breed_to_update.id,
                'name': breed_to_update.name,
                'size': breed_to_update.size,
            }
        }

    return json(status)


async def delete_breed(request, breed_id: int):
    try:
        breed_to_delete = Breed.get(Breed.id == breed_id)
    except DoesNotExist:
        status = {'error': f'can not find a breed with id {breed_id}'}
    else:
        breed_to_delete.delete_instance()
        status = {'success': f'breed with id {breed_id} has been deleted'}

    return json(status)
