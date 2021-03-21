# TODO: Implement excess element & attribute removal
# TODO: Implement in paragrapgh section linking

from bs4 import BeautifulSoup
import re
import json

# Setting this to true will allow the script to create links
CREATE_LINKS = False

def return_section_string_with_link(input_string):
    if CREATE_LINKS:
        section_id, link_start_pos, link_end_pos = \
            find_section_reference_and_return(input_string)
        if section_id != "":
            section_link_open_tag, section_link_close_tag = \
                create_section_link(section_id)
            input_string = input_string[:link_start_pos] \
                + section_link_open_tag \
                + input_string[link_start_pos:link_end_pos] \
                + section_link_close_tag \
                + input_string[link_end_pos:]
        return input_string
    return input_string


def create_section_link(section_id):
    return '<a href="#{}">'.format(section_id), '</a>'


def find_section_reference_and_return(input_string):
    SECTION_LINK_REGEX = \
        r"Section (\d+)\.([A-Z]+)\.*([0-9]*)\.*([a-z]*)\.*([mdclxvi]*)"

    regex = re.compile(SECTION_LINK_REGEX)
    match = regex.search(input_string)

    section_id = ""
    section_start_pos = 0
    section_end_pos = 0

    if match:
        for group in match.groups():
            section_id = section_id + group
        section_start_pos = match.start()
        section_end_pos = match.end()
    return section_id, section_start_pos, section_end_pos

def is_matched_paragraph_id_suspect(para_id):
    SUSPECT_PARA_IDS = ["84", "77", "71", "65"]
    for suspect_id in SUSPECT_PARA_IDS:
        if suspect_id == para_id:
            return True

def find_paragraph_id_and_set_node_id(input_nodes):
    LAST_SECTION = 32
    LOWER_LETTERS = "abcdefghijklmnopqrstuvwxyz" # added a because section 18C6aa 
    SECTION_NUMBER_REGEX = re.compile(r"Section (\d+):")
    PARAGRAPH_ID_REGEX = re.compile(r"\w+\.{1}")

    section = 0
    capital_letter = ""
    arab_num = ""
    lower_letter = ""
    roman_num = ""

    lower_count = 0

    # SECTION = 1
    #   SECTION + 1 if CAPLET == "A" .
    # CAPLET.ARABNUM.LOWLET.ROMANNUM

    para_id = ""
    lastString = ""

    for node in input_nodes:
        node_text = node.getText()
        section_match = SECTION_NUMBER_REGEX.match(node_text)
        para_id_match = PARAGRAPH_ID_REGEX.match(node_text)
    
        string = ""
        if section_match:
            section = int(section_match.group(1))
            node['id'] = str(section)


        # TODO: HACKY AS SHIT
        if node_text == "Lump Sum Payment Distribution (2015)":
            break

        if para_id_match:
            para_id = para_id_match.group(0).strip(".")
            
            # HACK FOR 1015 FDX SECTION 27
            # Default Algorithm treats percentages as
            # new paragraph numbers
            if not is_matched_paragraph_id_suspect(para_id):
                if para_id.isupper():
                    capital_letter = para_id
                    arab_num = ""
                    lower_letter = ""
                    lower_count = 0
                    roman_num = ""
                    
                    if len(node_text):
                        node.name = "h3"

                elif para_id.isnumeric():
                    arab_num = para_id
                    lower_letter = ""
                    roman_num = ""
                    lower_count = 0

                    if len(node_text) < 50:
                        node.name = "h4"

                elif para_id.islower():
                    if lower_count > len(LOWER_LETTERS) - 1:
                        lower_count = 0
                    if para_id[0] == LOWER_LETTERS[lower_count]:
                        
                        # HACK FOR FDX 8C1hi
                        # Default Algorithm treats 8C1hi as 8C1i
                        if lastString == "8C1h" or lastString == "8C1hi":
                            roman_num = para_id
                        else:
                            lower_letter = para_id
                            lower_count = lower_count + 1
                            roman_num = ""
                    else:
                        roman_num = para_id
                
                string = str(section) \
                    + capital_letter \
                    + arab_num \
                    + lower_letter \
                    + roman_num
                node['id'] = string
                lastString = string
        new_section_string = return_section_string_with_link(node_text)
        if new_section_string != node_text:
            new_soup = BeautifulSoup(
                new_section_string, features="html.parser"
            )
            node.clear()
            node.append(new_soup)


def main():
    print("")
    print("######################################")
    print("#                                    #")
    print("# FedEx CBA 2015 Parser Version 1.00 #")
    print("# Updated 27 June 2020               #")
    print("#                                    #")
    print("######################################")

    print("")

    DEFAULT_INPUT_FILENAME = "fdx_2015_working.html"
    DEFAULT_OUTPUT_FILENAME = "fdx_2015_parsed.html"
    DEFAULT_JSON_OUTPUT_FILENAME = "fdx_2015_parsed.json"

    input_filename = input("Enter input filename: ")

    if input_filename == "":
        input_filename = DEFAULT_INPUT_FILENAME

    soup = ""


    try:
        with open(input_filename, "r") as file:
            soup = BeautifulSoup(file, features="html.parser")

    except:
        print("")
        print("File not found. Exiting...")
        print("")
        exit()

    nodes = soup.findAll(["p","h1","h2","h3","h4","h5"])
    find_paragraph_id_and_set_node_id(nodes)

    output_filename = input("Enter output filename: ")

    if output_filename == "":
        output_filename = DEFAULT_OUTPUT_FILENAME

    with open(output_filename, "w") as file:
        file.write(str(soup))

    nodes = soup.findAll(["p","h1","h2","h3","h4","h5"])
    paragraphs = {}
    lastId = ""
    idNumber = 0
    for node in nodes:
        if node.text == "Lump Sum Payment Distribution (2015)":
            break
        if 'id' in node.attrs:
            paragraphs[node['id']] = node.text
            lastId = node['id']
            idNumber = 0
        else:
            paragraphs[f'{lastId}_{idNumber}'] = node.text
            print(f'{lastId}_{idNumber}')
            idNumber += 1

    for k,v in paragraphs.items():
        if v == None:
            print(f'{k} - is none!')
    
    json_output_filename = input("Enter JSON output filename: ")

    if json_output_filename == "":
        json_output_filename = DEFAULT_JSON_OUTPUT_FILENAME

    with open(json_output_filename, "w") as outfile:  
        json.dump(paragraphs, outfile)
    ##print(nodesWithId)

if __name__ == "__main__":
    main()
