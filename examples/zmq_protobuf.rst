Getting started with ZMQ and Google Protocol Buffers (Protobuf)
===============================================================

ZeroMQ (ZMQ), also known as "Sockets on steroids" is a great C library for building distributed
applications. It is efficient, implements multiple communication paradigms, with very wide
adoption in production systems at scale.

Google Protocol Buffers (Protobuf) is a serialization framework, well known for being the one
that Google uses in their whole infraestructure. 

Here we will build a small client-server application with ZMQ (actually also using the ZMQCPP C++
binding) and Protobuf:

The source code
---------------

You can just clone the following example repository:

.. code-block:: bash

   $ git clone https://github.com/memsharded/example-zmqprotobuf.git

Or alternatively, manually create the folder and copy the following files inside:

.. code-block:: bash

   $ mkdir example-zmqprotobuf
   $ cd example-zmqprotobuf
   

The files are:

**server.cpp** is a small zmq server that continuously listens for incoming messages, which
must be a serialized person protobuf message, and prints it out on the console.

.. code-block:: cpp

   #include "zmq.hpp"
   #include <string>
   #include <iostream>
   #include "message.pb.h"
   #include <google/protobuf/text_format.h>
   
   int main () { 
       zmq::context_t context (1); //  Prepare our context and socket
       zmq::socket_t socket(context, ZMQ_PAIR);
       socket.bind ("tcp://*:5555");
   
       while (true) {
           zmq::message_t request;      
           socket.recv (&request); //  Wait for next request from client
           std::cout << "Received" << std::endl;
           tutorial::Person person;
           std::string msg_str(static_cast<char*>(request.data()), request.size());
           person.ParseFromString(msg_str);
           std::string text_str;
           google::protobuf::TextFormat::PrintToString(person, &text_str);
           std::cout << text_str << std::endl;
       }
       return 0;
   }
   
**client.cpp** is a zmq client that hardcodes a protobuf "person" message, sends it to
the server, and then finishes.

.. code-block:: cpp

   #include "zmq.hpp"
   #include "message.pb.h"
   #include <string>
   #include <iostream>
   
   int main (){
       GOOGLE_PROTOBUF_VERIFY_VERSION;
       
       tutorial::Person person;
       person.set_id(1234);
       person.set_name("john");
       person.set_email("john@mycompany.com");
       tutorial::Person::PhoneNumber* phone_number = person.add_phone();
       phone_number->set_number("1234567");
       phone_number->set_type(tutorial::Person::MOBILE);
       phone_number = person.add_phone();
       phone_number->set_number("7654321");
       phone_number->set_type(tutorial::Person::HOME);
         
       zmq::context_t context (1); //  Prepare our context and socket
       zmq::socket_t socket (context, ZMQ_PAIR);
   
       std::cout << "Connecting to hello world server…" << std::endl;
       socket.connect ("tcp://localhost:5555");
   
       std::string msg_str;
       person.SerializeToString(&msg_str);
      
       zmq::message_t request (msg_str.size());
       memcpy ((void *) request.data (), msg_str.c_str(), msg_str.size());
       std::cout << "Sending Person data ..." << std::endl;
       socket.send (request);
      
       // Optional:  Delete all global objects allocated by libprotobuf.
       google::protobuf::ShutdownProtobufLibrary();
       return 0;
   }
   
**message.proto** is the protobuf definition of the Person message, that has to be converted
to C++ source code with the ``protoc`` application.

.. code-block:: bash

   package tutorial;
   
      message Person {
        required string name = 1;
        required int32 id = 2;
        optional string email = 3;
      
        enum PhoneType {
          MOBILE = 0;
          HOME = 1;
          WORK = 2;
        }
      
        message PhoneNumber {
          required string number = 1;
          optional PhoneType type = 2 [default = HOME];
        }
      
        repeated PhoneNumber phone = 4;
      }
      
      message AddressBook {
        repeated Person person = 1;
      }
      

**CMakeLists.txt** is a simple cmake configuration to build both the client and the server, assuming
that ``protoc`` has already been invoked and has generated the ``message.pb.cc`` file.

.. code-block:: cmake

   project(MyHello)
   cmake_minimum_required(VERSION 3.0)
   
   include(conanbuildinfo.cmake)
   conan_basic_setup()
   
   add_library(message message.pb.cc)
   add_executable(client client.cpp)
   add_executable(server server.cpp)
   target_link_libraries(client message ${CONAN_LIBS})
   target_link_libraries(server message ${CONAN_LIBS})
   
         
Declaring and installing dependencies
-------------------------------------

If not created, then create also a ``conanfile.txt`` with the following content:

**conanfile.txt**

.. code-block:: text

   [requirements]
   zmqcpp/4.1.1@memsharded/testing
   Protobuf/2.6.1@memsharded/testing
   
   [generators]
   cmake
   
   [imports]
   bin, protoc* -> ./
   bin, *.dll -> ./bin


In this example, we will use cmake for building the project as indicated in ``[generators]``, but you
could use another build system too.

Also, we are instructing conan, in the ``[imports]`` section, to import/copy the ``protoc`` executable to
the project folder, so that it is very simple to run it to generate the C++ protobuf stubs from the ``message.proto`` file. 
We are also telling conan to bring all shared libraries to our local bin folder, inside our project, as a convenience
for running the examples.

This particular example is intended only for Win, but it will work exactly the same on other platforms.
It is just a matter of generating the packages. We will specify Visual Studio 12, and assume that our
default build is Release and the system arch is "x86_64" (no need to specify):


.. code-block:: bash

   $ conan install -s compiler="Visual Studio" -s compiler.version=12
   
.. note::

   These (zmq) packages currently work only with VS 12. If you manage to build them
   with VS 14 (2015) or other settings, please try to contribute with a pull request to the package
   repositories.

This command will download the binary packages required for your configuration, and it
will create a ``conanbuildinfo.cmake`` with the required information (some CMake variables, like
``CONAN_INCLUDE_DIRS`` and ``CONAN_LIBS``) for building your example.

Generating protobuf stubs
-------------------------
The above command, copied the ``protoc`` executable to our current folder.
Protobuf works by automatically generating code from the ``message.proto`` IDL file. Just type:

.. code-block:: bash

   $ protoc message.proto --cpp_out="."
   
And it will generate ``message.pb.h`` and ``message.pb.cc``

Building your example
---------------------

You are ready to build and run your project:

.. code-block:: bash

    $ mkdir build && cd build
    $ cmake .. -G "Visual Studio 12 Win64"
    $ cmake --build . --config Release

Now, you can go to your project's bin folder. First launch the server and then, in another
terminal, go to the same folder and launch the client.

Other configurations
--------------------
Now try to build other configurations yourself:

* Build the 32bits version. You should install a different package, and then use the ``Visual Studio 12`` cmake generator
* Build against the static ZMQ version. You can use the option ``-o ZMQ:static=True`` in the install command.
  Remember that, if the binary package is not available in any remote, conan will build it from source
  if you so indicate by entering the ``--build=ZMQ`` or ``--build=missing`` options.

Got any doubts? Please check out our :ref:`FAQ section <faq>` or |write_us|.


.. |write_us| raw:: html

   <a href="mailto:info@conan.io" target="_blank">write us</a>
