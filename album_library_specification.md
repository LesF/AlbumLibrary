# Album Library Calibre Plugin - Technical Specification

## 1. Project Overview
This project aims to extend the Calibre ebook management application to serve as a comprehensive catalog for physical and digital record albums. Since Calibre is primarily designed for books, the plugin will "virtualize" albums as book entries, using a generated PDF as the primary file format for each entry.

## 2. Core Architecture
- **Multi-Library Support**: Uses Calibre's native library switching. Users are encouraged to create a dedicated library for albums.
- **PDF-as-Proxy**: Every album entry in Calibre will contain a generated PDF file. This PDF acts as a "digital sleeve" containing metadata, tracklists, and cover art.
- **Custom Schema**: Automated provisioning of music-specific metadata fields via Calibre's Custom Columns.

## 3. Data Schema (Custom Columns)
The plugin will ensure the following columns exist (prefixed with `#` in Calibre):

| Column Name | Lookup Name | Type | Description |
|-------------|-------------|------|-------------|
| Artist(s) | `#artist` | Text (Multi) | Performing artists or bands |
| Genre | `#genre` | Text (Multi) | Album genres (e.g., Jazz, Blues, Rock) |
| Media Type | `#media_type` | Enum | CD, Vinyl, Digital, etc. |
| Discs | `#num_discs` | Integer | Number of discs in the release |
| Release Date| `#release_date` | Date | Original album release date |
| Tracklist | `#track_listing` | Long Text | Ordered list of tracks |
| Lyrics URL | `#lyrics_url` | Text | Link to external lyrics provider |
| Album Grade | `#album_grade` | Rating | Condition of the record (1-5) |
| Cover Grade | `#cover_grade` | Rating | Condition of the sleeve (1-5) |
| Status | `#status` | Enum | Owned, Wanted, Upgrade Wanted |

## 4. Component Design

References:
- https://manual.calibre-ebook.com/creating_plugins.html

### 4.1 Metadata Provider (`AlbumMetadataSource`)
- **Class**: Extends `calibre.customize.MetadataSource`.
- **APIs**: Integrates with **MusicBrainz** (primary) and **Discogs** (fallback).
- **Functions**:
    - `identify()`: Searches for albums by Title/Artist.
    - `download_cover()`: Fetches high-resolution artwork.
    - Returns a `Metadata` object mapped to standard fields (Title -> Album Name, Author -> Artist) and custom columns.

### 4.2 PDF Generator (`AlbumPDFGenerator`)
- **Engine**: Bundled `reportlab` library.
- **Output**: A professionally formatted PDF containing:
    - Large front cover image.
    - Metadata summary (Label, Year, Genre, Status).
    - Formatted Tracklist table.
    - (Optional) Artist biography or lyrics snippets.
- **Trigger**: Runs automatically when an album is added or metadata is significantly updated.

### 4.3 User Interface (`AlbumUIPlugin`)
- **Actions**:
    - **"Add New Album"**: A custom dialog that combines search, metadata selection, and PDF generation in one flow.
    - **"Refresh Album PDF"**: Re-generates the proxy PDF for selected entries.
- **Context Menu**: Adds an "Album Library" sub-menu to the library view.

## 5. Development Phases

### Phase 1: Infrastructure
- Define plugin metadata and basic UI hooks.
- Implement "Schema Guard" logic to create custom columns if missing in the current library.

### Phase 2: Metadata Logic
- Develop MusicBrainz API client.
- Implement search and identification logic.

### Phase 3: PDF Engine
- Create `reportlab` templates for the album summary.
- Handle image scaling and table formatting for tracklists.

### Phase 4: Integration & UX
- Connect the metadata fetcher to the PDF generator.
- Add progress bars and error handling for network requests.

## 6. Constraints & Considerations
- **Environment**: Must run within Calibre's bundled Python 3 environment.
- **Performance**: PDF generation should be asynchronous to avoid freezing the UI.
- **Storage**: PDF files should be optimized for size while maintaining cover art quality.
- **Copyright**: Only store links to lyrics or short snippets to avoid legal complications.

