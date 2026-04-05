from calibre.ebooks.metadata.sources.base import Source
from calibre.ebooks.metadata.book.base import Metadata
from calibre_plugins.album_library.schema import CUSTOM_COLUMNS
import json
from calibre.utils.browser import Browser

class MusicBrainzSource(Source):
    name = 'MusicBrainz'
    description = 'Downloads music metadata from MusicBrainz'
    author = 'Gemini CLI'
    version = (0, 1, 0)
    capabilities = frozenset(['identify', 'cover'])
    touched_fields = frozenset([
        'title', 'authors', 'pubdate', 'tags', 'publisher', 'comments',
        '#artist', '#genre', '#release_date', '#track_listing'
    ])

    def get_browser(self):
        br = Browser()
        # MusicBrainz requires a User-Agent with contact info
        br.addheaders = [('User-Agent', 'CalibreAlbumLibrary/0.1.0 ( contact@example.com )')]
        return br

    def identify(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30):
        if not title:
            return
        
        br = self.get_browser()
        query = f'releasegroup:"{title}"'
        if authors:
            query += f' AND artist:"{" ".join(authors)}"'
            
        url = 'https://musicbrainz.org/ws/2/release-group'
        params = {'query': query, 'fmt': 'json'}
        
        try:
            res = br.open(url, data=params, timeout=timeout)
            data = json.load(res)
        except Exception as e:
            log.error(f"Failed to query MusicBrainz: {str(e)}")
            return

        for rg in data.get('release-groups', []):
            if abort.is_set():
                break
            
            # Map MusicBrainz release group to Calibre Metadata
            mi = self.create_metadata(rg, log)
            if mi:
                # Add to results
                self.clean_downloaded_metadata(mi)
                result_queue.put(mi)

    def create_metadata(self, rg, log):
        title = rg.get('title')
        artists = [ac.get('name') for ac in rg.get('artist-credit', [])]
        
        mi = Metadata(title, artists)
        
        # Release Date
        rd = rg.get('first-release-date')
        if rd:
            from calibre.utils.date import parse_date
            try:
                mi.pubdate = parse_date(rd)
                mi.set('#release_date', mi.pubdate)
            except:
                pass
        
        # Tags / Genre
        tags = [t.get('name') for t in rg.get('tags', [])]
        mi.tags = tags
        mi.set('#genre', tags)
        
        # Artist custom column
        mi.set('#artist', artists)
        
        # identifiers
        mi.identifiers = {'musicbrainz': rg.get('id')}
        
        return mi

    def get_cached_cover_url(self, identifiers):
        mbid = identifiers.get('musicbrainz')
        if mbid:
            return f'https://coverartarchive.org/release-group/{mbid}/front'
        return None

    def fetch_tracklist(self, mbid, log=None):
        br = self.get_browser()
        # To get tracklists, we need to browse releases for the release-group
        url = f'https://musicbrainz.org/ws/2/release?release-group={mbid}&inc=recordings&fmt=json'
        
        try:
            res = br.open(url)
            data = json.load(res)
            # Pick the first release (or the one with the most tracks)
            releases = data.get('releases', [])
            if not releases:
                return []
            
            # Sort by track count descending
            releases.sort(key=lambda x: x.get('track-count', 0), reverse=True)
            release = releases[0]
            
            tracks = []
            for medium in release.get('media', []):
                for track in medium.get('tracks', []):
                    title = track.get('title')
                    number = track.get('number')
                    tracks.append(f"{number}. {title}")
            return tracks
        except Exception as e:
            if log:
                log.error(f"Failed to fetch tracklist for {mbid}: {str(e)}")
            return []

    def download_cover(self, log, result_queue, abort, title=None, authors=None, identifiers={}, timeout=30, get_best=False):
        url = self.get_cached_cover_url(identifiers)
        if not url:
            return
        
        br = self.get_browser()
        try:
            cdata = br.open(url, timeout=timeout).read()
            result_queue.put((self, cdata))
        except Exception as e:
            log.error(f"Failed to download cover from {url}: {str(e)}")
