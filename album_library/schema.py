# Schema definition for Album Library

CUSTOM_COLUMNS = {
    'artist': {
        'lookup_name': 'artist',
        'column_heading': 'Artist(s)',
        'datatype': 'text',
        'is_multiple': True,
        'display': {'is_names': True}
    },
    'genre': {
        'lookup_name': 'genre',
        'column_heading': 'Genre',
        'datatype': 'text',
        'is_multiple': True,
        'display': {'is_names': False}
    },
    'media_type': {
        'lookup_name': 'media_type',
        'column_heading': 'Media Type',
        'datatype': 'enumeration',
        'is_multiple': False,
        'display': {'enum_values': ['CD', 'Vinyl', 'Digital', 'Cassette', 'DVD', 'Other'], 'enum_colors': []}
    },
    'num_discs': {
        'lookup_name': 'num_discs',
        'column_heading': 'Discs',
        'datatype': 'int',
        'is_multiple': False,
        'display': {}
    },
    'release_date': {
        'lookup_name': 'release_date',
        'column_heading': 'Release Date',
        'datatype': 'datetime',
        'is_multiple': False,
        'display': {'date_format': 'yyyy'}
    },
    'track_listing': {
        'lookup_name': 'track_listing',
        'column_heading': 'Tracklist',
        'datatype': 'comments',
        'is_multiple': False,
        'display': {'interpret_as': 'text'}
    },
    'lyrics_url': {
        'lookup_name': 'lyrics_url',
        'column_heading': 'Lyrics URL',
        'datatype': 'text',
        'is_multiple': False,
        'display': {}
    },
    'album_grade': {
        'lookup_name': 'album_grade',
        'column_heading': 'Album Grade',
        'datatype': 'rating',
        'is_multiple': False,
        'display': {}
    },
    'cover_grade': {
        'lookup_name': 'cover_grade',
        'column_heading': 'Cover Grade',
        'datatype': 'rating',
        'is_multiple': False,
        'display': {}
    },
    'status': {
        'lookup_name': 'status',
        'column_heading': 'Status',
        'datatype': 'enumeration',
        'is_multiple': False,
        'display': {'enum_values': ['Owned', 'Wanted', 'Upgrade Wanted'], 'enum_colors': []}
    }
}
