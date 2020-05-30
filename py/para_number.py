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

para_id = ""

for node in soup.findAll(text=True):
    match = regex.match(node)

    string = ""

    if match:
        para_id = match.group(0).strip(".")
        if para_id == "A":
            section = section + 1
            if section == 2:
                section = section + 1
        
        if section <= LAST_SECTION: # TODO: horribly inefficent
            if para_id.isupper():
                capital_letter = para_id
                arab_num = ""
                lower_letter = ""
                roman_num =""
                print(str(section) + capital_letter + " / " + str(node))

            elif para_id.isnumeric():
                arab_num = para_id
                lower_letter = ""
                roman_num = ""
            
            elif para_id.islower():
                if lower_letter != "":
                    roman_num = para_id
                else:
                    lower_letter = para_id
                    roman_num = ""
            
            #string = str(section) + capital_letter + arab_num + lower_letter + roman_num
            #print(string + " / " + str(node))


                
