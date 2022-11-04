from pathlib import Path
import shutil
import argparse

"""
Generates Zola's markdown and json files for a different language.
The generated files content is copied from the source files.
This script assumes to be run in the root folder of the Zola project.

Usage:
-----
python zola_translate -h
    -> will display arguments (help)

python zola_translate en 
    -> will generate files with 'en' in ./content folder

python zola_translate en -r mydir/other
    or
python zola_translate en -r ./mydir/other
     -> will generate files with 'en' in ./mydir/other directory

Currently, this will generate translated file for '.md' or '.json' extensions.
To generate other file types, add them to VALID_FILE_EXTENSIONS constant.
To generate only markdown files, replace VALID_FILE_EXTENSIONS value with ('.md',).

NOTE: VALID_FILE_EXTENSIONS is a Tuple so, don't forget the ending comma if
      it has only one element! 
      Ex: ('.md') is NOT a Tuple, but ('.md',) is.

NOTE: In order to prevent generating files like 'index.en.it.md' this script
      only split on '.' and skip any file with more one dot ('.') in its name.
      This is not ideal (and there are many ways to handle this) but it works
      me. 

NOTE: May also work for Hugo project, but I didn't test it.

"""

VALID_FILE_EXTENSIONS = (".md", ".json")
DEFAULT_LANGUAGE_TO_TRANSLATE = "en"
DEFAULT_ROOT_DIRECTORY = "content"


def is_valid(file_path: Path) -> bool:
    """Returns True if `file_path` is not hidden and its extension
    is valid.
    @see VALID_FILE_EXTENSIONS
    """
    if not file_path.is_file():
        return False
    
    if file_path.name.startswith('.'): return False
    
    return file_path.suffix in VALID_FILE_EXTENSIONS



def traversal(the_path: Path, to_process: list[Path]):
    """Recursively appends `the_path` to list argument if it's a valid file.
    @see "is_valid()"
    """
    for item in the_path.iterdir():
        if item.is_dir():
            traversal(the_path=item, to_process=to_process)
        elif is_valid(item):
            to_process.append(item)
        
    return the_path


def get_new_path(the_path: Path, lang: str) -> Path:
    """Generates a new path for translation.
    """
    filename = the_path.name

    # don't generate name for translated files!
    parts = filename.split('.')
    if len(parts) > 2:
        return the_path

    parent = the_path.parent
    extension = the_path.suffix
    new_name = f"{filename.replace(extension, '')}.{lang}{extension}"
    return parent / new_name


def process(root_dir: Path, lang: str):
    """Parses 'folder' recursively and generates translated file names."""
    to_process = []


    traversal(the_path=root_dir, to_process=to_process) 
    
    for fp in to_process:
        new_path = get_new_path(the_path=fp, lang=lang)
        if new_path.exists():
            continue
        shutil.copy2(fp, new_path)

if __name__ == "__main__":
    # defaults
    lang = DEFAULT_LANGUAGE_TO_TRANSLATE
    root_dir = DEFAULT_ROOT_DIRECTORY

    # parsing command line args
    parser = argparse.ArgumentParser()
    parser.add_argument("lang", help="language to translate")
    parser.add_argument("-r", "--root", help="root directory to parse, defaults to 'content' in current directory.")
    args = parser.parse_args()
    
    if args.lang: lang = args.lang
    if args.root: root_dir = args.root
    to_parse = Path.cwd() / root_dir

    if not to_parse.exists() or not to_parse.is_dir():
        print(f"Invalid root directory: '{to_parse}'")
        exit(1)

    print(f"I will translate files in {to_parse} to '{lang}'")
    input = input( "Type 'return' to proceed, any character(s) to abort! > ")
    ok = input == ''

    if not ok:
        print("Aborting, no translations done!")
        exit(0)
    
    print('translating...')
    process(root_dir=to_parse, lang=lang)
    print('done!')