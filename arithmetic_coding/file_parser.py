class FileParser:
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