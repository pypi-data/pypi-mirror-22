pycompressor
============

Package provides python implementation of string compressor

.. image:: https://travis-ci.org/chen0040/pycompressor.svg?branch=master
    :target: https://travis-ci.org/chen0040/pycompressor

.. image:: https://coveralls.io/repos/github/chen0040/pycompressor/badge.svg?branch=master
    :target: https://coveralls.io/github/chen0040/pycompressor?branch=master

.. image:: https://scrutinizer-ci.com/g/chen0040/pycompressor/badges/quality-score.png?b=master
    :target: https://scrutinizer-ci.com/g/chen0040/pycompressor/?branch=master


More details are provided in the `docs`_ for implementation, complexities and further info.

Install
=======

Run the following command to install pycompressor using pip

.. code-block:: bash

    $ pip install pycompressor


Usage:
======

.. code-block:: python

    from pycompressor.huffman import HuffmanCompressor
    huffman = HuffmanCompressor()
    original = 'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.'
    print('before compression: ' + original)
    print('length: ' + str(len(original)))
    compressed = huffman.compress_to_string(original)
    print('after compression: ' + compressed)
    print('length: ' + str(len(compressed)))
    decompressed = huffman.decompress_from_string(compressed)
    print('after decompression: ' + decompressed)
    print('length: ' + str(len(decompressed)))



