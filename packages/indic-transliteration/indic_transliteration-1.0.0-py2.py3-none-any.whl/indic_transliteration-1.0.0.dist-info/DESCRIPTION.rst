Indic transliteration tools
===========================

Intro
=====

For detailed examples and help, please see individual module files in
this package.

Example usage
=============

::

    import indic_transliteration.sanscript
    output = sanscript.transliterate('idam adbhutam', HK, DEVANAGARI)

Packaging
=========

-  ~/.pypirc should have your pypi login credentials.

   ::

       python setup.py bdist_wheel
       twine upload dist/*


