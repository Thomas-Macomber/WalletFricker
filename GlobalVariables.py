#because why the fuck not
CryptoHopperName = "Wallet Fucker"
version = "Indev 0.0.2"
#Prints the header
def header():
    print ( color.GREEN + CryptoHopperName + color.WHITE + "___" + color.RED + version + color.WHITE)

#Added color class. Each variable is a string representation that you need to enter to change the color of text.
#I made a change to printLogScreen to utilize colors for the first printed line. Feel free to check it to see implementation and run the program.
#Note: Colors only seem to work after the program starts looping. It's a little weird and I'm not sure why that is.
class color:
    RED = "\033[1;31;40m"
    YELLOW = "\033[1;33;40m"
    GREEN = "\033[1;32;40m"
    BLUE = "\033[1;34;40m"
    PURPLE = "\033[1;35;40m"
    CYAN = "\033[1;36;40m"
    BLACK = "\033[1;30;40m"
    WHITE = "\033[1;37;40m"
