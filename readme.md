# Calibre Album Library Plugin

A powerful extension for [Calibre](https://calibre-ebook.com/) that transforms the world's best ebook manager into a comprehensive music record album catalog. This plugin "virtualizes" physical and digital albums as library entries, automatically generating a professional PDF "digital sleeve" for each record.

## 🚀 Key Features

*   **Music-Specific Metadata**: Automatically provisions custom columns for Artists, Genres, Tracklists, Release Dates, and Album/Cover condition grades.
*   **MusicBrainz Integration**: Search and identify albums directly from the MusicBrainz database to fetch accurate metadata and high-resolution cover art.
*   **Automated PDF "Sleeves"**: Generates a beautiful PDF for every album containing:
    *   Large front cover art.
    *   Formatted metadata summary (Year, Genre, MBID).
    *   Complete track listing.
*   **Bulk PDF Refresh**: Regenerate the "digital sleeves" for your entire library or selected entries if you update metadata or artwork.
*   **Schema Guard**: One-click initialization to prepare any Calibre library with the necessary music-specific database fields.

## 🛠️ Technical Architecture

The plugin is built to run natively within Calibre's Python 3 environment:
- **UI Engine**: Qt6 (via Calibre's `qt.core` and `calibre.gui2`).
- **Metadata**: RESTful integration with the MusicBrainz API and Cover Art Archive.
- **PDF Generation**: Powered by the bundled `reportlab` library.
- **Database**: Extends Calibre's SQLite backend through its internal `db` API.

## 📦 Installation & Setup

### 1. Prepare the Plugin Package
Zip the `album_library` directory. Ensure the `__init__.py` file is at the root of the ZIP archive:
```text
album_library.zip
└── __init__.py
└── ui.py
└── metadata.py
└── pdf.py
└── ...
```

### 2. Install in Calibre
1.  Open **Calibre**.
2.  Go to **Preferences** (Ctrl+P) > **Advanced** > **Plugins**.
3.  Click **Load plugin from file** and select your `album_library.zip`.
4.  Acknowledge the security warning and **Restart Calibre**.

### 3. Initialize Your Library
1.  (Optional but Recommended) Create a new, empty Calibre library specifically for your albums.
2.  Locate the **Album Tools** button in the main toolbar (it may be under the "three dots" overflow menu).
3.  Click it and select **Ensure Custom Columns**.
4.  **Restart Calibre** one final time to allow the database to provision the new fields.

## 📖 Usage

### Adding an Album
1.  Click **Album Tools > Add New Album...**
2.  Enter the **Title** and optional **Artist**.
3.  Select the correct result from the list and click **Add Selected Album**.
4.  The plugin will automatically fetch the tracklist, download the cover, create the entry, and generate your PDF sleeve.

### Refreshing Existing Entries
If you manually edit an album's metadata or change its cover art:
1.  Select the album(s) in your library.
2.  Click **Album Tools > Refresh Album PDF(s)**.
3.  The proxy PDF file will be updated with the latest information.

---
*Developed with ❤️ for music collectors.*
