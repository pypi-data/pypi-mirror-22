BitList
=======

An bits array implement in pure python.
No dependency. 
Support python3+.

Package Installation and Usage
------------------------------

The package is available on PyPI ( called **py3bitlist** ):

    pip install py3bitlist

The library can be imported in the usual way:

    import bitlist

APIs
----

BitList(length)
    Return a BitList object with length bits.

Bitlist(bytes)
    Return a BitList object which is constructed by bytes.

BitList.get_bytes_length()
    Return the number of bytes that consist the Bitlist.

BitList.get_length()
    Return the number of bits that consist the Bitlist.

BitList.set_bit(position, num)
    Set the bit in position to num.

BitList.get_bit(position)
    Get the bit in position.
