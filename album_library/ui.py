from calibre.gui2.actions import InterfaceAction
from calibre_plugins.album_library.schema import CUSTOM_COLUMNS
from calibre.gui2.preferences.create_custom_column import CreateNewCustomColumn
from calibre.gui2 import error_dialog, info_dialog

from qt.core import QMenu
from calibre_plugins.album_library.dialogs import AddAlbumDialog
from calibre_plugins.album_library.pdf import AlbumPDFGenerator
from calibre_plugins.album_library.metadata import MusicBrainzSource
import os, tempfile

class AlbumUIAction(InterfaceAction):
    name = 'Album Library Tools'
    action_spec = ('Album Tools', None, 'Tools for managing your album collection', None)
    
    def genesis(self):
        # This method is called once when the interface is being initialized
        self.menu = QMenu(self.gui)
        self.qaction.setMenu(self.menu)
        
        self.add_album_action = self.menu.addAction('Add New Album...')
        self.add_album_action.triggered.connect(self.add_new_album)
        
        self.ensure_schema_action = self.menu.addAction('Ensure Custom Columns')
        self.ensure_schema_action.triggered.connect(self.run_schema_check)

        self.refresh_pdf_action = self.menu.addAction('Refresh Album PDF(s)')
        self.refresh_pdf_action.triggered.connect(self.refresh_album_pdfs)

    def refresh_album_pdfs(self):
        db = self.gui.current_db
        book_ids = self.gui.library_view.get_selected_ids()
        if not book_ids:
            return error_dialog(self.gui, 'No Books Selected', 'Please select at least one album to refresh.', show=True)

        pd = QProgressDialog('Refreshing PDFs...', 'Abort', 0, len(book_ids), self.gui)
        pd.show()
        
        for i, book_id in enumerate(book_ids):
            if pd.wasCanceled():
                break
            pd.setValue(i)
            
            mi = db.get_metadata(book_id, index_is_id=True)
            tracklist = (mi.get('#track_listing') or '').split('\n')
            cover_data = db.cover(book_id, index_is_id=True)
            
            temp_dir = tempfile.gettempdir()
            pdf_path = os.path.join(temp_dir, f"{mi.title}_refresh.pdf")
            
            gen = AlbumPDFGenerator(mi, tracklist, cover_data)
            gen.generate(pdf_path)
            
            db.add_format_with_path(book_id, 'PDF', pdf_path, index_is_id=True)
            
            try: os.remove(pdf_path)
            except: pass
            
        pd.setValue(len(book_ids))
        info_dialog(self.gui, 'Refresh Complete', f"Refreshed {len(book_ids)} album PDF(s).", show=True)

    def run_schema_check(self):
        if self.ensure_schema():
            info_dialog(self.gui, 'Schema Updated', 
                       'New custom columns have been created. Please restart Calibre to see them.', 
                       show=True)
        else:
            info_dialog(self.gui, 'Schema OK', 
                       'All required custom columns are already present in this library.', 
                       show=True)

    def add_new_album(self):
        # Check schema first
        if self.ensure_schema():
            return error_dialog(self.gui, 'Restart Required', 
                                'New custom columns were created. Please restart Calibre before adding albums.', 
                                show=True)

        d = AddAlbumDialog(self.gui)
        if d.exec_():
            mi = d.get_selected_metadata()
            if mi:
                self.process_selected_album(mi)

    def process_selected_album(self, mi):
        mbid = mi.identifiers.get('musicbrainz')
        source = MusicBrainzSource(None)
        
        # 1. Fetch Tracklist
        tracklist = source.fetch_tracklist(mbid)
        mi.set('#track_listing', "\n".join(tracklist))
        
        # 2. Download Cover
        class Log:
            def error(self, msg): print(msg)
            def info(self, msg): print(msg)
        class ResultQueue:
            def __init__(self): self.cover = None
            def put(self, data): self.cover = data[1]
        
        rq = ResultQueue()
        source.download_cover(Log(), rq, None, identifiers=mi.identifiers)
        cover_data = rq.cover

        # 3. Create entry in Calibre
        db = self.gui.current_db
        book_id = db.create_book_entry(mi, add_duplicates=True)
        
        # 4. Generate PDF
        temp_dir = tempfile.gettempdir()
        pdf_path = os.path.join(temp_dir, f"{mi.title}.pdf")
        gen = AlbumPDFGenerator(mi, tracklist, cover_data)
        gen.generate(pdf_path)
        
        # 5. Add PDF to Calibre entry
        db.add_format_with_path(book_id, 'PDF', pdf_path, index_is_id=True)
        
        # 6. Set Metadata and Cover
        db.set_metadata(book_id, mi)
        if cover_data:
            db.set_cover(book_id, cover_data)
        
        # Clean up temp PDF
        try: os.remove(pdf_path)
        except: pass
        
        self.gui.library_view.model().refresh_ids([book_id])
        info_dialog(self.gui, 'Success', f"Album '{mi.title}' added to library.", show=True)

    def ensure_schema(self):
        db = self.gui.current_db
        fm = db.field_metadata
        creator = CreateNewCustomColumn(self.gui)
        
        created_any = False
        
        for key, spec in CUSTOM_COLUMNS.items():
            lookup_name = spec['lookup_name']
            # Lookup names in database include the leading #
            if not fm.has_label('#' + lookup_name):
                print(f"Creating custom column: {lookup_name}")
                creator.create_column(
                    lookup_name=lookup_name,
                    column_heading=spec['column_heading'],
                    datatype=spec['datatype'],
                    is_multiple=spec['is_multiple'],
                    display=spec['display']
                )
                created_any = True
                
        return created_any

    def initialization_complete(self):
        # Called after all plugins have been initialized.
        # This is a good place to run our schema check.
        # But we don't want to nag the user every time they switch to a non-album library.
        # We'll probably want a way to "opt-in" a library as an album library.
        pass
