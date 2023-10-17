#!python3
import fitz
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

if os.path.isfile(FILENAME_AFFILIATIIONS):
    with open(FILENAME_AFFILIATIIONS) as f:
        AFFILIATIONS = f.read().strip().split("\n")
else:
    log.error(f"File not found: {FILENAME_AFFILIATIIONS}!")
    log.error(f"Please create the file within the working directory.")
    log.error(f"For format is one affiliation per line. Example:")
    log.error("Max-Planck-Institut für Radioastronomie, Auf dem Hügel 69, 53121 Bonn, Germany")
    log.error("Department of Physics, Moscow University, 119899 Moscow, Russia")
    log.error("Exiting ...")
    exit()

if os.path.isfile(FILENAME_AUTHORS):
    with open(FILENAME_AUTHORS) as f:
        AUTHORS = f.read().strip().split("\n")
else:
    log.error(f"File not found: {FILENAME_AUTHORS}!")
    log.error(f"Please create the file within the working directory.")
    log.error(f"For format is one author per line. Example:")
    log.error("Rainer Beck")
    log.error("D. Sokoloff")
    log.error("Exiting ...")
    exit()


if os.path.isfile(FILENAME_HEADERS):
    with open(FILENAME_HEADERS) as f:
        HEADERS = f.read().strip().split("\n")
else:
    log.error(f"File not found: {FILENAME_AUTHORS}!")
    log.error(f"Please create the file within the working directory.")
    log.error(f"For format is one author per line. Example:")
    log.error("A&A.*DOI.*\ ([0-9]{4})\ Astrophysics$")
    log.error("MNRAS.*\(2022\)$")
    log.error("https://doi\.org.*/mnras/[a-z0-9]*$")
    log.error("Exiting ...")
    exit()
# read files
# # # # # # #

def get_matches(words, regex):
    matches = []
    start = 0
    end = 1
    concat = ""

    while end <= len(words):
        concat = " ".join([w[4] for w in words[start:end]])
        found = regex.search(concat)
        if not found:
            end += 1
        else:
            found2 = regex.search(concat)
            while found2:
                start += 1
                concat = " ".join([w[4] for w in words[start:end]])
                found2 = regex.search(concat)
                #print(concat)
                #print(start, end)
                if not found2:
                    matches += words[start-1:end]
                    start = end
                    end += 1
    return list(set(matches))



def highlight(pdf, regex, max_page=None):
    total_matches = []
    for ii, pg in enumerate(pdf):
        words = pg.get_text("words", flags=0)
        matches = get_matches(words, regex)
        total_matches += matches
        for word in matches:
            highlight = pg.add_highlight_annot([word[0], word[1], word[2], word[3]])
            highlight.update()
        if ii == max_page:
            break
    return total_matches


def highlight_title(pdf):
    title = pdf.metadata.get("title")
    if title:
        log.info(f"Highlighting title: {title}")
        regex = re.compile(title, re.IGNORECASE)
        highlight(pdf, regex, max_page=0)
    else:
        log.warning("No title found in pdf metadata!")


def get_author_variation(authors):
    authors_plus = []
    for author in authors:
        a_list = author.strip().split(" ")
        s = ""
        for a in a_list[0:-1]:
            s += a[0] + ". "
        s += a_list[-1]
        authors_plus.append(s)
        s = a_list[0][0] + ". " + a_list[-1]
        authors_plus.append(s)
    return list(set(authors_plus))



def highlight_authors(pdf):
    log.info("Checking authors.")
    matches = []
    authors_plus = AUTHORS + get_author_variation(AUTHORS)
    for author in authors_plus:
        regex = re.compile(author, re.IGNORECASE | re.UNICODE)
        matches += highlight(pdf, regex, max_page=1)
    if not matches:
        log.warning("No authors found!")


def highlight_headers(pdf):
    log.info("Checking header.")
    matches = []
    for header in HEADERS:
        regex = re.compile(r"" + str(header), re.IGNORECASE | re.UNICODE)
        matches += highlight(pdf, regex, max_page=0)
    if not matches:
        log.warning("No headers found!")


def highlight_affiliations(pdf):
    log.info("Checking affiliations.")
    matches = []
    for affiliation in AFFILIATIONS:
        regex = re.compile(affiliation, re.IGNORECASE | re.UNICODE)
        matches += highlight(pdf, regex, max_page=0)
    if not matches:
        log.warning("No affiliation found!")


def main():
    listing = glob("*pdf")
    log.info(SEPERATOR)
    log.info(SEPERATOR)
    for filepath in listing:
        log.info(f"Opening file: {filepath}")
        pdf = fitz.open(filepath)
        highlight_title(pdf)
        highlight_authors(pdf)
        highlight_headers(pdf)
        highlight_affiliations(pdf)
        log.info(SEPERATOR)
        pdf.saveIncr()
        pdf.close()
    log.info(SEPERATOR)

if __name__ == "__main__":
    main()
