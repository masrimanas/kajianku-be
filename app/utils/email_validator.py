import re

REGEX = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b"


def check(email):
    if re.fullmatch(REGEX, email):
        return True
    else:
        return False
