From 355fd785ef13f12d303358af5c0e6ee536f8eb77 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Wed, 20 Aug 2025 11:12:06 +0200
Subject: [PATCH 01/11] Add Sanitizers documentation

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 examples/dev_flow.rst                         |   1 +
 .../sanitizers/compiler_sanitizers.rst        | 198 ++++++++++++++++++
 2 files changed, 199 insertions(+)
 create mode 100644 examples/dev_flow/sanitizers/compiler_sanitizers.rst

diff --git a/examples/dev_flow.rst b/examples/dev_flow.rst
index 4363e2e079b52f9a72f84f566321b3b9be8a3abd..21d7e0e947449cf9b6edc97bdd27b8d6f8178089 100644
--- a/examples/dev_flow.rst
+++ b/examples/dev_flow.rst
@@ -8,4 +8,5 @@ Developer tools and flows
 
    dev_flow/debug/step_into_dependencies
    dev_flow/debug/debugging_visual
+   dev_flow/sanitizers/compiler_sanitizers
    dev_flow/tool_requires/mingw
diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
new file mode 100644
index 0000000000000000000000000000000000000000..f789417f15c30abaeaa4b1eea720bba5856b37e4
--- /dev/null
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -0,0 +1,198 @@
+.. _examples_dev_flow_sanitizers_compiler_sanitizers:
+
+Compiler sanitizers
+===================
+
+Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, memory leaks,
+dangling pointers, and various types of undefined behavior.
+
+Compilers such as GCC, Clang and MSVC support these tools through specific compiler and linker flags.
+
+This example explains a recommended approach for integrating compiler sanitizers into your Conan 2.x workflow.
+
+Modeling and Applying Sanitizers using Settings
+------------------------------------------------
+
+If you want to model the sanitizer options so that the package id is affected by them, you have to
+:ref:`customize new compiler sub-settings<reference_config_files_customizing_settings>`. You should not need
+modify ``settings.yml`` directly, but adding :ref:`the settings_user.yml <examples_config_files_settings_user>`
+instead.
+
+This approach is preferred because it ensures that enabling a sanitizer alters the package ID, allowing you to use the same
+binary package with or without sanitizers, which is ideal for development and debugging workflows.
+
+To better illustrate this, please, first clone the sources to recreate this project. You can find them in the
+`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:
+
+.. code-block:: bash
+
+    $ git clone https://github.com/conan-io/examples2.git
+    $ cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers
+
+In this example we are going to see how to prepare Conan to use sanitizers in different ways.
+
+
+Configuring Sanitizers as Part of Settings
+##########################################
+
+If you typically use a specific set of sanitizers or combinations for your builds, you can specify
+them as a list of values. For example, with Clang, you might do the following:
+
+.. code-block:: yaml
+    :caption: *settings_user.yml*
+    :emphasize-lines: 6
+
+    compiler:
+      clang:
+        sanitizer: [None, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
+
+Here you have modeled the use of ``-fsanitize=address``, ``-fsanitize=thread``,
+``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``, ``-fsanitize=kernel-address``, the combination of ``-fsanitize=address`` with
+``-fsanitize=undefined`` and ``-fsanitize=thread`` with ``-fsanitize=undefined``.
+
+It seems be a large number of options, but for Clang, these are only a portion.
+To obtain the complete list of available sanitizers, you can refer to the `Clang documentation <https://clang.llvm.org/docs/>`_.
+The GCC supports a similar number of sanitizers, and you can find the complete list in the `GCC documentation <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
+For MSVC, the available sanitizers are more limited, and you can find the complete list in the `MSVC documentation <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.
+
+Note that not all sanitizer combinations are possible, for example, with Clang, you cannot use more than one of the Address, Thread, or Memory sanitizers in the same program.
+
+Be aware once ``setting_user.yml`` is present in your Conan home, it will affect all your projects using Conan, asking for the setting ``compiler.sanitizer`` always.
+In order to disable it, just remove the ``settings_user.yml`` file from your Conan home.
+
+Adding Sanitizers as Part of the Profile
+########################################
+
+An option would be to add the sanitizer values as part of the profile.
+This way, you can easily switch between different sanitizer configurations by using different dedicated profiles.
+
+.. code-block:: ini
+    :caption: *~/.conan/profiles/asan*
+    :emphasize-lines: 6
+
+    include(default)
+
+    [settings]
+    compiler.sanitizer=Address
+
+    [conf]
+    tools.build:cflags=['-fsanitize=address']
+    tools.build:cxxflags=['-fsanitize=address']
+
+The Conan client is capable to deduce the necessary flags from the profile and apply them during the build process.
+It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.
+
+
+Passing the information to the compiler or build system
+-------------------------------------------------------
+
+Here again, we have multiple choices to pass sanitizers information to the compiler or build system.
+
+Using from custom profiles
+##########################
+
+It is possible to have different custom profiles defining the compiler sanitizer setting and
+environment variables to inject that information to the compiler, and then passing those profiles to
+Conan commands. An example of this would be a profile like:
+
+.. code-block:: text
+   :caption: *address_sanitizer_profile*
+   :emphasize-lines: 10,12,13,14
+
+    [settings]
+    os=Macos
+    os_build=Macos
+    arch=x86_64
+    arch_build=x86_64
+    compiler=apple-clang
+    compiler.version=10.0
+    compiler.libcxx=libc++
+    build_type=Release
+    compiler.sanitizer=Address
+    [env]
+    CFLAGS=-fsanitize=address
+    CXXFLAGS=-fsanitize=address
+    LDFLAGS=-fsanitize=address
+
+Then calling :command:`conan create . -pr address_sanitizer_profile` would inject
+``-fsanitize=address`` to the build through the ``CFLAGS``, ``CXXFLAGS``, and ``LDFLAGS`` environment variables.
+
+Managing sanitizer settings with the build system
+#################################################
+
+Another option is to make use of the information that is propagated to the *conan generator*. For
+example, if we are using CMake we could use the information from the *CMakeLists.txt* to append
+the flags to the compiler settings like this:
+
+.. code-block:: cmake
+   :caption: *CMakeLists.txt*
+
+    cmake_minimum_required(VERSION 3.2)
+    project(SanitizerExample)
+    set (CMAKE_CXX_STANDARD 11)
+    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
+    conan_basic_setup()
+    set(SANITIZER ${CONAN_SETTINGS_COMPILER_SANITIZER})
+    if(SANITIZER)
+        if(SANITIZER MATCHES "(Address)")
+        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
+        endif()
+    endif()
+    add_executable(sanit_example src/main.cpp)
+
+
+The sanitizer setting is propagated to CMake as the ``CONAN_SETTINGS_COMPILER_SANITIZER`` variable
+with a value equals to ``"Address"`` and we can set the behavior in CMake depending on the value of
+the variable.
+
+
+Using conan Hooks to set compiler environment variables
+#######################################################
+
+.. warning::
+
+    This way of adding sanitizers is recommended just for testing purposes. In general, it's not a
+    good practice to inject this in the environment using a Conan hook. It's much better explicitly
+    defining this in the profiles.
+
+.. important::
+
+    Take into account that the package ID doesn't encode information about the environment,
+    so different binaries due to different `CXX_FLAGS` would be considered by Conan as the same package.
+
+
+If you are not interested in modelling the settings in the Conan package you can use a
+Hook to modify the environment variable and apply the sanitizer
+flags to the build. It could be something like:
+
+.. code-block:: python
+    :caption: *sanitizer_hook.py*
+
+    import os
+
+
+    class SanitizerHook(object):
+        def __init__(self):
+            self._old_cxx_flags = None
+
+        def set_sanitize_address_flag(self):
+            self._old_cxx_flags = os.environ.get("CXXFLAGS")
+            flags_str = self._old_cxx_flags or ""
+            os.environ["CXXFLAGS"] = flags_str + " -fsanitize=address"
+
+        def reset_sanitize_address_flag(self):
+            if self._old_cxx_flags is None:
+                del os.environ["CXXFLAGS"]
+            else:
+                os.environ["CXXFLAGS"] = self._old_cxx_flags
+
+
+    sanitizer = SanitizerHook()
+
+
+    def pre_build(output, conanfile, **kwargs):
+        sanitizer.set_sanitize_address_flag()
+
+
+    def post_build(output, conanfile, **kwargs):
+        sanitizer.reset_sanitize_address_flag()
-- 
2.51.0


