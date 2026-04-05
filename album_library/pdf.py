from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
import io

class AlbumPDFGenerator:
    def __init__(self, metadata, tracklist=None, cover_data=None):
        self.mi = metadata
        self.tracklist = tracklist or []
        self.cover_data = cover_data

    def generate(self, output_path):
        doc = SimpleDocTemplate(output_path, pagesize=letter)
        styles = getSampleStyleSheet()
        elements = []

        # Title and Artist
        elements.append(Paragraph(f"<b>{self.mi.title}</b>", styles['Title']))
        artist_str = ", ".join(self.mi.authors)
        elements.append(Paragraph(f"<i>{artist_str}</i>", styles['Subtitle']))
        elements.append(Spacer(1, 24))

        # Cover Image
        if self.cover_data:
            img_stream = io.BytesIO(self.cover_data)
            img = Image(img_stream, width=200, height=200)
            img.hAlign = 'CENTER'
            elements.append(img)
            elements.append(Spacer(1, 24))

        # Metadata Summary
        meta_data = [
            ['Release Date:', self.mi.pubdate.strftime('%Y') if self.mi.pubdate else 'N/A'],
            ['Genre:', ", ".join(self.mi.tags) if self.mi.tags else 'N/A'],
            ['MusicBrainz ID:', self.mi.identifiers.get('musicbrainz', 'N/A')]
        ]
        t = Table(meta_data, colWidths=[100, 300])
        t.setStyle(TableStyle([
            ('FONTNAME', (0,0), (0,-1), 'Helvetica-Bold'),
            ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ]))
        elements.append(t)
        elements.append(Spacer(1, 12))

        # Tracklist
        if self.tracklist:
            elements.append(Paragraph("<b>Track Listing</b>", styles['Heading2']))
            track_data = [[track] for track in self.tracklist]
            tt = Table(track_data, colWidths=[400])
            tt.setStyle(TableStyle([
                ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
            ]))
            elements.append(tt)

        doc.build(elements)
        return output_path
