import sys

Red: str = "\033[31m"
Green: str = "\033[32m"
Yellow: str = "\033[33m"
Blue: str = "\033[34m"
Magenta: str = "\033[35m"
Cyan: str = "\033[36m"
White: str = "\033[37m"


BrightRed: str = "\033[91m"
BrightGreen: str = "\033[92m"
BrightYellow: str = "\033[93m"
BrightBlue: str = "\033[94m"
BrightMagenta: str = "\033[95m"
BrightCyan: str = "\033[96m"
BrightWhite: str = "\033[97m"

UBrightRed: str = "\033[4;91m"
UBrightGreen: str = "\033[4;92m"
UBrightYellow: str = "\033[4;93m"
UBrightBlue: str = "\033[4;94m"
UBrightMagenta: str = "\033[4;95m"
UBrightCyan: str = "\033[4;96m"
UBrightWhite: str = "\033[4;97m"


Reset: str = "\033[0m"

def perr(Kwargs, end="\n"):
    print(Kwargs, end=end, file=sys.stderr)
