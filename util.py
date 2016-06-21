import os
import sublime
from .configs import SYNC_PREFERENCES_FILE, USER_PACKAGE_LOCATION


class Util:

    @staticmethod
    def get_user_package_location():
        settings = sublime.load_settings(SYNC_PREFERENCES_FILE)
        location = settings.get(USER_PACKAGE_LOCATION)
        substituted_location = [folder if "$" not in folder
                                else os.environ[folder[1:]] for folder in location.split("/")]
        return os.sep.join(substituted_location)
