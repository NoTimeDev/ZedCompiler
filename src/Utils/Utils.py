import sys

Colour = {
    "Blue" : "\033[31m",
    "Red" : "\033[31m",
    "Reset" : "\033[0m",
    "Green" : "\033[32m",
    "Cyan" : "\033[36m",
    "Yellow" : "\033[33m",
    "Magenta" : "\033[35m",

    "BrightGreen" : "\033[92m",
    "BrightCyan" : "\033[96m",
    "BrightYellow" : "\033[93m",
    "BrightMagenta" : "\033[95m",
    "BrightRed" : "\033[91m",
    "BrightWhite" : "\033[97m",
    "BrightBlue" : "\033[94m",
}

def printf(*Kwargs) -> None: #Dumb Shit For Errors Cool Name   
    print(*Kwargs, file=sys.stderr)
