from bs4 import BeautifulSoup
import re

html_filename = input("Enter Filename: ")

if html_filename == "":
    html_filename = "fdx_2015_working.html"

soup = ""
try:
    soup = BeautifulSoup(
        open(html_filename), features="html.parser"
    )

except:
    print("File not found. Exiting...")

regex = re.compile(r"\w+\.{1}")


LAST_SECTION = 31

section = 0
capital_letter = ""
arab_num = ""
lower_letter = ""
roman_num = ""

# SECTION = 1
#   SECTION + 1 if CAPLET == "A" .
# CAPLET.ARABNUM.LOWLET.ROMANNUM

for node in soup.findAll(text=True):
    match = regex.match(node)
    if match:
        if match.group(0) == "A.":
            section = section + 1
            if section == 2:
                section = section + 1
        
        if section <= LAST_SECTION: # TODO: horribly inefficent
            if match.group(0).isupper():
                print("{}.{} // {}".format(section, match.group(0), node))