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
import unittest
import StringIO

import plsparser

class ValidPLSFileTest(unittest.TestCase):
    """Test valid pls file content."""

    def testSingleEntry(self):
        """Test with single entry in the pls file."""
        pls_file = StringIO.StringIO("[playlist]\n"
                                     "NumberOfEntries=1\n"
                                     "File1=http://ip:port\n"
                                     "Title1=A Title\n"
                                     "Length1=-1\n"
                                     "Version=2")
        expected = ("http://ip:port", "A Title", "-1")

        actual = [entry for entry in plsparser.playlist(pls_file)]

        self.assertEquals([expected], actual)


    def testMultipleEntries(self):
        """Test with multiple entries in the pls file."""
        tmpl = "File%d=File %d\nTitle%d=Title %d\nLength%d=%d\n"
        data = "".join([tmpl % (i, i, i, i, i, i) for i in range(1, 4)])
        pls_file = StringIO.StringIO("[playlist]\n"
                                     "NumberOfEntries=3\n" +
                                     data +
                                     "Version=2")
        expected = [("File %d" % i, "Title %d" % i, "%d" % i) for i in range(1, 4)]

        actual = [entry for entry in plsparser.playlist(pls_file)]

        self.assertEquals(expected, actual)

class NonValidPLSFileTest(unittest.TestCase):
    """Test non valid pls file."""

    def testFileWithoutPLSMarker(self):
        """Should raise a NotAPLSFileError."""
        pls_file = StringIO.StringIO("\n"
                                     "NumberOfEntries=1\n"
                                     "File1=http://ip:port\n"
                                     "Title1=A Title\n"
                                     "Length1=-1\n"
                                     "Version=2")

        plist = plsparser.playlist(pls_file)
        self.assertRaises(plsparser.NotAPLSFileError, plist.next)

    def testFileWithWrongPLSMarker(self):
        """Should raise a NotAPLSFileError."""
        pls_file = StringIO.StringIO("[my_playlist]\n"
                                     "NumberOfEntries=1\n"
                                     "File1=http://ip:port\n"
                                     "Title1=A Title\n"
                                     "Length1=-1\n"
                                     "Version=2")

        plist = plsparser.playlist(pls_file)
        self.assertRaises(plsparser.NotAPLSFileError, plist.next)

    def testMissingNumberOfEntries(self):
        """Should raise a CorruptPLSFileError."""
        pls_file = StringIO.StringIO("[playlist]\n"
                                     "\n"
                                     "File1=http://ip:port\n"
                                     "Title1=A Title\n"
                                     "Length1=-1\n"
                                     "Version=2")

        plist = plsparser.playlist(pls_file)
        self.assertRaises(plsparser.CorruptPLSFileError, plist.next)

    def testInvalidNumberOfEntries(self):
        """Should raise a CorruptPLSFileError."""
        pls_file = StringIO.StringIO("[playlist]\n"
                                     "NumberOfEntries=ABC\n"
                                     "File1=http://ip:port\n"
                                     "Title1=A Title\n"
                                     "Length1=-1\n"
                                     "Version=2")

        plist = plsparser.playlist(pls_file)
        self.assertRaises(plsparser.CorruptPLSFileError, plist.next)

if __name__ == "__main__":
    unittest.main()