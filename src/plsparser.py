"""
Copyright (c) 2009, Mario Boikov <mario@beblue.org>
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
      this list of conditions and the following disclaimer.
    * Redistributions in binary form must reproduce the above copyright notice,
      this list of conditions and the following disclaimer in the
      documentation and/or other materials provided with the distribution.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
"""

import ConfigParser

_SECTION_PLAYLIST = "playlist"

class NotAPLSFileError(Exception):
    """Raised when the file isn't recognized as a pls file."""
    pass

class CorruptPLSFileError(Exception):
    """Raised when the file contains invalid data or the formatting is wrong"""
    pass


def playlist(pls_fp):
    """Python generator which returns a playlist item for each call to next.
    Each item is a tuple containing a url, title and length.
    Example: ('http://host/song.mp3', 'A Song Title', 210)

    Arguments:
    pls_fp -- A file-like object with pls data (only the readLine
              method is used).

    Exceptions:
    NotAPLSFileError if the file isn't recognized as a pls file.

    Example usage:
    with open("list.pls") as f:
        for entry in playlist(f):
            player.add_url(entry[0])

    See 'http://en.wikipedia.org/wiki/PLS_(file_format)' for more
    information about the pls file format.

    """
    parser = ConfigParser.RawConfigParser()

    try:
        parser.readfp(pls_fp)
    except ConfigParser.MissingSectionHeaderError:
        raise NotAPLSFileError()

    if not parser.has_section(_SECTION_PLAYLIST):
        raise NotAPLSFileError()

    try:
        num_entries = parser.getint(_SECTION_PLAYLIST, "NumberOfEntries") + 1
    except (ConfigParser.NoOptionError, ValueError):
        raise CorruptPLSFileError()

    index = 1

    while not index == num_entries:
        yield (parser.get(_SECTION_PLAYLIST, "File%d" % index),
               parser.get(_SECTION_PLAYLIST, "Title%d" % index),
               parser.get(_SECTION_PLAYLIST, "Length%d" % index))
        index = index + 1
