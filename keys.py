import json

def get_key(name):
    with open("/Users/felixbieswanger/Desktop/Uni_Stuff/Bachelorarbeit/OpionionMining/resources/keys.json") as file:
        keys = json.loads(file.read())
        try:
            return keys[name]
        except:
            print("no key with that name available")
            return None
