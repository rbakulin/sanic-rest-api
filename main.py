from sanic import Sanic

from library.database import create_tables
from library.views.dogs import (
    show_root_message,
    get_dogs,
    get_dog,
    get_dog_by_name,
    create_dog,
    update_dog,
    delete_dog
)
from library.views.breeds import (
    get_breeds,
    get_breed,
    create_breed,
    update_breed,
    delete_breed
)

app = Sanic(__name__)

create_tables()

"""ROOT"""
app.add_route(show_root_message, '/', methods=['GET'])

"""DOGS"""
# Read
app.add_route(get_dogs, 'api/dogs', methods=['GET'])

app.add_route(get_dog, 'api/dogs/<dog_id>', methods=['GET'])

app.add_route(get_dog_by_name, 'api/dogs/name_search/<dog_name>', methods=['GET'])

# Create
app.add_route(create_dog, 'api/dogs', methods=['POST'])

# Update
app.add_route(update_dog, 'api/dogs/<dog_id>', methods=['PUT'])

# Delete
app.add_route(delete_dog, 'api/dogs/<dog_id>', methods=['DELETE'])


"""BREEDS"""
# Read
app.add_route(get_breeds, 'api/breeds', methods=['GET'])

app.add_route(get_breed, 'api/breeds/<breed_id>', methods=['GET'])

# Create
app.add_route(create_breed, 'api/breeds', methods=['POST'])

# Update
app.add_route(update_breed, 'api/breeds/<breed_id>', methods=['PUT'])

# Delete
app.add_route(delete_breed, 'api/breeds/<breed_id>', methods=['DELETE'])


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
