.. _short_paths:


short_paths.conf
----------------

Deprecated. This file is no longer used. If one of your packages hit the Windows path length limit
of 260 chars, just add ``short_paths=True`` to the conanfile.py, and it will automatically handle it.