From 84ba72d20e0024ac44eccb248d1d748efe28da61 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Wed, 20 Aug 2025 11:22:31 +0200
Subject: [PATCH 02/11] Add Sanitizers

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 128 ++++--------------
 1 file changed, 24 insertions(+), 104 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index f789417f15c30abaeaa4b1eea720bba5856b37e4..7a3fe106b92d8c9e2b039157a46954e842de2d68 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -3,6 +3,12 @@
 Compiler sanitizers
 ===================
 
+.. warning::
+
+    Using sanitizers in production with suid binaries is dangerous, as the libsanitizer runtime
+    relies on environment variables that could enable privilege escalation attacks.
+    Use sanitizers only in development and testing environments.
+
 Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, memory leaks,
 dangling pointers, and various types of undefined behavior.
 
@@ -40,7 +46,7 @@ them as a list of values. For example, with Clang, you might do the following:
 
 .. code-block:: yaml
     :caption: *settings_user.yml*
-    :emphasize-lines: 6
+    :emphasize-lines: 3
 
     compiler:
       clang:
@@ -82,117 +88,31 @@ This way, you can easily switch between different sanitizer configurations by us
 The Conan client is capable to deduce the necessary flags from the profile and apply them during the build process.
 It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.
 
+Building Examples Using Sanitizers
+----------------------------------
 
-Passing the information to the compiler or build system
--------------------------------------------------------
-
-Here again, we have multiple choices to pass sanitizers information to the compiler or build system.
-
-Using from custom profiles
-##########################
-
-It is possible to have different custom profiles defining the compiler sanitizer setting and
-environment variables to inject that information to the compiler, and then passing those profiles to
-Conan commands. An example of this would be a profile like:
-
-.. code-block:: text
-   :caption: *address_sanitizer_profile*
-   :emphasize-lines: 10,12,13,14
-
-    [settings]
-    os=Macos
-    os_build=Macos
-    arch=x86_64
-    arch_build=x86_64
-    compiler=apple-clang
-    compiler.version=10.0
-    compiler.libcxx=libc++
-    build_type=Release
-    compiler.sanitizer=Address
-    [env]
-    CFLAGS=-fsanitize=address
-    CXXFLAGS=-fsanitize=address
-    LDFLAGS=-fsanitize=address
-
-Then calling :command:`conan create . -pr address_sanitizer_profile` would inject
-``-fsanitize=address`` to the build through the ``CFLAGS``, ``CXXFLAGS``, and ``LDFLAGS`` environment variables.
-
-Managing sanitizer settings with the build system
-#################################################
-
-Another option is to make use of the information that is propagated to the *conan generator*. For
-example, if we are using CMake we could use the information from the *CMakeLists.txt* to append
-the flags to the compiler settings like this:
-
-.. code-block:: cmake
-   :caption: *CMakeLists.txt*
+Address Sanitizer: Index Out of Bounds
+######################################
 
-    cmake_minimum_required(VERSION 3.2)
-    project(SanitizerExample)
-    set (CMAKE_CXX_STANDARD 11)
-    include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
-    conan_basic_setup()
-    set(SANITIZER ${CONAN_SETTINGS_COMPILER_SANITIZER})
-    if(SANITIZER)
-        if(SANITIZER MATCHES "(Address)")
-        set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address" )
-        endif()
-    endif()
-    add_executable(sanit_example src/main.cpp)
+**TODO**
 
+Undefined Sanitizer: Signed Integer Overflow
+############################################
 
-The sanitizer setting is propagated to CMake as the ``CONAN_SETTINGS_COMPILER_SANITIZER`` variable
-with a value equals to ``"Address"`` and we can set the behavior in CMake depending on the value of
-the variable.
+**TODO**
 
+Passing the information to the compiler or build system
+-------------------------------------------------------
 
-Using conan Hooks to set compiler environment variables
-#######################################################
-
-.. warning::
-
-    This way of adding sanitizers is recommended just for testing purposes. In general, it's not a
-    good practice to inject this in the environment using a Conan hook. It's much better explicitly
-    defining this in the profiles.
-
-.. important::
-
-    Take into account that the package ID doesn't encode information about the environment,
-    so different binaries due to different `CXX_FLAGS` would be considered by Conan as the same package.
-
-
-If you are not interested in modelling the settings in the Conan package you can use a
-Hook to modify the environment variable and apply the sanitizer
-flags to the build. It could be something like:
-
-.. code-block:: python
-    :caption: *sanitizer_hook.py*
-
-    import os
-
-
-    class SanitizerHook(object):
-        def __init__(self):
-            self._old_cxx_flags = None
-
-        def set_sanitize_address_flag(self):
-            self._old_cxx_flags = os.environ.get("CXXFLAGS")
-            flags_str = self._old_cxx_flags or ""
-            os.environ["CXXFLAGS"] = flags_str + " -fsanitize=address"
-
-        def reset_sanitize_address_flag(self):
-            if self._old_cxx_flags is None:
-                del os.environ["CXXFLAGS"]
-            else:
-                os.environ["CXXFLAGS"] = self._old_cxx_flags
-
+Besides using Conan profiles to manage sanitizer settings, you can also use different approaches.
 
-    sanitizer = SanitizerHook()
+Managing Sanitizer with CMake Toolchain
+#######################################
 
+**TODO**
 
-    def pre_build(output, conanfile, **kwargs):
-        sanitizer.set_sanitize_address_flag()
 
+Mananaging Sanitizer with Conan Hooks
+#####################################
 
-    def post_build(output, conanfile, **kwargs):
-        sanitizer.reset_sanitize_address_flag()
+**TODO**
\ No newline at end of file
-- 
2.51.0


From 6c6a71ec7ce9af99c8463c09016d01d1e56fbe54 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Thu, 21 Aug 2025 09:42:11 +0200
Subject: [PATCH 03/11] Add more sections

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 140 +++++++++++++++++-
 1 file changed, 136 insertions(+), 4 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 7a3fe106b92d8c9e2b039157a46954e842de2d68..0c758844264a8ebef2432975401aaa471021ddf1 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -74,7 +74,7 @@ This way, you can easily switch between different sanitizer configurations by us
 
 .. code-block:: ini
     :caption: *~/.conan/profiles/asan*
-    :emphasize-lines: 6
+    :emphasize-lines: 7
 
     include(default)
 
@@ -84,22 +84,154 @@ This way, you can easily switch between different sanitizer configurations by us
     [conf]
     tools.build:cflags=['-fsanitize=address']
     tools.build:cxxflags=['-fsanitize=address']
+    tools.build:exelinkflags=['-fsanitize=address']
 
-The Conan client is capable to deduce the necessary flags from the profile and apply them during the build process.
+The Conan client is not capable to deduce the necessary flags from the settings and apply them during the build process.
 It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.
 
 Building Examples Using Sanitizers
 ----------------------------------
 
+To show how to use sanitizers in your builds, let's consider a couple of examples.
+
 Address Sanitizer: Index Out of Bounds
 ######################################
 
