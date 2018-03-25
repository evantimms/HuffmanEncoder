# The functions in this file are to be implemented by students.

import bitio
import huffman


def read_tree(bitreader):
    '''Read a description of a Huffman tree from the given bit reader,
    and construct and return the tree. When this function returns, the
    bit reader should be ready to read the next bit immediately
    following the tree description.

    Huffman trees are stored in the following format:
      * TreeLeaf is represented by the two bits 01, followed by 8 bits
          for the symbol at that leaf.
      * TreeLeaf that is None (the special "end of message" character) 
          is represented by the two bits 00.
      * TreeBranch is represented by the single bit 1, followed by a
          description of the left subtree and then the right subtree.

    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.

    Returns:
      A Huffman tree constructed according to the given description.
      

    implementation: read each bit, and sort depending on what value it makes up
    '''     
    #pass the input of the bitreader(the opened file) and construct
    #the frequency table from the stream
    def construct_tree(bitreader):
        bit = bitreader.readbit()
        if bit == 1:
            return huffman.TreeBranch(construct_tree(bitreader),construct_tree(bitreader))
        elif bit == 0:
            bit2 == bitreader.readbit()
            if bit == 0:
                return huffman.TreeLeaf(None)
            else:
                val = bitreader.readbits(8)
                return huffman.TreeLeaf(val)
        

    tree = huffman.TreeBranch(None,None)
    bitreader.readbit()
    tree.left = construct_tree(bitreader)
    tree.right = construct_tree(bitreader)

    
    
    return tree



def decode_byte(tree, bitreader):
    """
    Reads bits from the bit reader and traverses the tree from
    the root to a leaf. Once a leaf is reached, bits are no longer read
    and the value of that leaf is returned.
    
    Args:
      bitreader: An instance of bitio.BitReader to read the tree from.
      tree: A Huffman tree.

    Returns:
      Next byte of the compressed bit stream.

    Starting from the root, traverse the Huffman tree. Each bit from
    the input sequence tells you when to go left or right.
    """
    #read a bit
    bit = bitreader.readbit()
    if isinstance(tree, TreeBranch):
        if bit == 1 :
            #traverse left
            tree = tree.left
            return decode_byte(tree, bitreader)
        elif bit == 0:
            #traverse right
            tree = tree.right
            return decode_byte(tree, bitreader)
    elif isInstance(tree, TreeLeaf):
        #return value of tree leaf
        return tree.value
    else:
        print("big problems boys    ")
    


def decompress(compressed, uncompressed):
    '''First, read a Huffman tree from the 'compressed' stream using your
    read_tree function. Then use that tree to decode the rest of the
    stream and write the resulting symbols to the 'uncompressed'
    stream.

    Args:
      compressed: A file stream from which compressed input is read.
      uncompressed: A writable file stream to which the uncompressed
          output is written.

    '''
    #set up reader and writer 
    reader = bitio.BitReader(compressed)
    writer = bitio.BitWriter(uncompressed)
    #initate tree from 
    tree = read_tree(reader)
    byte = 0
    while(byte != None):
        #until eof occurs, read byte from reader and decode using reader
        #then right the byte to the uncompressed file using the writer
        byte = decode_byte(tree, reader)
        writer.writebits(byte,8)


    
    
def write_tree(tree, bitwriter):
    '''Write the specified Huffman tree to the given bit writer.  The
    tree is written in the format described above for the read_tree
    function.

    DO NOT flush the bit writer after writing the tree.

    Args:
      tree: A Huffman tree.
      bitwriter: An instance of bitio.BitWriter to write the tree to.
    '''
    if isinstance(tree, huffman.TreeLeaf):
        if tree.value is None:
            bitwriter.writebit(False)
            bitwriter.writebit(False)
        else:
            bitwriter.writebit(False)
            bitwriter.writebit(True)
            bitwriter.writebits(tree.value, 8)

    if isinstance(tree, huffman.TreeBranch):
        write_tree(tree.left, bitwriter)
        write_tree(tree.right, bitwriter)


def compress(tree, uncompressed, compressed):
    '''First write the given tree to the stream 'compressed' using the
    write_tree function. Then use the same tree to encode the data
    from the input stream 'uncompressed' and write it to 'compressed'.
    If there are any partially-written bytes remaining at the end,
    write 0 bits to form a complete byte.

    Flush the bitwriter after writing the entire compressed file.

    Args:
      tree: A Huffman tree.
      uncompressed: A file stream from which you can read the input.
      compressed: A file stream that will receive the tree description
          and the coded input data.
    '''
    #set up reader and writer 
    reader = bitio.BitReader(compressed)
    writer = bitio.BitWriter(uncompressed)
    write_tree(tree, writer)

    encoder = huffman.make_encoding_table(tree)

    while(True):
        try:
            byte = reader.readbits(8)
            sequence = encoder[byte]
            #TODO: read in path and add to sequence
            for bit in sequence:
                if bit == '1':
                    writer.writebit(True)
                else:
                    writer.writebit(False)
        except EOFError:
            break

