.. _devops_consuming_conan_center:

Using ConanCenter packages in production environments
=====================================================

ConanCenter is a fantastic resource that contains reference implementations of 
recipes for over 1500 libraries and applications contributed by the community. 
As such, it is a great knowledge base on how to create and build Conan packages 
for open source dependencies.

ConanCenter also builds and provides binary packages for a wide range of 
configurations: multiple operating systems (Windows, Linux, macOS), compilers, 
compiler versions, and library variants (shared, static). On top of this, 
for a lot of libraries community contributors ensure that recipes are compatible 
for additional operating systems (Android, iOS, FreeBSD, QNX) and CPU architectures. 
The recipes in Conan Center are the greatest example of Conan’s universality promise.

Unlike other package managers or repositories, ConanCenter does not maintain a 
fixed snapshot of versions. On the contrary, for a given library (e.g. OpenCV), 
multiple versions are actively maintained at the same time. This gives users 
greater control of which versions to use, rather than having to remain fixed 
to an older version, or pushing them to always be on the latest version.

In order to support this ecosystem, ConanCenter recipes are updated very 
frequently. Recipes themselves may be updated to support a new platform, 
bug fixes, or to require newer versions of their dependencies. 
On the other hand, each user of ConanCenter may have a different combination 
of versions in their requirements. This means that given the same input 
list of requirements, Conan may resolve the graph differently at different 
points in time - resolving to different recipe revisions, versions, or packages. 
This is similar to the default behavior of package managers in other languages 
(pip/PyPi, npm, cargo, etc). In production environments where reproducibility 
is important, it is therefore discouraged to depend directly on Conan Center 
in an unconstrained manner.

The following guidelines contain a series of recommendations to ensure repeatability,
reliability, compliance and, where applicable, control to enable customization.
As a summary, it is highly recommended to follow these approaches when using packages from ConanCenter:

- Lock the versions and revisions you depend on using :ref:`lockfiles<tutorial_versioning_lockfiles>`
- Host your own copy of ConanCenter recipes and package binaries :ref:`in a server under your control <devops_conancenter_hosting_your_own_conancenter_fork>`

Repeatability and reproducibility
---------------------------------
As mentioned earlier - given a set of requirements, changes in ConanCenter 
can cause the Conan dependency solver to resolve different graphs over time. 
This does not only apply to the actual versions of libraries (e.g. ``opencv/4.5.0`` 
instead ``opencv/4.2.1``) - but also the recipes themselves. That is, 
there may exist multiple revisions of the ``opencv/4.5.0`` recipe, which can 
have side effects for consumers. Changes in recipes typically address a problem 
(bugfixes), target functionality (e.g. adding a conditional option, support for 
a new platform), or change versions of dependencies.

In order to ensure repeatability, the use of lockfiles on the consumer side 
is greatly encouraged: please check :ref:`the lockfile docs<tutorial_versioning_lockfiles>` 
for more information.

Lockfiles ensure that Conan will resolve the same graph in a repeatable and 
consistent manner - thus making sure the same versions are used across multiple 
systems (CI, developers, etc). 

Lockfiles are also used in other package managers like Python pip, Rust Cargo, npm -
these recommendations are in line with the practices of these other technologies.

Additionally, it is highly recommended to host your recipes and packages in your
own server (see below). Both of these approaches help you achieve having control 
on when upstream changes from ConanCenter are propagated across your team and systems.


Service reliability
-------------------
Consuming recipes and packages from the ConanCenter remote can be impacted during 
periods of downtime (scheduled or otherwise). While every effort is made to ensure 
that the ConanCenter is always available, and unscheduled downtime is rare and 
treated with urgency - this can impact users that depend on ConanCenter directly. 
Additionally, when building recipes from source, this requires retrieving the source 
packages (typically zip or tar files) from remote servers outside of the control of 
ConanCenter. Occasionally, these too can suffer from unscheduled downtime.

In enterprise production environments with strong uptime is required, it is strongly 
recommended to host recipes and binary packages in a server under your control. 

- Read more: :ref:`creating and hosting your own Conan Center binaries <devops_conancenter_hosting_your_own_conancenter_fork>`

This can also protect against transient network issues, and issues caused by transfer 
of binary data from external sources. These recommendations also apply when consuming 
packages from external sources in any package manager. 


Compliance and security
-----------------------
Some industries such as finance, robotics and embedded, have stronger requirements 
around change management, open source licenses and reproducibility. For example, 
changes in recipes could result in a new version being resolved for a dependency, 
in a way that the license for that version has changed and needs to be validated 
and audited by your organization. 
In some industries like medical or automotive, you may be required to ensure all 
your dependencies can be built from source in a repeatable way, and thus using 
binaries provided by Conan Center may not be advisable. In these instances, 
we recommend building your own binary packages from source:

- Read more: :ref:`creating and hosting your own Conan Center binaries <devops_conancenter_hosting_your_own_conancenter_fork>`

Control and customization
-------------------------
It is very common for users of dependencies to require custom changes to external 
libraries - typically to support specific platform configurations not considered 
by either ConanCenter or the original library authors, backport bug fixes, etc. 
Some of these changes may not be suitable to be merged in ConanCenter, 
and it may not happen until this has been reviewed and validated by ConanCenter maintainers. 
For this reason, if you need tight control over the changes in recipes, 
it is highly recommended to host not only a Conan remote, but your own fork of the 
conan-center-index recipe repository.

- Read more: :ref:`creating and hosting your own Conan Center binaries <devops_conancenter_hosting_your_own_conancenter_fork>`


The following subsections describe in more details the above strategies:

.. toctree::
   :maxdepth: 1

   conancenter/hosting_binaries