-**TODO**
+In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds
+index in an array, which should trigger the Address Sanitizer when running the program.
+
+The following code demonstrates this:
+
+.. code-block:: cpp
+    :caption: *index_out_of_bounds/main.cpp*
+    :emphasize-lines: 11
+
+    #include <iostream>
+    #include <cstdlib>
+
+    int main() {
+        #ifdef __SANITIZE_ADDRESS__
+            std::cout << "Address sanitizer enabled\n";
+        #else
+            std::cout << "Address sanitizer not enabled\n";
+        #endif
+
+        int foo[100];
+        foo[100] = 42; // Out-of-bounds write
+
+        return EXIT_SUCCESS;
+    }
+
+The definition ``__SANITIZE_ADDRESS__`` is used to check if the Address Sanitizer is enabled when
+running the produced application. It's supported by GCC, Clang and MSVC compilers.
+
+To build this example, you can use Conan to invoke CMake and perform the build.
+
+.. code-block:: bash
+
+    conan export index_out_of_bounds/
+    conan install --requires=index_out_of_bounds/0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing
+
+
+Here we are using Conan to export the recipe and build the project.
+The profile file `profiles/asan` was demonstrated already and will merge with the default profile
+from your configuration. The resulting build will produce an executable in a specific package folder,
+in order to access it, you can use the script produced by the ``VirtualRunEnv`` generator,
+then run the executable:
+
+.. code-block:: text
+
+    source index_out_of_bounds/install/conanrun.sh
+    index_out_of_bounds
+
+    Address sanitizer enabled
+    =================================================================
+    ==32018==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbe04a6d0 at pc 0x5dad4506e2eb bp 0x7fffbe04a500 sp 0x7fffbe04a4f0
+    WRITE of size 4 at 0x7fffbe04a6d0 thread T0
+        #0 0x5dad4506e2ea in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea)
+        #1 0x731331629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
+        #2 0x731331629e3f in __libc_start_main_impl ../csu/libc-start.c:392
+        #3 0x5dad4506e3d4 in _start (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x13d4)
+
+    Address 0x7fffbe04a6d0 is located in stack of thread T0 at offset 448 in frame
+        #0 0x5dad4506e1ef in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x11ef)
+
+    This frame has 1 object(s):
+        [48, 448) 'foo' (line 11) <== Memory access at offset 448 overflows this variable
+    HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
+        (longjmp and C++ exceptions *are* supported)
+    SUMMARY: AddressSanitizer: stack-buffer-overflow (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea) in main
+
+Once running the example, you should see an error message from the Address Sanitizer indicating the
+out-of-bounds. The message is simplified here, but it provides useful information about the error,
+including the expected index of bounds error.
+
 
 Undefined Sanitizer: Signed Integer Overflow
 ############################################
 
-**TODO**
+This example demonstrates how to use the Undefined Behavior Sanitizer to detect signed integer overflow.
+It combines the usage of two sanitizers at same time: Address Sanitizer and Undefined Behavior Sanitizer.
+For this example, we will be using the following Conan profile:
+
+.. code-block:: ini
+    :caption: *~/.conan/profiles/asan_ubsan*
+    :emphasize-lines: 7
+
+    include(default)
+
+    [settings]
+    compiler.sanitizer=AddressUndefinedBehavior
+
+    [conf]
+    tools.build:cflags=['-fsanitize=address,undefined']
+    tools.build:cxxflags=['-fsanitize=address,undefined']
+    tools.build:exelinkflags=['-fsanitize=address,undefined']
+
+It's important to mention it only works for GCC and Clang compilers,
+as MSVC does not support the Undefined Behavior Sanitizer yet.
+
+The source code for this example is as follows:
+
+.. code-block:: cpp
+    :caption: *signed_integer_overflow/main.cpp*
+    :emphasize-lines: 12
+
+    #include <iostream>
+    #include <cstdlib>
+    #include <cstdint>
+
+    int main(int argc, char* argv[]) {
+        #ifdef __SANITIZE_ADDRESS__
+            std::cout << "Address sanitizer enabled\n";
+        #else
+            std::cout << "Address sanitizer not enabled\n";
+        #endif
+
+        int foo = 0x7fffffff;
+        foo += argc; // Signed integer overflow
+
+        return EXIT_SUCCESS;
+    }
+
+In this example, it's intentionally causing a signed integer overflow by adding the command line argument count to a large integer value.
+
+As next step, the code can be built using Conan and CMake, similar to the previous example:
+
+.. code-block:: bash
+
+    conan export signed_integer_overflow/
+    conan install --requires=signed_integer_overflow/0.1.0 -pr profiles/asan -of signed_integer_overflow/install --build=missing
+
+
+Once the project built successfully, you can run the example with the sanitizers enabled:
+
+.. code-block:: bash
+
+    conan build signed_integer_overflow/install
+    ./build/signed_integer_overflow
+
+This should trigger the Address and Undefined Behavior Sanitizers, and you should see output indicating any detected issues.z
 
 Passing the information to the compiler or build system
 -------------------------------------------------------
-- 
2.51.0


From 9ef3092aa6dd092b1c1ae36f28753fb5703df312 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Fri, 22 Aug 2025 09:26:52 +0200
Subject: [PATCH 04/11] Sanitizer setting is optional

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 examples/dev_flow/sanitizers/compiler_sanitizers.rst | 5 +----
 1 file changed, 1 insertion(+), 4 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 0c758844264a8ebef2432975401aaa471021ddf1..28c050f3c660f5066f49d202730d3f985de04fff 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -50,7 +50,7 @@ them as a list of values. For example, with Clang, you might do the following:
 
     compiler:
       clang:
