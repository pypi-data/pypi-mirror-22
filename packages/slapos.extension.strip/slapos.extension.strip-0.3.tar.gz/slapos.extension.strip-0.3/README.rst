Buildout Extension to strip binaries
====================================

slapos.extension.strip is a buildout extension that finds shared
libraries, binary executables and static libraries, and calls strip(1)
against them to reduce the size. It is triggered at the end of the
buildout process.

Usage
-----

Add ``slapos.extension.strip`` in ``[buildout]`` section's ``extensions`` option like :

::

  [buildout]
  extensions = slapos.extension.strip

Requirements
------------

The following programs are required. If any of them is missing, this
extension does nothing.

- ``file``
- ``find``
- ``strip``

Supported Options
-----------------

``file-binary``

  Path to ``file`` program. Defaults to 'file' which should work on
  any system that has the make program available in the system
  ``PATH``.

``find-binary``

  Path to ``find`` program. Defaults to 'find' which should work on
  any system that has the find program available in the system
  ``PATH``.

``strip-binary``

  Path to ``strip`` program. Defaults to 'strip' which should work on
  any system that has the strip program available in the system
  ``PATH``.

``do-not-strip-path``

  A new-line separated list of absolute paths of the files you do not
  want to strip. Do not refer a section to get its location. If you do
  like ${bazel:location}/bin/bazel, buildout will not work correctly.
  Instead do like ${buildout:parts-directory}/bazel/bin/bazel.

  An example::

    [buildout]
    do-not-strip-path =
      ${buildout:parts-directory}/bazel/bin/bazel
      ${buildout:parts-directory}/anotherparts/bin/dontstripbinary
