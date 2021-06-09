import json
import os

class RGB:
    def __init__(self):
        self.image_directory = 'images'
        self.images_dict_file = "data.json"

        self.images_dict = {}
        if (os.path.isfile(self.images_dict_file)):
            image_dict = self.deseralize_dict(self.images_dict_file)
        else:
            image_dict = self.generate_data_structure(self.image_directory)
            self.serialize_dict(image_dict, self.images_dict_file) 

    def serialize_dict(kv_pair, file):
        with open(file, 'w') as f:
            f.write(json.dumps(kv_pair))

    def deseralize_dict(file):
        with open(file) as f:
            data = f.read()
        
        return json.loads(data)