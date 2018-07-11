import json
from jsonschema import validate

class Out:
    def __init__(self, msg : str):
        self.id : int = -1
        self.status : bool = False
        self.msgs = []

        try:
            dict_obj = json.loads(msg)
        except:
            self.msgs.append('invalid json')
            return

        try:
            validate(dict_obj, self._get_schema())
        except:
            self.msgs.append('invalid schema')
            return
        
        self.id = dict_obj['id']
        self.status = True
        
        if dict_obj['side'] not in ('buy', 'sell'):
            self.msgs.append('invalid side')
            self.status = False
        
        if dict_obj['price'] < 0:
            self.msgs.append('price is negative')
            self.status = False

        if dict_obj['quantity'] < 0:
            self.msgs.append('quantity is negative')
            self.status = False


    def _get_schema(self):
        schema = {
            "type" : "object",
            "properties" : {
                "id" : {"type" : "integer"},
                "side" : {"type" : "string"},
                "price" : {"type" : "number"},
                "quantity" : {"type" : "integer"},
                "symbol" : {"type" : "string"},
            },
        }
        return schema
        
    
    def to_dict(self):
        return {'id': self.id, 'status': self.status, 'msgs': self.msgs}
    
    def to_str(self):
        return json.dumps(self.to_dict())