jwxml
=====

*Note: This is probably mostly useful internally at STScI.*

Miscellaneous XML support helper code related to some JWST configuration files, mostly optics and wavefront sensing related.

So far this provides support for reading in and interacting with:

  * The so-called SIAF (Science Instrument Aperture Files)
  * Wavefront control SUR (Segment Update Request) files

More functionality may be added ad hoc as needed; no overall long term development master plan is implied.

SIAF
----

Science Instrument Aperture Files contain detailed focal plane and pointing models for the science instruments. They are maintained in the JWST PRD (Project Reference Database). Snapshots taken from the PRD are bundled with jwxml, but care should be taken to ensure one is using the latest files from the PRD directly.

For a file obtained from the PRD:

.. code:: python

    siaf = jwxml.SIAF(filename='/your/path/to/NIRCam_SIAF_2016-01-28.xml')

To use the bundled SIAF:

.. code:: python

    siaf = jwxml.SIAF('NIRCam')

To check which PRD version is in use:

.. code:: python

    print(jwxml.PRD_VERSION)


