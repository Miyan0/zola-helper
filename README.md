# zola_translate

Generates Zola's markdown and json files for a different language.
The generated files content is copied from the source files.

**NOTE**: This script assumes to be run in the root folder of the Zola project.

## Dependencies

This script only use packages from the standard library so it has no dependencies. It uses `f strings` though so it needs `Python 3.6` or greater. I only tested on `Python 3.10.6` so your mileage may vary... Thus, there's no need for a virtual environment.

## Installation

Clone or download the project and copy `zola_translate.py` to the root of your Zola project.

## Run

```bash
python zola_translate -h  # <- will display arguments (help)
```

```bash
python zola_translate en
 # -> will generate files with 'en' in ./content folder
```

```bash
python zola_translate en -r mydir/other
    # or
python zola_translate en -r ./mydir/other
    #-> will generate files with 'en' in ./mydir/other directory
```

## Remarks

Currently, this will generate translated file for `.md` or `.json` extensions.
To generate other file types, add them to `VALID_FILE_EXTENSIONS` constant.
To generate only markdown files, replace `VALID_FILE_EXTENSIONS` value with `('.md',)`.

**NOTE**: `VALID_FILE_EXTENSIONS` is a `Tuple` so, don't forget the ending comma if it has only one element!

Ex: `('.md')` is **NOT** a Tuple, but `('.md',)` is.

**NOTE**: In order to prevent generating files like `index.en.it.md` this script only split on `'.'` and skip any file with more one dot `('.')` in its name. This is not ideal (and there are many ways to handle this) but it works for me.

**NOTE**: May also work for **Hugo** project, but I didn't test it.
