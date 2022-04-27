class FileParser:
    def __init__(self,file_name: str) -> None:
        self.__input_file = file_name #open(file_name,"rb")
        
#with open("test.txt","rb") as input_file:
#    current_byte = input_file.read(1)
#    while current_byte:
#        current_byte = input_file.read(1)
#    my_byte = current_byte[0]