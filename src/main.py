import os
import sys
from textnode import TextNode, TextType
from copystatic import copy_files_recursive, folder_cleanup
from gencontent import generate_page, generate_pages_recursive


DIR_PATH_STATIC = "./static"
DIR_PATH_PUBLIC = "./docs"

def main():
    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"

    folder_cleanup(DIR_PATH_PUBLIC)
    copy_files_recursive(DIR_PATH_STATIC, DIR_PATH_PUBLIC)
    generate_pages_recursive("content/", "template.html", DIR_PATH_PUBLIC, basepath)
    
    


if __name__ == "__main__":
    main()