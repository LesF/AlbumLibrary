from calibre.customize import InterfaceActionBase

class AlbumUIPlugin(InterfaceActionBase):
    name                = 'Album Library Management'
    description         = 'Tools for managing a music record album library within Calibre'
    supported_platforms = ['windows', 'osx', 'linux']
    author              = 'Gemini CLI'
    version             = (0, 1, 0)
    minimum_calibre_version = (5, 0, 0)

    # Point to the class that actually implements the UI action
    actual_plugin = 'calibre_plugins.album_library.ui:AlbumUIAction'

    def is_customizable(self):
        return True

    def config_widget(self):
        # We can implement a configuration dialog later
        from calibre_plugins.album_library.config import ConfigWidget
        return ConfigWidget()

    def save_settings(self, config_widget):
        config_widget.save_settings()
