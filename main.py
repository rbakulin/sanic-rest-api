from sanic import Sanic
from sanic.response import json
from database import Breed, Dog, create_tables
from peewee import fn, DoesNotExist, DataError

app = Sanic(__name__)

create_tables()


@app.route('/')
async def test(request):
    return json(
        {'use api urls to work with data': ['api/dogs', 'api/breeds']}
    )


"""DOGS"""
# Read
@app.route("api/dogs", methods=['GET'])
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


@app.route("api/dogs/<dog_id>", methods=['GET'])
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


@app.route("api/dogs/name_search/<dog_name>", methods=['GET'])
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

# Create
@app.route('api/dogs', methods=['POST'])
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

# Update
@app.route("api/dogs/<dog_id>", methods=['PUT'])
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

# Delete
@app.route("api/dogs/<dog_id>", methods=['DELETE'])
async def delete_dog(request, dog_id: int):
    try:
        dog_to_delete = Dog.get(Dog.id == dog_id)
    except DoesNotExist:
        status = {'error': f'can not find a dog with id {dog_id}'}
    else:
        dog_to_delete.delete_instance()
        status = {'success': f'dog with id {dog_id} has been deleted'}

    return json(status)


"""BREEDS"""
# Read
@app.route("api/breeds", methods=['GET'])
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


@app.route("api/breeds/<breed_id>", methods=['GET'])
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


# Create
@app.route('api/breeds', methods=['POST'])
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


# Update
@app.route("api/breeds/<breed_id>", methods=['PUT'])
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


# Delete
@app.route("api/breeds/<breed_id>", methods=['DELETE'])
async def delete_breed(request, breed_id: int):
    try:
        breed_to_delete = Breed.get(Breed.id == breed_id)
    except DoesNotExist:
        status = {'error': f'can not find a breed with id {breed_id}'}
    else:
        breed_to_delete.delete_instance()
        status = {'success': f'breed with id {breed_id} has been deleted'}

    return json(status)


if __name__ == '__main__':
    app.run(host='localhost', port=8000)
