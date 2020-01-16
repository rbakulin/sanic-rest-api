## Simple CRUD for managing dog and breed entities

---

### To create a breed:
*'api/breeds', methods=['POST']*
```json
{"name": "Toyrerier", "size": "small"}
```

### To create a dog:
*'api/dogs', methods=['POST']*
```json
{"name": "Jack", "birthday": "05-19-2019", "color": "black", "breed": 1, "vaccinated": 1}
```

### To search a dog:
*'api/dogs/name_search/<dog_name>', methods=['GET']*
