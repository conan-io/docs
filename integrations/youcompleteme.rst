.. _youcompleteme_integration:

YouCompleteMe (vim)
___________________

If you are a vim user, you are possibly already also a user of `YouCompleteMe <http://valloric.github.io/YouCompleteMe/>`_.

With this generator, you can create the necessary file for your project dependencies, so YouCompleteMe
will show symbols from your conan installed dependencies for your project. 
You only have to add the ``ycm`` generator to your ``conanfile``:


**conanfile.txt**

.. code-block:: text

   ...
   
   [generators]
   ycm
   
It will generate a ``.ycm_extra_conf.py`` file in your project folder, and YouCompleteMe automatically
loads this file.


