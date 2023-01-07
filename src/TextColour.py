class TC:
    def __init__(self):
        self.colour_codes = {
            "black": "\033[30m",
            "red": "\033[31m",
            "green": "\033[32m",
            "yellow": "\033[33m",
            "blue": "\033[34m",
            "magenta": "\033[35m",
            "cyan": "\033[36m",
            "white": "\033[37m",
            "bright black": "\033[90m",
            "bright red": "\033[91m",
            "bright green": "\033[92m",
            "bright yellow": "\033[93m",
            "bright blue": "\033[94m",
            "bright magenta": "\033[95m",
            "bright cyan": "\033[96m",
            "bright white": "\033[97m",
            "brown": "\033[93m",
            "default": "\033[0;37;m"
        }

    def colour(self, colour = "default"):
        if colour != '':
            return self.colour_codes[colour.lower()]

