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

def munge_time(time):
    nulldate = datetime.datetime(2018, 1, 1, 0, 0)
    
    if isinstance(time, str):
        return datetime.datetime.strptime(
            time, "%H:%M"
        ).time()
    else:
        return (
            nulldate + datetime.timedelta(minutes=time)
        ).time()
    
def get_details(files):
    '''Looks at the YAML data in each file listed in `files`,
    and returns two lists: one of details of events in the past,
    and one of events in the future.'''

    default = {
        "start": 900,
        "end": 1020
    }

    past = []
    future = []
    ids = set()

    for f in files:
        detail = {**default, **yaml.load(get_file_contents(f))}
        if not {'date', 'location', 'locref'}.issubset(detail):
            print("{} is missing essential parameters.format(f)")
            continue
        detail['start'] = munge_time(detail['start'])
        detail['end'] = munge_time(detail['end'])                                     
        detail['id'] = md5(repr(detail).encode()).hexdigest()
        if detail['id'] not in ids:
            ids.add(detail['id'])
            if detail["date"] < datetime.date.today():
                past.append(detail)
            else:
                future.append(detail)
            
    return past, future

def group_dates(details):
    '''Takes a list of detail dicts (`details`), and returns a 
    dict of lists of dicts, where each key is a year.'''

    details.sort(key=itemgetter('date', 'time'))
    if len(details) == 0:
        return {}
    
    first_year = details[0]['date'].year
    last_year = details[-1]['date'].year

    years = {year: [] for year in range(first_year, last_year + 1)}

    for detail in details:
        years[detail['date'].year].append(detail)

    return years
    
def generate_inner(details, inner_template):
    '''Takes a list of `details`, and formats each according 
    to `inner_template`'''

    for detail in details:
        yield inner_template.format(**detail)

def year_html(years, inner_template):
    '''Takes a dict of lists of events for each year, and 
    yields tuples of the year and the corresponding HTML,
    in reverse chronological order.'''
    
    for year in sorted(years.keys(), reverse=True):
        yield year, '\n'.join(inner_html
                              for inner_html
                              in generate_inner(years[year], inner_template))
        
def generate_html(folder, output_file,
                  outer_template_file, inner_template_file,
                  next_template_file, annual_template_file=None):
    '''Takes a `folder` of .yaml files and specified `inner_template_file`,
    `annual_template_file`, `next_template_file`, and `outer_template_file`, 
    and generates an HTML page, output at `output_file`.

    Syntax for the template files matches Python string formatting,
    described in README.md.'''

    files = get_file_list(folder)
    past_events, future_events = get_details(files)

    future_events.sort(key=itemgetter('date', 'start', 'end'))
    next_template = next_template_file.read()
    next_html = next_template.format(**future_events[0])
    
    inner_template = inner_template_file.read()
    future_html = '\n'.join(inner_html
                            for inner_html
                            in generate_inner(future_events, inner_template))
    if annual_template_file:
        annual_template = annual_template_file.read()
    else:
        annual_template = "{content}"
        
    past_html = '\n'.join(
        annual_template.format(
            year=year,
            content=inner_html
        )
        for year, inner_html
        in year_html(group_dates(past_events), inner_template)
    )

    html = outer_template_file.read().format(
        past=past_html, future=future_html, next=next_html
    )

    output_file.write(html)
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Takes a folder full of YAML clinic descriptions "
        "and arranges them into a HTML page based on the given templates"
    )
    parser.add_argument("folder",
                        help="Folder to search recursively for .yaml files")
    parser.add_argument("output_file",
                        help="Where to place the resulting output file",
                        type=argparse.FileType('w'))
    parser.add_argument("--outer_template",
                        default="outer_template.html",
                        type=argparse.FileType('r'),
                        dest="outer_template_file")
    parser.add_argument("--next_template",
                        default="next_template.html",
                        type=argparse.FileType('r'),
                        dest="next_template_file")
    parser.add_argument("--inner_template",
                        default="inner_template.html",
                        type=argparse.FileType('r'),
                        dest="inner_template_file")
    parser.add_argument("--annual_template",
                        type=argparse.FileType('r'),
                        dest="annual_template_file")
    args = parser.parse_args()
    generate_html(**vars(args))
