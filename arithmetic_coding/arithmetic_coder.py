class ArithmeticCoder:
    def __init__(self):
        """
        We'll be using the constructor to initialize the current coding model.
        The model used in this application is similar to the one described by
        Edgar Sibley and Panel Editor in their 'Arithmetic Coding for Data Compression'
        paper, but the approach is simplified by using Macarie Breazu's
        'Arithmetic coding with integer representation' paper.
        """
        self.__low = 0
        self.__high = pow(2,32)-1 #equivalent to (1 << 32) - 1
        self.__range = 0 #initializing range with 0(it could be initialized with any value, since its value is always modified before being used)
        self.__symbol = []
        self.__counts = []
        self.__sums = []
        self.__bits_to_follow = 0 #keeps track of bits to append in case of 2nd level shifting
        self.__model_init()

    def __model_init(self):
        self.__sums.append(0)
        for i in range(0,256):
            self.__symbol.append(i)
            self.__counts.append(1)
            if i > 0:
                self.__sums.append(self.__sums[i-1] + self.__counts[i-1])
