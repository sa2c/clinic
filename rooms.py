import datetime
import argparse
import yaml
import os
from operator import itemgetter
from hashlib import md5
import sys

def get_file_contents(filename):
    with open(filename, 'r') as f:
        return f.read()
    
def get_file_list(folder):
    '''Return a list of all .yaml files found in a recursive search of 
    the specified `folder`.'''
    
    file_list = []
    for root, subdirs, files in os.walk(folder):
        file_list.extend(os.path.join(root, f)
                         for f in files
                         if f.lower().endswith("yaml"))
    return file_list

def get_details(files):
    '''Looks at the YAML data in each file listed in `files`,
    and returns a list of dicts containing room information.'''

    details = []
    default = {'hasvideostart': '', 'hasvideoend': '',
               'hasmapstart': '', 'hasmapend': '',
               'videoid': '', 'map': ''}
    
    for f in files:
        detail = {**default, **yaml.safe_load(get_file_contents(f))}
        if not {'name', 'code', 'directions'}.issubset(detail):
            print("{} is missing essential parameters".format(f))
            continue

        if detail['videoid'] == '':
            detail['hasvideostart'] = '<!--'
            detail['hasvideoend'] = '-->'
        
        if detail['map'] == '':
            detail['hasmapstart'] = '<!--'
            detail['hasmapend'] = '-->'
        
        details.append(detail)

    return details

def generate_single_file(detail, output_folder, room_template):
    '''Takes a dict `detail`, and formats each according 
    to `room_template`, outputting to `output_folder`'''

    with open("{}/{}.html".format(output_folder, detail['code']), 'w') as f:
        f.write(room_template.format(**detail))

def generate_html(room_folder, output_folder, room_template_file):
    '''Takes a `room_folder` of .yaml files and specified `room_template_file`,
    and generates HTML pages, output in `output_folder`.

    Syntax for the template files matches Python string formatting,
    described in README.md.'''

    files = get_file_list(room_folder)
    rooms = get_details(files)

    room_template = room_template_file.read()

    for room in rooms:
        generate_single_file(room, output_folder, room_template)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Takes a folder full of YAML clinic descriptions "
        "and arranges them into a HTML page based on the given templates"
    )
    parser.add_argument("room_folder",
                        help="Folder to search recursively for .yaml files")
    parser.add_argument("output_folder",
                        help="Where to place the resulting output file")
    parser.add_argument("--room_template",
                        default="room_template.html",
                        type=argparse.FileType('r'),
                        dest="room_template_file")
    args = parser.parse_args()
    generate_html(**vars(args))
