class FileReader:
    #The class constructor is used to initialize the input file reader object.
    def __init__(self,file_name: str):
        self.__input_file = open(file_name,"rb")
    def read_byte(self) -> int:
        """
        read_byte method is meant to read a single byte from the input file
        and to return its decimal ASCII value in case the symbol is found,
        otherwise it'll close the file and return the 256 value,
        so we can keep track of the EOF symbol.
        """
        try:
            return self.__input_file.read(1)[0]
        except IndexError:
            self.__input_file.close()
            return 256
    def __del__(self):
        self.__input_file.close()

class FileWriter:
    #The class constructor is used to initialize the output file writer object.
    def __init__(self,file_name: str):
        self.__output_file = open(file_name,"wb")
        self.__bit_buffer = 0 #8bit buffer that will be written to the outputfile
        self.__bits_to_go = 8 #bit counter used to keep track of how many bits were appended by this point
    def append_bit(self, bit):
    #append_bit method is meant to append a single bit to the final byte that will be written in the output file
        self.__bit_buffer >>= 1
        if bit:
            self.__bit_buffer |= 0x80
        self.__bits_to_go -= 1
        if not self.__bits_to_go:
            self.__write_byte() #once a byte is written, reinitialize the bit buffer and bits to go
            self.__bit_buffer = 0
            self.__bits_to_go = 8
    def __write_byte(self):
        #write_byte method is meant to write a single byte to the output file(encoded file)
        self.__output_file.write(self.__bit_buffer.to_bytes(1,'big'))
    def __del__(self):
        self.__output_file.close()