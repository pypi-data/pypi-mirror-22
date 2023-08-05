sokoenginepy - Sokoban and variants game engine
***********************************************



sokoenginepy is game engine for Sokoban and variants written in Python and
loaded with features:

- implements game logic for ``Sokoban``, ``Hexoban``, ``Trioban`` and ``Octoban`` variants
    - supports ``Sokoban+`` for all implemented variants
    - supports ``Multiban`` (muliple pushers on board) for all variants
- two game engines implementations
    - fast and memory lightweight with single step undo/redo
    - somewhat slower and larger with unlimited movement undo/redo
- reading and writing level collections
    - fully compatible with `SokobanYASC`_ .sok file format and variants (.xsb, .tsb, .hsb, .txt)

sokoenginepy was inspired by `SokobanYASC`_, `JSoko`_, MazezaM

Installing
----------

Installing sokoenginepy should be as simple as

.. code-block:: sh

    pip install sokoenginepy

Using
-----

- For quick glance of features and usage check the `Tutorial`_.
- For in-depth docs of whole package see `API Reference`_.


.. _SokobanYASC: https://sourceforge.net/projects/sokobanyasc/
.. _JSoko: http://www.sokoban-online.de/jsoko.html
.. _Sokobano: http://sokobano.de/en/index.php
.. _Sokoban for Windows: http://www.sourcecode.se/sokoban/
.. _Tutorial: https://sokoenginepy.readthedocs.io/en/development/tutorial.html
.. _API reference: https://sokoenginepy.readthedocs.io/en/development/api.html


