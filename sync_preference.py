import os
import uuid
import shutil
import datetime
import sublime
import sublime_plugin
from threading import Thread
from uuid import UUID
from .util import Util
from .sync_api import SyncApi
from .configs import *


class SyncPreferencesCommand(sublime_plugin.TextCommand):
    settings = sublime.load_settings(SYNC_PREFERENCES_FILE)
    sync_api = SyncApi()

    def _get_user_custom_sync_folder_files(self):
        custom_sync_folders = self.settings.get(FOLDERS_TO_SYNC)
        print("user defined custom folders: ", custom_sync_folders)
        files = []
        for folder in custom_sync_folders:
            files += self.get_files_to_sync(folder)
        return files

    def sync_files(self):
        print("sync files in progres...")
        files_to_sync = self.get_files_to_sync(
            Util.get_user_package_location()) + self._get_user_custom_sync_folder_files()
        user_id = self._get_user_id()
        self.sync_api.sync_file_names(user_id, files_to_sync)
        for file in files_to_sync:
            self.sync_api.sync_file(user_id, file)

    def get_files_to_sync(self, sync_folder):

        def can_include_file(file):
            return os.path.isfile(os.path.join(sync_folder, file)) and file not in exclude_files

        exclude_files = self.settings.get(FILES_TO_EXCLUDE)
        sync_folder = Util.substitute_env_variables(sync_folder)
        return [os.path.join(sync_folder, file) for file in os.listdir(sync_folder) if can_include_file(file)]


    def _get_user_id(self):
        user_id = self.settings.get(USER_ID)
        if not user_id:
            print("Generating user_id for first time")
            user_id = uuid.uuid4()
            self._save_id(user_id)
        return user_id

    def _save_id(self, id):
        self.settings.set(USER_ID, str(id))

    def sync_and_save_settings(self):
        self.sync_files()
        sublime.save_settings(SYNC_PREFERENCES_FILE)

    def run(self, edit):
        Thread(target=self.sync_and_save_settings).start()



class SyncToLocalCommand(sublime_plugin.TextCommand):

    sync_api = SyncApi()

    def sync_to_local(self, uuid):
        self.archive_old_user_folder()
        self.download_files(uuid, self.sync_api.get_files_to_download(uuid))

    def download_files(self, user_id, files):
        print("downloading files.." + str(files))
        package_location = Util.get_user_package_location()
        for file in files:
            file_content = self.sync_api.get_file_contents(user_id, file)
            if file_content:
                self._save_file_content(package_location, file, file_content)
                print("saving response content:" + str(file_content))

    def archive_old_user_folder(self):
        timestamp = datetime.datetime.utcnow().strftime("%F:%T")
        archive_name = os.environ['TMPDIR'] + "user_pkg_" + timestamp
        package_location = Util.get_user_package_location()
        print("archiving..." + archive_name + "dir:" + package_location)
        resulted_archive = shutil.make_archive(archive_name, 'gztar', root_dir=package_location)
        print("archived: " + resulted_archive)

    def on_uuid_entered(self, input_uuid):
        if self._is_valid_uuid(input_uuid):
            print("sync to local for " + input_uuid)
            Thread(target=self.sync_to_local, args=(input_uuid,)).start()

    def _is_valid_uuid(self, uuid):
        try:
            value = UUID(uuid)
        except ValueError:
            return False
        return str(value) == uuid

    def run(self, edit):
        self._get_uuid_from_user()

    def _save_file_content(self, dir_name, file_name, file_content):
        with open(os.path.join(dir_name, file_name), 'w+') as file:
            file.write(file_content)

    def _get_uuid_from_user(self):
        self.view.window().show_input_panel(
            "Enter UUID to Sync files to local:", "", self.on_uuid_entered, None, None)
