from main import app
import json
import unittest

TEST_DOG = {'name': 'test_one', 'birthday': '11-11-2011'}


def create_test_item(module, data):
    request, response = app.test_client.post(f'/api/{module}', data=json.dumps(data))

    return response


def delete_test_item(module, item_id):
    app.test_client.delete(f'/api/{module}/{item_id}')


class DogsTests(unittest.TestCase):

    def test_create_dog(self):
        response = create_test_item('dogs', TEST_DOG)
        resp_text = json.loads(response.text)
        id_created = int(resp_text['dog']['id'])

        self.assertEqual(response.status, 200)
        self.assertAlmostEqual(resp_text['dog']['name'], 'test_one')

        delete_test_item('dogs', id_created)

    def test_get_dogs(self):
        request, response = app.test_client.get('api/dogs')
        self.assertEqual(response.status, 200)

    def test_get_dog(self):
        post_response = create_test_item('dogs', TEST_DOG)
        resp_text = json.loads(post_response.text)
        id_created = int(resp_text['dog']['id'])

        get_request, get_response = app.test_client.get(f'api/dogs/{id_created}')
        get_data = json.loads(get_response.text)

        self.assertEqual(get_response.status, 200)
        self.assertEqual(get_data['name'], 'test_one')

        delete_test_item('dogs', id_created)

    def test_update_dog(self):
        post_response = create_test_item('dogs', TEST_DOG)
        resp_text = json.loads(post_response.text)
        id_created = int(resp_text['dog']['id'])

        update_data = {'name': 'test_two'}
        update_request, update_response = app.test_client.put(f'api/dogs/{id_created}', data=json.dumps(update_data))
        update_res_data = json.loads(update_response.text)

        self.assertEqual(update_response.status, 200)
        self.assertEqual(update_res_data['dog']['name'], update_data['name'])

        delete_test_item('dogs', id_created)

    def test_delete_dog(self):
        post_response = create_test_item('dogs', TEST_DOG)
        resp_text = json.loads(post_response.text)
        id_created = int(resp_text['dog']['id'])

        delete_test_item('dogs', id_created)

        get_request, get_response = app.test_client.get(f'api/dogs/{id_created}')
        get_data = json.loads(get_response.text)
        self.assertEqual(get_data['error'], f'can not find a dog with id {id_created}')

    def test_get_dog_by_name(self):
        post_response = create_test_item('dogs', TEST_DOG)
        resp_text = json.loads(post_response.text)
        id_created = int(resp_text['dog']['id'])

        get_request, get_response = app.test_client.get(f'api/dogs/name_search/{TEST_DOG["name"]}')
        get_data = json.loads(get_response.text)

        self.assertEqual(get_response.status, 200)
        self.assertEqual(get_data[0]['id'], id_created)

        delete_test_item('dogs', id_created)


if __name__ == '__main__':
    unittest.main()
