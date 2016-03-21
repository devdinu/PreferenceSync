## Sublime Text Sync

Syncs User Package Folder of Sublime Text.

### Features

It uploads the User packages directory of Sublime Text, and can dowload it later via UUID.

* The UUID 'll be written to `Sync Prerences.sublime-settings` in User Packages directory.
* Default Mac location `$HOME/Library/Application Support/Sublime Text 3/Packages/User`
* The plugin accepts configuration via `Sync Prerences.sublime-settings` file present inside the plugin directory PreferencesSync  present in packages folder of Sublime Text.
    - `user_package_location`: accepts relative path to package directory, its defaulted to Mac location.
    - `files_to_exclude_in_sync`: [accepts an array of files to exclude in the User directory to prevent syncing]

### Key Shortcut

sync_preferences syncs to remote, and sync_local sync files from remote to local.
To change Trigger for Download / Upload change the keymap file content to your option.

```
[
    { "keys": ["alt+super+u"], "command": "sync_preferences" },
    { "keys": ["alt+super+l"], "command": "sync_to_local" }
]
```

### Recovering old Data

Before overwritting the existing files, plugin creates an archive in $TMPDIR folder, the filename and logs can be viewed in sublime console `(ctrl + `)`. you can unzip the gzip, untar and use it in case if you want the old directory.
