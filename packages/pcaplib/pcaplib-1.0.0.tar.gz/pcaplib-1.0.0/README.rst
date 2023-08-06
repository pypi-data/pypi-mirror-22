Python PCAP Library
===================

.. image:: https://gitlab.com/salah.gherdaoui/pcaplib/badges/master/build.svg
.. image:: https://gitlab.com/salah.gherdaoui/pcaplib/badges/master/coverage.svg


``pcaplib`` is a very simple and lightweight library for reading and writing PCAP files

Reader example::

        import pcaplib
        pcap_reader = pcaplib.Reader('capture.pcap')
        for ts in pcap_reader:
            print(packet)

        (1494608771, 459378, 6, 6, b'\\x00\\x0c)\\xaa4\\xc9')
        (1494608771, 459556, 6, 6, b'\\x00\\x0c)\\xaa4\\xc9')




Writer example::

         import pcaplib

         pkt_list = [
             (1494608771, 459378, 6, 6, b'\\x00\\x0c)\\xaa4\\xc9'),
             (1494608771, 459556, 6, 6, b'\\x00\\x0c)\\xaa4\\xc9'),
         ]

         pcap_writer = pcaplib.Writer('capture.pcap', pkt_list)
         pcap_writer.writer()
