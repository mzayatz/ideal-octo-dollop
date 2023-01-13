# TODO: Implement excess element & attribute removal
# TODO: Implement in paragrapgh section linking

from bs4 import BeautifulSoup
import re
import json
import time
import cba_html_cleaner

# Setting this to true will allow the script to create links
CREATE_LINKS = True

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
    SUB_PARAGRAPH_LETTERS = "abcdefghijklmnopqrstuvwxyz"
    SECTION_NUMBER_REGEX = re.compile(r"Section (\d+):")
    PARAGRAPH_ID_REGEX = re.compile(r"\w+\.{1}")

    section = 0         # arabic number
    sub_section = ""    # capital letter
    paragraph = ""      # arabic number 
    sub_paragraph = ""  # lowercase letter
    clause = ""         # roman numeral

    sub_paragraph_count = 0

    # SECTION = 1
    #   SECTION + 1 if CAPLET == "A" .
    # CAPLET.ARABNUM.LOWLET.ROMANNUM

    line_identifier = ""
    last_constructed_cba_identifier = ""

    for node in input_nodes:
        node_text = node.getText()
        section_match = SECTION_NUMBER_REGEX.match(node_text)
        para_id_match = PARAGRAPH_ID_REGEX.match(node_text)
    
        constructed_cba_identifier = ""
        if section_match:
            section = int(section_match.group(1))
            node['id'] = str(section)


        # TODO: HACKY AS SHIT
        if node_text == "Lump Sum Payment Distribution (2015)":
            break

        if para_id_match:
            line_identifier = para_id_match.group(0).strip(".")
            
            # HACK FOR 2015 FDX SECTION 27
            # Default algorithm treats percentages as
            # new paragraph numbers
            if not is_matched_paragraph_id_suspect(line_identifier):
                if line_identifier.isupper():
                    sub_section = line_identifier
                    paragraph = ""
                    sub_paragraph = ""
                    sub_paragraph_count = 0
                    clause = ""

                elif line_identifier.isnumeric():
                    paragraph = line_identifier
                    sub_paragraph = ""
                    clause = ""
                    sub_paragraph_count = 0

                elif line_identifier.islower():
                    if sub_paragraph_count > len(SUB_PARAGRAPH_LETTERS) - 1:
                        sub_paragraph_count = 0
                    if line_identifier[0] == SUB_PARAGRAPH_LETTERS[sub_paragraph_count]:
                        
                        # HACK FOR FDX 8C1hi
                        # Default Algorithm treats 8C1hi as 8C1i
                        if last_constructed_cba_identifier == "8C1h" or last_constructed_cba_identifier == "8C1hi":
                            clause = line_identifier
                        else:
                            sub_paragraph = line_identifier
                            sub_paragraph_count = sub_paragraph_count + 1
                            clause = ""
                    else:
                        clause = line_identifier
                
                constructed_cba_identifier = str(section) \
                    + sub_section \
                    + paragraph \
                    + sub_paragraph \
                    + clause
                node['id'] = constructed_cba_identifier
                last_constructed_cba_identifier = constructed_cba_identifier
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

    int_time = int(time.time())
    DEFAULT_INPUT_FILENAME = "fdx_2015_original.html"
    DEFAULT_OUTPUT_FILENAME = f"fdx_2015_parsed_{int_time}.html"

    input_filename = input(f"Enter input filename ({DEFAULT_INPUT_FILENAME}): ")

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

    cba_html_cleaner.clean_fdx_cba(soup)

    nodes = soup.findAll(["p","h1","h2","h3","h4","h5","table"])
    find_paragraph_id_and_set_node_id(nodes)
    newest_soup = BeautifulSoup()
    for node in nodes: 
        nodeId = ""
        if node.has_attr('id'):
            nodeId = node['id']
        if nodeId != "": 
            node['id'] = nodeId
        newest_soup.append(node)
        


    output_filename = input(f"Enter output filename ({DEFAULT_OUTPUT_FILENAME}): ")

    if output_filename == "":
        output_filename = DEFAULT_OUTPUT_FILENAME

    with open(output_filename, "w") as file:
        file.write(str(newest_soup))

if __name__ == "__main__":
    main()
