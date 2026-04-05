from qt.core import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QProgressDialog
from calibre_plugins.album_library.metadata import MusicBrainzSource
from calibre.gui2 import error_dialog, info_dialog

class AddAlbumDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Add New Album')
        self.setMinimumWidth(500)
        self.layout = QVBoxLayout(self)

        # Search inputs
        search_layout = QHBoxLayout()
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText('Album Title')
        self.artist_input = QLineEdit()
        self.artist_input.setPlaceholderText('Artist (Optional)')
        self.search_btn = QPushButton('Search')
        self.search_btn.clicked.connect(self.perform_search)
        
        search_layout.addWidget(QLabel('Title:'))
        search_layout.addWidget(self.title_input)
        search_layout.addWidget(QLabel('Artist:'))
        search_layout.addWidget(self.artist_input)
        search_layout.addWidget(self.search_btn)
        self.layout.addLayout(search_layout)

        # Results list
        self.results_list = QListWidget()
        self.layout.addWidget(self.results_list)

        # Action buttons
        btn_layout = QHBoxLayout()
        self.ok_btn = QPushButton('Add Selected Album')
        self.ok_btn.setEnabled(False)
        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton('Cancel')
        self.cancel_btn.clicked.connect(self.reject)
        
        btn_layout.addWidget(self.ok_btn)
        btn_layout.addWidget(self.cancel_btn)
        self.layout.addLayout(btn_layout)

        self.results_list.itemSelectionChanged.connect(lambda: self.ok_btn.setEnabled(True))
        
        self.source = MusicBrainzSource(None)
        self.found_metadata = []

    def perform_search(self):
        title = self.title_input.text().strip()
        artist = self.artist_input.text().strip()
        if not title:
            return error_dialog(self, 'Input Required', 'Please enter at least an album title.', show=True)

        self.results_list.clear()
        self.found_metadata = []
        
        pd = QProgressDialog('Searching MusicBrainz...', 'Abort', 0, 0, self)
        pd.show()
        
        class Log:
            def error(self, msg): print(msg)
            def info(self, msg): print(msg)
        
        class ResultQueue:
            def __init__(self, dialog):
                self.dialog = dialog
            def put(self, mi):
                self.dialog.found_metadata.append(mi)
                item = QListWidgetItem(f"{mi.title} - {', '.join(mi.authors)} ({mi.pubdate.strftime('%Y') if mi.pubdate else 'N/A'})")
                self.dialog.results_list.addItem(item)
        
        class Abort:
            def is_set(self): return pd.wasCanceled()

        self.source.identify(Log(), ResultQueue(self), Abort(), title=title, authors=[artist] if artist else None)
        pd.hide()
        
        if not self.found_metadata:
            info_dialog(self, 'No Results', 'No albums found matching your search.', show=True)

    def get_selected_metadata(self):
        idx = self.results_list.currentRow()
        if idx >= 0:
            return self.found_metadata[idx]
        return None
