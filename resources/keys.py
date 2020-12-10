import json

def get_key(name):
    with open("./resources/keys.json") as file:
        keys = json.loads(file.read())
        try:
            return keys[name]
        except:
            print("no key with that name available")
            return None
