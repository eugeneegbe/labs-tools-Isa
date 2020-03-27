﻿# Isa

This tool helps to describe the images contributed to Wiki Loves competitions.

Isa is not only an acronym for information structured additions, but is also a [chiShona](https://sn.wikipedia.org/wiki/ChiShona) language word for ‘put’.

# Requirements

* [Python 3.x+](https://www.python.org/downloads/)
* [PIP (Python Dependency Manager)](https://pip.pypa.io/en/stable/installing/)

## Installing dependencies

Install application dependencies using the `get-deps.sh` script:
```bash 
./get-deps.sh
```
The above script attempts to check system requirements and informs user on next steps.

## Quickstart the app
```bash
export FLASK_APP=app.py # add --reload parameter to enable Flask auto-compilation feature
flask run
```

## Adding Translations

To add translations, the following steps should be followed while located in the /isa subfolder

- Mark the string to be translated using formats shown below
 * Templates: _('<string>')
 * Python & JavaScript: gettext('<string>')

- run ```pybabel extract -F babel.cfg -o messages.pot --input-dirs=.``` from the *isa* module to extract the strings

- run ```find src/*.js -type f -print > js-file-list``` to create/update list of all source JS files needed for next step

- run ```xgettext --files-from=js-file-list --output=messages.pot --language=JavaScript --from-code=UTF-8 --join-existing --omit-header```
This extracts JavaScript strings and merges them into messages.pot file (along with existing Python and template strings)

- run ```pybabel init (update in case you are modifying) -i messages.pot -d translations -l <lang_code>``` to generate translations in a new language with code <lang_code>

- Enter the strings corresponding translations in 'translations/<lang_code>/LC_MESSAGES/messages.po'

- run ``` pybabel compile -d translations ``` to compile the translations

- run ``` npm run build-fr-json ``` to convert the .po file to json for use in JavaScript translations.
Note: generalised system still to be finalised for adding new languages

# Testing the application

- To run tests from the applications root directory, use the command `nose2 -v tests.<test_module_name>`

- To get a blueprint's coverage, run following commands:

    - From the applications root directory, run `coverage run -m unittest discover`
    - Then run `coverage report -m isa/<blueprint_name>/*.py>`