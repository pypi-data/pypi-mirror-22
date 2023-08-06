Dots Editor
===========
A six-key brailler emulator written in python.
----------------------------------------------
|version| |license| |dependencies| |travis|

.. |license| image:: https://img.shields.io/badge/license-MIT-blue.svg
    :target: https://github.com/Gailbear/dots-editor/blob/master/LICENSE.txt
.. |version| image:: https://img.shields.io/pypi/v/dots-editor.svg
    :target: https://pypi.python.org/pypi/dots-editor
.. |dependencies| image:: https://img.shields.io/librariesio/github/gailbear/dots-editor.svg
    :target: https://libraries.io/github/Gailbear/dots-editor
.. |travis| image:: https://travis-ci.org/Gailbear/dots-editor.svg?branch=master
    :target: https://travis-ci.org/Gailbear/dots-editor

Tired of being on a mac and having no viable options for a six-key brailler emulator?
Tired of not being able to fix bugs or request features with existing emulators?
**Me too!**

I was sick of there not being an emulator that is free, easy to use, and easy to install on any operating system.

This is in Pre-Alpha. Expect bugs, and missing features.

Installation
------------

``pip install dots-editor``

Usage
_____

``dots_editor filename.brl``

This will open a file for editing. When you quit (I know, scary), it will save.

``dots_editor --unicode filename.txt``

This will save a file using the unicode braille glyphs. (U+2800 to U+2840)

Pre-Alpha features to add
-------------------------
- Edit an existing file (I know, big oversight)
- Start standalone
- Menu to make a new file or open an existing one
- Save without exit
- Binaries for common operating systems
- Cursor

Alpha features to add
---------------------
- resizable window
- change font size
- change margin
- figure out brf format
- Logo
- Documentation (and documentation tests)
- automatic line breaks
- 8-dot mode

Beta features to add
--------------------
- Integration with liblouis
- contraction help
- highlighting text to edit or move
- find/replace
- save in all common filetypes
- print (to printer or embosser)
- spellcheck?

Want to contribute?
-------------------

Wow, cool. I don't currently have any guidelines, but contact me using github,
and we'll talk. It's much more likely to be a successful talk if you have a pull
request and a good summary of what you're trying to accomplish.
