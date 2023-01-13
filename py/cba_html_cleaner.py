from bs4 import BeautifulSoup

FDX_TAGS_TO_REMOVE = ['span','strong','a']

def remove_tags(soup, tag_list):
    for tag in soup.find_all(tag_list):
        tag.unwrap()

def remove_all_tag_attributes(soup):
    for tag in soup.find_all():
        tag.attrs = {}

def clean_fdx_cba(soup):
    remove_tags(soup, FDX_TAGS_TO_REMOVE)
    remove_all_tag_attributes(soup)
        
