import numpy as np
import json


# A numpy encoder to convert numpy values to json seriable format
import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    """ Special json encoder for numpy types """
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)



def encode_to_json(data, as_py=True):
    encoded = json.dumps(data, cls=NumpyEncoder)
    if as_py:
        return json.loads(encoded)
    return encoded