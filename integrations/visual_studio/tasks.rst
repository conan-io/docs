.. _visual_tasks:

Using tasks with tasks.vs.json
==============================

Another way of using Conan with Visual Studio is using file `tasks <https://docs.microsoft.com/en-us/visualstudio/ide/customize-build-and-debug-tasks-in-visual-studio?view=vs-2017>`_
feature of Visual Studio 2017. This way you can install dependencies by running
:command:`conan install` as task directly in the IDE.

All you need is to right click on your *conanfile.py* -> Configure Tasks (see the `link above <https://docs.microsoft.com/en-us/visualstudio/ide/customize-build-and-debug-tasks-in-visual-studio?view=vs-2017>`_)
and add the following to your *tasks.vs.json*.

.. warning::

    The file *tasks.vs.json* is added to your local *.vs* folder so it is not supposed to be added
    to your version control system.

.. code-block:: text
   :emphasize-lines: 7,9,16,18

    {
        "tasks": [
            {
            "taskName": "conan install debug",
            "appliesTo": "conanfile.py",
            "type": "launch",
            "command": "${env.COMSPEC}",
            "args": [
                "conan install ${file} -s build_type=Debug -if C:/Users/user/CMakeBuilds/4c2d87b9-ec5a-9a30-a47a-32ccb6cca172/build/x64-Debug/"
            ]
            },
            {
            "taskName": "conan install release",
            "appliesTo": "conanfile.py",
            "type": "launch",
            "command": "${env.COMSPEC}",
            "args": [
                "conan install ${file} -s build_type=Release -if C:/Users/user/CMakeBuilds/4c2d87b9-ec5a-9a30-a47a-32ccb6cca172/build/x64-Release/"
            ]
            }
        ],
        "version": "0.2.1"
    }

Then just right click on your *conanfile.py* and launch your :command:`conan install` and
regenerate your *CMakeLists.txt*.
