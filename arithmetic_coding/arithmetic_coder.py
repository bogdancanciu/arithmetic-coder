from file_parser import FileWriter

class ArithmeticCoder:
    def __init__(self, output_file_name: str):
        """
        We'll be using the constructor to initialize the current coding model.
        The model used in this application is similar to the one described by
        Edgar Sibley and Panel Editor in their 'Arithmetic Coding for Data Compression'
        paper, but the approach is simplified by using Macarie Breazu's
        'Arithmetic coding with integer representation' paper.
        """
        self.__encoder = FileWriter(output_file_name) #FileWriter object used to output the encoded file.
        self.__low = 0
        self.__high = pow(2,32)-1 #equivalent to (1 << 32) - 1
        self.__range = 0 #initializing range with 0(it could be initialized with any value, since its value is always modified before being used)
        self.__symbols = []
        self.__counts = []
        self.__sums = []
        self.__bits_to_follow = 0 #keeps track of bits to append in case of 2nd level shifting
        self.__model_init()

    def __model_init(self):
        self.__sums.append(0)
        for i in range(0,257):
            self.__symbols.append(i)
            self.__counts.append(1)
            if i > 0:
                self.__sums.append(self.__sums[i-1] + self.__counts[i-1])
        self.__sums.append(self.__sums[len(self.__sums)-1] + self.__counts[len(self.__counts)-1])
    def __output_bit(self, bit):
        self.__encoder.append_bit(bit)
        while self.__bits_to_follow > 0:
            self.__encoder.append_bit(not bit)
            self.__bits_to_follow -= 1
    def encode_symbol(self, symbol):
        self.__range = self.__high - self.__low + 1
        self.__high = self.__low + self.__range * self.__sums[symbol+1]//self.__sums[len(self.__sums)-1] - 1
        self.__low = self.__low + self.__range * self.__sums[symbol]//self.__sums[len(self.__sums)-1]
        while True:
            if self.__high <= (pow(2,32)-1)//2: #high is in the low half
                self.__output_bit(0)
                self.__high <<= 1
                self.__high |= 0x01
                self.__low <<= 1
                self.__low &= 0xFFFFFFFE
            elif self.__low > (pow(2,32)-1)//2:
                self.__output_bit(1)
                self.__high <<= 1
                self.__high |= 0x01
                self.__high &= 0x0FFFFFFFF#flush the most significant bit resulted from shifting
                self.__low <<= 1
                self.__low &= 0xFFFFFFFE
            elif self.__low > (pow(2,32)-1)//4 and self.__high < ((pow(2,32)-1)//4 + 1) * 3 :
                self.__bits_to_follow += 1
                mask_high = 0b00111111111111111111111111111111
                self.__high &= mask_high #remove top 2 most significant bits
                mask_high = 0b01000000000000000000000000000000
                self.__high |= mask_high #set bit 30 to true, see Macarie Breazu's paper.
                self.__high <<= 1
                self.__high |= 0x01
                mask_low = 0b01111111111111111111111111111111
                self.__low <<=1 #add a 0 to the bit 0
                self.__low &= mask_low #remove bit 30
            else:
                break
    def done_encoding(self):
        self.__bits_to_follow += 1
        if self.__low <= (pow(2,32)-1)//4:
            self.__output_bit(0)
        else:
            self.__output_bit(1)
        self.__encoder.done_outputing()