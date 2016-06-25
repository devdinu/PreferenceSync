import os
import sublime
from .configs import *


class Util:

    user_package_location = "Packages/User"


    @classmethod
    def _get_location(cls):
        return sublime.installed_packages_path().split(os.sep)[:-1]

    @classmethod
    def get_user_package_location(cls):
        settings = sublime.load_settings(SYNC_PREFERENCES_FILE)
        location = os.sep.join(cls._get_location() + [cls.user_package_location])
        return cls.substitute_env_variables(location)

    @staticmethod
    def substitute_env_variables(location):
        substituted_location = [folder if "$" not in folder
                                else os.environ[folder[1:]] for folder in location.split(os.sep)]
        return os.sep.join(substituted_location)

    @staticmethod
    def get_user_defined_sync_folder():
        return sublime.load_settings(SYNC_PREFERENCES_FILE).get(FOLDERS_TO_SYNC)
