<a id="setting-up-conan-remotes"></a>

# Setting up a Conan remote

There are several options to set up a Conan repository:

**For private development:**

- [Artifactory Community Edition for C/C++](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html.md#artifactory-ce-cpp): Artifactory
  Community Edition (CE) for C/C++ is a completely free Artifactory server that implements
  both Conan and generic repositories. It is the recommended server for companies and
  teams wanting to host their own private repository. It has a web UI, advanced
  authentication and permissions, very good performance and scalability, a REST API, and
  can host generic artifacts (tarballs, zips, etc). Check [Artifactory Community Edition for C/C++](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/artifactory/artifactory_ce_cpp.html.md#artifactory-ce-cpp) for
  more information.
- [Conan server](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/conan_server.html.md#conan-server): Simple, free and open source, MIT
  licensed server that is part of the [conan-io organization](https://github.com/conan-io) project. Check
  [Setting up a Conan Server](https://docs.conan.io/2//tutorial/conan_repositories/setting_up_conan_remotes/conan_server.html.md#conan-server) for more information.

**Enterprise solutions:**

- **Artifactory Pro**: Artifactory is the binary repository manager for all major
  packaging formats. It is the recommended remote type for enterprise and professional
  package management. Check the [Artifactory Documentation](https://www.jfrog.com/confluence/display/JFROG/JFrog+Artifactory) for more
  information. For a comparison between Artifactory editions, check the [Artifactory
  Comparison Matrix](https://www.jfrog.com/confluence/display/JFROG/Artifactory+Comparison+Matrix).

#### SEE ALSO
- [JFrog Academy Conan 2 Essentials Module 2, Lesson 13: Working with Conan Repositories](https://academy.jfrog.com/path/conan-cc-package-manager/conan-2-essentials-module-2-package-creation-and-uploading?utm_source=Conan+Docs)
