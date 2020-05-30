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

lower_count = 0
LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyza" # added a because section 18C6aa

# SECTION = 1
#   SECTION + 1 if CAPLET == "A" .
# CAPLET.ARABNUM.LOWLET.ROMANNUM

para_id = ""

nodes = soup.findAll()

for ac_node in nodes:
    node = ac_node.getText()
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
                lower_count = 0
                roman_num = ""
                
                if len(node) < 75:
                    ac_node.name = "h3"

            elif para_id.isnumeric():
                arab_num = para_id
                lower_letter = ""
                roman_num = ""
                lower_count = 0

                if len(node) < 50:
                    ac_node.name = "h4"
            
            elif para_id.islower():
                if para_id == LOWER_LETTERS[lower_count]:
                    lower_letter = para_id
                    lower_count = lower_count + 1
                    roman_num = ""
                else:
                    roman_num = para_id
            
            string = str(section) + capital_letter + arab_num + lower_letter + roman_num
            #TESTING
            if ac_node.name != "td":
                ac_node['id'] = string

with open("fdx_2015_tester.html", "w") as file:
    file.write(str(soup))


                
