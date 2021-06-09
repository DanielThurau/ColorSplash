import json

class Env():
    def __init__(self, file_path):
        self.envs = self.read_env_file(file_path)

    def read_env_file(self, file_path=".env.json"):
        try:
            with open(file_path) as f:
                data = f.read()
        except Exception:
            print("Unable to access environmental values at " + file_path)
            raise Exception

        return json.loads(data)
