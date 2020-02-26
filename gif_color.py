"""A module to handle the bytes inside of a .gif image

At the moment, this only changes colors if a Global Color Table
is set for the gif (true for most gifs).  I have plans to add
more features and clean up the code.
"""

# used for byte I/O
import struct

# TODO: gifs are in Little-endian format
# TODO: allow for changing the color of each frame when global
#    color table is not set
# TODO: make a function to turn gif into png's of frames

class GlobalColorTableNotSet(Exception):
    """To be raised if there is no Global Color Table"""
    pass

class GifData():
    """This is an object to hande Gif color data"""
    def __init__(self, in_file):
        """Reads a .gif file and gets nessessary bytes"""
        self.in_file = in_file
        with open(self.in_file, 'rb') as fin:
            self.data = fin.read(11)
            # convert byte 11 to binary, then string
            condensed_byte = str(bin(struct.unpack('>B', self.data[-1:])[0])[2:])
            if condensed_byte[0] != '1':
                raise GlobalColorTableNotSet
                print('Global Color Table Flag is not set\n\
cannot change color fot this .gif file...\n\
Exiting program...')
                exit(0)
            # last 3 bits of byte 10 are size of global color table
            self.color_table_size = int(condensed_byte[-3:], base=2)
            # from onicos.com/staff/iz/formats/gif.html#ib
            # (gif format gives this formula for color table size)
            self.color_table_size = 2**(1+self.color_table_size)
            self.data += fin.read(2)
            # color data
            self.colors = []
            for i in range(0, self.color_table_size):
                three_bytes = fin.read(3)
                self.data += three_bytes
                red = struct.unpack('>Bxx', three_bytes)[0]
                green = struct.unpack('>xBx', three_bytes)[0]
                blue = struct.unpack('>xxB', three_bytes)[0]
                self.colors.append((red, green, blue))
            # read the rest of the data
            # TODO: copy .gif to a new filename and
            # overwrite ONLY the part of the file you need to,
            # so the entire file isn't in memory
            print('Loading file...')
            self.data += fin.read()
    def __set_color_binary(self):
        """Private method to set the correct bytes for self.colors"""
        # TODO: this is taking up more memory than it needs to
        data_byte_arr = bytearray(self.data)
        with open(self.in_file, 'rb'):
            for i in range(0, self.color_table_size*3, 3):
                red, green, blue = self.colors[int(i/3)]
                data_byte_arr[13 + i] = red
                data_byte_arr[14 + i] = green
                data_byte_arr[15 + i] = blue
        self.data = bytes(data_byte_arr)
    def get_colors(self):
        """Returns a list of all global gif colors"""
        return self.colors
    def set_color(self, index, rgb_tuple):
        """Sets one global color in rgb format

        Parameters:
            index: what index to set (starts at 0)
            rgb_tuple: a tuple in (red, green, blue) format
        """
        self.colors[index] = rgb_tuple
        self.__set_color_binary()
    def write(self, output_filename=None):
        """Write the changed gif image to a file

        Parameters:
            output_filename [OPTIONAL]: sets the filename of the .gif to output
        """
        if output_filename is None:
            output_filename = self.in_file[:-4] + '_colored.gif'
        # remove .gif and add _colored.gif, 'wb' = write binary
        with open(output_filename, 'wb') as fout:
            fout.write(self.data)
        print('Wrote file to', output_filename)
