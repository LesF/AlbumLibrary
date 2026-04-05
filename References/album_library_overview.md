# Album Library Plan

## Purpose
Create an extension for the Calibre ebook library management application, which allows me to create a catalog of my record albums

### Features
- define a new library type for Calibre
- the album library type will have it's own directory set in configuration, to keep content separate from ebooks and other libraries configured in Calibre
- a record album can be added to the library using the standard Calibre tools and methods, with some extra features:
	1. Instead of author(s) an album will have one or more bands or artists (some albums will be produced by a single band, some may be compilation albums)
	2. On creation of an album, the user will be able to search online services (yet to be discovered/defined) which may provide data on the album, it's artist(s) or band details, the sound tracks on the album, images of the album covers, maybe even song lyrics
	3. Information retrieved from external services, or alternatively typed in or edited by the user, will be compiled into a PDF file which gets saved in the album library
	
### Metadata for an album will include:
- album name
- band(s) or artist(s) names, consider links to relevant web sites for these
- album release date
- track listing
- song lyrics or URL to these, if available (TODO check copyright etc affecting how we may retrieve lyrics)
- grading of album and cover condition (maybe scale 1 to 5 for each)
- owned, wanted, or upgrade-wanted status

## methods
- Review guidelines for creating an extension (or do they call it a plugin?) for Calibre
- Find how a new library or catalog type is defined in Calibre

# References
https://manual.calibre-ebook.com/creating_plugins.html

https://manual.calibre-ebook.com/creating_plugins.html#the-plugin-api

