.. _extract_licenses_from_headers:

How to extract licenses from headers
====================================

Sometimes there is no ``license`` file, and you will need to extract the license from a header file, as in the following example:

  .. code-block:: python

    def package():
        # Extract the License/s from the header to a file
        tmp = tools.load("header.h")
        license_contents = tmp[2:tmp.find("*/", 1)] # The license begins with a C comment /* and ends with */
        tools.save("LICENSE", license_contents)

        # Package it
        self.copy("license*", dst="licenses",  ignore_case=True, keep_path=False)