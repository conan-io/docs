.. _deploy_generator:

deploy
======

The deploy generator makes a bulk copy of the packages folders of all dependencies in a graph. It can be used to deploy binaries from the
local cache to the user space:

.. code-block:: bash

    $ conan install openssl/1.0.2u@ -g deploy
    ...
    Installing package: openssl/1.0.2u
    ...
    Generator deploy created deploy_manifest.txt

Files from dependencies are deployed under a folder with the name of the dependency.

.. code-block:: bash

    $ ls -R
    openssl/  conanbuildinfo.txt  deploy_manifest.txt  zlib/

    ./openssl:
    LICENSE  include/  lib/

    ./openssl/include:
    openssl/

    ./openssl/include/openssl:
    aes.h       blowfish.h  cms.h       des_old.h  ebcdic.h  evp.h       md4.h      ocsp.h         pkcs12.h  ripemd.h     srtp.h   symhacks.h   whrlpool.h
    applink.c   bn.h        comp.h      dh.h       ec.h      hmac.h      md5.h      opensslconf.h  pkcs7.h   rsa.h        ssl.h    tls1.h       x509.h
    asn1.h      buffer.h    conf.h      dsa.h      ecdh.h    idea.h      mdc2.h     opensslv.h     pqueue.h  safestack.h  ssl2.h   ts.h         x509_vfy.h
    asn1_mac.h  camellia.h  conf_api.h  dso.h      ecdsa.h   krb5_asn.h  modes.h    ossl_typ.h     rand.h    seed.h       ssl23.h  txt_db.h     x509v3.h
    asn1t.h     cast.h      crypto.h    dtls1.h    engine.h  kssl.h      obj_mac.h  pem.h          rc2.h     sha.h        ssl3.h   ui.h
    bio.h       cmac.h      des.h       e_os2.h    err.h     lhash.h     objects.h  pem2.h         rc4.h     srp.h        stack.h  ui_compat.h

    ./openssl/lib:
    libeay32.lib  ssleay32.lib

    ./zlib:
    FindZLIB.cmake  include/  lib/  licenses/  zlib.pc

    ./zlib/include:
    zconf.h  zlib.h

    ./zlib/lib:
    pkgconfig/  zlib.lib

    ./zlib/lib/pkgconfig:
    zlib.pc

    ./zlib/licenses:
    LICENSE

The generated *deploy_manifest.txt* file is a manifest file with a list of all the files deployed and hash of the contents for each of them.

If any symbolic is present in the package folder, it will be preserved as well, and not copied as a new file.

.. tip::

    You can use the parameter :command:`--install-folder` in the :command:`conan install` to output the contents of the packages to a
    specific folder.