import json
import os

from habitica_with_gitlab.settings import PROJECT_DIRECTORY


class Config:
    data = None

    def get_config(self):
        if self.data is None:
            path = os.path.join(PROJECT_DIRECTORY, 'config.json')
            print('loading config from %s' % path)
            file_data = open(path).read()
            self.data = json.loads(file_data)

        return self.data


CONFIG = Config()
