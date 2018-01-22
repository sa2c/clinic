# Seminar schedule generator

```usage: generate.py [-h] [--outer_template OUTER_TEMPLATE]
                   [--inner_template INNER_TEMPLATE]
		   [--next_template NEXT_TEMPLATE]
                   [--annual_template ANNUAL_TEMPLATE]
                   folder output_file

Takes a folder full of YAML clinic descriptions and arranges them into a HTML
page based on the given templates

positional arguments:
  folder                Folder to search recursively for .yaml files
  output_file           Where to place the resulting output file

optional arguments:
  -h, --help            show this help message and exit
  --outer_template OUTER_TEMPLATE
  --inner_template INNER_TEMPLATE
  --next_template NEXT_TEMPLATE
  --annual_template ANNUAL_TEMPLATE```

## Template syntax

Parameters are specified in curly braces, as if they will be passed to
Python's `.format()` (because they will).

### `inner_template.html`

This is iterated over for each event (i.e. each YAML file).

The following names are recognised:

* `id`
* `date`
* `start`
* `end`
* `locref`
* `location`

`locref` should point to a web page describing the room in question.

`date`, `locref`, and `location` are compulsory.

### `next_template.html`

Formats the next scheduled event. Parameters are as `inner_template.html`.

### `annual_template.html`

This file must be specified by hand; by default a dummy version is used.

The following names are recognised:

* `year`
* `content`

The latter is replaced by the results of applying `inner_template.html`
to each YAML file for the relevant year.

### `outer_template.html`

The main design of the page. Two names are recognised:

* `past`
* `future`

The former is replaced by the results of applying `inner_template.html`
to each YAML file for all future events. The latter is replaced by
the result of applying `annual_template.html` to each year.

