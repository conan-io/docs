.. note::
   
   **Default Remote Update in Conan 2.9.2**

   Starting from **Conan version 2.9.2**, the default remote has been changed to
   `https://center2.conan.io`. The previous default remote `https://center.conan.io` is
   now frozen and will no longer receive updates. It is recommended to update your remote
   configuration to use the new default remote to ensure access to the latest recipes and
   package updates (for more information, please read this `post
   <https://blog.conan.io/2024/09/30/Conan-Center-will-stop-receiving-updates-for-Conan-1.html>`_).

   If you still have the deprecated remote configured as the default, please update using
   the following command:

   .. code-block:: bash

       conan remote update conancenter --url="https://center2.conan.io"    
