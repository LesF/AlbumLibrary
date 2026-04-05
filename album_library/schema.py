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
