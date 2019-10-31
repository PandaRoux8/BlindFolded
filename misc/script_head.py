import sys
from os import listdir
from os.path import isfile, join

IGNORE = ['__pycache__']


def get_header():
    return """# ------------------------------------------
# Name        : Jules Schluchter
# Mail        : jules.schluchter@gmail.com
# Date        : 22.10.2019
# Package     : gamePackage
# Project     : BlindFolded
# -----------------------------------------

"""


def add_header(file):
    with open(file, "r+") as f:
        file_content = f.read()

    with open(file, "w+") as f:
        f.write(get_header() + file_content)


def search_for_files(path):
    # sys.path(path)
    # path = os.path(path)
    for f in listdir(path):
        if f not in IGNORE:
            if isfile(join(path, f)) and ".py" in f:
                add_header(join(path, f))
                continue
            search_for_files(join(path, f))

        #     print(f)
        # print(join(path, f))


if __name__ == '__main__':
    path = "/home/jules/BlindFolded/gamePackage/"
    # path = "/home/user/test"
    search_for_files(path)
