from jsonschema import validate
from jsonschema.exceptions import ValidationError
import json

schema = {
    "type" : "object",
    "properties" : {
        "n" : {"type" : "integer", "minimum": 0},
        "price" : {"type" : "number", "minimum": 0},
        "name" : {"type" : "string"},
    },
    "required": ["name", "price", "n"]
}

obj = {"n": -3, "name" : "Eggs", "price" : -3.45}
jsonstr = json.dumps(obj)
print(type(jsonstr))
new_obj = json.loads(jsonstr)
print(new_obj)
#wrong = json.loads('{')
#print('aqui')