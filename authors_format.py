#!python3
import time
import re
import os
import logging
from glob import glob
'''
Version: 0.1
Author: Lennart Heino
'''

# # # # # # #
# set logger
FILEPATH_LOG_PIPELINE = "highlight.log"

logger = logging.getLogger('general')
logger.setLevel(logging.INFO)
fh = logging.FileHandler(FILEPATH_LOG_PIPELINE)
fh.setLevel(logging.INFO)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s\t[ %(levelname)s ]\t%(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)
logger.addHandler(fh)
logger.addHandler(ch)

info = logger.info
debug = logger.debug
warning = logger.warning
error = logger.error
log = logger

SEPERATOR = "-"*79
SEPERATOR_SOFT = "- "*79
SEPERATOR_SOFT = SEPERATOR_SOFT[:80]
# set logger
# # # # # # #


# # # # # # #
# read files
FILENAME_AFFILIATIIONS = "affiliations.txt"
FILENAME_AUTHORS = "authors.txt"
FILENAME_HEADERS = "headers.txt"


def print_cleaned_string():
    #s = 'Kenneth J. *Duncan,1‹ Michael J. I. Brown,2,3,4 Wendy L. van der Williams,4 Philip N. Best,5 Veronique Buat,6 Denis Burgarella,6 Matt J. Jarvis,7,8 Katarzyna Małek,6,9 S. J. Oliver,10 Huub J. A. R¨ottgering1 and Daniel J. B. Smith'
    print()
    s = input()
    print()
    s_original = s
    s = re.sub(r'[0-9]', "", s)
    s = re.sub(r',+', ",", s)
    s = re.sub(r'\*', "", s)
    s = re.sub("‹", "", s)
    s = re.sub("¨o", "ö", s)
    s = re.sub("¨u", "ü", s)
    s = re.sub("¨a", "ä", s)
    s = re.sub(" and ", ", ", s)
    listing = s.split(", ")
    new = []
    for author in listing:
        a = author.strip().split(" ")
        ss = a[0][0] + " "
        for initial in a[1:]:
            if initial.strip()[-1] == ".":
                ss += initial[0] + " "
            else:
                ss += initial + " "
        new.append(ss.strip())
    s_new = ", ".join(new)
    special_char = re.search(r"^[A-Z]", s)
    #import string
    info(SEPERATOR)
    info("OLD STRING:")
    info(s_original)
    info(SEPERATOR_SOFT)
    info("NEW STRING:")
    info(s_new)
    if not s_new.isascii():
        info(SEPERATOR_SOFT)
        info("ATTENTION! Non-ascii character found. Double-check the output!:")
        not_ascii = []
        for char in s_new:
            if not char.isascii():
                not_ascii.append(char)
        info(", ".join(not_ascii))

    info(SEPERATOR)
    #print(set(string.printable)  )





def main():
    while True:
        info("Copy and paste the author list into this terminal and hit Enter.")
        try:
            print_cleaned_string()
        except Exception as e:
            warning(e)


if __name__ == "__main__":
    main()