-        sanitizer: [None, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
+        sanitizer: [null, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
 
 Here you have modeled the use of ``-fsanitize=address``, ``-fsanitize=thread``,
 ``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``, ``-fsanitize=kernel-address``, the combination of ``-fsanitize=address`` with
@@ -63,9 +63,6 @@ For MSVC, the available sanitizers are more limited, and you can find the comple
 
 Note that not all sanitizer combinations are possible, for example, with Clang, you cannot use more than one of the Address, Thread, or Memory sanitizers in the same program.
 
-Be aware once ``setting_user.yml`` is present in your Conan home, it will affect all your projects using Conan, asking for the setting ``compiler.sanitizer`` always.
-In order to disable it, just remove the ``settings_user.yml`` file from your Conan home.
-
 Adding Sanitizers as Part of the Profile
 ########################################
 
-- 
2.51.0


From 057ca97b64b1a0b500540be7402933d88ce423fd Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Fri, 22 Aug 2025 11:54:07 +0200
Subject: [PATCH 05/11] Add toolchain and hook section

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 73 +++++++++++++++++--
 1 file changed, 65 insertions(+), 8 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 28c050f3c660f5066f49d202730d3f985de04fff..3fca65f5f3e14a86cff0b21bbf5feabe3a0681d7 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -84,7 +84,8 @@ This way, you can easily switch between different sanitizer configurations by us
     tools.build:exelinkflags=['-fsanitize=address']
 
 The Conan client is not capable to deduce the necessary flags from the settings and apply them during the build process.
-It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value.
+It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value
+as part of the compiler flags.
 
 Building Examples Using Sanitizers
 ----------------------------------
@@ -228,20 +229,76 @@ Once the project built successfully, you can run the example with the sanitizers
     conan build signed_integer_overflow/install
     ./build/signed_integer_overflow
 
-This should trigger the Address and Undefined Behavior Sanitizers, and you should see output indicating any detected issues.z
+This should trigger the Address and Undefined Behavior Sanitizers, and you should see output indicating any detected issues.
 
-Passing the information to the compiler or build system
--------------------------------------------------------
+.. code-block:: text
+
+    source signed_integer_overflow/install/conanrun.sh
+    signed_integer_overflow
+
+    Address sanitizer enabled
+    /root/.conan2/p/b/signe47ab122831752/b/main.cpp:13:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
+
+The output indicates that the Address Sanitizer is enabled and reports a runtime error due to signed integer overflow.
+
+Passing then Information to the Compiler or Build System
+--------------------------------------------------------
 
 Besides using Conan profiles to manage sanitizer settings, you can also use different approaches.
 
 Managing Sanitizer with CMake Toolchain
 #######################################
 
-**TODO**
+For those cases when a company or developer has a :ref:`custom CMake toolchain file <conan_cmake_user_toolchain>`
+to manage compiler and build options already, it can be used to pass the necessary flags to enable sanitizers
+instead of using profiles to configure extra compiler flags.
+
+For example, you can create a CMake toolchain file like this:
+
+.. code-block:: cmake
+    :caption: *cmake/my_toolchain.cmake*
+
+    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined")
+    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address,undefined")
+
+Then, you can specify this toolchain file as part of your Conan profile as well:
+
+.. code-block:: ini
+    :caption: *profiles/asan_ubsan*
+
+    include(default)
+
+    [settings]
+    compiler.sanitizer=AddressUndefinedBehavior
+
+    [conf]
+    tools.cmake.cmaketoolchain:user_toolchain=cmake/my_toolchain.cmake
+
+This way, you can keep your existing CMake toolchain file and still leverage Conan profiles to manage other settings.
+
+Managing Sanitizer with Conan Hooks
+###################################
+
+Another approach to manage sanitizers is by using :ref:`Conan hooks <reference_extensions_hooks>`.
+Using hooks, you can inject compiler flags on-the-fly during the build process,
+allowing for more dynamic configurations without modifying the original build files.
+
+For instance, we can add a ``pre_build`` hook to append the necessary sanitizer flags based on the
+``compiler.sanitizer`` setting.
 
+.. code-block:: python
+    :caption: ~/.conan2/extentions/hooks/hook_sanitizer_flags.py
 
-Mananaging Sanitizer with Conan Hooks
-#####################################
+    def pre_generate(conanfile):
+        if conanfile.settings.get_safe("compiler.sanitizer"):
+            sanitizer = {"Address": "address", "UndefinedBehavior": "undefined"}
+            if conanfile.settings.compiler.sanitizer in sanitizer:
+                flag = f"-fsanitize={sanitizer[conanfile.settings.compiler.sanitizer]}"
+                conanfile.conf.append("tools.build:cflags", flag)
+                conanfile.conf.append("tools.build:cxxflags", flag)
+                conanfile.conf.append("tools.build:exelinkflags", flag)
 
-**TODO**
\ No newline at end of file
+The ``pre_generate`` hook is executed before Conan generates toolchain files, being able to consume
+the respective configuration for the compiler flags. This approach allows for more dynamic configurations
+as it's possible to run a Python script, but it also increase the maintainance complexity as it keeps the
+logic out for the profile management.
-- 
2.51.0


From 14dfdcfe59c721ad5306402bf1a55ff27d698b28 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Fri, 22 Aug 2025 15:04:03 +0200
Subject: [PATCH 06/11] Improve description

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 458 ++++++++++--------
 1 file changed, 255 insertions(+), 203 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 3fca65f5f3e14a86cff0b21bbf5feabe3a0681d7..14a582d6a0c0f04a82c57b6e80150f4c616955f9 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -1,3 +1,5 @@
+### Compiler sanitizers
+
 .. _examples_dev_flow_sanitizers_compiler_sanitizers:
 
 Compiler sanitizers
@@ -5,300 +7,350 @@ Compiler sanitizers
 
 .. warning::
 
-    Using sanitizers in production with suid binaries is dangerous, as the libsanitizer runtime
-    relies on environment variables that could enable privilege escalation attacks.
-    Use sanitizers only in development and testing environments.
-
-Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, memory leaks,
-dangling pointers, and various types of undefined behavior.
+   Using sanitizers in production, particularly with SUID binaries, is dangerous. The libsanitizer
+   runtimes rely on environment variables that could enable privilege escalation attacks.
+   Use sanitizers only in development and testing environments.
 
-Compilers such as GCC, Clang and MSVC support these tools through specific compiler and linker flags.
+Sanitizers are powerful tools for detecting runtime bugs like buffer overflows, data races, memory leaks,
+dangling pointers, use-of-uninitialized memory, and various types of undefined behavior. Compilers such as
+GCC, Clang, and MSVC support these tools through specific compiler and linker flags.
 
-This example explains a recommended approach for integrating compiler sanitizers into your Conan 2.x workflow.
+This document explains recommended approaches for integrating compiler sanitizers into your Conan 2.x workflow.
 
-Modeling and Applying Sanitizers using Settings
-------------------------------------------------
+Modeling and applying sanitizers using settings
+-----------------------------------------------
 
-If you want to model the sanitizer options so that the package id is affected by them, you have to
-:ref:`customize new compiler sub-settings<reference_config_files_customizing_settings>`. You should not need
-modify ``settings.yml`` directly, but adding :ref:`the settings_user.yml <examples_config_files_settings_user>`
-instead.
+If you want to model sanitizer options so that the package ID is affected by them, you can
+:ref:`customize new compiler sub-settings <reference_config_files_customizing_settings>`. You should not need
+to modify ``settings.yml`` directly; instead add :ref:`the settings_user.yml <examples_config_files_settings_user>`.
 
-This approach is preferred because it ensures that enabling a sanitizer alters the package ID, allowing you to use the same
-binary package with or without sanitizers, which is ideal for development and debugging workflows.
+This approach is preferred because enabling a sanitizer alters the package ID, allowing you to build and use
+the same binary package with or without sanitizers. This is ideal for development and debugging workflows.
 
-To better illustrate this, please, first clone the sources to recreate this project. You can find them in the
-`examples2 repository <https://github.com/conan-io/examples2>`_ in GitHub:
+To better illustrate this, please clone the sources to recreate this project. You can find them in the
+`examples2 repository <https://github.com/conan-io/examples2>`_ on GitHub:
 
 .. code-block:: bash
 
-    $ git clone https://github.com/conan-io/examples2.git
-    $ cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers
-
-In this example we are going to see how to prepare Conan to use sanitizers in different ways.
+   git clone https://github.com/conan-io/examples2.git
+   cd examples2/examples/dev_flow/sanitizers/compiler_sanitizers
 
+In this example we will see how to prepare Conan to use sanitizers in different ways.
 
-Configuring Sanitizers as Part of Settings
-##########################################
+Configuring sanitizers as part of settings
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
 If you typically use a specific set of sanitizers or combinations for your builds, you can specify
-them as a list of values. For example, with Clang, you might do the following:
+a sub-setting as a list of values in your ``settings_user.yml``. For example, for Clang:
 
 .. code-block:: yaml
-    :caption: *settings_user.yml*
-    :emphasize-lines: 3
+   :caption: settings_user.yml
+   :emphasize-lines: 3
 
-    compiler:
-      clang:
-        sanitizer: [null, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
+   compiler:
+     clang:
+       sanitizer: [null, Address, Leak, Thread, Memory, UndefinedBehavior, HardwareAssistanceAddress, KernelAddress, AddressUndefinedBehavior, ThreadUndefinedBehavior]
 
-Here you have modeled the use of ``-fsanitize=address``, ``-fsanitize=thread``,
-``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``, ``-fsanitize=kernel-address``, the combination of ``-fsanitize=address`` with
-``-fsanitize=undefined`` and ``-fsanitize=thread`` with ``-fsanitize=undefined``.
+This example defines a few common sanitizers. You can add any sanitizer your compiler supports.
+The ``null`` value represents a build without sanitizers. The above models the use of ``-fsanitize=address``,
+``-fsanitize=thread``, ``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``,
+``-fsanitize=kernel-address``, as well as combinations like ``-fsanitize=address,undefined`` and ``-fsanitize=thread,undefined``.
 
-It seems be a large number of options, but for Clang, these are only a portion.
-To obtain the complete list of available sanitizers, you can refer to the `Clang documentation <https://clang.llvm.org/docs/>`_.
-The GCC supports a similar number of sanitizers, and you can find the complete list in the `GCC documentation <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
-For MSVC, the available sanitizers are more limited, and you can find the complete list in the `MSVC documentation <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.
+It may seem like a large number of options, but for Clang, these are only a portion. To obtain the complete list,
+refer to:
 
-Note that not all sanitizer combinations are possible, for example, with Clang, you cannot use more than one of the Address, Thread, or Memory sanitizers in the same program.
+* Clang: `AddressSanitizer <https://clang.llvm.org/docs/AddressSanitizer.html>`_,
+  `ThreadSanitizer <https://clang.llvm.org/docs/ThreadSanitizer.html>`_,
+  `MemorySanitizer <https://clang.llvm.org/docs/MemorySanitizer.html>`_,
+  `UndefinedBehaviorSanitizer <https://clang.llvm.org/docs/UndefinedBehaviorSanitizer.html>`_.
+* GCC: `Instrumentation Options <https://gcc.gnu.org/onlinedocs/gcc/Instrumentation-Options.html>`_.
+* MSVC: `MSVC Sanitizers <https://learn.microsoft.com/en-us/cpp/sanitizers/>`_.
 
-Adding Sanitizers as Part of the Profile
-########################################
+**Notes on combinations**:
 
-An option would be to add the sanitizer values as part of the profile.
-This way, you can easily switch between different sanitizer configurations by using different dedicated profiles.
+* AddressSanitizer (ASan), ThreadSanitizer (TSan), and MemorySanitizer (MSan) are mutually exclusive with one another.
+* Address + UndefinedBehavior (UBSan) is a common and supported combination.
+* Thread + UndefinedBehavior is also supported.
+* MemorySanitizer often requires special flags such as ``-O1``, ``-fno-omit-frame-pointer`` and fully-instrumented dependencies.
 
-.. code-block:: ini
-    :caption: *~/.conan/profiles/asan*
-    :emphasize-lines: 7
-
-    include(default)
+Adding sanitizers as part of the profile
+----------------------------------------
 
-    [settings]
-    compiler.sanitizer=Address
+Another option is to add the sanitizer values as part of a profile. This way, you can easily switch between
+different configurations by using dedicated profiles.
 
-    [conf]
-    tools.build:cflags=['-fsanitize=address']
-    tools.build:cxxflags=['-fsanitize=address']
-    tools.build:exelinkflags=['-fsanitize=address']
+.. code-block:: ini
+   :caption: compiler_sanitizers/profiles/asan
 
-The Conan client is not capable to deduce the necessary flags from the settings and apply them during the build process.
-It's necessary to pass those expected sanitizer flags according to the setting ``compiler.sanitizer`` value
-as part of the compiler flags.
+   include(default)
 
-Building Examples Using Sanitizers
-----------------------------------
+   [settings]
+   build_type=Debug
+   compiler.sanitizer=Address
 
-To show how to use sanitizers in your builds, let's consider a couple of examples.
+   [conf]
+   tools.build:cflags+=["-fsanitize=address", "-fno-omit-frame-pointer"]
+   tools.build:cxxflags+=["-fsanitize=address", "-fno-omit-frame-pointer"]
+   tools.build:exelinkflags+=["-fsanitize=address"]
+   tools.build:sharedlinkflags+=["-fsanitize=address"]
 
-Address Sanitizer: Index Out of Bounds
-######################################
+   [runenv]
+   ASAN_OPTIONS="halt_on_error=1:detect_leaks=1"
 
-In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds
-index in an array, which should trigger the Address Sanitizer when running the program.
+For Visual Studio (MSVC) we can obtain an equivalent profile for AddressSanitizer:
 
-The following code demonstrates this:
+.. code-block:: ini
+   :caption: ~/.conan/profiles/asan
 
-.. code-block:: cpp
-    :caption: *index_out_of_bounds/main.cpp*
-    :emphasize-lines: 11
+   include(default)
 
-    #include <iostream>
-    #include <cstdlib>
+   [settings]
+   build_type=Debug
+   compiler.sanitizer=Address
 
-    int main() {
-        #ifdef __SANITIZE_ADDRESS__
-            std::cout << "Address sanitizer enabled\n";
-        #else
-            std::cout << "Address sanitizer not enabled\n";
-        #endif
+   [conf]
+   tools.build:cxxflags+=["/fsanitize=address", "/Zi"]
+   tools.build:exelinkflags+=["/fsanitize=address"]
 
-        int foo[100];
-        foo[100] = 42; // Out-of-bounds write
+The Conan client is not capable of deducing the necessary flags from the settings and applying them automatically
+during the build process. It is necessary to pass the expected sanitizer flags according to the
+``compiler.sanitizer`` value as part of the compiler and linker flags.
+Conan's built-in toolchains (like ``CMakeToolchain`` and ``MesonToolchain``) will automatically
+pick up the flags defined in the ``[conf]`` section and apply them to the build.
 
-        return EXIT_SUCCESS;
-    }
 
-The definition ``__SANITIZE_ADDRESS__`` is used to check if the Address Sanitizer is enabled when
-running the produced application. It's supported by GCC, Clang and MSVC compilers.
+Building examples using sanitizers
+----------------------------------
 
-To build this example, you can use Conan to invoke CMake and perform the build.
+To show how to use sanitizers in your builds, let's consider two examples.
 
-.. code-block:: bash
+.. note::
 
-    conan export index_out_of_bounds/
-    conan install --requires=index_out_of_bounds/0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing
+   To build your project with a sanitizer, simply use the corresponding profile.
+   It is crucial to **rebuild all dependencies from source** to ensure they are also instrumented,
+   which prevents false positives and other issues.
 
+AddressSanitizer: index out of bounds
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
-Here we are using Conan to export the recipe and build the project.
-The profile file `profiles/asan` was demonstrated already and will merge with the default profile
-from your configuration. The resulting build will produce an executable in a specific package folder,
-in order to access it, you can use the script produced by the ``VirtualRunEnv`` generator,
-then run the executable:
+In this example, we will build a simple C++ program that intentionally accesses an out-of-bounds index
+in an array, which should trigger ASan when running the program.
 
-.. code-block:: text
+.. code-block:: cpp
+   :caption: index_out_of_bounds/main.cpp
+   :emphasize-lines: 11
 
-    source index_out_of_bounds/install/conanrun.sh
-    index_out_of_bounds
+   #include <iostream>
+   #include <cstdlib>
 
-    Address sanitizer enabled
-    =================================================================
-    ==32018==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbe04a6d0 at pc 0x5dad4506e2eb bp 0x7fffbe04a500 sp 0x7fffbe04a4f0
-    WRITE of size 4 at 0x7fffbe04a6d0 thread T0
-        #0 0x5dad4506e2ea in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea)
-        #1 0x731331629d8f in __libc_start_call_main ../sysdeps/nptl/libc_start_call_main.h:58
-        #2 0x731331629e3f in __libc_start_main_impl ../csu/libc-start.c:392
-        #3 0x5dad4506e3d4 in _start (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x13d4)
+   int main() {
+   #ifdef __SANITIZE_ADDRESS__
+     std::cout << "Address sanitizer enabled\n";
+   #else
+     std::cout << "Address sanitizer not enabled\n";
+   #endif
 
-    Address 0x7fffbe04a6d0 is located in stack of thread T0 at offset 448 in frame
-        #0 0x5dad4506e1ef in main (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x11ef)
+     int foo[100];
+     foo[100] = 42; // Out-of-bounds write
 
-    This frame has 1 object(s):
-        [48, 448) 'foo' (line 11) <== Memory access at offset 448 overflows this variable
-    HINT: this may be a false positive if your program uses some custom stack unwind mechanism, swapcontext or vfork
-        (longjmp and C++ exceptions *are* supported)
-    SUMMARY: AddressSanitizer: stack-buffer-overflow (.../examples2/examples/dev_flow/sanitizers/compiler_sanitizers/index_out_of_bounds/build/Debug/index_out_of_bounds+0x12ea) in main
+     return EXIT_SUCCESS;
+   }
 
-Once running the example, you should see an error message from the Address Sanitizer indicating the
-out-of-bounds. The message is simplified here, but it provides useful information about the error,
-including the expected index of bounds error.
+**Note:** The preprocessor check above is portable for GCC, Clang and MSVC.
+The define ``__SANITIZE_ADDRESS__`` is present when ASan is active;
 
+**To build and run this example using Conan:**
 
-Undefined Sanitizer: Signed Integer Overflow
-############################################
+.. code-block:: bash
 
-This example demonstrates how to use the Undefined Behavior Sanitizer to detect signed integer overflow.
-It combines the usage of two sanitizers at same time: Address Sanitizer and Undefined Behavior Sanitizer.
-For this example, we will be using the following Conan profile:
+   conan export index_out_of_bounds/
+   conan install --requires=index_out_of_bounds/0.1.0 -pr profiles/asan -of index_out_of_bounds/install --build=missing
+   # Activate run environment to ensure sanitizer runtime and paths are set
+   source index_out_of_bounds/install/conanrun.sh
+   index_out_of_bounds
 
-.. code-block:: ini
-    :caption: *~/.conan/profiles/asan_ubsan*
-    :emphasize-lines: 7
+**Expected output (abbreviated):**
 
-    include(default)
+.. code-block:: text
 
-    [settings]
-    compiler.sanitizer=AddressUndefinedBehavior
+   Address sanitizer enabled
+   ==32018==ERROR: AddressSanitizer: stack-buffer-overflow on address 0x7fffbe04a6d0 ...
+   WRITE of size 4 at 0x7fffbe04a6d0 thread T0
+   #0 ... in main .../index_out_of_bounds+0x12ea
+   ...
+   SUMMARY: AddressSanitizer: stack-buffer-overflow ... in main
+   This frame has 1 object(s):
+   [48, 448) 'foo' (line 11) <== Memory access at offset 448 overflows this variable
 
-    [conf]
-    tools.build:cflags=['-fsanitize=address,undefined']
-    tools.build:cxxflags=['-fsanitize=address,undefined']
-    tools.build:exelinkflags=['-fsanitize=address,undefined']
+UndefinedBehaviorSanitizer: signed integer overflow
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
-It's important to mention it only works for GCC and Clang compilers,
-as MSVC does not support the Undefined Behavior Sanitizer yet.
+This example demonstrates how to use UBSan to detect signed integer overflow. It combines ASan and UBSan.
+Create a dedicated profile:
 
-The source code for this example is as follows:
+.. code-block:: ini
+   :caption: ~/.conan/profiles/asan_ubsan
+   :emphasize-lines: 7
 
-.. code-block:: cpp
-    :caption: *signed_integer_overflow/main.cpp*
-    :emphasize-lines: 12
+   include(default)
 
-    #include <iostream>
-    #include <cstdlib>
-    #include <cstdint>
+   [settings]
+   build_type=Debug
+   compiler.sanitizer=AddressUndefinedBehavior
 
-    int main(int argc, char* argv[]) {
-        #ifdef __SANITIZE_ADDRESS__
-            std::cout << "Address sanitizer enabled\n";
-        #else
-            std::cout << "Address sanitizer not enabled\n";
-        #endif
+   [conf]
+   tools.build:cflags+=["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
+   tools.build:cxxflags+=["-fsanitize=address,undefined", "-fno-omit-frame-pointer"]
+   tools.build:exelinkflags+=["-fsanitize=address,undefined"]
+   tools.build:sharedlinkflags+=["-fsanitize=address,undefined"]
 
-        int foo = 0x7fffffff;
-        foo += argc; // Signed integer overflow
+It is supported by GCC and Clang. MSVC does not support UBSan.
 
-        return EXIT_SUCCESS;
-    }
+**Source code:**
 
-In this example, it's intentionally causing a signed integer overflow by adding the command line argument count to a large integer value.
+.. code-block:: cpp
+   :caption: signed_integer_overflow/main.cpp
+   :emphasize-lines: 14
 
-As next step, the code can be built using Conan and CMake, similar to the previous example:
+   #include <iostream>
+   #include <cstdlib>
+   #include <climits>
 
-.. code-block:: bash
+   int main() {
+   #ifdef __SANITIZE_ADDRESS__
+     std::cout << "Address sanitizer enabled\n";
+   #else
+     std::cout << "Address sanitizer not enabled\n";
+   #endif
 
-    conan export signed_integer_overflow/
-    conan install --requires=signed_integer_overflow/0.1.0 -pr profiles/asan -of signed_integer_overflow/install --build=missing
+     int x = INT_MAX;
+     x += 42;                     // signed integer overflow
 
+     return EXIT_SUCCESS;
+   }
 
-Once the project built successfully, you can run the example with the sanitizers enabled:
+**Build and run:**
 
 .. code-block:: bash
 
-    conan build signed_integer_overflow/install
-    ./build/signed_integer_overflow
+   conan export signed_integer_overflow/
+   conan install --requires=signed_integer_overflow/0.1.0 -pr profiles/asan_ubsan -of signed_integer_overflow/install --build=missing
+   source signed_integer_overflow/install/conanrun.sh
+   signed_integer_overflow
 
-This should trigger the Address and Undefined Behavior Sanitizers, and you should see output indicating any detected issues.
+**Expected output (abbreviated):**
 
 .. code-block:: text
 
-    source signed_integer_overflow/install/conanrun.sh
-    signed_integer_overflow
-
-    Address sanitizer enabled
-    /root/.conan2/p/b/signe47ab122831752/b/main.cpp:13:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
-
-The output indicates that the Address Sanitizer is enabled and reports a runtime error due to signed integer overflow.
-
-Passing then Information to the Compiler or Build System
---------------------------------------------------------
+   Address sanitizer enabled
+   .../main.cpp:16:9: runtime error: signed integer overflow: 2147483647 + 1 cannot be represented in type 'int'
 
-Besides using Conan profiles to manage sanitizer settings, you can also use different approaches.
+Passing the information to the compiler or build system
+-------------------------------------------------------
 
-Managing Sanitizer with CMake Toolchain
-#######################################
+Besides using Conan profiles to manage sanitizer settings, you can also use other approaches.
 
-For those cases when a company or developer has a :ref:`custom CMake toolchain file <conan_cmake_user_toolchain>`
-to manage compiler and build options already, it can be used to pass the necessary flags to enable sanitizers
-instead of using profiles to configure extra compiler flags.
+Managing sanitizers with a CMake toolchain
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
-For example, you can create a CMake toolchain file like this:
+If you already have a :ref:`custom CMake toolchain file <conan_cmake_user_toolchain>` to manage compiler
+and build options, you can pass the necessary flags to enable sanitizers there instead of profiles.
 
 .. code-block:: cmake
-    :caption: *cmake/my_toolchain.cmake*
+   :caption: cmake/my_toolchain.cmake
 
-    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined")
-    set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address,undefined")
+   # Apply to all targets; consider per-target options for finer control
+   set(CMAKE_C_FLAGS "${CMAKE_C_FLAGS} -fsanitize=address,undefined -fno-omit-frame-pointer")
+   set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -fsanitize=address,undefined -fno-omit-frame-pointer")
+   set(CMAKE_EXE_LINKER_FLAGS "${CMAKE_EXE_LINKER_FLAGS} -fsanitize=address,undefined")
+   set(CMAKE_SHARED_LINKER_FLAGS "${CMAKE_SHARED_LINKER_FLAGS} -fsanitize=address,undefined")
 
-Then, you can specify this toolchain file as part of your Conan profile as well:
+Then, specify this toolchain file as part of your Conan profile:
 
 .. code-block:: ini
-    :caption: *profiles/asan_ubsan*
+   :caption: profiles/asan_ubsan
 
-    include(default)
+   include(default)
 
-    [settings]
-    compiler.sanitizer=AddressUndefinedBehavior
+   [settings]
+   build_type=Debug
+   compiler.sanitizer=AddressUndefinedBehavior
 
-    [conf]
-    tools.cmake.cmaketoolchain:user_toolchain=cmake/my_toolchain.cmake
+   [conf]
+   tools.cmake.cmaketoolchain:user_toolchain=cmake/my_toolchain.cmake
 
 This way, you can keep your existing CMake toolchain file and still leverage Conan profiles to manage other settings.
 
-Managing Sanitizer with Conan Hooks
-###################################
+Managing sanitizers with Conan hooks
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
 
-Another approach to manage sanitizers is by using :ref:`Conan hooks <reference_extensions_hooks>`.
-Using hooks, you can inject compiler flags on-the-fly during the build process,
-allowing for more dynamic configurations without modifying the original build files.
+Another approach is using :ref:`Conan hooks <reference_extensions_hooks>`. With hooks, you can inject compiler
+flags on-the-fly during the build process, allowing for dynamic configurations without modifying the original
+build files.
 
-For instance, we can add a ``pre_build`` hook to append the necessary sanitizer flags based on the
-``compiler.sanitizer`` setting.
+For instance, add a ``pre_generate`` hook to append the necessary sanitizer flags based on the
+``compiler.sanitizer`` setting:
 
 .. code-block:: python
-    :caption: ~/.conan2/extentions/hooks/hook_sanitizer_flags.py
-
-    def pre_generate(conanfile):
-        if conanfile.settings.get_safe("compiler.sanitizer"):
-            sanitizer = {"Address": "address", "UndefinedBehavior": "undefined"}
-            if conanfile.settings.compiler.sanitizer in sanitizer:
-                flag = f"-fsanitize={sanitizer[conanfile.settings.compiler.sanitizer]}"
-                conanfile.conf.append("tools.build:cflags", flag)
-                conanfile.conf.append("tools.build:cxxflags", flag)
-                conanfile.conf.append("tools.build:exelinkflags", flag)
-
-The ``pre_generate`` hook is executed before Conan generates toolchain files, being able to consume
-the respective configuration for the compiler flags. This approach allows for more dynamic configurations
-as it's possible to run a Python script, but it also increase the maintainance complexity as it keeps the
-logic out for the profile management.
+   :caption: ~/.conan2/extensions/hooks/hook_sanitizer_flags.py
+
+   def pre_generate(conanfile):
+       sani = conanfile.settings.get_safe("compiler.sanitizer")
+       if not sani or sani == "null":
+           return
+       mapping = {
+           "Address": "address",
+           "Leak": "leak",
+           "Thread": "thread",
+           "Memory": "memory",
+           "UndefinedBehavior": "undefined",
+           "HardwareAssistanceAddress": "hwaddress",
+           "KernelAddress": "kernel-address",
+           "AddressUndefinedBehavior": "address,undefined",
+           "ThreadUndefinedBehavior": "thread,undefined",
+       }
+       fs = mapping.get(sani)
+       if not fs:
+           return
+       flag = f"-fsanitize={fs}"
+       for k in ("tools.build:cflags", "tools.build:cxxflags",
+                 "tools.build:exelinkflags", "tools.build:sharedlinkflags"):
+           conanfile.conf.append(k, flag)
+       # Optional: better stack traces
+       conanfile.conf.append("tools.build:cxxflags", "-fno-omit-frame-pointer")
+
+The ``pre_generate`` hook is executed before Conan generates toolchain files, so it can contribute to the final
+configuration for compiler and linker flags. This approach is flexible, but can increase maintenance complexity
+as it moves logic out of profile management.
+
+Additional recommendations
+--------------------------
+
+* Debug info and optimization:
+
+  * For ASan/TSan, ``-O1`` or ``-O2`` generally works; for MSan, prefer ``-O1`` and avoid aggressive inlining.
+  * ``-fno-omit-frame-pointer`` helps stack traces.
+
+* Runtime symbolization:
+
+  * Useful settings for CI:
+
+    * ``ASAN_OPTIONS=halt_on_error=1:detect_leaks=1:log_path=asan``.
+    * ``UBSAN_OPTIONS=print_stacktrace=1:halt_on_error=1:log_path=ubsan``.
+
+* Suppressions:
+
+  * For ASan: ``ASAN_OPTIONS=suppressions=asan.supp``.
+  * For UBSan: ``UBSAN_OPTIONS=suppressions=ubsan.supp``.
+  * Keep suppressions under version control and load them in CI jobs.
+
+* Third-party dependencies:
+
+  * Mixed instrumented/uninstrumented code can lead to false positives or crashes, especially with MSan.
+  * Prefer building dependencies with the same sanitizer or limit sanitizers to leaf applications.
+
+* MSVC and Windows notes:
+
+  * ASan with MSVC/Clang-cl uses ``/fsanitize=address`` and PDBs via ``/Zi``. Not supported for 32-bit targets.
+  * KAsan requires Windows 11.
+  * Some features are limited when using whole program optimization (``/GL``) or certain runtime libraries.
-- 
2.51.0


From 2abb246d9d6ff96331b3f31fb27fcf92433bfd35 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianries@gmail.com>
Date: Wed, 1 Oct 2025 12:49:19 +0200
Subject: [PATCH 07/11] Remove unsed header.

Co-authored-by: Carlos Zoido <mrgalleta@gmail.com>
Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 examples/dev_flow/sanitizers/compiler_sanitizers.rst | 2 --
 1 file changed, 2 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 14a582d6a0c0f04a82c57b6e80150f4c616955f9..c1e4513feefbf3472cb740f35fa8635486b8953c 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -1,5 +1,3 @@
-### Compiler sanitizers
-
 .. _examples_dev_flow_sanitizers_compiler_sanitizers:
 
 Compiler sanitizers
-- 
2.51.0


From 19954284cdc49241647ef737bca92f828a6e34c0 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianries@gmail.com>
Date: Wed, 1 Oct 2025 13:49:15 +0200
Subject: [PATCH 08/11] Update sanitizers warning

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 examples/dev_flow/sanitizers/compiler_sanitizers.rst | 4 +++-
 1 file changed, 3 insertions(+), 1 deletion(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index c1e4513feefbf3472cb740f35fa8635486b8953c..5aca1a985a3a30211480c436c146e3fb24332fc1 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -5,7 +5,9 @@ Compiler sanitizers
 
 .. warning::
 
-   Using sanitizers in production, particularly with SUID binaries, is dangerous. The libsanitizer
+   Using sanitizers in production, especially with programs that run with elevated privileges (for example, SUID binaries on Linux), is dangerous.
+   The sanitizer runtime libraries depend on environment variables, which could allow privilege escalation attacks.
+   Use sanitizers only in development and testing environments.
    runtimes rely on environment variables that could enable privilege escalation attacks.
    Use sanitizers only in development and testing environments.
 
-- 
2.51.0


From 4a7bef9163f828c1a4203a201d77f4445cf2cdff Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianries@gmail.com>
Date: Wed, 1 Oct 2025 13:50:13 +0200
Subject: [PATCH 09/11] Improve document description

Co-authored-by: Carlos Zoido <mrgalleta@gmail.com>
Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 examples/dev_flow/sanitizers/compiler_sanitizers.rst | 2 +-
 1 file changed, 1 insertion(+), 1 deletion(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 5aca1a985a3a30211480c436c146e3fb24332fc1..45afba9d54e0af72e652aff1cbe37073ce75cce3 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -15,7 +15,7 @@ Sanitizers are powerful tools for detecting runtime bugs like buffer overflows,
 dangling pointers, use-of-uninitialized memory, and various types of undefined behavior. Compilers such as
 GCC, Clang, and MSVC support these tools through specific compiler and linker flags.
 
-This document explains recommended approaches for integrating compiler sanitizers into your Conan 2.x workflow.
+This page explains recommended approaches for integrating compiler sanitizers into your workflow with Conan.
 
 Modeling and applying sanitizers using settings
 -----------------------------------------------
-- 
2.51.0


From bcb5eec599d6ea83a1837903f560f9a3235af7b1 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Thu, 2 Oct 2025 08:10:00 +0200
Subject: [PATCH 10/11] Remove Sanitizers with Conan hooks section

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 42 -------------------
 1 file changed, 42 deletions(-)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 45afba9d54e0af72e652aff1cbe37073ce75cce3..0bdc8a9dbc75c6bc3d6393a350c195e5eeb6dac1 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -281,48 +281,6 @@ Then, specify this toolchain file as part of your Conan profile:
 
 This way, you can keep your existing CMake toolchain file and still leverage Conan profiles to manage other settings.
 
-Managing sanitizers with Conan hooks
-^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
-
-Another approach is using :ref:`Conan hooks <reference_extensions_hooks>`. With hooks, you can inject compiler
-flags on-the-fly during the build process, allowing for dynamic configurations without modifying the original
-build files.
-
-For instance, add a ``pre_generate`` hook to append the necessary sanitizer flags based on the
-``compiler.sanitizer`` setting:
-
-.. code-block:: python
-   :caption: ~/.conan2/extensions/hooks/hook_sanitizer_flags.py
-
-   def pre_generate(conanfile):
-       sani = conanfile.settings.get_safe("compiler.sanitizer")
-       if not sani or sani == "null":
-           return
-       mapping = {
-           "Address": "address",
-           "Leak": "leak",
-           "Thread": "thread",
-           "Memory": "memory",
-           "UndefinedBehavior": "undefined",
-           "HardwareAssistanceAddress": "hwaddress",
-           "KernelAddress": "kernel-address",
-           "AddressUndefinedBehavior": "address,undefined",
-           "ThreadUndefinedBehavior": "thread,undefined",
-       }
-       fs = mapping.get(sani)
-       if not fs:
-           return
-       flag = f"-fsanitize={fs}"
-       for k in ("tools.build:cflags", "tools.build:cxxflags",
-                 "tools.build:exelinkflags", "tools.build:sharedlinkflags"):
-           conanfile.conf.append(k, flag)
-       # Optional: better stack traces
-       conanfile.conf.append("tools.build:cxxflags", "-fno-omit-frame-pointer")
-
-The ``pre_generate`` hook is executed before Conan generates toolchain files, so it can contribute to the final
-configuration for compiler and linker flags. This approach is flexible, but can increase maintenance complexity
-as it moves logic out of profile management.
-
 Additional recommendations
 --------------------------
 
-- 
2.51.0


From 607a8f206a3fd3bebb6b49aa133f11dbf0a97ba5 Mon Sep 17 00:00:00 2001
From: Uilian Ries <uilianr@jfrog.com>
Date: Thu, 2 Oct 2025 08:36:41 +0200
Subject: [PATCH 11/11] Add tables

Signed-off-by: Uilian Ries <uilianr@jfrog.com>
---
 .../sanitizers/compiler_sanitizers.rst        | 60 +++++++++++++++++++
 1 file changed, 60 insertions(+)

diff --git a/examples/dev_flow/sanitizers/compiler_sanitizers.rst b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
index 0bdc8a9dbc75c6bc3d6393a350c195e5eeb6dac1..cb7fcc47c56e71c0a1178e5235ccf5943ae581da 100644
--- a/examples/dev_flow/sanitizers/compiler_sanitizers.rst
+++ b/examples/dev_flow/sanitizers/compiler_sanitizers.rst
@@ -15,6 +15,34 @@ Sanitizers are powerful tools for detecting runtime bugs like buffer overflows,
 dangling pointers, use-of-uninitialized memory, and various types of undefined behavior. Compilers such as
 GCC, Clang, and MSVC support these tools through specific compiler and linker flags.
 
+Compiler Sanitizer Support Comparison
+-------------------------------------
+
+The following table summarizes the support for various sanitizers across different compilers:
+
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| Sanitizer                              | GCC | Clang | MSVC | Notes                                   |
++========================================+=====+=======+======+=========================================+
+| **AddressSanitizer (ASan)**            | ✅  | ✅    | ✅   | MSVC: Not supported for 32-bit targets  |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **ThreadSanitizer (TSan)**             | ✅  | ✅    | ❌   | Detects data races                      |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **MemorySanitizer (MSan)**             | ❌  | ✅    | ❌   | Clang-only, requires `-O1`              |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **UndefinedBehaviorSanitizer (UBSan)** | ✅  | ✅    | ❌   | Wide range of undefined behavior checks |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **LeakSanitizer (LSan)**               | ✅  | ✅    | ❌   | Often integrated with ASan              |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **HardwareAddressSanitizer (HWASan)**  | ❌  | ✅    | ❌   | ARM64 only, lower overhead than ASan    |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **KernelAddressSanitizer (KASan)**     | ✅  | ✅    | ✅   | MSVC: Requires Windows 11               |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **DataFlowSanitizer (DFSan)**          | ❌  | ✅    | ❌   | Dynamic data flow analysis              |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+| **Control Flow Integrity (CFI)**       | ❌  | ✅    | ✅   | MSVC: `/guard:cf`                       |
++----------------------------------------+-----+-------+------+-----------------------------------------+
+
+
 This page explains recommended approaches for integrating compiler sanitizers into your workflow with Conan.
 
 Modeling and applying sanitizers using settings
@@ -56,6 +84,38 @@ The ``null`` value represents a build without sanitizers. The above models the u
 ``-fsanitize=thread``, ``-fsanitize=memory``, ``-fsanitize=leak``, ``-fsanitize=undefined``, ``-fsanitize=hwaddress``,
 ``-fsanitize=kernel-address``, as well as combinations like ``-fsanitize=address,undefined`` and ``-fsanitize=thread,undefined``.
 
+Common Sanitizer Combinations
+^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
+
++-------------------+-----+-------+------+-----------------------------------------+
+| Combination       | GCC | Clang | MSVC | Compatibility                           |
++===================+=====+=======+======+=========================================+
+| **ASan + UBSan**  | ✅  | ✅    | ❌   | Most common combination                 |
++-------------------+-----+-------+------+-----------------------------------------+
+| **TSan + UBSan**  | ✅  | ✅    | ❌   | Good for multithreaded code             |
++-------------------+-----+-------+------+-----------------------------------------+
+| **ASan + LSan**   | ✅  | ✅    | ❌   | LSan often enabled by default with ASan |
++-------------------+-----+-------+------+-----------------------------------------+
+| **MSan + UBSan**  | ❌  | ✅    | ❌   | Requires careful dependency management  |
++-------------------+-----+-------+------+-----------------------------------------+
+
+Compiler-Specific Flags
+^^^^^^^^^^^^^^^^^^^^^^^
+
++-----------------------+------------------------+------------------------+----------------------+
+| Sanitizer             | GCC Flag               | Clang Flag             | MSVC Flag            |
++=======================+========================+========================+======================+
+| **AddressSanitizer**  | `-fsanitize=address`   | `-fsanitize=address`   | `/fsanitize=address` |
++-----------------------+------------------------+------------------------+----------------------+
+| **ThreadSanitizer**   | `-fsanitize=thread`    | `-fsanitize=thread`    | N/A                  |
++-----------------------+------------------------+------------------------+----------------------+
+| **MemorySanitizer**   | N/A                    | `-fsanitize=memory`    | N/A                  |
++-----------------------+------------------------+------------------------+----------------------+
+| **UndefinedBehavior** | `-fsanitize=undefined` | `-fsanitize=undefined` | N/A                  |
++-----------------------+------------------------+------------------------+----------------------+
+| **LeakSanitizer**     | `-fsanitize=leak`      | `-fsanitize=leak`      | N/A                  |
++-----------------------+------------------------+------------------------+----------------------+
+
 It may seem like a large number of options, but for Clang, these are only a portion. To obtain the complete list,
 refer to:
 
-- 
2.51.0

