import requests
import json

class SyncApi:
    host = "http://localhost:8888/"
    def sync_file_names(self, id, files):
        print("saving for {0} with {1}".format(id, files))
        payload = {'files_to_sync': files}
        requests.post(self.host + "users/{0}/preferences.json".format(id), data=json.dumps(payload))
