import os
import requests
import json

class SyncApi:
    host = "http://localhost:8888/"
    def sync_file_names(self, id, files):
        print("saving for {0} with {1}".format(id, files))
        payload = {'files_to_sync': files}
        requests.post(self.host + "users/{0}/preferences.json".format(id), data=json.dumps(payload))

    def sync_file(self, id, dir_name, file_name):
        print("syncing file" + file_name)
        file_content = open(os.path.join(dir_name, file_name)).read()
        requests.post(self.host + "users/{0}/files/{1}/sync.json".format(id, file_name), data=file_content)
