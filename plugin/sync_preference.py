import os
import uuid
import pdb
import sublime
import sublime_plugin

from .configs import *

class SyncPreferencesCommand(sublime_plugin.TextCommand):

    settings = sublime.load_settings(SYNC_PREFERENCES_FILE)

    def sync_files(self):
        files_to_sync = self.get_files_to_sync()
        user_id = self._get_user_id()
        print("saving for {0} with {1}".format(user_id, files_to_sync))

    def get_files_to_sync(self):
        package_location = self.settings.get(USER_PACKAGE_LOCATION)
        exclude_files = self.settings.get(FILES_TO_EXCLUDE)
        files_to_sync = [ file
            for file in os.listdir(package_location)
            if os.path.isfile(os.path.join(package_location, file))
            and file not in exclude_files
            ]
        return files_to_sync

    def _get_user_id(self):
        user_id = self.settings.get(USER_ID)
        if not user_id:
            print("Generating user_id for first time")
            user_id = uuid.uuid4()
            self._save_id(user_id)
        return user_id

    def _save_id(self, id):
        self.settings.set(USER_ID, str(id))

    def run(self, edit):
        self.sync_files()
        sublime.save_settings(SYNC_PREFERENCES_FILE)
