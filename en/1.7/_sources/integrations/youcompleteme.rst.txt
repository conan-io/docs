.. _youcompleteme_integration:

YouCompleteMe (vim)
-------------------

If you are a vim user, you are possibly already also a user of `YouCompleteMe <http://valloric.github.io/YouCompleteMe/>`_.

With this generator, you can create the necessary files for your project dependencies, so YouCompleteMe
will show symbols from your conan installed dependencies for your project.
You only have to add the ``ycm`` generator to your ``conanfile``:

.. code-block:: text
   :caption: *conanfile.txt*
 
    [generators]
    ycm
   
It will generate a *conan_ycm_extra_conf.py* and a *conan_ycm_flags.json* file in your folder. Those files will be overwritten each time you run :command:`conan install`.

In order to make YouCompleteMe work, copy/move *conan_ycm_extra_conf.py* to your project base folder (usually the one containing your ``conanfile``) and rename it to *.ycm_extra_conf.py*.

You can (and probably should) edit this file to add your project specific configuration.
If your base folder is different from your build folder, link the *conan_ycm_flags.json* from your build folder to your base folder.

.. code-block:: bash

    # from your base folder
    $ cp build/conan_ycm_extra_conf.py .ycm_extra_conf.py
    $ ln -s build/conan_ycm_flags.json conan_ycm_flags.json
